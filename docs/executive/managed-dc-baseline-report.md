# AtlasForge Bank - Managed Datacenter Baseline Report

> Synthetic public-safe executive report. No real infrastructure data is included.

## Executive KPIs

- **Total hosts:** 22
- **Final OK:** 22
- **Rocky Linux:** 19
- **Ubuntu exceptions:** 3
- **Docker active:** 22
- **External repo refs:** 0

## Scope

This demo models Web, API Gateway, Application API, DB Access, Messaging/Cache, DevOps Platform, and Observability tiers.

## Exceptions

- **af-gitlab-01** — FIREWALL_CONTROL_ACCEPTED_EXCEPTION — Docker-based GitLab service requires SOC-approved Docker/firewalld design before enabling host firewalld.
- **af-gitlab-runner-01** — FIREWALL_CONTROL_ACCEPTED_EXCEPTION — GitLab Runner Docker executor uses dynamic container networking and requires approved firewall model.
- **af-api-notification-legacy-01** — UBUNTU_OS_SCOPE_EXCEPTION — Legacy Ubuntu host included as migration exception in synthetic baseline.
- **af-log-legacy-01** — UBUNTU_OS_SCOPE_EXCEPTION — Legacy Ubuntu host included as migration exception in synthetic baseline.
- **af-web-legacy-01** — UBUNTU_OS_SCOPE_EXCEPTION — Legacy Ubuntu host included as migration exception in synthetic baseline.

## Evidence Pack

- Final baseline CSV: `reports/final/99-managed-dc-baseline-readonly.csv`
- Excel dashboard: `reports/final/managed-dc-baseline-cto.xlsx`
- Charts: `docs/executive/charts/*.svg`
