# Runbook 03 - GitLab and Runner Firewalld Exception

## Scope

This synthetic exception applies only to:

- `af-gitlab-01`
- `af-gitlab-runner-01`

## Reason

Docker-based GitLab and GitLab Runner require SOC-approved Docker/firewalld design before enabling host firewalld.

## Evidence

```bash
column -t -s '|' reports/exceptions/74-firewalld-operational-exceptions.csv
column -t -s '|' reports/firewall/73-gitlab-firewalld-readonly-report.csv
```

## Review cadence

Review quarterly or before any production network policy change.
