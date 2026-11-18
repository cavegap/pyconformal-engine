"""Build the public gallery and Markdown companion as a portable static site."""

from __future__ import annotations

import html
import json
import posixpath
import shutil
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit, urlunsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/cavegap/pyconformal-engine"
MARKER = ".pyconformal-build.json"


def public_link(value: str, source: Path, root: Path) -> str:
    """Convert repository Markdown and source links without changing externals."""
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return value
    target = (source.parent / unquote(parsed.path)).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Link escapes repository: {source.name}: {value}")
    relative = target.relative_to(root)
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
    body = markdown.markdown(content, extensions=["tables", "fenced_code", "toc"])
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace(
        "</table>", "</table></div>"
    )
    title = next(
        (line.lstrip("# ") for line in content.splitlines() if line.startswith("# ")), source.stem
    )
    prefix = posixpath.relpath(root.as_posix(), source.parent.as_posix())

    def root_link(path: str) -> str:
        return f"{prefix}/{path}"

    source_url = f"{REPOSITORY}/blob/main/{source.relative_to(root).as_posix()}"
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | PyConformal Engine</title><link rel="stylesheet" href="{root_link("assets/site.css")}"></head>
<body><header class="site-header"><a class="brand" href="{root_link("index.html")}">PyConformal Engine</a>
<nav aria-label="Main"><a href="{root_link("examples/index.html")}">Gallery</a><a href="{root_link("docs/thesis-guide.html")}">Thesis companion</a><a href="{root_link("docs/exercises.html")}">Exercises</a><a href="{REPOSITORY}">GitHub</a></nav></header>
<main class="document"><p class="breadcrumb"><a href="{root_link("index.html")}">Home</a> / Companion</p>
{body}
<p class="source-link"><a href="{source_url}">Read this page in the repository</a></p></main>
<footer class="site-footer">Vega Penagos &amp; Olivero Zapata (2015) · PyConformal Engine research preview</footer></body></html>'''
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
    root = root.resolve()
    output = root / "site"
    if output.resolve() != output or output.parent != root:
        raise ValueError("The site output must be a direct, nonsymlink child of the repository.")
    if output.exists() and not (output / MARKER).is_file():
        raise ValueError("Refusing to replace site/: it lacks the generated-build marker.")
    with TemporaryDirectory(prefix="pyconformal-pages-") as temporary:
        staging = Path(temporary) / "site"
        staging.mkdir()
        (staging / "assets").mkdir()
        shutil.copy2(root / "web/site.css", staging / "assets/site.css")
        landing = (root / "web/index.html").read_text(encoding="utf-8")
        (staging / "index.html").write_text(
            rewrite(landing, root / "index.html", root), encoding="utf-8"
        )
        suffixes = {".html", ".js", ".json", ".jpg", ".jpeg", ".png", ".py"}
        for source in (root / "examples").iterdir():
            if source.is_symlink():
                raise ValueError(f"Symlink not permitted in public assets: {source.name}")
            if not source.is_file() or source.suffix not in suffixes:
                continue
            target = staging / "examples" / source.name
            target.parent.mkdir(exist_ok=True)
            if source.suffix == ".html":
                target.write_text(
                    rewrite(source.read_text(encoding="utf-8"), source, root), encoding="utf-8"
                )
            else:
                shutil.copy2(source, target)
        markdown_files = [
            root / name
            for name in ("README.md", "ROADMAP.md", "CHANGELOG.md")
            if (root / name).is_file()
        ]
        markdown_files.extend((root / "docs").rglob("*.md"))
        markdown_files.extend(
            root / folder / "README.md"
            for folder in ("examples", "thesis", "notebooks")
            if (root / folder / "README.md").is_file()
        )
        for source in markdown_files:
            target = staging / source.relative_to(root).with_suffix(".html")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                document(source.read_text(encoding="utf-8"), source, root), encoding="utf-8"
            )
        extras = [root / "LICENSE", root / "CITATION.cff"]
        extras.extend((root / "thesis").glob("*.pdf"))
        extras.extend(
            root / "scripts" / name
            for name in ("recover_lunar_outlines.py", "verify_browser_math.py", "build_pages.py")
        )
        for source in extras:
            if source.is_file():
                target = staging / source.relative_to(root)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
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
    build()
