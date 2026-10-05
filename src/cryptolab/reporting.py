"""Reporting: structured JSON + HTML dashboard."""
import html, json
from datetime import datetime
from pathlib import Path

def save_json(data, path="results/results.json"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    return path

def _table(rows):
    cols = list(rows[0])
    head = "".join(f"<th>{html.escape(c)}</th>" for c in cols)
    body = "".join("<tr>" + "".join(
        f"<td>{html.escape(f'{v:.4f}' if isinstance(v, float) else str(v))}</td>" for v in r.values()) + "</tr>"
        for r in rows)
    return f"<table><tr>{head}</tr>{body}</table>"

def save_html(data, path="results/report.html"):
    sections = ""
    for name, c in data.items():
        if isinstance(c, list) and c and isinstance(c[0], dict):
            sections += f"<h2>{html.escape(name)}</h2>{_table(c)}"
        else:
            sections += f"<h2>{html.escape(name)}</h2><pre>{html.escape(json.dumps(c, indent=2, default=str))}</pre>"
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><title>CryptoLab Report</title>
<style>body{{font-family:sans-serif;margin:2rem}}table{{border-collapse:collapse;margin-bottom:1rem}}
td,th{{border:1px solid #ccc;padding:4px 8px;font-size:13px}}th{{background:#222;color:#fff}}
tr:nth-child(even){{background:#f4f4f4}}pre{{background:#f4f4f4;padding:1rem}}</style>
<h1>Comparative analysis of cryptographic algorithms</h1><p>Generated: {datetime.now():%Y-%m-%d %H:%M:%S}</p>{sections}</html>"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(page, encoding="utf-8")
    return path
