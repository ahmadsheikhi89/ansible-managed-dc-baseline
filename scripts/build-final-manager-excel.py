#!/usr/bin/env python3
"""Build CTO-ready Excel workbook from synthetic Ansible baseline reports."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, PieChart, Reference
    from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
    from openpyxl.worksheet.table import Table, TableStyleInfo
except ImportError as exc:
    raise SystemExit("openpyxl is required. On Rocky Linux: sudo dnf install -y python3-openpyxl") from exc

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / 'reports/final/99-managed-dc-baseline-readonly.csv'
LYNIS = ROOT / 'reports/61-lynis-rocky-summary.csv'
EXCEPTIONS = ROOT / 'reports/exceptions/74-firewalld-operational-exceptions.csv'
FIREWALL = ROOT / 'reports/firewall/73-gitlab-firewalld-readonly-report.csv'
REPO_CLEANUP = ROOT / 'reports/repo-cleanup/69-external-repo-refs-report.csv'
OUTPUT = ROOT / 'reports/final/managed-dc-baseline-cto.xlsx'

INPUTS = [FINAL, LYNIS, EXCEPTIONS, FIREWALL, REPO_CLEANUP]


def read_pipe_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing input file: {path}")
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='|'))


def style_sheet(ws):
    header_fill = PatternFill('solid', fgColor='1F2937')
    header_font = Font(color='FFFFFF', bold=True)
    thin = Side(style='thin', color='D1D5DB')
    for row in ws.iter_rows():
        for cell in row:
            cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
            cell.alignment = Alignment(vertical='top', wrap_text=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
    ws.freeze_panes = 'A2'
    for col in ws.columns:
        max_len = 0
        letter = col[0].column_letter
        for cell in col:
            if cell.value is not None:
                max_len = max(max_len, min(len(str(cell.value)), 42))
        ws.column_dimensions[letter].width = max(12, min(max_len + 2, 38))


def write_table(ws, rows: list[dict[str, str]], table_name: str):
    if not rows:
        ws.append(['No data'])
        return
    headers = list(rows[0].keys())
    ws.append(headers)
    for row in rows:
        ws.append([row.get(h, '') for h in headers])
    style_sheet(ws)
    end_col = ws.max_column
    end_row = ws.max_row
    tab = Table(displayName=table_name, ref=f"A1:{ws.cell(row=end_row, column=end_col).coordinate}")
    tab.tableStyleInfo = TableStyleInfo(name='TableStyleMedium2', showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws.add_table(tab)


def main():
    final_rows = read_pipe_csv(FINAL)
    lynis_rows = read_pipe_csv(LYNIS)
    exception_rows = read_pipe_csv(EXCEPTIONS)
    firewall_rows = read_pipe_csv(FIREWALL)
    repo_rows = read_pipe_csv(REPO_CLEANUP)

    wb = Workbook()
    ws = wb.active
    ws.title = '00_Dashboard'
    sheets = {
        '01_Final_Baseline': final_rows,
        '02_Yes_No_Matrix': final_rows,
        '03_CIS_Lynis': lynis_rows,
        '04_Exceptions': exception_rows,
        '05_Firewall_Evidence': firewall_rows,
        '06_Repo_Cleanup': repo_rows,
    }
    for name, rows in sheets.items():
        write_table(wb.create_sheet(name), rows, name.replace('_',''))

    checklist = wb.create_sheet('07_Control_Checklist')
    checklist_rows = [
        {'Control': 'Inventory managed and classified', 'Status': 'READY', 'Evidence': '01_Final_Baseline'},
        {'Control': 'Internal repository policy validated', 'Status': 'READY', 'Evidence': '06_Repo_Cleanup'},
        {'Control': 'Time sync validated', 'Status': 'READY', 'Evidence': '01_Final_Baseline'},
        {'Control': 'Docker runtime validated', 'Status': 'READY', 'Evidence': '01_Final_Baseline'},
        {'Control': 'Rocky SELinux enforcing', 'Status': 'READY', 'Evidence': '01_Final_Baseline'},
        {'Control': 'Firewall exceptions documented', 'Status': 'READY', 'Evidence': '04_Exceptions'},
        {'Control': 'Lynis-like evidence collected', 'Status': 'READY', 'Evidence': '03_CIS_Lynis'},
    ]
    write_table(checklist, checklist_rows, 'ControlChecklist')

    ws['A1'] = 'AtlasForge Bank - Managed Datacenter Baseline Dashboard'
    ws['A1'].font = Font(size=16, bold=True, color='111827')
    ws.merge_cells('A1:H1')
    ws['A2'] = 'Synthetic public-safe executive report generated from demo CSV evidence.'
    ws.merge_cells('A2:H2')

    total = len(final_rows)
    os_counts = Counter(r['os'] for r in final_rows)
    status_counts = Counter(r['final_status'] for r in final_rows)
    fw_counts = Counter(r['firewall_control'] for r in final_rows)
    tier_counts = Counter(r['tier'] for r in final_rows)
    kpis = [
        ('Total Hosts', total),
        ('Final OK', status_counts.get('OK', 0)),
        ('Rocky Linux', os_counts.get('Rocky Linux', 0)),
        ('Ubuntu Exceptions', os_counts.get('Ubuntu', 0)),
        ('External Repo Refs', sum(int(r['external_repo_refs']) for r in final_rows)),
        ('Docker Active', sum(1 for r in final_rows if r['docker'] == 'active')),
        ('Time Sync Yes', sum(1 for r in final_rows if r['time_sync'] == 'yes')),
        ('SELinux Enforcing', sum(1 for r in final_rows if r['selinux'] == 'Enforcing')),
    ]
    ws.append([])
    start = 4
    ws[f'A{start}'] = 'KPI'
    ws[f'B{start}'] = 'Value'
    for idx, (k, v) in enumerate(kpis, start + 1):
        ws[f'A{idx}'] = k
        ws[f'B{idx}'] = v

    row = start
    for title, data in [('OS Distribution', os_counts), ('Final Status', status_counts), ('Firewall Control', fw_counts), ('Tier Distribution', tier_counts)]:
        col = 4 if title in ('OS Distribution','Final Status') else 7
        base_row = 4 if title in ('OS Distribution','Firewall Control') else 16
        ws.cell(base_row, col, title)
        ws.cell(base_row+1, col, 'Category')
        ws.cell(base_row+1, col+1, 'Count')
        for offset, (k, v) in enumerate(data.items(), base_row+2):
            ws.cell(offset, col, k)
            ws.cell(offset, col+1, v)
        chart = PieChart() if title in ('OS Distribution','Final Status') else BarChart()
        chart.title = title
        labels = Reference(ws, min_col=col, min_row=base_row+2, max_row=base_row+1+len(data))
        values = Reference(ws, min_col=col+1, min_row=base_row+1, max_row=base_row+1+len(data))
        chart.add_data(values, titles_from_data=True)
        chart.set_categories(labels)
        chart.height = 7
        chart.width = 9
        ws.add_chart(chart, 'J4' if title == 'OS Distribution' else 'J20' if title == 'Final Status' else 'S4' if title == 'Firewall Control' else 'S20')

    for col in ['A','B','D','E','G','H']:
        ws.column_dimensions[col].width = 24
    for cell in ws[4]:
        cell.fill = PatternFill('solid', fgColor='1F2937')
        cell.font = Font(color='FFFFFF', bold=True)
    ws.freeze_panes = 'A4'
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT)
    print(f"Generated {OUTPUT}")

if __name__ == '__main__':
    main()
