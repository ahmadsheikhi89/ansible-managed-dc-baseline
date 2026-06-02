# Ansible Managed Datacenter Baseline

Production-style public demo repository for **Ansible Managed Datacenter Baseline Automation**.

This repository models a realistic on-prem and air-gapped enterprise datacenter baseline program using **fully synthetic data**. It is designed for DevOps, infrastructure, SRE, security operations, and platform engineering teams that need a reusable pattern for read-only Linux fleet audits, evidence collection, operational exception tracking, and executive reporting.

> **Public-data disclaimer**  
> This repository contains synthetic data for training and demonstration purposes only.  
> It does not contain real infrastructure data, secrets, IPs, domains, or production evidence.

## Repository Version

Current demo model: **v1.1.0 - Clean Enterprise Datacenter Model**

The synthetic scope models 22 hosts across Web, API Gateway, Application API, DB Access, Messaging/Cache, DevOps Platform, and Observability tiers.

## Fictional Organization Context

| Field | Value |
|---|---|
| Company | AtlasForge Bank |
| Business Unit | Digital Infrastructure Engineering |
| Environment | On-Prem / Air-Gapped Datacenter Lab |
| Domain | atlasforge.example |
| Registry | registry.atlasforge.example |
| Git | git.atlasforge.example |
| Artifact Repository | nexus.atlasforge.example |
| NTP Source | ntp01.atlasforge.example |

## Synthetic Network Model

| CIDR | Purpose |
|---|---|
| 10.44.10.0/24 | Management and Ansible access |
| 10.44.20.0/24 | Web, API Gateway, Application and DB access runtime |
| 10.44.30.0/24 | Platform services, messaging and cache |
| 10.44.40.0/24 | Observability and logging |

## Inventory Scope

| Metric | Value |
|---|---:|
| Total managed hosts | 22 |
| Rocky Linux managed hosts | 19 |
| Ubuntu exception hosts | 3 |
| Final OK | 22 |
| Docker active | 22 |
| Time sync yes | 22 |
| External repository references | 0 |

## Architecture

```text
AtlasForge Bank - Synthetic Enterprise Datacenter
├── API Gateway Tier
├── Web Tier
├── Application API Tier
├── DB Access Tier
├── Messaging / Cache Tier
├── DevOps Platform Tier
└── Observability Tier
```

## Safety Rules

- No real IP addresses
- No real domains
- No real hostnames
- No real usernames
- No secrets, tokens, or passwords
- No production findings
- No internal ticket references
- No copied security evidence
- Synthetic reports only

## Repository Layout

```text
ansible-managed-dc-baseline/
├── ansible.cfg
├── inventory/
├── group_vars/
├── files/
├── templates/
├── playbooks/
├── scripts/
├── reports/
├── docs/
├── archive/
└── examples/
```

## Bootstrap

```bash
sudo dnf install -y ansible-core python3 python3-openpyxl git unzip
ansible --version
python3 -c "import openpyxl; print(openpyxl.__version__)"
```

## Validate Inventory

```bash
ansible-inventory --graph
ansible-inventory --list | jq '.all.children'
```

## Run Read-only Audits

```bash
ansible-playbook playbooks/19-classify-os.yml
ansible-playbook playbooks/20-fleet-readonly-report.yml
ansible-playbook playbooks/22-audit-dnf-repos.yml
ansible-playbook playbooks/69-audit-external-repo-refs-readonly.yml
ansible-playbook playbooks/71-audit-time-sync-readonly.yml
ansible-playbook playbooks/73-audit-gitlab-firewalld-readonly.yml
```

## Generate CTO Excel Report

```bash
python3 scripts/build-final-manager-excel.py
```

Output:

```text
reports/final/managed-dc-baseline-cto.xlsx
```

Workbook sheets:

```text
00_Dashboard
01_Final_Baseline
02_Yes_No_Matrix
03_CIS_Lynis
04_Exceptions
05_Firewall_Evidence
06_Repo_Cleanup
07_Control_Checklist
```

## Generate HTML Executive Report

```bash
python3 scripts/build-final-manager-report.py
```

Outputs:

```text
docs/executive/managed-dc-baseline-report.html
docs/executive/managed-dc-baseline-report.md
docs/executive/charts/*.svg
```

## Validate GitLab and Runner Exception

```bash
grep -E 'af-gitlab-01|af-gitlab-runner-01' reports/exceptions/74-firewalld-operational-exceptions.csv
```

Expected exception type:

```text
FIREWALL_CONTROL_ACCEPTED_EXCEPTION
```

## Archive Intermediate Evidence Safely

```bash
mkdir -p archive/$(date +%Y%m%d)
cp -a reports archive/$(date +%Y%m%d)/reports-snapshot
```

Do not archive secrets, tokens, private keys, or raw production evidence.

## Mermaid Diagrams

GitHub renders Mermaid diagrams directly in Markdown files under `docs/diagrams/`.

```bash
grep -RIn '^```mermaid$' docs/diagrams/*.md
grep -RInE 'xychart-beta|themeVariables|%%\{init' docs/diagrams/*.md && exit 1 || echo "Mermaid syntax policy check passed"
```

PlantUML fallback files are available under:

```text
docs/diagrams/plantuml-fallback/
```

## Publishing to GitHub

```bash
git init
git branch -M main
git add .
git commit -m "Initial public-safe Ansible managed datacenter baseline"
git remote add origin git@github.com:ahmadsheikhi89/ansible-managed-dc-baseline.git
git push -u origin main
```

For the refactored enterprise model:

```bash
git add .
git commit -m "Refactor synthetic enterprise datacenter baseline model"
git push origin main
git tag -a v1.1.0 -m "Refactored synthetic enterprise datacenter baseline model"
git push origin v1.1.0
```

## Troubleshooting

| Problem | Check |
|---|---|
| Inventory does not load | `ansible-inventory --graph -vvv` |
| Excel script fails | `sudo dnf install -y python3-openpyxl` |
| HTML charts missing | Run `python3 scripts/build-final-manager-report.py` |
| Mermaid not rendering | Use only diagrams under `docs/diagrams/*.md` |
| No GitHub SSH access | `ssh -T git@github.com` |

## FAQ

### Is this real banking data?

No. Everything is synthetic and public-safe.

### Can I reuse this internally?

Yes. Replace the fictional inventory, reports, exception register, and repo policy values with your internal approved data.

### Does this modify hosts?

Most audit playbooks are read-only. Any example that could modify state includes an explicit note to test with `--check --diff` before production use.

### Why include Ubuntu hosts?

Many enterprise datacenters have OS exceptions. This repo demonstrates how to keep them visible without pretending they are fully compliant Rocky Linux nodes.

## Contribution Guide

- Keep all sample data synthetic
- Keep comments and code in English
- Do not commit secrets or production output
- Keep diagrams GitHub-compatible
- Keep reports deterministic
- Prefer read-only evidence collection first

## Roadmap

- Add Molecule tests for playbook syntax
- Add CI workflow for Markdown and YAML linting
- Add signed release checklist
- Add optional AWX/Tower job template examples
- Add optional Grafana dashboard import examples
