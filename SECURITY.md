# Security policy

The published gallery is a static educational site. It has no reader
accounts, file uploads, payment flow or application backend. Python files
are source downloads; GitHub Pages does not execute them for visitors.
The absence of a backend reduces exposure but does not establish zero risk.

## Reporting

Please report suspected vulnerabilities through
[GitHub private vulnerability reporting](https://github.com/cavegap/pyconformal-engine/security/advisories/new).
Do not put access tokens or exploit details in a public classroom issue.
If private reporting is unavailable, contact the repository owner through
the account's published contact route before disclosing sensitive details.

## Maintenance scope

Security changes target the current main branch. Historical prerelease
archives are immutable snapshots and may lack later site hardening.
Use the current public site or a current checkout for the latest changes.
See the [site-security notes](docs/site-security.md) for the controls,
their validation and the remaining hosting limits.

Maintainers should use a passkey or strong two-factor authentication,
review collaborators and installed GitHub Apps, and protect publication
branches. These account controls require owner verification; a successful
site build does not prove the account is secure.
