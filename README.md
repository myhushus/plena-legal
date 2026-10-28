# Plena Legal Site

Static legal pages for Plena by Meroviq. GitHub Pages deploys `public/` on pushes to `main` through `.github/workflows/pages.yml`. CNAME remains `plena.meroviq.com`.

| Document | Current version | Effective date | Languages |
| --- | --- | --- | --- |
| Privacy | 1.2 | October 24, 2026 | KO / EN / ES / FR / PT-BR / DE / JA |
| Terms | 1.1 | October 26, 2026 | KO / EN / ES / FR / PT-BR / DE / JA |
| Licenses | 1.1 | October 26, 2026 | KO / EN / ES / FR / PT-BR / DE / JA |

Stable public URLs: https://plena.meroviq.com/privacy, https://plena.meroviq.com/terms, https://plena.meroviq.com/licenses.
Entry pages use the browser language (`ko`, `es`, `fr`, `pt`, `de`, `ja`, otherwise `en`). `?lang=ja` (or `ko` / `en` / `es` / `fr` / `pt` / `de`) selects a language; `?choose` leaves the accessible manual selector visible. Translated document links remain in the selected language. Previous published Privacy 1.0/1.1 and Terms 1.0 pages are unchanged; the original bilingual Licenses 1.0 page is preserved at `/licenses/v1.0/`. The unpublished Spanish Terms 1.0 draft was superseded by 1.1 and removed.

## Dependency baseline

App HEAD: `35596b94258d3d7c6b6e628685fc4c53a178656c`.
Audit: October 26, 2026. User-supplied `DEPENDENCY_INVENTORY.md` and `inventory.json` from `plena-spanish-integration-20261026/dependency-inventory` are the dependency source of truth. No app repository files are modified by this site.

`public/licenses/data/inventory.json` is the normalized runtime/native inventory (134 Dart runtime entries, 123 Android entries including desugaring, three Swift packages), plus audited SDK/font notices. Original texts are deduplicated under `public/licenses/texts/` and keep content SHA-256 filenames. Fonts reused from the existing Legal audit were accepted only after matching exact Plena font hashes. `scripts/render-licenses.py` regenerates the seven Licenses 1.1 pages from that data. Do not translate upstream license originals or relabel Google SDK binaries as open-source Flutter plugins.

Validation: `python3 tests/validate.py`. It checks local links, dates, versions, inventory parity and original text hashes; browser locale routing, mobile layout, public HTTP and Pages deployment are also checked before completion.

Contact: plena@meroviq.com

## French translation (October 27, 2026)

French Privacy 1.2, Terms 1.1 and Licenses 1.1 translate the existing current policies. Their policy versions and effective dates remain unchanged; October 27 is the translation publication date, not a new policy effective date. Original third-party license texts, audited dependency versions and published archives are preserved. `scripts/licenses-fr.json` extends the existing notices renderer. No French-specific jurisdiction, rights, obligations or governing-law clause has been added. App French implementation and validation are separate from this Legal translation.

## Brazilian Portuguese translation (October 28, 2026)

Privacy 1.2, Terms 1.1 and Licenses 1.1 now include plain Brazilian Portuguese at `/privacy/pt/v1.2/`, `/terms/pt/v1.1/` and `/licenses/pt/v1.1/`. HTML language is `pt-BR`; browser `pt`, `pt-BR` and `pt-PT` use this same Brazilian translation, not a separate European translation. `?lang=pt-BR` works with the existing selector. Policy versions/effective dates, existing translations, archives and dependency evidence are unchanged. No Brazil-specific jurisdiction, rights, obligations or legal claims have been added. `scripts/licenses-pt.json` reuses the existing renderer. App Portuguese implementation is separate; this website does not certify an updated app binary.

## German translation (October 28, 2026)

Privacy 1.2, Terms 1.1 and Licenses 1.1 are available at `/privacy/de/v1.2/`, `/terms/de/v1.1/` and `/licenses/de/v1.1/`. Standard German uses the same informal address as the app. Browser `de`, `de-DE`, `de-AT` and `de-CH` use the shared German text; no jurisdiction-specific edition is implied. `?lang=de` explicitly selects it. Policy versions/effective dates, all five prior translations, archives, CNAME and dependency evidence remain unchanged. No German-specific governing law, collection purpose, legal basis or rights provision has been added. `scripts/licenses-de.json` reuses the existing renderer. App German implementation and Legal-link integration are separate from this website translation.

## Japanese translation (October 28, 2026)

Privacy 1.2, Terms 1.1 and Licenses 1.1 add standard Japanese at `/privacy/ja/v1.2/`, `/terms/ja/v1.1/` and `/licenses/ja/v1.1/`. Browser `ja`, `ja-JP` and other Japanese regional tags share this text; `?lang=ja` explicitly selects it. Policy versions and effective dates remain unchanged, as do existing translations, archives, dependency records and original license texts. No Japan-specific governing law, obligations, collection purpose or rights have been added. `scripts/licenses-ja.json` reuses the existing notices renderer. The license audit still describes app commit `35596b9`, not an unverified newer app binary. App Japanese implementation and Legal-link integration are separate.
