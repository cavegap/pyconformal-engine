"""Build the public gallery and Markdown companion as a portable static site."""

from __future__ import annotations

import hashlib
import html
import json
import posixpath
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit, urlunsplit

import markdown
from latex2mathml.converter import convert
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.preprocessors import Preprocessor

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/cavegap/pyconformal-engine"
MARKER = ".pyconformal-build.json"
MATH_NS = "http://www.w3.org/1998/Math/MathML"
POLICY = (
    "default-src 'none'; script-src 'self'; script-src-attr 'none'; "
    "style-src 'self'; style-src-attr 'none'; img-src 'self' data:; "
    "font-src 'self'; connect-src 'none'; object-src 'none'; "
    "frame-src 'none'; worker-src 'none'; media-src 'none'; "
    "base-uri 'none'; form-action 'none'"
)


def mathml(tex: str, display: bool = False) -> str:
    """Render bounded author-supplied TeX as validated, inert native MathML."""
    if len(tex) > 3000 or re.search(
        r"\\(?:href|url|html\w*|include\w*|input|require|def|newcommand|style|class)\b",
        tex,
    ):
        raise ValueError("Unsupported or oversized formula.")
    rendered = convert(tex, display="block" if display else "inline")
    if "<!DOCTYPE" in rendered.upper() or "<!ENTITY" in rendered.upper():
        raise ValueError("MathML document declarations are forbidden.")
    tree = ET.fromstring(rendered)
    allowed = {
        "math",
        "mrow",
        "mi",
        "mn",
        "mo",
        "mtext",
        "mspace",
        "mfrac",
        "msqrt",
        "mroot",
        "msup",
        "msub",
        "msubsup",
        "munder",
        "mover",
        "munderover",
        "mtable",
        "mtr",
        "mtd",
        "mstyle",
        "mpadded",
        "mphantom",
        "menclose",
        "mmultiscripts",
        "mprescripts",
        "none",
    }
    attributes = {
        "display",
        "form",
        "mathvariant",
        "stretchy",
        "fence",
        "separator",
        "lspace",
        "rspace",
        "largeop",
        "movablelimits",
        "accent",
        "accentunder",
        "rowspacing",
        "columnspacing",
        "rowalign",
        "columnalign",
        "columnlines",
        "rowlines",
        "linethickness",
        "height",
        "width",
        "depth",
        "voffset",
        "notation",
        "equalrows",
        "equalcolumns",
        "scriptlevel",
        "displaystyle",
        "columnspan",
        "rowspan",
        "minsize",
        "maxsize",
        "symmetric",
    }
    nodes = list(tree.iter())
    if len(nodes) > 2000:
        raise ValueError("Formula exceeds the element limit.")
    for node in nodes:
        if node.tag not in {f"{{{MATH_NS}}}{tag}" for tag in allowed}:
            raise ValueError("Unsupported MathML element.")
        if any(key not in attributes for key in node.attrib):
            raise ValueError("Unsupported MathML attribute.")
        if any(len(value) > 80 for value in node.attrib.values()):
            raise ValueError("Oversized MathML attribute.")
    semantics = ET.Element(f"{{{MATH_NS}}}semantics")
    for child in list(tree):
        tree.remove(child)
        semantics.append(child)
    annotation = ET.SubElement(
        semantics, f"{{{MATH_NS}}}annotation", {"encoding": "application/x-tex"}
    )
    annotation.text = tex
    tree.append(semantics)
    ET.register_namespace("", MATH_NS)
    return ET.tostring(tree, encoding="unicode")


def math_container(tex: str, display: bool) -> str:
    """Wrap formulas in a scrollable block or an inline span."""
    tag = "div" if display else "span"
    css = "math-display" if display else "math-inline"
    return f'<{tag} class="{css}">{mathml(tex, display)}</{tag}>'


class MathBlocks(Preprocessor):
    """Render display formulas after fenced code has been protected."""

    def run(self, lines: list[str]) -> list[str]:
        """Replace dollar-delimited blocks with protected rendered markup."""

        def replace(match: re.Match[str]) -> str:
            return "\n\n" + self.md.htmlStash.store(math_container(match[1].strip(), True)) + "\n\n"

        return re.sub(
            r"(?m)^\$\$\s*\n(.*?)\n\$\$\s*$", replace, "\n".join(lines), flags=re.DOTALL
        ).split("\n")


class InlineMath(InlineProcessor):
    """Render inline formulas after Markdown code spans have been protected."""

    # types-Markdown exposes the legacy Pattern signature here; the runtime
    # InlineProcessor API receives both match and data and returns a triple.
    def handleMatch(self, match: re.Match[str], data: str) -> tuple[str, int, int]:  # type: ignore[override]  # noqa: N802
        """Return an HTML-stash placeholder rather than reparsing MathML text."""
        return (
            self.md.htmlStash.store(math_container(match[1], False)),
            match.start(0),
            match.end(0),
        )


class MathExtension(Extension):
    """Support explicit dollar-delimited TeX in the thesis companion."""

    def extendMarkdown(self, md: markdown.Markdown) -> None:  # noqa: N802
        """Keep program listings separate from mathematical notation."""
        md.preprocessors.register(MathBlocks(md), "math-blocks", 24)
        md.inlinePatterns.register(
            InlineMath(r"(?<!\\)\$(?!\$)([^\n$]+?)\$(?!\$)", md), "math-inline", 185
        )


def render_html_math(content: str) -> str:
    """Replace explicit HTML formula fallbacks at build time."""

    def replace(match: re.Match[str]) -> str:
        tex = html.unescape(match[3])
        rendered = mathml(tex, match[1] == "div")
        return f"<{match[1]}{match[2]}>{rendered}</{match[1]}>"

    return re.sub(
        r'<(span|div)([^>]*\bdata-tex="([^"]+)"[^>]*)>.*?</\1>',
        replace,
        content,
        flags=re.DOTALL,
    )


def harden_page(content: str, path: Path, output: Path) -> str:
    """Move inline code to local files and add an enforced resource policy."""
    content = render_html_math(content)
    content = re.sub(
        r'<(td|th) style="text-align:\s*(left|right|center);?">',
        lambda match: f'<{match[1]} class="align-{match[2]}">',
        content,
    )
    generated = output / "assets/generated"
    generated.mkdir(parents=True, exist_ok=True)

    def externalize(match: re.Match[str]) -> str:
        tag, attrs, text = match[1], match[2], match[3]
        if tag == "script" and re.search(r"\bsrc=", attrs):
            return match[0]
        if attrs.strip():
            raise ValueError(f"Unexpected inline {tag} attributes in {path.name}")
        extension = "js" if tag == "script" else "css"
        digest = hashlib.sha256(text.encode()).hexdigest()[:20]
        asset = generated / f"{path.stem}-{digest}.{extension}"
        asset.write_bytes(text.encode("utf-8"))
        href = posixpath.relpath(asset.as_posix(), path.parent.as_posix())
        return (
            f'<script src="{href}"></script>'
            if tag == "script"
            else f'<link rel="stylesheet" href="{href}">'
        )

    content = re.sub(
        r"<(script|style)([^>]*)>(.*?)</\1>",
        externalize,
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not re.search(r"<html[\s>]", content, re.IGNORECASE):
        content = "<!doctype html><html><head></head><body>" + content + "</body></html>"
    if not re.search(r"<head[\s>]", content, re.IGNORECASE):
        content = re.sub(r"(<html[^>]*>)", r"\1<head>", content, count=1, flags=re.IGNORECASE)
        content = content.replace("<main>", "</head><body><main>", 1)
        content = content.replace("</html>", "</body></html>")
    security = (
        f'<meta http-equiv="Content-Security-Policy" content="{html.escape(POLICY, quote=True)}">'
        '<meta name="referrer" content="no-referrer">'
    )
    content = re.sub(r"(<head[^>]*>)", r"\1" + security, content, count=1, flags=re.IGNORECASE)
    return content


def public_link(value: str, source: Path, root: Path) -> str:
    """Convert repository Markdown and source links without changing externals."""
    parsed = urlsplit(value)
    if parsed.scheme and parsed.scheme not in {"https", "mailto"}:
        raise ValueError(f"Unsupported link scheme in {source.name}")
    if parsed.scheme or parsed.netloc or not parsed.path:
        return value
    target = (source.parent / unquote(parsed.path)).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Link escapes repository: {source.name}: {value}")
    relative = target.relative_to(root)
    if relative in {Path("web/math.css"), Path("web/site.css")}:
        target = root / "assets" / relative.name
    if relative == Path("web/index.html"):
        target = root / "index.html"
    if relative.parts[:2] == ("web", "landing"):
        target = root / "assets" / relative.relative_to("web")
    if relative.parts and relative.parts[0] in {"src", "tests", ".github"}:
        kind = "tree" if target.is_dir() else "blob"
        return f"{REPOSITORY}/{kind}/main/{relative.as_posix()}"
    if target.suffix == ".ipynb":
        return f"{REPOSITORY}/blob/main/{relative.as_posix()}"
    if target.is_dir() and (target / "README.md").is_file():
        target /= "README.md"
    if target.suffix == ".md":
        target = target.with_suffix(".html")
    destination = source.with_suffix(".html") if source.suffix == ".md" else source
    rewritten = posixpath.relpath(target.as_posix(), destination.parent.as_posix())
    return urlunsplit(("", "", rewritten, parsed.query, parsed.fragment))


class LinkRewriter(HTMLParser):
    """Rewrite actual HTML attributes while preserving script text and entities."""

    def __init__(self, source: Path, root: Path) -> None:
        super().__init__(convert_charrefs=False)
        self.source, self.root = source, root
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Serialize attributes, converting only local href and src targets."""
        attributes = dict(attrs)
        if tag == "img" and urlsplit(attributes.get("src") or "").netloc:
            self.parts.append(
                '<span class="external-image-label">'
                + html.escape(attributes.get("alt") or "External image")
                + "</span>"
            )
            return
        values = []
        for key, value in attrs:
            if value is None:
                values.append(key)
                continue
            if key in {"href", "src"}:
                value = public_link(value, self.source, self.root)
            values.append(f'{key}="{html.escape(value, quote=True)}"')
        self.parts.append("<" + " ".join([tag, *values]) + ">")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Serialize self-closing elements through the same attribute rules."""
        self.handle_starttag(tag, attrs)
        self.parts[-1] = self.parts[-1][:-1] + " />"

    def handle_endtag(self, tag: str) -> None:
        """Preserve closing tags."""
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        """Preserve content, including JavaScript source."""
        self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        """Preserve a named entity."""
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        """Preserve a numeric entity."""
        self.parts.append(f"&#{name};")

    def handle_decl(self, decl: str) -> None:
        """Preserve the document type."""
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data: str) -> None:
        """Preserve comments."""
        self.parts.append(f"<!--{data}-->")


def rewrite(content: str, source: Path, root: Path) -> str:
    """Rewrite local navigation inside a document or standalone example."""
    parser = LinkRewriter(source, root)
    parser.feed(content)
    parser.close()
    return "".join(parser.parts)


def document(content: str, source: Path, root: Path) -> str:
    """Render a Markdown companion page with shared navigation and typography."""
    body = markdown.markdown(content, extensions=["tables", "fenced_code", "toc", MathExtension()])
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace(
        "</table>", "</table></div>"
    )
    title = next(
        (line.lstrip("# ") for line in content.splitlines() if line.startswith("# ")),
        source.stem,
    )
    prefix = posixpath.relpath(root.as_posix(), source.parent.as_posix())

    def root_link(path: str) -> str:
        return f"{prefix}/{path}"

    source_url = f"{REPOSITORY}/blob/main/{source.relative_to(root).as_posix()}"
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | PyConformal Engine</title><link rel="stylesheet" href="{root_link("assets/site.css")}"><link rel="stylesheet" href="{root_link("assets/math.css")}"></head>
<body><header class="site-header"><a class="brand" href="{root_link("index.html")}">PyConformal Engine</a>
<nav aria-label="Main"><a href="{root_link("examples/index.html")}">Gallery</a><a href="{root_link("docs/thesis-guide.html")}">Learn</a><a href="{root_link("docs/reproducibility.html")}">Reproduce</a><a href="{root_link("docs/sources-and-scope.html")}">Sources and scope</a><a href="{REPOSITORY}">GitHub</a></nav></header>
<main class="document"><p class="breadcrumb"><a href="{root_link("index.html")}">Home</a> / Companion</p>
{body}
<p class="source-link"><a href="{source_url}">Read this page in the repository</a></p></main>
<footer class="site-footer"><p class="project-credit">PyConformal Engine · Conceived and developed by César Augusto Vega Penagos.</p></footer></body></html>'''
    return rewrite(page, source, root)


class LinkInventory(HTMLParser):
    """Collect local navigation and named anchors for the static-site check."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Collect references independently of the renderer's rewrite logic."""
        for key, value in attrs:
            if value and key in {"src", "href"}:
                self.links.append(value)
            if value and key in {"id", "name"}:
                self.anchors.add(value)


class PolicyInventory(LinkInventory):
    """Fail the build for active markup outside the static-site contract."""

    def __init__(self) -> None:
        super().__init__()
        self.policy_seen = False
        self.in_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Reject event attributes, embeds and remote resources before publication."""
        super().handle_starttag(tag, attrs)
        attributes = dict(attrs)
        if tag in {"form", "iframe", "object", "embed", "base", "style"}:
            raise ValueError(f"Forbidden element: {tag}")
        if any(key.startswith("on") or key == "style" for key in attributes):
            raise ValueError("Inline event or style attribute is forbidden.")
        if (
            tag == "meta"
            and (attributes.get("http-equiv") or "").lower() == "content-security-policy"
        ):
            if attributes.get("content") != POLICY or self.policy_seen:
                raise ValueError("Unexpected or duplicate content security policy.")
            self.policy_seen = True
        if tag == "script":
            if not self.policy_seen or not attributes.get("src"):
                raise ValueError("Scripts must be local external files after the security policy.")
            self.in_script = True
        for key in ("href", "src"):
            value = attributes.get(key)
            if not value:
                continue
            if re.search(r"[\x00-\x1f]", value):
                raise ValueError("Control character in a URL.")
            parsed = urlsplit(value)
            if parsed.scheme and parsed.scheme not in {"https", "mailto"}:
                raise ValueError("Unsafe URL scheme.")
            if (key == "src" or tag == "link") and (parsed.scheme or parsed.netloc):
                if tag == "link" and attributes.get("rel") == "canonical":
                    continue
                raise ValueError("Remote embedded resources are forbidden.")

    def handle_data(self, data: str) -> None:
        """Inline executable code is not part of the published format."""
        if self.in_script and data.strip():
            raise ValueError("Inline scripts are forbidden.")

    def handle_endtag(self, tag: str) -> None:
        """Track external-script closing tags."""
        if tag == "script":
            self.in_script = False


def audit_publication(output: Path) -> None:
    """Check resource policy, known secret signatures and executable sinks."""
    signatures = re.compile(
        r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[A-Z0-9]{16}"
    )
    for path in output.rglob("*"):
        if not path.is_file() or path.suffix not in {
            ".html",
            ".js",
            ".css",
            ".json",
            ".py",
            ".cff",
            ".bib",
            ".ris",
            ".txt",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        if signatures.search(text):
            raise ValueError(f"Possible secret in public file: {path.name}")
        if path.suffix == ".html":
            parser = PolicyInventory()
            parser.feed(text)
            if not parser.policy_seen:
                raise ValueError(f"Missing content security policy: {path.name}")
        if path.suffix == ".js" and re.search(
            r"\beval\s*\(|\bnew\s+Function\s*\(|document\.write\s*\(|"
            r"\.(?:innerHTML|outerHTML)\s*=|insertAdjacentHTML\s*\(|"
            r"\bfetch\s*\(|XMLHttpRequest|\bWebSocket\s*\(",
            text,
        ):
            raise ValueError(f"Unreviewed executable or network sink: {path.name}")
        if path.suffix == ".css" and re.search(r"@import\b|url\s*\(", text, re.IGNORECASE):
            raise ValueError(f"CSS resource loading needs explicit review: {path.name}")


def publication_sources(root: Path) -> list[Path]:
    """Read the reviewed manifest and reject traversal, hidden files and symlinks."""
    data = json.loads((root / "web/public-assets.json").read_text(encoding="utf-8"))
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise ValueError("The public asset manifest must be a list of relative paths.")
    result = []
    for name in data:
        relative = Path(name)
        if (
            relative.is_absolute()
            or "\\" in name
            or ":" in name
            or any(
                part.startswith(".") or part in {"node_modules", "__pycache__", "_build"}
                for part in relative.parts
            )
            or relative.as_posix() != name
        ):
            raise ValueError("Unsafe public asset path.")
        path = root / relative
        if (
            not path.resolve().is_relative_to(root)
            or any(parent.is_symlink() for parent in (path, *path.parents) if parent != root)
            or not path.is_file()
        ):
            raise ValueError(f"Missing or unsafe public asset: {name}")
        result.append(path)
    if len(set(result)) != len(result):
        raise ValueError("Duplicate public asset path.")
    return result


def validate_site(output: Path) -> tuple[int, int]:
    """Require all local files and HTML fragments to resolve under the build."""
    pages: dict[Path, LinkInventory] = {}
    for path in output.rglob("*.html"):
        parser = LinkInventory()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = parser
    links = 0
    for source, parser in pages.items():
        for value in parser.links:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            links += 1
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if not target.is_relative_to(output.resolve()) or not target.is_file():
                raise ValueError(f"Missing or unsafe link: {source.name}: {value}")
            if (
                parsed.fragment
                and target in pages
                and unquote(parsed.fragment) not in pages[target].anchors
            ):
                raise ValueError(f"Missing fragment: {source.name}: {value}")
    return len(pages), links


def build(root: Path = ROOT) -> Path:
    """Build an allowlisted site, replacing only a previously marked output."""
    from scripts.site_languages import editions

    root = root.resolve()
    output = root / "site"
    if output.resolve() != output or output.parent != root:
        raise ValueError("The site output must be a direct, nonsymlink child of the repository.")
    if output.exists() and not (output / MARKER).is_file():
        raise ValueError("Refusing to replace site/: it lacks the generated-build marker.")
    with TemporaryDirectory(prefix="pyconformal-pages-") as temporary:
        staging = Path(temporary) / "site"
        staging.mkdir()
        sources = publication_sources(root)
        required = {root / "web" / name for name in ("index.html", "site.css", "math.css")}
        if not required.issubset(sources):
            raise ValueError("Public manifest must include the reviewed templates and styles.")
        (staging / "assets").mkdir()
        for name in ("site.css", "math.css"):
            shutil.copy2(root / "web" / name, staging / "assets" / name)
        landing = (root / "web/index.html").read_text(encoding="utf-8")
        (staging / "index.html").write_text(
            rewrite(landing, root / "index.html", root), encoding="utf-8"
        )
        for source in sources:
            relative = source.relative_to(root)
            if relative.parts[0] == "web":
                if relative in {Path("web/index.html"), Path("web/site.css"), Path("web/math.css")}:
                    continue
                if relative.parts[:2] != ("web", "landing") or source.suffix not in {
                    ".css",
                    ".js",
                    ".jpg",
                    ".svg",
                    ".json",
                    ".bib",
                    ".ris",
                    ".txt",
                    ".cff",
                }:
                    raise ValueError("Unreviewed web asset type or directory.")
                if source.suffix == ".svg" and relative not in {
                    Path("web/landing/pyconformal-mark.svg"),
                    Path("web/landing/pyconformal-wordmark-dark.svg"),
                    Path("web/landing/pyconformal-wordmark-light.svg"),
                }:
                    raise ValueError("Unreviewed SVG asset.")
                target = staging / "assets" / relative.relative_to("web")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                continue
            if relative.parts[0] not in {
                "examples",
                "docs",
                "thesis",
                "scripts",
                "notebooks",
            } and str(relative) not in {
                "README.md",
                "ROADMAP.md",
                "CHANGELOG.md",
                "SECURITY.md",
                "CITATION.cff",
                "LICENSE",
            }:
                raise ValueError("Public source outside the curated directories.")
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix == ".md":
                target = target.with_suffix(".html")
                target.write_text(
                    document(source.read_text(encoding="utf-8"), source, root),
                    encoding="utf-8",
                )
            elif source.suffix == ".html":
                target.write_text(
                    rewrite(source.read_text(encoding="utf-8"), source, root),
                    encoding="utf-8",
                )
            else:
                shutil.copy2(source, target)
        if root / "web/landing/es.json" in sources:
            editions(staging, root)
        for page in staging.rglob("*.html"):
            page.write_text(
                harden_page(page.read_text(encoding="utf-8"), page, staging),
                encoding="utf-8",
            )
        audit_publication(staging)
        (staging / ".nojekyll").touch()
        pages, links = validate_site(staging)
        (staging / MARKER).write_text(
            json.dumps({"pages": pages, "local_links": links}), encoding="utf-8"
        )
        if output.exists():
            # output was resolved and restricted to root/site above; the marker
            # prevents removing an arbitrary user-owned directory.
            shutil.rmtree(output)
        shutil.copytree(staging, output)
    print(f"Built {pages} pages; verified {links} local links and fragments: {output}")
    return output


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    build()
