from pathlib import Path

import pytest
from scripts.build_pages import (
    LinkInventory,
    build,
    public_link,
    rewrite,
    validate_site,
)


def test_markdown_navigation_keeps_query_and_fragment(tmp_path: Path) -> None:
    source = tmp_path / "examples/map.html"
    assert public_link("../docs/exercises.md?mode=read#e2", source, tmp_path) == (
        "../docs/exercises.html?mode=read#e2"
    )
    external = "https://example.org/reference?q=1#section"
    assert public_link(external, source, tmp_path) == external


def test_rewrite_preserves_numerical_script_and_entities(tmp_path: Path) -> None:
    content = '<a href="notes.md">A &amp; B</a><script>const f=x=>x<0?x*x:1;</script>'
    rendered = rewrite(content, tmp_path / "index.html", tmp_path)
    assert 'href="notes.html"' in rendered
    assert "A &amp; B" in rendered
    assert "const f=x=>x<0?x*x:1;" in rendered


def test_local_link_validator_rejects_a_missing_fragment(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text('<a href="notes.html#missing">Read</a>', encoding="utf-8")
    (tmp_path / "notes.html").write_text('<h1 id="present">Notes</h1>', encoding="utf-8")
    with pytest.raises(ValueError, match="Missing fragment"):
        validate_site(tmp_path)


def test_output_safety_preserves_unmanaged_directory(tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    sentinel = site / "my-file.txt"
    sentinel.write_text("user data", encoding="utf-8")
    with pytest.raises(ValueError, match="lacks the generated-build marker"):
        build(tmp_path)
    assert sentinel.read_text(encoding="utf-8") == "user data"


def test_allowlisted_build_excludes_secrets_and_rebuilds(tmp_path: Path) -> None:
    (tmp_path / "web").mkdir()
    (tmp_path / "web/site.css").write_text("body{}", encoding="utf-8")
    (tmp_path / "web/index.html").write_text(
        '<a href="docs/guide.md#exercise">Guide</a>', encoding="utf-8"
    )
    (tmp_path / "examples").mkdir()
    (tmp_path / "examples/.env").write_text("not public", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/guide.md").write_text("# Exercise\n\nA reader task.", encoding="utf-8")
    # The generated document template links to these curated destinations.
    for relative in ("examples/index.html", "docs/thesis-guide.md", "docs/exercises.md"):
        (tmp_path / relative).write_text("# Notes", encoding="utf-8")
    (tmp_path / "thesis").mkdir()
    output = build(tmp_path)
    assert not (output / "examples/.env").exists()
    inventory = LinkInventory()
    inventory.feed((output / "docs/guide.html").read_text(encoding="utf-8"))
    assert "exercise" in inventory.anchors
    (output / "stale.txt").touch()
    assert build(tmp_path) == output
    assert not (output / "stale.txt").exists()
