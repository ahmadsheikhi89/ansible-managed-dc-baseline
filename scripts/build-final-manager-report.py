#!/usr/bin/env python3
"""Build executive HTML, Markdown, and SVG reports from synthetic CSV evidence."""
from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FINAL_CSV = REPO_ROOT / "reports/final/99-managed-dc-baseline-readonly.csv"
LYNIS_CSV = REPO_ROOT / "reports/61-lynis-rocky-summary.csv"
EXCEPTIONS_CSV = REPO_ROOT / "reports/exceptions/74-firewalld-operational-exceptions.csv"
HTML_OUT = REPO_ROOT / "docs/executive/managed-dc-baseline-report.html"
MD_OUT = REPO_ROOT / "docs/executive/managed-dc-baseline-report.md"
CHART_DIR = REPO_ROOT / "docs/executive/charts"


def read_pipe_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="|"))


def svg_bar_chart(title: str, data: dict[str, int], path: Path) -> None:
    width = 720
    height = 80 + 38 * len(data)
    max_value = max(data.values()) if data else 1
    rows = []
    y = 60
    for label, value in data.items():
        bar_width = int((value / max_value) * 420) if max_value else 0
        rows.append(f'<text x="20" y="{y + 16}" font-size="13">{html.escape(label)}</text>')
        rows.append(f'<rect x="220" y="{y}" width="{bar_width}" height="22" fill="#111827"/>')
        rows.append(f'<text x="{230 + bar_width}" y="{y + 16}" font-size="13">{value}</text>')
        y += 38
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>
  <text x="20" y="30" font-size="18" font-weight="700">{html.escape(title)}</text>
  {''.join(rows)}
</svg>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def markdown_table(rows: list[dict[str, str]], limit: int = 12) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows[:limit]:
        output.append("| " + " | ".join(str(row.get(h, "")).replace("|", "/") for h in headers) + " |")
    return "\n".join(output)


def main() -> None:
    final_rows = read_pipe_csv(FINAL_CSV)
    lynis_rows = read_pipe_csv(LYNIS_CSV)
    exception_rows = read_pipe_csv(EXCEPTIONS_CSV)

    os_counts = Counter(row["os"] for row in final_rows)
    fw_counts = Counter(row["firewall_control"] for row in final_rows)
    final_counts = Counter(row["final_status"] for row in final_rows)
    readiness = Counter({
        "Hosts Entry Ready": sum(1 for r in final_rows if r["hub_hosts_entry"] == "yes" and r["git_hosts_entry"] == "yes"),
        "Repo Clean": sum(1 for r in final_rows if r["external_repo_refs"] == "0"),
        "Time Sync Ready": sum(1 for r in final_rows if r["time_sync"] == "yes"),
        "Docker Ready": sum(1 for r in final_rows if r["docker"] == "active"),
        "SELinux Ready": sum(1 for r in final_rows if r["selinux"] in {"Enforcing", "NotApplicable"}),
    })

    CHART_DIR.mkdir(parents=True, exist_ok=True)
    svg_bar_chart("OS Distribution", dict(os_counts), CHART_DIR / "os-distribution.svg")
    svg_bar_chart("Firewall Control", dict(fw_counts), CHART_DIR / "firewall-control.svg")
    svg_bar_chart("Control Readiness", dict(readiness), CHART_DIR / "control-readiness.svg")

    total_hosts = len(final_rows)
    avg_lynis = round(sum(int(r["hardening_index"]) for r in lynis_rows) / len(lynis_rows), 1)

    md = f"""# AtlasForge Bank - Managed DC Baseline Executive Report

This executive report is generated from deterministic synthetic evidence for public training only.

## Executive summary

| KPI | Value |
|---|---:|
| Total managed hosts | {total_hosts} |
| Final OK hosts | {final_counts.get('OK', 0)} |
| Rocky Linux hosts | {os_counts.get('Rocky', 0)} |
| Ubuntu exception hosts | {os_counts.get('Ubuntu', 0)} |
| Docker active hosts | {sum(1 for r in final_rows if r['docker'] == 'active')} |
| Time synchronized hosts | {sum(1 for r in final_rows if r['time_sync'] == 'yes')} |
| External repository references | {sum(int(r['external_repo_refs']) for r in final_rows)} |
| Average Rocky hardening index | {avg_lynis} |

## Firewall control status

{markdown_table([{'status': k, 'count': str(v)} for k, v in fw_counts.items()])}

## Operational exceptions

{markdown_table(exception_rows)}

## Sample final baseline rows

{markdown_table(final_rows, limit=8)}

## Charts

- `docs/executive/charts/os-distribution.svg`
- `docs/executive/charts/firewall-control.svg`
- `docs/executive/charts/control-readiness.svg`
"""
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text(md, encoding="utf-8")

    def esc(value: object) -> str:
        return html.escape(str(value))

    kpi_cards = "".join([
        f'<div class="card"><div class="metric">{esc(value)}</div><div class="label">{esc(label)}</div></div>'
        for label, value in [
            ("Total Hosts", total_hosts),
            ("Final OK", final_counts.get("OK", 0)),
            ("Rocky Linux", os_counts.get("Rocky", 0)),
            ("Ubuntu Exception", os_counts.get("Ubuntu", 0)),
            ("External Repo Refs", sum(int(r["external_repo_refs"]) for r in final_rows)),
            ("Average Lynis Index", avg_lynis),
        ]
    ])

    def html_table(rows: list[dict[str, str]], limit: int | None = None) -> str:
        if not rows:
            return "<p>No rows.</p>"
        rows = rows if limit is None else rows[:limit]
        headers = list(rows[0].keys())
        head = "".join(f"<th>{esc(h)}</th>" for h in headers)
        body = "".join("<tr>" + "".join(f"<td>{esc(row.get(h, ''))}</td>" for h in headers) + "</tr>" for row in rows)
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AtlasForge Bank - Managed DC Baseline Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #111827; background: #ffffff; }}
    header {{ border-bottom: 3px solid #111827; padding-bottom: 16px; margin-bottom: 24px; }}
    h1 {{ margin: 0 0 8px 0; font-size: 28px; }}
    h2 {{ margin-top: 32px; border-bottom: 1px solid #D1D5DB; padding-bottom: 6px; }}
    .subtitle {{ color: #4B5563; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(160px, 1fr)); gap: 14px; }}
    .card {{ border: 1px solid #111827; padding: 16px; background: #F9FAFB; }}
    .metric {{ font-size: 28px; font-weight: 700; }}
    .label {{ color: #374151; margin-top: 6px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 13px; margin-top: 12px; }}
    th {{ background: #111827; color: #ffffff; text-align: left; }}
    th, td {{ border: 1px solid #D1D5DB; padding: 8px; vertical-align: top; }}
    .charts {{ display: grid; grid-template-columns: repeat(1, 1fr); gap: 18px; }}
    .charts img {{ border: 1px solid #D1D5DB; max-width: 100%; }}
    .notice {{ border: 1px solid #111827; padding: 12px; background: #FEF3C7; }}
    @media print {{ body {{ margin: 18px; }} .grid {{ grid-template-columns: repeat(3, 1fr); }} }}
  </style>
</head>
<body>
<header>
  <h1>AtlasForge Bank - Managed DC Baseline Report</h1>
  <div class="subtitle">Digital Infrastructure Engineering - On-Prem / Air-Gapped Datacenter Lab</div>
</header>
<section class="notice">This report contains synthetic data for training and demonstration only. It contains no real infrastructure data, secrets, IPs, domains, or production evidence.</section>
<h2>Executive KPIs</h2>
<div class="grid">{kpi_cards}</div>
<h2>Charts</h2>
<div class="charts">
  <img src="charts/os-distribution.svg" alt="OS Distribution" />
  <img src="charts/firewall-control.svg" alt="Firewall Control" />
  <img src="charts/control-readiness.svg" alt="Control Readiness" />
</div>
<h2>Operational Exceptions</h2>
{html_table(exception_rows)}
<h2>Sample Final Baseline Rows</h2>
{html_table(final_rows, limit=10)}
</body>
</html>
"""
    HTML_OUT.write_text(html_doc, encoding="utf-8")
    print(f"Executive HTML report generated: {HTML_OUT}")
    print(f"Executive Markdown report generated: {MD_OUT}")


if __name__ == "__main__":
    main()
