import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from scripts.build_pages import (
    MATH_NS,
    POLICY,
    PolicyInventory,
    audit_publication,
    document,
    harden_page,
    mathml,
    public_link,
    publication_sources,
)


def test_math_fractions_keep_structure_and_tex_annotation() -> None:
    tree = ET.fromstring(mathml(r"f'(z)=\frac{-2i}{(1+z)^2}", True))
    assert tree.find(f".//{{{MATH_NS}}}mfrac") is not None
    assert tree.find(f".//{{{MATH_NS}}}msup") is not None
    annotation = tree.find(f".//{{{MATH_NS}}}annotation")
    assert annotation is not None
    assert annotation.text == r"f'(z)=\frac{-2i}{(1+z)^2}"


@pytest.mark.parametrize(
    "tex", [r"\href{https://example.org}{x}", r"\includegraphics{x}", "x" * 3001]
)
def test_math_rejects_active_commands_and_oversized_input(tex: str) -> None:
    with pytest.raises(ValueError, match="Unsupported or oversized"):
        mathml(tex)


def test_math_renderer_preserves_program_listings(tmp_path: Path) -> None:
    source = "# Map\n\n$f(z)=\\frac{1}{z}$\n\n`$leave_code$`\n\n```python\nprint('$not_math$')\n```"
    rendered = document(source, tmp_path / "note.md", tmp_path)
    assert "<mfrac>" in rendered
    assert "<code>$leave_code$</code>" in rendered
    assert "$not_math$" in rendered
    assert rendered.count("<math ") == 1


def test_inline_code_moves_to_local_files_with_enforced_policy(tmp_path: Path) -> None:
    source = (
        "<html><head><style>p{color:red}</style></head>"
        "<body><script>window.answer=42;</script></body></html>"
    )
    rendered = harden_page(source, tmp_path / "index.html", tmp_path)
    assert "window.answer=42;" not in rendered
    assert "<style>" not in rendered
    assert len(list((tmp_path / "assets/generated").glob("*.js"))) == 1
    parser = PolicyInventory()
    parser.feed(rendered)
    assert parser.policy_seen


@pytest.mark.parametrize(
    "payload",
    [
        '<img src="x" onerror="alert(1)">',
        '<iframe src="https://example.org"></iframe>',
        '<script src="https://example.org/a.js"></script>',
        '<a href="javascript:alert(1)">x</a>',
        '<input style="display:none">',
        "<script>alert(1)</script>",
        "<form></form>",
    ],
)
def test_public_markup_fails_closed(payload: str) -> None:
    parser = PolicyInventory()
    parser.feed(f'<meta http-equiv="Content-Security-Policy" content="{POLICY}">')
    with pytest.raises(ValueError, match=r"Forbidden|forbidden|Unsafe|Scripts|Remote"):
        parser.feed(payload)


@pytest.mark.parametrize("url", ["javascript:alert(1)", "data:text/html,hello", "file:///private"])
def test_unsafe_link_schemes_fail_before_rendering(tmp_path: Path, url: str) -> None:
    with pytest.raises(ValueError, match="Unsupported link scheme"):
        public_link(url, tmp_path / "index.html", tmp_path)


@pytest.mark.parametrize(
    "name", ["../secret.txt", ".env", "docs/../../secret.txt", "C:/private.txt"]
)
def test_manifest_rejects_private_or_traversing_paths(tmp_path: Path, name: str) -> None:
    (tmp_path / "web").mkdir()
    (tmp_path / "web/public-assets.json").write_text(json.dumps([name]), encoding="utf-8")
    with pytest.raises(ValueError, match="Unsafe public asset path"):
        publication_sources(tmp_path)


def test_secret_signature_and_dynamic_execution_fail_the_audit(tmp_path: Path) -> None:
    script = tmp_path / "data.js"
    script.write_text("const token='ghp_" + "X" * 36 + "';", encoding="utf-8")
    with pytest.raises(ValueError, match="Possible secret"):
        audit_publication(tmp_path)
    script.write_text("eval('1+1');", encoding="utf-8")
    with pytest.raises(ValueError, match="Unreviewed executable"):
        audit_publication(tmp_path)
