# Aurora Studio website

Static, dependency-free studio site intended for Cloudflare Pages. Build command: none. Output directory: `/` (repository root). Keep the repository private if desired; connect it via Cloudflare Pages Git integration.

The site includes Home, Projects, Project Numazu, About, News and Contact. `assets/` contains supplied game screenshots. Do not add invoices, settlement spreadsheets or internal test PDFs to this public deployment.

Before changing DNS, verify the Pages preview, then add both `aurora-studio.org` and `www.aurora-studio.org` as custom domains in Cloudflare Pages. Review any existing DNS records for other subdomains and email before editing. The original Squarespace site and its article archive should remain available until migration is checked. Remaining historical news URLs require separate restoration.
