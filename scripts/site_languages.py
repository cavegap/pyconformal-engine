"""Generate Spanish web pages and retain the original English edition."""

from __future__ import annotations

import html
import json
import posixpath
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path


class LanguagePage(HTMLParser):
    """Translate prose, never mathematics, listings, identifiers or URLs."""

    def __init__(self, catalog: dict[str, str], page: Path, language: str) -> None:
        super().__init__(convert_charrefs=True)
        self.catalog = catalog
        self.page = page
        self.language = language
        self.parts: list[str] = []
        self.protected: list[str] = []

    def translate(self, value: str) -> str:
        """Keep inline spacing around a complete translated text node."""
        trimmed = value.strip()
        if not trimmed or self.language == "en":
            return value
        if re.search(r"[A-Za-z]{2}", trimmed) and trimmed not in self.catalog:
            raise ValueError(f"Missing Spanish translation in {self.page}: {trimmed}")
        translated = self.catalog.get(trimmed, trimmed)
        return value[: len(value) - len(value.lstrip())] + translated + value[len(value.rstrip()) :]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Localize readable attributes while preserving public link targets."""
        attributes = dict(attrs)
        if tag in {"code", "pre", "math", "script", "style"} or "data-tex" in attributes:
            self.protected.append(tag)
        values = []
        for key, value in attrs:
            if value is not None:
                if key in {"alt", "title", "aria-label", "placeholder"} or (
                    tag == "meta"
                    and key == "content"
                    and (
                        attributes.get("name") == "description"
                        or attributes.get("property") in {"og:title", "og:description"}
                    )
                ):
                    value = self.translate(value)
                if tag == "html" and key == "lang":
                    value = self.language
                if self.language == "es" and (
                    (tag == "link" and attributes.get("rel") == "canonical" and key == "href")
                    or (
                        tag == "meta"
                        and attributes.get("property") == "og:url"
                        and key == "content"
                    )
                ):
                    value = value.rstrip("/") + "/es/"
            values.append(key if value is None else f'{key}="{html.escape(value, quote=True)}"')
        self.parts.append("<" + " ".join([tag, *values]) + ">")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Retain self-closing MathML and SVG markup."""
        self.handle_starttag(tag, attrs)
        self.parts[-1] = self.parts[-1][:-1] + " />"
        if self.protected and self.protected[-1] == tag:
            self.protected.pop()

    def handle_endtag(self, tag: str) -> None:
        """Restore translation after a protected element."""
        self.parts.append(f"</{tag}>")
        if self.protected and self.protected[-1] == tag:
            self.protected.pop()

    def handle_data(self, data: str) -> None:
        """Escape prose; preserve raw executable and stylesheet source."""
        if self.protected and self.protected[-1] in {"script", "style"}:
            self.parts.append(data)
        else:
            self.parts.append(html.escape(data if self.protected else self.translate(data)))

    def handle_decl(self, decl: str) -> None:
        """Preserve the doctype."""
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data: str) -> None:
        """Preserve build markers."""
        self.parts.append(f"<!--{data}-->")


def editions(output: Path, root: Path) -> None:
    """Add two real HTML editions, with shared assets and native language links."""
    catalog = json.loads((root / "web/landing/es.json").read_text(encoding="utf-8"))
    replacements = json.loads((root / "web/landing/messages-es.json").read_text(encoding="utf-8"))
    # Retain portable relative URLs, including image paths created by numerical demos.
    shutil.copytree(output, output / "es", ignore=shutil.ignore_patterns("es"))
    for page in list(output.rglob("*.html")):
        relative = page.relative_to(output)
        if relative.parts[0] == "es":
            continue
        original = page.read_text(encoding="utf-8")
        logo = posixpath.relpath(
            (output / "assets/landing/pyconformal-mark.svg").as_posix(), page.parent.as_posix()
        )
        wordmark = posixpath.relpath(
            (output / "assets/landing/pyconformal-wordmark-dark.svg").as_posix(),
            page.parent.as_posix(),
        )
        brand = (
            f'<img class="brand-logo" src="{logo}" alt="" width="48" height="48">'
            '<span class="brand-copy"><span class="brand-name">'
            f'<img class="brand-wordmark" src="{wordmark}" alt="PyConformal" width="170" height="36"></span>'
            '<span class="brand-tagline">Interactive mathematics lab</span></span>'
        )
        original = re.sub(
            r'(<a class="brand"[^>]*>).*?</a>',
            r"\g<1>" + brand + "</a>",
            original,
            flags=re.DOTALL,
        )
        if 'class="project-credit"' not in original:
            credit = '<p class="project-credit">PyConformal Engine · Conceived and developed by César Augusto Vega Penagos.</p>'
            if "</footer>" in original:
                original = original.replace("</footer>", credit + "</footer>", 1)
            else:
                original = original.replace(
                    "</main>", '</main><footer class="site-footer">' + credit + "</footer>", 1
                )

        for language in ("en", "es"):
            destination = output / "es" / relative if language == "es" else page
            parser = LanguagePage(catalog, relative, language)
            parser.feed(original)
            parser.close()
            content = "".join(parser.parts)
            if "<head" not in content:
                content = re.sub(r"(<html[^>]*>)", r"\1<head>", content, count=1)
                content = content.replace("<main>", "</head><body><main>", 1)
                content = content.replace("</html>", "</body></html>", 1)
            # Dynamic messages in scripts have an explicit, separate web-only catalog.
            if language == "es":

                def localize(match: re.Match[str]) -> str:
                    script = match[0]
                    for source, target in replacements.items():
                        script = script.replace(source, target)
                    return script

                content = re.sub(r"<script\b[^>]*>.*?</script>", localize, content, flags=re.DOTALL)
            prefix = posixpath.relpath(output.as_posix(), destination.parent.as_posix())
            spanish = posixpath.relpath(
                (output / "es" / relative).as_posix(), destination.parent.as_posix()
            )
            english = posixpath.relpath(page.as_posix(), destination.parent.as_posix())
            selector = (
                '<nav class="language-picker" aria-label="Language / Idioma">'
                f'<a lang="en" hreflang="en" href="{english}?lang=en"'
                + (' aria-current="true"' if language == "en" else "")
                + ">English</a>"
                f'<a lang="es" hreflang="es" href="{spanish}?lang=es"'
                + (' aria-current="true"' if language == "es" else "")
                + ">Español</a></nav>"
            )
            kind = (
                "landing"
                if relative == Path("index.html")
                else "gallery"
                if relative == Path("examples/index.html")
                else "example"
                if relative.parts[0] == "examples" and relative.name != "README.html"
                else "document"
            )
            content = content.replace("<body>", f'<body class="page-{kind}">', 1)
            if kind == "example":
                content = content.replace(
                    "<main>", '<main><div class="language-topbar">' + selector + "</div>", 1
                )
            elif "</header>" in content:
                content = content.replace("</header>", selector + "</header>", 1)
            else:
                content = content.replace(
                    "<main>",
                    '<main><header class="example-language-header">' + selector + "</header>",
                    1,
                )
            head = (
                f'<link rel="icon" type="image/svg+xml" href="{prefix}/assets/landing/pyconformal-mark.svg">'
                f'<link rel="stylesheet" href="{prefix}/assets/landing/language.css">'
                f'<link rel="stylesheet" href="{prefix}/assets/landing/experience.css">'
                f'<script src="{prefix}/assets/landing/language.js"></script>'
                f'<link rel="alternate" hreflang="es" href="{spanish}">'
                f'<link rel="alternate" hreflang="en" href="{english}">'
            )
            content = content.replace("</head>", head + "</head>", 1)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
    for name in ("animation.js", "citations.js"):
        path = output / "es/assets/landing" / name
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        for original, translated in replacements.items():
            source = source.replace(original, translated)
        path.write_text(source, encoding="utf-8")
