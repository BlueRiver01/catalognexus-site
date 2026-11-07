# CatalogNexus file-only diagnostic prototype

A working sales demonstration prepared on November 7, 2026. No client, sale, certification, or revenue is claimed. All demo records are fictional; example.com URLs are placeholders and are never requested.

## Run

Python 3.10+; no third-party packages, account, network, or installation required.

```sh
python3 catalog_audit.py demo_catalog.csv new-report-directory --demo
```

On this Mac, use the bundled Python executable at `/Users/jdlc/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` because the system Python currently launches a developer-tools installer.

The source is opened in binary read mode. Report files use exclusive creation; output must be a new directory whose parent exists. An existing output directory is rejected. Inputs with invalid UTF-8, malformed CSV, ambiguous headers, missing schema fields, no records, over 10 MiB, or over 10,000 records are rejected. Header names are interpreted with lowercase and trimmed whitespace. Extra named columns are retained in the input and scanned for whitespace/formula prefixes, but their business meaning is not validated.

## Declared schema

Required columns: `sku`, `title`, `price`, `currency`, `stock`. Optional: `gtin`, `image_url`. Map other export formats into a separate new file only after agreeing the mapping; this prototype does not infer Shopify schemas or create import files.

- SKU strings retain leading zeroes. Case/whitespace collisions require review; variants may legitimately repeat SKUs. Nothing is merged or fixed.
- Price must be a finite nonnegative decimal without grouping separators or currency symbols. Zero is allowed. Currency check validates three uppercase letters, not ISO registration or exchange rates.
- Stock must be a nonnegative whole number under this schema. A negative backorder policy would need a different agreed schema.
- Optional GTIN validation checks lengths 8/12/13/14 and the check digit. It does not verify registration, ownership or matching to a product.
- Image URL checks syntax only. Formula prefixes and whitespace are review findings, not automatic errors.
- JSON includes issue codes, CSV record numbers and a source SHA-256. HTML escapes dynamic content and uses no scripts or external assets.

## Commercial readiness

This is enough to demonstrate the diagnostic, not to promise a complete migration, marketplace approval, storefront changes, or sales lift. Inspect samples, agree explicit rules, verify outputs and obtain the user's approval of commercial terms before taking any paid engagement. Keep source and reports private unless authorized. A buyer's confidential catalog must not be published as a portfolio example.
