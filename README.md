# Ansible Managed Datacenter Baseline

Production-style public demo repository for **Ansible Managed Datacenter Baseline Automation**.

This repository demonstrates how infrastructure, DevOps, SRE, security operations, and platform engineering teams can build a reusable Ansible baseline framework for Linux fleet auditing, service-group inventory modeling, evidence collection, operational exception tracking, and executive reporting.

The repository is intentionally built with **fully synthetic data** so it can be used safely for public training, internal workshops, GitHub learning, and baseline automation design.

> **Public-data disclaimer**
> This repository contains synthetic data for training and demonstration purposes only.
> It does not contain real infrastructure data, secrets, IPs, domains, hostnames, tickets, or production evidence.

---

## Repository Purpose

This project provides a public-safe pattern for:

* Managing a datacenter inventory with service-based Ansible groups
* Separating business runtime services from shared platform services
* Running read-only Linux baseline audits
* Validating repository configuration
* Validating `/etc/hosts`
* Validating time synchronization
* Validating Docker runtime state
* Validating SELinux state on Rocky Linux
* Tracking Ubuntu operational exceptions
* Tracking firewall operational exceptions
* Collecting Lynis/CIS-like evidence
* Generating CTO-ready Excel and HTML reports
* Archiving intermediate evidence safely
* Preparing a reusable internal baseline automation model

---

## Synthetic Organization Context

| Field               | Value                               |
| ------------------- | ----------------------------------- |
| Company             | AtlasForge Bank                     |
| Business Unit       | Digital Infrastructure Engineering  |
| Environment         | On-Prem / Air-Gapped Datacenter Lab |
| Domain              | atlasforge.example                  |
| Registry            | registry.atlasforge.example         |
| Git                 | git.atlasforge.example              |
| Artifact Repository | nexus.atlasforge.example            |
| NTP Source          | ntp01.atlasforge.example            |

---

## Synthetic Network Model

| CIDR          | Purpose                                                  |
| ------------- | -------------------------------------------------------- |
| 10.44.10.0/24 | Management and Ansible access                            |
| 10.44.20.0/24 | Web, API Gateway, Application API, and DB access runtime |
| 10.44.30.0/24 | Platform services, message broker, and cache             |
| 10.44.40.0/24 | Observability and logging                                |

All IP addresses, domains, hostnames, and service names in this repository are fictional.

---

## Inventory Scope

| Metric                         | Value |
| ------------------------------ | ----: |
| Total managed hosts            |    22 |
| Rocky Linux managed hosts      |    19 |
| Ubuntu exception hosts         |     3 |
| Final OK                       |    22 |
| Docker active                  |    22 |
| Time sync yes                  |    22 |
| External repository references |     0 |

---

## Service Group Model

The repository uses service-based inventory groups instead of generic host lists.

```text
AtlasForge Bank - Synthetic Managed Datacenter
├── Business Runtime Services
│   ├── Web Services
│   ├── API Gateway Services
│   ├── Application API Services
│   ├── Database Access Services
│   ├── Message Broker Services
│   └── Cache Services
└── Shared Platform Services
    ├── DevOps CI Services
    ├── Artifact Repository Services
    └── Observability Services
```

Primary service groups:

```text
web_services
api_gateway_services
application_api_services
database_access_services
message_broker_services
cache_services
devops_ci_services
artifact_repository_services
observability_services
```

Operational exception groups:

```text
firewalld_operational_exception
ubuntu_operational_exception
```

---

## Repository Layout

```text
ansible-managed-dc-baseline/
├── README.md
├── LICENSE
├── .gitignore
├── ansible.cfg
├── inventory/
│   ├── hosts.yml
│   ├── 90-active-groups.yml
│   └── 91-managed-os-scope.yml
├── group_vars/
│   └── all/
│       └── main.yml
├── host_vars/
│   └── .gitkeep
├── files/
│   └── yum.repos.d/
├── templates/
│   └── apt.sources.list.d/
├── playbooks/
├── scripts/
├── reports/
├── docs/
├── archive/
└── examples/
```

---

## Quick Start - Clone and Run the Demo

### 1. Clone the repository

Using SSH:

```bash
git clone git@github.com:ahmadsheikhi89/ansible-managed-dc-baseline.git
cd ansible-managed-dc-baseline
```

Using HTTPS:

```bash
git clone https://github.com/ahmadsheikhi89/ansible-managed-dc-baseline.git
cd ansible-managed-dc-baseline
```

### 2. Install local prerequisites

Rocky Linux / RHEL / Fedora:

```bash
sudo dnf install -y ansible-core python3 python3-openpyxl git unzip jq
```

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install -y ansible python3 python3-openpyxl git unzip jq
```

Air-gapped environments should install these packages from an approved internal repository or offline package mirror.

### 3. Validate tools

```bash
ansible --version
python3 --version
python3 -c "import openpyxl; print(openpyxl.__version__)"
git --version
```

### 4. Validate the synthetic inventory

```bash
ansible-inventory \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  --graph
```

List inventory as JSON:

```bash
ansible-inventory \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  --list
```

### 5. Validate playbook syntax

```bash
for playbook in playbooks/*.yml; do
  echo "Checking $playbook"
  ansible-playbook \
    -i inventory/hosts.yml \
    -i inventory/90-active-groups.yml \
    -i inventory/91-managed-os-scope.yml \
    "$playbook" \
    --syntax-check
done
```

---

## Demo Mode

The repository includes synthetic inventory and synthetic reports. Use demo mode when you want to understand the structure without touching real hosts.

Generate the demo reports:

```bash
python3 scripts/generate-demo-data.py
python3 scripts/build-final-manager-excel.py
python3 scripts/build-final-manager-report.py
```

Generated outputs:

```text
reports/final/managed-dc-baseline-cto.xlsx
docs/executive/managed-dc-baseline-report.html
docs/executive/managed-dc-baseline-report.md
docs/executive/charts/*.svg
```

---

## Use With Your Own Real Inventory

This repository is designed so teams can clone it, keep the structure, and replace the synthetic data with their own approved internal inventory.

> Do not commit real infrastructure data to a public fork.
> Use a private internal Git repository before adding real IP addresses, domains, hostnames, usernames, reports, or evidence.

### 1. Create an internal private copy

```bash
git clone git@github.com:ahmadsheikhi89/ansible-managed-dc-baseline.git
cd ansible-managed-dc-baseline
```

Then change the remote to your internal Git server:

```bash
git remote remove origin
git remote add origin git@git.example.internal:platform/ansible-managed-dc-baseline.git
git push -u origin main
```

### 2. Back up the synthetic inventory

```bash
mkdir -p archive/bootstrap
cp -a inventory archive/bootstrap/inventory-synthetic-demo
cp -a group_vars archive/bootstrap/group-vars-synthetic-demo
cp -a reports archive/bootstrap/reports-synthetic-demo
```

### 3. Replace `inventory/hosts.yml`

Use this file for real managed hosts, IP addresses, SSH variables, and host-level metadata.

Example structure:

```yaml
---
all:
  hosts:
    web-prd-01:
      ansible_host: 10.10.20.11
      ansible_user: ansible
      service_name: web-prd-01
      service_role: production_web_frontend
      environment: production
      os_family_expected: rocky

    api-gw-in-01:
      ansible_host: 10.10.20.21
      ansible_user: ansible
      service_name: api-gw-in-01
      service_role: inbound_api_gateway
      environment: production
      os_family_expected: rocky
```

Recommended host variables:

```yaml
ansible_host: 10.10.20.11
ansible_user: ansible
ansible_port: 22
ansible_become: true
service_name: web-prd-01
service_role: production_web_frontend
environment: production
os_family_expected: rocky
```

### 4. Replace `inventory/90-active-groups.yml`

Use this file for service-group membership.

Recommended service-group model:

```yaml
---
all:
  children:
    business_runtime_services:
      children:
        web_services:
        api_gateway_services:
        application_api_services:
        database_access_services:
        message_broker_services:
        cache_services:

    shared_platform_services:
      children:
        devops_ci_services:
        artifact_repository_services:
        observability_services:

    web_services:
      hosts:
        web-prd-01:
        web-prd-02:

    api_gateway_services:
      hosts:
        api-gw-in-01:
        api-gw-out-01:

    application_api_services:
      hosts:
        api-core-prd-01:
        api-payment-prd-01:

    database_access_services:
      hosts:
        db-proxy-01:
        db-proxy-02:

    message_broker_services:
      hosts:
        rmq-01:
        rmq-02:

    cache_services:
      hosts:
        redis-01:

    devops_ci_services:
      hosts:
        gitlab-01:
        gitlab-runner-01:

    artifact_repository_services:
      hosts:
        nexus-01:

    observability_services:
      hosts:
        monitor-01:
        log-01:

    firewalld_operational_exception:
      hosts:
        gitlab-01:
        gitlab-runner-01:

    ubuntu_operational_exception:
      hosts:
        log-01:
```

### 5. Replace `inventory/91-managed-os-scope.yml`

Use this file to separate standard managed operating systems from approved exceptions.

Example:

```yaml
---
all:
  children:
    rocky_managed:
      hosts:
        web-prd-01:
        api-gw-in-01:
        api-core-prd-01:
        db-proxy-01:
        rmq-01:
        redis-01:
        nexus-01:
        monitor-01:

    ubuntu_exception:
      hosts:
        gitlab-01:
        gitlab-runner-01:
        log-01:
```

### 6. Replace `group_vars/all/main.yml`

Use this file for internal baseline policy values.

Example:

```yaml
---
company_name: "Example Internal Company"
business_unit: "Digital Infrastructure Engineering"
environment_name: "production"
internal_domain: "example.internal"
internal_registry: "registry.example.internal"
internal_git: "git.example.internal"
internal_artifact_repo: "nexus.example.internal"
ntp_source: "ntp01.example.internal"

baseline_report_owner: "Infrastructure Automation Team"
baseline_execution_mode: "read_only"
```

Do not store secrets in `group_vars`.

### 7. Keep secrets outside Git

Do not commit:

```text
SSH private keys
Passwords
Tokens
API keys
Vault passwords
Production evidence with sensitive values
Raw security findings
Customer data
```

Recommended local-only secret files:

```text
~/.ssh/id_ed25519
~/.ansible/vault_pass
.env.local
```

---

## Real Inventory Validation Workflow

### 1. Confirm inventory parses

```bash
ansible-inventory \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  --graph
```

### 2. Confirm target selection before running

```bash
ansible-playbook \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  playbooks/20-fleet-readonly-report.yml \
  --list-hosts
```

### 3. Test one host first

```bash
ansible all \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  -m ping \
  --limit web-prd-01
```

### 4. Test one service group first

```bash
ansible web_services \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  -m ping
```

### 5. Run read-only reports with a host limit first

```bash
ansible-playbook \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  playbooks/20-fleet-readonly-report.yml \
  --limit web-prd-01
```

### 6. Run the full read-only baseline

```bash
ansible-playbook \
  -i inventory/hosts.yml \
  -i inventory/90-active-groups.yml \
  -i inventory/91-managed-os-scope.yml \
  playbooks/99-final-managed-dc-baseline-readonly.yml
```

---

## Read-only Audit Playbooks

Common read-only audit flow:

```bash
ansible-playbook playbooks/19-classify-os.yml
ansible-playbook playbooks/20-fleet-readonly-report.yml
ansible-playbook playbooks/22-audit-dnf-repos.yml
ansible-playbook playbooks/24-audit-ubuntu-apt-no-update.yml
ansible-playbook playbooks/57-audit-rocky-epel-basic.yml
ansible-playbook playbooks/59-audit-lynis-availability.yml
ansible-playbook playbooks/61-run-lynis-rocky-report.yml
ansible-playbook playbooks/67-cis-preflight-basic-readonly-report.yml
ansible-playbook playbooks/69-audit-external-repo-refs-readonly.yml
ansible-playbook playbooks/71-audit-time-sync-readonly.yml
ansible-playbook playbooks/72-audit-chrony-selected-source-readonly.yml
ansible-playbook playbooks/73-audit-gitlab-firewalld-readonly.yml
ansible-playbook playbooks/99-final-managed-dc-baseline-readonly.yml
```

For real environments, start with:

```bash
ansible-playbook playbooks/99-final-managed-dc-baseline-readonly.yml --list-hosts
ansible-playbook playbooks/99-final-managed-dc-baseline-readonly.yml --syntax-check
ansible-playbook playbooks/99-final-managed-dc-baseline-readonly.yml --limit web-prd-01
```

---

## Reports

### Final baseline CSV

```text
reports/final/99-managed-dc-baseline-readonly.csv
```

### CTO Excel workbook

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

### Executive HTML report

```bash
python3 scripts/build-final-manager-report.py
```

Outputs:

```text
docs/executive/managed-dc-baseline-report.html
docs/executive/managed-dc-baseline-report.md
docs/executive/charts/*.svg
```

---

## Operational Exceptions

This repo demonstrates exception tracking instead of hiding non-standard systems.

Example exception groups:

```text
firewalld_operational_exception
ubuntu_operational_exception
```

Example exception CSV:

```text
reports/exceptions/74-firewalld-operational-exceptions.csv
```

Exception workflow:

```bash
grep -E 'gitlab|runner|legacy' reports/exceptions/74-firewalld-operational-exceptions.csv
```

Expected policy:

```text
Exceptions must be documented, approved, time-bound, and visible in executive reporting.
```

---

## Mermaid Diagrams

GitHub-compatible Mermaid diagrams are stored under:

```text
docs/diagrams/
```

Validate Mermaid blocks:

````bash
grep -RIn '^```mermaid$' docs/diagrams/*.md
grep -RInE 'xychart-beta|themeVariables|%%\{init' docs/diagrams/*.md && exit 1 || echo "Mermaid syntax policy check passed"
````

PlantUML fallback files:

```text
docs/diagrams/plantuml-fallback/
```

---

## Safe Evidence Archiving

Create a dated evidence archive:

```bash
mkdir -p archive/$(date +%Y%m%d)
cp -a reports archive/$(date +%Y%m%d)/reports-snapshot
```

Do not archive:

```text
Secrets
Tokens
Private keys
Raw production logs
Unmasked vulnerabilities
Customer data
Internal ticket exports
```

---

## Git Workflow for Internal Teams

Recommended internal workflow:

```bash
git checkout -b feature/update-real-inventory
git status
git add inventory group_vars
git commit -m "Add internal production inventory baseline"
git push origin feature/update-real-inventory
```

Merge only after peer review.

For public forks:

```text
Do not push real inventory.
Do not push real reports.
Do not push sensitive evidence.
Do not push credentials.
```

---

## Troubleshooting

| Problem                    | Check                                               |                  |
| -------------------------- | --------------------------------------------------- | ---------------- |
| Inventory does not load    | `ansible-inventory --graph -vvv`                    |                  |
| Host not matched by group  | `ansible-inventory --graph                          | grep <hostname>` |
| SSH fails                  | `ssh -vvv <user>@<host>`                            |                  |
| Ansible ping fails         | `ansible all -m ping --limit <host>`                |                  |
| Privilege escalation fails | Check `ansible_become`, sudo policy, and SSH user   |                  |
| Excel script fails         | Install `python3-openpyxl`                          |                  |
| HTML charts missing        | Run `python3 scripts/build-final-manager-report.py` |                  |
| Mermaid does not render    | Use only diagrams under `docs/diagrams/*.md`        |                  |
| GitHub SSH fails           | `ssh -T git@github.com`                             |                  |

---

## FAQ

### Is this real banking data?

No. Everything is synthetic and public-safe.

### Can I use this inside my organization?

Yes. Clone the repository into a private internal Git server, then replace the synthetic inventory, reports, exception registers, and policy values with approved internal data.

### Does this modify hosts?

The baseline audit flow is designed around read-only evidence collection. Any playbook that may change state should be reviewed separately and tested with `--check --diff` before use.

### Why include Ubuntu exception hosts?

Enterprise environments often include exception systems. This repository demonstrates how to track them transparently instead of hiding them from reporting.

### Should I publish my real inventory?

No. Keep real hostnames, IP addresses, domains, and reports inside private internal repositories only.

---

## Contribution Guide

* Keep all sample data synthetic
* Keep comments and code in English
* Do not commit secrets or production output
* Keep diagrams GitHub-compatible
* Keep reports deterministic
* Prefer read-only evidence collection first
* Keep service groups clear and reusable
* Document every operational exception

---

## Roadmap

* Add CI validation for YAML and Markdown
* Add Ansible syntax-check workflow
* Add optional Molecule tests
* Add AWX/Tower job template examples
* Add signed release checklist
* Add optional Grafana dashboard import examples
* Add internal adoption checklist template
