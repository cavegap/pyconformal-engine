# Publishing the gallery and companion

The repository builds a static public site for GitHub Pages. Interactive
examples retain their numerical scripts and local images; Markdown
documentation becomes HTML with working local links. The public landing
page offers learning, applications and lunar-cartography routes.

## Build locally

```bash
python -m pip install -e ".[site]"
python scripts/build_pages.py
python -m http.server 8000 --directory site
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

## GitHub Pages

Set the repository's Pages source to **GitHub Actions**. The
`Publish gallery and thesis companion` workflow builds and validates
the site on pull requests and pushes to main. Only pushes or manual
dispatches on main can deploy. The deployment job uses the
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
runs before publishing the GitHub prerelease. Attach the validated
offline static-site archive and its SHA-256 checksum.

Publication to GitHub does not upload the package to PyPI. A future
package release needs a separate packaging and compatibility review.
