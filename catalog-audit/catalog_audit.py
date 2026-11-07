#!/usr/bin/env python3
"""File-only catalog diagnostic. Standard library; never changes the source CSV.

This checks the declared generic schema, not Shopify import compatibility.
Output must be a brand-new directory. No network calls or store access.
"""

import argparse
import csv
import hashlib
import html
import io
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlsplit

VERSION = "0.1.0"
REQUIRED = ("sku", "title", "price", "currency", "stock")
MAX_BYTES = 10 * 1024 * 1024
MAX_ROWS = 10000


def valid_gtin(value):
    if not re.fullmatch(r"(?:[0-9]{8}|[0-9]{12}|[0-9]{13}|[0-9]{14})", value):
        return False
    total = sum(int(n) * (3 if i % 2 == 0 else 1)
                for i, n in enumerate(reversed(value[:-1])))
    return (10 - total % 10) % 10 == int(value[-1])


def audit(data, source_name="catalog.csv", demo=False):
    if len(data) > MAX_BYTES:
        raise ValueError("File exceeds the 10 MiB limit")
    text = data.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    try:
        original_headers = next(reader)
    except StopIteration:
        raise ValueError("Empty input") from None
    headers = [h.strip().lower() for h in original_headers]
    if not headers or any(not h for h in headers):
        raise ValueError("Every column must have a name")
    if len(headers) != len(set(headers)):
        raise ValueError("Duplicate column names after case/whitespace normalization")
    missing = sorted(set(REQUIRED) - set(headers))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    issues = []
    sku_groups = defaultdict(list)
    records = 0

    def add(row, field, code, severity, detail):
        issues.append(dict(record=row, field=field, code=code,
                           severity=severity, detail=detail))

    if headers != original_headers:
        add(1, "header", "HEADER_NORMALIZATION", "review",
            "Checks used trimmed, lowercase column names; source headers were not changed.")
    for record, values in enumerate(reader, 2):
        records += 1
        if records > MAX_ROWS:
            raise ValueError("Input exceeds the 10,000 data-record limit")
        if len(values) != len(headers):
            add(record, "record", "COLUMN_COUNT", "error",
                f"Expected {len(headers)} fields; found {len(values)}. Record was not interpreted.")
            continue
        raw = dict(zip(headers, values))
        row = {k: v.strip() for k, v in raw.items()}
        for field, value in raw.items():
            if value != value.strip():
                add(record, field, "SURROUNDING_WHITESPACE", "review",
                    "Surrounding whitespace found; source was not changed.")
            if value.lstrip().startswith(("=", "+", "@", "-", "\t", "\r")):
                add(record, field, "SPREADSHEET_FORMULA_PREFIX", "review",
                    "Potential spreadsheet formula prefix. Review before opening as a spreadsheet; may be legitimate text or a negative number.")
        for field in REQUIRED:
            if not row[field]:
                add(record, field, "MISSING_VALUE", "error", "Required value is blank.")
        if row["sku"]:
            # Case/whitespace collisions are a review item, not proof of duplicate products.
            sku_groups[row["sku"].casefold()].append((record, raw["sku"]))
        if row["price"]:
            try:
                price = Decimal(row["price"])
                if not price.is_finite() or price < 0:
                    raise InvalidOperation
                if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", row["price"]):
                    add(record, "price", "PRICE_FORMAT", "review",
                        "Price is numeric but outside the declared decimal-point format.")
            except (InvalidOperation, ValueError):
                add(record, "price", "INVALID_PRICE", "error",
                    "Expected a finite, nonnegative decimal price without a currency symbol or grouping separator.")
        if row["currency"] and not re.fullmatch(r"[A-Z]{3}", row["currency"]):
            add(record, "currency", "CURRENCY_FORMAT", "error",
                "Expected three uppercase ASCII letters. Currency-code existence is not checked.")
        if row["stock"] and not re.fullmatch(r"[0-9]+", row["stock"]):
            add(record, "stock", "INVALID_STOCK", "error",
                "Expected a nonnegative whole number under this schema; backorders require a separately agreed rule.")
        if row.get("gtin") and not valid_gtin(row["gtin"]):
            add(record, "gtin", "GTIN_CHECK_DIGIT", "error",
                "GTIN length, digits or check digit failed. Ownership and product identity are not verified.")
        if row.get("image_url"):
            try:
                url = urlsplit(row["image_url"])
                valid = url.scheme in ("http", "https") and bool(url.hostname) and not url.username and not url.password and not any(c.isspace() for c in row["image_url"])
            except ValueError:
                valid = False
            if not valid:
                add(record, "image_url", "IMAGE_URL_FORMAT", "error",
                    "Expected an HTTP(S) URL without embedded credentials or whitespace. No network request was made.")
    if not records:
        raise ValueError("No data records")
    for group in sku_groups.values():
        if len(group) > 1:
            refs = ", ".join(str(r) for r, _ in group)
            for record, _ in group:
                add(record, "sku", "SKU_COLLISION", "review",
                    f"Case/whitespace-normalized SKU also occurs in records {refs}. Check variant rules before merging or changing anything.")
    issues.sort(key=lambda x: (x["record"], x["field"], x["code"]))
    return dict(tool="CatalogNexus file-only diagnostic", version=VERSION,
                demo=demo, source=source_name, source_sha256=hashlib.sha256(data).hexdigest(),
                generated_utc=datetime.now(timezone.utc).isoformat(),
                data_records=records, columns=headers,
                affected_records=len({x["record"] for x in issues if x["record"] > 1}),
                issue_counts=dict(Counter(x["code"] for x in issues)),
                severity_counts=dict(Counter(x["severity"] for x in issues)), issues=issues,
                limits=["Generic declared schema, not a Shopify or marketplace compliance certification.",
                        "Review findings do not prove invalid products or lost revenue.",
                        "GTIN registration, currency-code existence, images, inventory truth and live prices are not verified.",
                        "No source edits, store imports, network calls, payment handling or customer data needed.",
                        "Record numbers count CSV records including the header; multiline records differ from physical line numbers."])


def render(report):
    esc = lambda value: html.escape(str(value), quote=True)
    badge = "SYNTHETIC DEMO — NO CLIENT DATA" if report["demo"] else "FILE-ONLY DIAGNOSTIC"
    rows = "".join(f'<tr><td>{i["record"]}</td><td>{esc(i["field"])}</td><td>{esc(i["severity"])}</td><td><strong>{esc(i["code"])}</strong><br>{esc(i["detail"])}</td></tr>' for i in report["issues"])
    limits = "".join(f"<li>{esc(item)}</li>" for item in report["limits"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>Catalog diagnostic</title><style>body{{font:16px/1.55 system-ui,sans-serif;background:#f4f6f8;color:#172b3a;max-width:1120px;margin:40px auto;padding:0 24px}}header{{background:#122f3b;color:white;padding:32px;border-radius:12px}}h1{{font-size:36px;margin:10px 0}}.badge{{color:#9ce9d9;font-size:12px;letter-spacing:1px}}.metrics{{display:flex;gap:16px;flex-wrap:wrap;margin:24px 0}}.metric{{background:white;padding:20px;flex:1;min-width:140px;border:1px solid #dae2e7;border-radius:10px}}.metric b{{display:block;font-size:30px}}table{{border-collapse:collapse;width:100%;background:white}}td,th{{text-align:left;padding:12px;border-bottom:1px solid #dbe3e8;vertical-align:top}}th{{background:#dfe9ed}}.table{{overflow-x:auto}}code{{overflow-wrap:anywhere;font-size:12px}}footer{{margin:32px 0;color:#536774}}@media print{{body{{background:white;margin:0}}header{{color:black;background:white;padding:0}}.badge{{color:black}}tr{{break-inside:avoid}}}}</style></head><body><header><span class="badge">{badge}</span><h1>Catalog quality diagnostic</h1><p>Evidence for a review before an import. Every original record stays intact.</p></header><div class="metrics"><div class="metric"><b>{report["data_records"]}</b>data records</div><div class="metric"><b>{report["affected_records"]}</b>records with findings</div><div class="metric"><b>{len(report["issues"])}</b>findings to inspect</div></div><p><strong>Source:</strong> {esc(report["source"])}<br><strong>SHA-256:</strong> <code>{report["source_sha256"]}</code></p><h2>Review queue</h2><div class="table"><table><thead><tr><th>Record</th><th>Field</th><th>Level</th><th>Finding and next action</th></tr></thead><tbody>{rows or '<tr><td colspan="4">No findings under these checks.</td></tr>'}</tbody></table></div><h2>Scope and limits</h2><ul>{limits}</ul><footer>Generated {esc(report["generated_utc"])} · Diagnostic {esc(VERSION)} · AI-assisted prototype. A demonstration does not establish paid client experience.</footer></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, help="New directory, must not already exist")
    parser.add_argument("--demo", action="store_true", help="Label synthetic demonstrations")
    args = parser.parse_args()
    try:
        with args.source.open("rb") as handle:
            data = handle.read(MAX_BYTES + 1)
        report = audit(data, args.source.name, args.demo)
        args.output.mkdir(parents=False, exist_ok=False)
        with (args.output / "report.json").open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
        with (args.output / "report.html").open("x", encoding="utf-8") as handle:
            handle.write(render(report))
        print(f"{report['data_records']} records; {len(report['issues'])} findings. Source unchanged. Reports: {args.output}")
    except (ValueError, UnicodeError, csv.Error, OSError) as exc:
        print(f"Audit stopped: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
