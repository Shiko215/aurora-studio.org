# Aurora Studio website

Static website for Aurora Studio. No package installation or build command is required. Deploy the repository root (`.`) as the public output directory.

## Site map

- `/` — English home; `/project/`, `/about/`, `/news/`, `/contact/`, `/services/`, `/support/`, `/governance/` — main pages.
- `/project/project-numazu/`, `/project/revenant-of-tsushima/`, `/project/railway-depot/`, `/project/aurora-engine/` — project pages.
- `/zh-hant/`, `/zh-hans/`, `/ja/`, `/ko/` — translated core landing pages. The deeper English articles and new services/support/governance pages are not yet translated; localized landings link to those pages with an EN label.
- Selected old news slugs have clearly labeled migration summaries; the full archive has not been restored.

`build.py` and `localize.py` generate the checked-in HTML pages. Run `python build.py && python localize.py` from this directory after editing their source copy. Regenerate `sitemap.xml` when routes change.

Only public game screenshots belong in `assets/`. Keep contracts, invoices, settlement spreadsheets and internal test documents outside this repository.

The existing `CNAME` file is controlled separately and is preserved. Review the deployment preview and current DNS, email and subdomain records before routing `aurora-studio.org` or `www.aurora-studio.org` to a new host.
