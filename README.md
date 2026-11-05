# CatalogNexus

Static developer landing page and legal policy suite for https://catalognexus.com/.

## Contents and operation

`index.html`, `privacy.html`, and `terms.html` are complete semantic HTML documents. `styles.css` provides the entire responsive design without JavaScript. The homepage additionally loads the explicitly requested Tailwind browser CDN; no package installation, build, backend, cookies, analytics, form submissions, or paid services are required. Legal pages do not depend on third-party scripts. `CNAME` declares the custom domain; `.nojekyll` disables Jekyll processing; `robots.txt` and `sitemap.xml` make the three public pages discoverable.

GitHub repository: https://github.com/BlueRiver01/catalognexus-site. Deployment source is `main` at `/`. The repository must remain public for the selected free hosting arrangement. Do not commit credentials or the ignored `.tools` directory.

## Policy scope and tradeoffs

The policies describe this static website's actual scope. No OAuth integration or public application API is enabled. Future integrations must disclose exact scopes, data fields, recipients, retention, and deletion behavior before collecting account data. Provider approval is separate from publishing legal pages; no approval or certification is claimed. The operator remains responsible for honoring the stated support, deletion, and support-email retention commitments.

Google Limited Use disclosure follows https://developers.google.com/terms/api-services-user-data-policy. TLS transport is distinguished from end-to-end encryption. Ephemeral payload processing is distinguished from support email, infrastructure logs, persistent catalog outputs, and provider-controlled backups. Email forwarding records must be preserved during DNS changes.

Tailwind's documentation says the Play CDN is intended for development, not production: https://tailwindcss.com/docs/installation/play-cdn. Its inclusion follows the requested stack. Complete local CSS ensures the design works when that external script is blocked. A future hardened release can remove the browser runtime or generate static Tailwind CSS if the CDN/no-build requirement changes. GitHub Pages controls HTTP response headers; custom server-side security headers cannot be configured with repository HTML alone.

## DNS and HTTPS

Only `catalognexus.com` is authorized for DNS access or changes. Apex `A` records must be `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`. `www` must be a `CNAME` to `blueriver01.github.io`. Preserve all MX and SPF records. Claim the custom domain in GitHub Pages before pointing DNS at it. Never purchase or upgrade a product for this site.

GitHub guidance: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site. DNS propagation and certificate issuance are asynchronous. After certificate approval, enable HTTPS enforcement through repository Pages settings or `gh api --method PUT repos/BlueRiver01/catalognexus-site/pages -F https_enforced=true`.

## Verification

Local structural validation passed for BOM-less UTF-8, document metadata, a single H1 and main landmark per page, unique IDs, all internal link targets and fragments, contact addresses, CNAME content, and sitemap XML. A validation pass is not a legal opinion or API approval.

Browser verification and deployment results are recorded below after execution. Windows is the authoring platform; macOS and Linux have not been independently tested. The static site does not require Python, but the adjacent Scrapper environment's mandated pytest, Ruff check, Ruff format check, and mypy checks are run separately without changing its application source.
