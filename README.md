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

Windows is the authoring platform; macOS and Linux have not been independently tested. The static site does not require Python, but the adjacent Scrapper environment's mandated pytest, Ruff check, Ruff format check, and mypy checks were run separately without changing its application source: 104 tests passed, Ruff lint and formatting passed, and mypy found no issues in 32 source files.

### Deployment verification — November 5, 2026

- Public repository created and site committed to `main`; GitHub Pages reports a successful build from branch `main`, path `/`.
- Headless Microsoft Edge checked all three pages at widths of 1440, 768, 390, and 320 pixels, both with the Tailwind CDN enabled and blocked. Every page returned HTTP 200 with no horizontal overflow or JavaScript exceptions. Desktop and mobile screenshots were visually inspected. Browser processes and temporary HTTP servers were closed after checks.
- Spaceship readback confirms exactly four apex A records and the `www` CNAME specified above. Both original MX records and the original SPF TXT record remain intact. No other domain was queried or modified.
- PowerShell `Resolve-DnsName` confirms all four apex addresses and the `www` CNAME; Cloudflare and Google public resolvers also returned the apex records. Email MX routing was verified separately.
- GitHub approved the TLS certificate for `catalognexus.com` and `www.catalognexus.com`; its reported expiry is February 2, 2027. HTTPS enforcement is enabled. Initial negative DNS caching delayed provisioning; removing and restoring the Pages custom-domain setting restarted the check, as documented by GitHub. GitHub's automatic CNAME commits were synchronized locally.
- The homepage, privacy policy, terms, stylesheet, robots file, and sitemap were fetched over certificate-verified HTTPS and matched their local SHA-256 hashes. Both HTTP apex and HTTPS `www` return HTTP 301 to `https://catalognexus.com/`. The published CNAME also returned HTTP 200.
- No purchase, subscription, hosting upgrade, paid add-on, email, or live retailer request was made. No email verification was requested by the deployment tools. No OAuth app or third-party API approval was submitted or granted by this deployment.
