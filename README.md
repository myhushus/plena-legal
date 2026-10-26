# Plena Legal Site

Static legal pages for Plena by Meroviq. GitHub Pages deploys `public/` on pushes to `main` through `.github/workflows/pages.yml`. CNAME remains `plena.meroviq.com`.

| Document | Current version | Effective date | Languages |
| --- | --- | --- | --- |
| Privacy | 1.2 | October 24, 2026 | KO / EN / ES |
| Terms | 1.1 | October 26, 2026 | KO / EN / ES |
| Licenses | 1.1 | October 26, 2026 | KO / EN / ES |

Stable public URLs: https://plena.meroviq.com/privacy, https://plena.meroviq.com/terms, https://plena.meroviq.com/licenses.
Entry pages use the browser language (`ko`, `es`, otherwise `en`). `?lang=es` selects a language; `?choose` leaves the accessible manual selector visible. Translated document links remain in the selected language. Previous published Privacy 1.0/1.1 and Terms 1.0 pages are unchanged; the original bilingual Licenses 1.0 page is preserved at `/licenses/v1.0/`. The unpublished Spanish Terms 1.0 draft was superseded by 1.1 and removed.

## Dependency baseline

App HEAD: `35596b94258d3d7c6b6e628685fc4c53a178656c`.
Audit: October 26, 2026. User-supplied `DEPENDENCY_INVENTORY.md` and `inventory.json` from `plena-spanish-integration-20261026/dependency-inventory` are the dependency source of truth. No app repository files are modified by this site.

`public/licenses/data/inventory.json` is the normalized runtime/native inventory (134 Dart runtime entries, 123 Android entries including desugaring, three Swift packages), plus audited SDK/font notices. Original texts are deduplicated under `public/licenses/texts/` and keep content SHA-256 filenames. Fonts reused from the existing Legal audit were accepted only after matching exact Plena font hashes. `scripts/render-licenses.py` regenerates the three Licenses 1.1 pages from that data. Do not translate upstream license originals or relabel Google SDK binaries as open-source Flutter plugins.

Validation: `python3 tests/validate.py`. It checks local links, dates, versions, inventory parity and original text hashes; browser locale routing, mobile layout, public HTTP and Pages deployment are also checked before completion.

Contact: plena@meroviq.com
