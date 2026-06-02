#!/usr/bin/env python3
"""Build executive HTML and Markdown reports from synthetic baseline CSV evidence."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / 'reports/final/99-managed-dc-baseline-readonly.csv'
LYNIS = ROOT / 'reports/61-lynis-rocky-summary.csv'
EXCEPTIONS = ROOT / 'reports/exceptions/74-firewalld-operational-exceptions.csv'
OUT_HTML = ROOT / 'docs/executive/managed-dc-baseline-report.html'
OUT_MD = ROOT / 'docs/executive/managed-dc-baseline-report.md'
CHART_DIR = ROOT / 'docs/executive/charts'


def read_csv(path: Path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='|'))


def svg_bar_chart(path: Path, title: str, data: dict[str, int]):
    width, height = 760, 320
    max_v = max(data.values()) if data else 1
    bar_w = 70
    gap = 28
    x = 80
    bars=[]
    for label, value in data.items():
        h = int((value / max_v) * 180)
        y = 250 - h
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="#ffffff" stroke="#000000"/>')
        bars.append(f'<text x="{x + bar_w/2}" y="275" text-anchor="middle" font-size="12">{label}</text>')
        bars.append(f'<text x="{x + bar_w/2}" y="{y - 8}" text-anchor="middle" font-size="12">{value}</text>')
        x += bar_w + gap
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>
  <text x="30" y="35" font-size="20" font-family="Arial" font-weight="bold">{title}</text>
  <line x1="60" y1="250" x2="720" y2="250" stroke="#000000"/>
  {''.join(bars)}
</svg>"""
    path.write_text(svg, encoding='utf-8')


def main():
    final = read_csv(FINAL)
    lynis = read_csv(LYNIS)
    exceptions = read_csv(EXCEPTIONS)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    os_counts = Counter(r['os'] for r in final)
    fw_counts = Counter(r['firewall_control'] for r in final)
    tier_counts = Counter(r['tier'] for r in final)
    svg_bar_chart(CHART_DIR / 'os-distribution.svg', 'OS Distribution', dict(os_counts))
    svg_bar_chart(CHART_DIR / 'firewall-control.svg', 'Firewall Control', dict(fw_counts))
    svg_bar_chart(CHART_DIR / 'tier-distribution.svg', 'Tier Distribution', dict(tier_counts))
    kpi = {
        'Total hosts': len(final),
        'Final OK': sum(1 for r in final if r['final_status'] == 'OK'),
        'Rocky Linux': os_counts.get('Rocky Linux', 0),
        'Ubuntu exceptions': os_counts.get('Ubuntu', 0),
        'Docker active': sum(1 for r in final if r['docker'] == 'active'),
        'External repo refs': sum(int(r['external_repo_refs']) for r in final),
    }
    md = ['# AtlasForge Bank - Managed Datacenter Baseline Report', '', '> Synthetic public-safe executive report. No real infrastructure data is included.', '', '## Executive KPIs', '']
    for key, value in kpi.items(): md.append(f'- **{key}:** {value}')
    md += ['', '## Scope', '', 'This demo models Web, API Gateway, Application API, DB Access, Messaging/Cache, DevOps Platform, and Observability tiers.', '', '## Exceptions', '']
    for row in exceptions:
        md.append(f"- **{row['inventory_hostname']}** — {row['exception_type']} — {row['reason']}")
    md += ['', '## Evidence Pack', '', '- Final baseline CSV: `reports/final/99-managed-dc-baseline-readonly.csv`', '- Excel dashboard: `reports/final/managed-dc-baseline-cto.xlsx`', '- Charts: `docs/executive/charts/*.svg`']
    OUT_MD.write_text('\n'.join(md) + '\n', encoding='utf-8')
    cards = ''.join(f'<div class="card"><b>{k}</b><span>{v}</span></div>' for k, v in kpi.items())
    exception_rows = ''.join(f"<tr><td>{r['inventory_hostname']}</td><td>{r['exception_type']}</td><td>{r['reason']}</td></tr>" for r in exceptions)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AtlasForge Bank - Managed DC Baseline Report</title>
<style>
body{{font-family:Arial,sans-serif;margin:40px;color:#111827;background:#ffffff}}
h1{{border-bottom:3px solid #111827;padding-bottom:10px}}
.notice{{border:1px solid #111827;padding:12px;background:#f9fafb}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0}}
.card{{border:1px solid #111827;padding:14px;background:#ffffff}}
.card b{{display:block;font-size:13px;color:#374151}}
.card span{{font-size:28px;font-weight:bold}}
table{{border-collapse:collapse;width:100%;margin-top:16px}}
th,td{{border:1px solid #111827;padding:8px;text-align:left;vertical-align:top}}
th{{background:#111827;color:#ffffff}}
img{{max-width:100%;border:1px solid #111827;margin:10px 0}}
</style>
</head>
<body>
<h1>AtlasForge Bank - Managed Datacenter Baseline Report</h1>
<p class="notice">This repository contains synthetic data for training and demonstration purposes only. It does not contain real infrastructure data, secrets, IPs, domains, or production evidence.</p>
<h2>Executive KPIs</h2>
<div class="grid">{cards}</div>
<h2>Charts</h2>
<img src="charts/os-distribution.svg" alt="OS Distribution">
<img src="charts/firewall-control.svg" alt="Firewall Control">
<img src="charts/tier-distribution.svg" alt="Tier Distribution">
<h2>Operational Exceptions</h2>
<table><thead><tr><th>Host</th><th>Exception Type</th><th>Reason</th></tr></thead><tbody>{exception_rows}</tbody></table>
<h2>Evidence Pack</h2>
<ul><li>Final baseline CSV</li><li>CTO Excel workbook</li><li>Lynis-like summary</li><li>Firewall exception register</li></ul>
</body></html>"""
    OUT_HTML.write_text(html, encoding='utf-8')
    print(f"Generated {OUT_HTML}")
    print(f"Generated {OUT_MD}")

if __name__ == '__main__':
    main()
