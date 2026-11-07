# CatalogNexus — file-only catalog quality diagnostic

Preparing a product-data import? Get a record-by-record queue of issues to review while preserving every source record.

**Proposed pilot: US$250 for one product CSV, up to 5,000 data records and 10 MiB.** This is indicative pricing for inquiries. No order is accepted, contract formed, payment requested or delivery deadline promised by this page. The operator must approve a written scope and commercial terms first.

## Deliverables

- A private HTML diagnostic and machine-readable JSON findings with record numbers, issue codes and the input's SHA-256 fingerprint.
- Checks for blank required values, potential SKU collisions, price and stock format problems, currency format, optional GTIN check digits, optional image URL syntax, whitespace and spreadsheet formula prefixes.
- A concise explanation of the findings, their limits, and questions to resolve before importing anything. No product values are silently guessed or corrected.

The declared schema uses `sku`, `title`, `price`, `currency`, and `stock`; optional fields are `gtin` and `image_url`. Other column layouts need an explicitly agreed mapping into a new file. This diagnostic does not certify Shopify or any other marketplace import compatibility.

## Working demonstration

The [synthetic demo report](demo-report/report.html), [JSON findings](demo-report/report.json), [fictional input](demo_catalog.csv), and [Python prototype](catalog_audit.py) show the actual current capability. The demo contains 14 data records, with 12 findings across 10 records. These are fictional products and deliberately inserted issues; this is not a client case study or evidence of financial results.

This is an AI-assisted service prototype. Automated checks have been verified against valid and invalid inputs, input-file preservation, existing-output refusal, malformed CSV, identifier check digits, HTML escaping, and a 10,000-record fixture. There are no claimed customer references, professional certifications, platform partnerships or guaranteed business results.

## Scope

This is a file diagnostic. Store access, live imports, storefront changes, stock reconciliation, image downloads, licensed-data acquisition, marketplace approval, revenue estimates and ongoing hosting are outside this proposed pilot. Collision flags need business review: repeated SKUs may be legitimate variants. GTIN checksum validity does not establish registration or product identity. Currency checks validate formatting only.

Start with your approximate record count, source column names and desired checks. Do not send customer/order data, credentials, confidential files, payment details or an entire catalog in an initial inquiry. Any sample should be synthetic or a small, non-confidential product-only extract that you are authorized to share. Data handling and retention must be agreed before accepting actual client data.

**Inquiries:** [support@catalognexus.com](mailto:support@catalognexus.com)

No payment or account connection is available on this page. Any eventual paid work and payout setup require operator approval.
