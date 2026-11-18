# Site security and publication boundaries

This is a scoped review of the static gallery and its publication path,
not a guarantee of security or an independent penetration test.

## Architecture and controls

The browser receives static HTML, CSS, JavaScript, MathML and local
images. There is no application API, reader account, upload endpoint,
arbitrary expression evaluator or database. Numeric controls perform
their calculations locally. Python source files are served as files.

- Mathematical TeX is converted during the build. Only validated inert
  MathML is published; there is no visitor-side typesetter or math CDN.
- Inline scripts and styles are moved to local, content-named files in
  the generated output. The resource policy allows local scripts and
  styles, blocks inline event attributes and dynamic code evaluation,
  and denies connections, forms, frames, objects and workers.
- External badge images become text labels in the HTML companion.
  Following an external reference remains an explicit reader action.
  A no-referrer policy limits referrer information sent with navigation.
- An explicit public-asset manifest defines the files that may be
  copied. Traversal, symlinks, hidden files, missing inputs and common
  credential signatures fail the build. This signature check cannot
  recognize every possible secret.
- Tests include malicious URL schemes, active markup, forbidden math
  commands, inline execution, manifest traversal and unmanaged output
  safety. Browser smoke checks exercise the actual resource policy.

The resource-policy approach follows the
[OWASP CSP guidance](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html).
The generated policy is a restrictive same-origin policy; it is not
described as a nonce-based strict CSP.

## GitHub and dependency controls

Builds and tests have read-only repository access and do not retain
checkout credentials. Deployment privileges belong only to the deployment
job, which runs after the quality gate. Workflow action references are
pinned to reviewed full commit hashes, following
[GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

The site build installs only its two direct Markdown and MathML
dependencies, with pinned versions and verified wheel hashes. Weekly
Dependabot proposals cover Python dependencies and workflow actions. Pinning
improves reproducibility but does not prove a dependency safe. Review
security advisories and dependency-update proposals, then run the full
checks before accepting updates. Do not execute pull-request code in a
privileged `pull_request_target` publication job. Coverage artifacts stay
in GitHub; the workflow does not send them to a third-party coverage service.

Repository settings checked on 2026-11-18: GitHub secret scanning and push
protection were enabled. Dependency alerts, Dependabot security-update
proposals and private vulnerability reporting were enabled and confirmed
through the repository API. These settings can change independently of
the source files and need periodic review.

## Hosting limits that remain

The build inserts CSP as an early HTML meta policy. Some controls require
HTTP response headers. In particular, browsers ignore `frame-ancestors`
in a meta policy; a meta tag does not establish clickjacking protection.
Permissions-Policy, MIME-sniffing protection, cross-origin isolation and
other response-header controls are hosting responsibilities. The builder
does not pretend that an `_headers` file changes GitHub Pages responses.

If those header controls become requirements, use a host or controlled
reverse proxy that can set them and verify the actual HTTPS responses.
Retest the atlas and all interactive pages after a hosting change.
[OWASP on policy delivery and framing](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)

HTTPS must remain enabled. Account takeover, a compromised publishing
dependency, an approved malicious contribution, host outages and browser
vulnerabilities remain possible risks. Restricting resource loads does
not prevent every malicious script if a maintainer knowingly approves it
as a local asset.
[GitHub Pages HTTPS guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)

## Owner actions and operating practice

1. Verify a passkey or two-factor authentication on GitHub and retain
   recovery codes securely outside the repository.
2. Review collaborators, installed Apps, token scopes and branch rules.
   Prefer pull requests with passing checks for publication changes.
3. Review dependency alerts and update proposals regularly. Revoke and
   rotate any exposed credential; removing its current file is not enough.
4. Keep an incident contact route and a tested rollback to a known commit.
5. Review mathematical domains, units and validation as carefully as the
   technical controls. Numerical tests are not a physical calibration.

Account settings and future hosting controls must be verified separately.
See [the security policy](../SECURITY.md) and
[publication instructions](publishing.md).
