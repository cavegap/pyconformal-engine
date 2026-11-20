"""Check the boundaries of the web-only translation layer."""

import json
from pathlib import Path

import pytest
from scripts.site_languages import LanguagePage, editions


def test_translation_preserves_links_code_formulas_and_inline_spacing() -> None:
    parser = LanguagePage({"Hello": "Hola", "Read": "Leer"}, Path("docs/guide.html"), "es")
    parser.feed(
        '<html lang="en"><p>Hello <code>Hello &lt; 3</code></p>'
        '<a href="guide.html#same-id" title="Read">Read</a>'
        "<math><mtext>Hello</mtext></math>"
        '<span data-tex="x">Hello</span>'
        '<script>const message="Hello";</script></html>'
    )
    rendered = "".join(parser.parts)
    assert '<html lang="es">' in rendered
    assert "<p>Hola <code>Hello &lt; 3</code></p>" in rendered
    assert 'href="guide.html#same-id" title="Leer">Leer</a>' in rendered
    assert "<mtext>Hello</mtext>" in rendered
    assert '<span data-tex="x">Hello</span>' in rendered
    assert 'const message="Hello";' in rendered


def test_missing_prose_translation_fails_instead_of_publishing_mixed_language() -> None:
    parser = LanguagePage({}, Path("examples/map.html"), "es")
    with pytest.raises(ValueError, match="Missing Spanish translation"):
        parser.feed("<p>A new explanation</p>")


def test_translations_are_inert_text_and_english_remains_original() -> None:
    spanish = LanguagePage({"Read": "<img src=x>"}, Path("index.html"), "es")
    spanish.feed('<p title="Read">Read</p>')
    assert "<img" not in "".join(spanish.parts)
    english = LanguagePage({}, Path("index.html"), "en")
    english.feed("<p>Read &amp; compare</p>")
    assert "".join(english.parts) == "<p>Read &amp; compare</p>"


def test_english_is_static_default_and_spanish_has_native_link(tmp_path: Path) -> None:
    root = tmp_path / "source"
    config = root / "web/landing"
    config.mkdir(parents=True)
    (config / "es.json").write_text(
        json.dumps(
            {
                "Read": "Leer",
                "PyConformal Engine · Conceived and developed by César Augusto Vega Penagos.": (
                    "PyConformal Engine · Ideado y desarrollado por César Augusto Vega Penagos."
                ),
            }
        ),
        encoding="utf-8",
    )
    (config / "messages-es.json").write_text("{}", encoding="utf-8")
    output = tmp_path / "site"
    output.mkdir()
    original = '<html lang="en"><head></head><body><header></header><main>Read</main></body></html>'
    (output / "index.html").write_text(original, encoding="utf-8")
    editions(output, root)
    english = (output / "index.html").read_text(encoding="utf-8")
    spanish = (output / "es/index.html").read_text(encoding="utf-8")
    assert '<html lang="en">' in english
    assert "<main>Read</main>" in english
    assert '<html lang="es">' in spanish
    assert "<main>Leer</main>" in spanish
    assert english.index('lang="en" hreflang="en"') < english.index('lang="es" hreflang="es"')
    assert 'href="es/index.html?lang=es"' in english
    assert 'href="../index.html?lang=en"' in spanish
    assert not (output / "en").exists()
    assert english.count('class="project-credit"') == 1
    assert "Ideado y desarrollado por César Augusto Vega Penagos" in spanish
