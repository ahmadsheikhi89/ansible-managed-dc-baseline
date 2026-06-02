# Runbook 01 - Final Baseline Workflow

## Purpose

Generate a repeatable read-only evidence pack for the managed Linux datacenter baseline.

## Steps

```bash
ansible-inventory -i inventory --graph
ansible-playbook -i inventory playbooks/99-final-managed-dc-baseline-readonly.yml
python3 scripts/build-final-manager-excel.py
python3 scripts/build-final-manager-report.py
```

## Validation

```bash
test -f reports/final/99-managed-dc-baseline-readonly.csv
test -f reports/final/managed-dc-baseline-cto.xlsx
test -f docs/executive/managed-dc-baseline-report.html
```

## Rollback

Read-only audit playbooks do not change managed hosts. Delete generated report files if a run should be discarded.
