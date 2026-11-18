# Publishing the gallery and companion

The repository builds a static public site for GitHub Pages. Interactive
examples retain their numerical scripts and local images; Markdown
documentation becomes HTML with working local links. The public landing
page offers learning, applications and lunar-cartography routes.

## Build locally

The hashed publication environment uses Python 3.11 or newer. For a
Python 3.10 development installation, `.[site]` selects the compatible
Markdown 3.10 series; the mathematical package still supports Python 3.10.

```bash
python -m pip install --require-hashes -r requirements/site.txt
python scripts/build_pages.py
python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open `http://localhost:8000`. The output can also be opened offline at
`site/index.html`. The builder validates local files and HTML fragments
before replacing an older generated build. It refuses to replace a
`site/` directory without its generated-build marker.

The allowlist includes the curated examples, documentation, original
thesis and reproducibility scripts. It excludes Git metadata, caches,
credentials, environment files and arbitrary workspace content. Links
to package source and notebooks lead to their GitHub pages. Source
Markdown remains the editable documentation; generated HTML stays
ignored by Git.

The reviewed input list is `web/public-assets.json`. Add a new public
asset deliberately, then rebuild and check its links. Mathematical TeX
in Markdown uses `$...$` or a separate `$$` block. HTML examples use
`data-tex` with a readable source fallback. The builder produces native
MathML and local script/style files; it does not load a remote typesetter.
See the [notation guide](notation.md) and [security boundaries](site-security.md).

With Chromium or Edge installed, run `node scripts/check_site_browser.cjs`.
Set `CHROME_PATH` if detection fails. It serves the build on loopback,
checks representative controls and math at desktop and mobile widths,
and tests that the policy blocks inline execution and outbound requests.
`SITE_SCREENSHOTS` optionally names a directory for visual review captures.

## GitHub Pages

Set the repository's Pages source to **GitHub Actions**. The
`CI` workflow builds and validates the site on pull requests and pushes
to main. The `Quality gate` requires lint, types, all nine Python/OS test
combinations and the site/browser job to pass. Only pushes to main can
deploy that run's verified artifact. The deployment job uses the
`github-pages` environment with `pages: write` and `id-token: write`.
These requirements follow the
[GitHub Pages custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

The intended public URL is
[cavegap.github.io/pyconformal-engine](https://cavegap.github.io/pyconformal-engine/).
Check the workflow's deployment result before announcing that a new
revision is live. A local build alone does not confirm publication.

## Prereleases

Keep package metadata, `pyconformal.__version__`, citation metadata and
release notes at the same version. Use a prerelease tag such as
`v0.1.0a1` for experimental work. Wait for the matching CI and Pages
deployment before publishing the GitHub prerelease. Attach the validated
offline static-site archive and its SHA-256 checksum.

Publication to GitHub does not upload the package to PyPI. A future
package release needs a separate packaging and compatibility review.
