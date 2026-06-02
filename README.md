# Ansible Managed Datacenter Baseline Automation

`ansible-managed-dc-baseline` is a public-safe, enterprise-style Ansible repository that demonstrates how a platform team can standardize baseline evidence collection across a Linux fleet and produce executive-ready reporting artifacts.

The repository is intentionally built as a realistic banking infrastructure demo for **AtlasForge Bank**, a fictional organization used only for training.

> **Public-data disclaimer**  
> This repository contains synthetic data for training and demonstration purposes only.  
> It does not contain real infrastructure data, secrets, IPs, domains, or production evidence.

## 1. Project overview

This repository demonstrates a read-only infrastructure baseline workflow for an on-premises, air-gapped datacenter lab. It focuses on controls that infrastructure, platform, security, and operations teams typically need to prove before a production migration or annual audit review.

Covered controls:

| Control area | Purpose | Evidence output |
|---|---|---|
| Fleet inventory | Show managed host scope and OS classification | YAML inventory and final CSV |
| `/etc/hosts` validation | Confirm required internal service aliases exist | Final baseline CSV |
| Repository hygiene | Detect external package repository references | Repo cleanup CSV |
| Time synchronization | Validate Chrony/NTP source and sync state | Final baseline CSV |
| Docker runtime | Confirm container runtime availability | Final baseline CSV |
| Rocky SELinux | Confirm enforcing state for Rocky Linux hosts | Final baseline CSV |
| Firewall control | Validate firewalld or document exceptions | Firewall and exception CSVs |
| Lynis/CIS-like evidence | Collect training-grade hardening evidence | Lynis summary CSV |
| Executive reporting | Generate CTO-ready Excel and HTML | XLSX, HTML, Markdown, SVG |

## 2. Architecture

The fictional environment is modeled as a segmented air-gapped datacenter lab:

| Network | CIDR | Purpose |
|---|---:|---|
| Management | `10.44.10.0/24` | Administrative access and time services |
| Application | `10.44.20.0/24` | API gateways and business applications |
| Platform Services | `10.44.30.0/24` | Git, registry, Nexus, CI/CD |
| Observability | `10.44.40.0/24` | Monitoring and logging services |

Internal service endpoints:

| Service | FQDN |
|---|---|
| Internal Registry | `registry.atlasforge.example` |
| Internal Git | `git.atlasforge.example` |
| Artifact Repository | `nexus.atlasforge.example` |
| NTP Source | `ntp01.atlasforge.example` |

## 3. Safety rules

This project is safe for public GitHub release because it follows these rules:

- Uses only fictional organization names.
- Uses only `.example` domains.
- Uses only RFC1918 demonstration IP addresses.
- Contains no passwords, API keys, SSH private keys, tokens, or production evidence.
- Contains no real Jira references, personal names, or internal findings.
- All reports are deterministic synthetic data generated from local scripts.

## 4. Repository layout

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

## 5. Inventory scope

The demo inventory includes 22 managed hosts:

| OS scope | Count | Notes |
|---|---:|---|
| Rocky Linux | 19 | Primary managed baseline scope |
| Ubuntu | 3 | Operational exception hosts |
| Total | 22 | All synthetic |

Useful inventory commands:

```bash
ansible-inventory -i inventory --graph
ansible-inventory -i inventory --list > /tmp/atlasforge-inventory.json
ansible all -i inventory -m ping
```

## 6. Bootstrap workstation

Rocky Linux control-node example:

```bash
sudo dnf install -y python3 python3-pip ansible-core
python3 -m pip install --user openpyxl
ansible --version
```

If `openpyxl` is packaged internally by your OS mirror, install it without internet access:

```bash
sudo dnf install -y python3-openpyxl
```

## 7. Configure SSH access

The bootstrap playbook is intentionally isolated from the read-only audit workflow. Review it before use.

```bash
ansible-playbook -i inventory playbooks/00-bootstrap-ssh-key.yml --check --diff
ansible-playbook -i inventory playbooks/00-bootstrap-ssh-key.yml
```

## 8. Run read-only audits

Run individual control checks:

```bash
ansible-playbook -i inventory playbooks/19-classify-os.yml
ansible-playbook -i inventory playbooks/20-fleet-readonly-report.yml
ansible-playbook -i inventory playbooks/22-audit-dnf-repos.yml
ansible-playbook -i inventory playbooks/24-audit-ubuntu-apt-no-update.yml
ansible-playbook -i inventory playbooks/57-audit-rocky-epel-basic.yml
ansible-playbook -i inventory playbooks/59-audit-lynis-availability.yml
ansible-playbook -i inventory playbooks/67-cis-preflight-basic-readonly-report.yml
ansible-playbook -i inventory playbooks/69-audit-external-repo-refs-readonly.yml
ansible-playbook -i inventory playbooks/71-audit-time-sync-readonly.yml
ansible-playbook -i inventory playbooks/72-audit-chrony-selected-source-readonly.yml
ansible-playbook -i inventory playbooks/73-audit-gitlab-firewalld-readonly.yml
```

Run the final aggregator:

```bash
ansible-playbook -i inventory playbooks/99-final-managed-dc-baseline-readonly.yml
```

## 9. Generate demo data

The repository already includes generated synthetic report output. To rebuild it deterministically:

```bash
python3 scripts/generate-demo-data.py
```

## 10. Generate final CSV baseline

The final synthetic baseline lives here:

```text
reports/final/99-managed-dc-baseline-readonly.csv
```

Inspect it:

```bash
column -t -s '|' reports/final/99-managed-dc-baseline-readonly.csv | less -S
```

Expected synthetic outcome:

| Metric | Expected value |
|---|---:|
| Total hosts | 22 |
| Final OK | 22 |
| Rocky Linux | 19 |
| Ubuntu exception | 3 |
| External repo refs | 0 |
| Docker active | 22 |
| Time sync yes | 22 |
| Rocky SELinux enforcing | 19 |
| Firewall OK | 17 |
| Firewall accepted exception | 2 |
| Firewall Ubuntu exception | 3 |

## 11. Generate CTO Excel report

```bash
python3 scripts/build-final-manager-excel.py
```

Output:

```text
reports/final/managed-dc-baseline-cto.xlsx
```

Workbook sheets:

| Sheet | Purpose |
|---|---|
| `00_Dashboard` | KPI tiles and executive charts |
| `01_Final_Baseline` | Full host-level baseline matrix |
| `02_Yes_No_Matrix` | Control readiness matrix |
| `03_CIS_Lynis` | Rocky Lynis/CIS-like evidence |
| `04_Exceptions` | Operational exceptions |
| `05_Firewall_Evidence` | GitLab/Runner firewall evidence |
| `06_Repo_Cleanup` | External repository reference evidence |
| `07_Control_Checklist` | Audit control checklist |

## 12. Generate HTML executive report

```bash
python3 scripts/build-final-manager-report.py
```

Outputs:

```text
docs/executive/managed-dc-baseline-report.html
docs/executive/managed-dc-baseline-report.md
docs/executive/charts/*.svg
```

## 13. Validate GitLab/Runner exception

The only firewalld exceptions are fictional GitLab components:

```bash
column -t -s '|' reports/exceptions/74-firewalld-operational-exceptions.csv
```

Expected exception hosts:

```text
af-gitlab-01
af-gitlab-runner-01
```

Reason:

```text
Docker-based GitLab and GitLab Runner require SOC-approved Docker/firewalld design before enabling host firewalld.
```

## 14. Archive intermediate evidence

Use the archive path for generated raw outputs that should not remain in working report directories:

```bash
mkdir -p archive/$(date +%Y%m%d)-baseline-run
cp -a reports/*.csv reports/final reports/firewall reports/repo-cleanup archive/$(date +%Y%m%d)-baseline-run/
find archive -type f -name '*.log' -o -name '*.tmp'
```

Do not archive secrets, private keys, production logs, or files copied from real infrastructure.

## 15. Publish to GitHub

```bash
git init
git add .
git status
git commit -m "Initial public-safe Ansible managed DC baseline demo"
git branch -M main
git remote add origin git@github.com:YOUR-ORG/ansible-managed-dc-baseline.git
git push -u origin main
```

Before pushing, run:

```bash
grep -RInE 'password|secret|token|PRIVATE KEY|BEGIN RSA|BEGIN OPENSSH' . --exclude-dir=.git || true
python3 scripts/generate-demo-data.py
python3 scripts/build-final-manager-excel.py
python3 scripts/build-final-manager-report.py
```

## 16. Mermaid diagrams

GitHub renders Mermaid diagrams in Markdown code fences. Diagram sources are under:

```text
docs/diagrams/
```

PlantUML fallbacks are under:

```text
docs/diagrams/plantuml-fallback/
```

Validate that only stable GitHub-compatible Mermaid blocks are used:

```bash
grep -RIn '^```mermaid$' docs/diagrams/*.md
grep -RInE 'xychart-beta|themeVariables|%%\{init' docs/diagrams/*.md && exit 1 || echo "Mermaid syntax policy check passed"
```

## 17. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `openpyxl` import error | Offline host lacks Python package | Install `python3-openpyxl` from internal mirror |
| Empty Ansible facts | Python missing on remote host | Install platform Python package from internal repo |
| Chrony source unknown | `chronyc` missing or service inactive | Validate `chronyd` package and time source policy |
| SELinux unknown | Non-Rocky host or command missing | Confirm OS scope before enforcing control |
| Mermaid not rendering | Unsupported syntax or old GitHub Enterprise | Use PlantUML fallback files |
| Excel opens in protected view | File downloaded from browser | Save internally or trust the local lab path |

## 18. FAQ

### Is this repository safe for public release?

Yes. All hosts, IPs, domains, reports, exceptions, and evidence files are fictional and deterministic.

### Can this be used in a real bank?

Use it as a pattern only. Replace fictional inventory, controls, and reports with your own approved internal data after legal and security review.

### Why pipe-delimited CSV?

Pipe-delimited CSV reduces ambiguity when report notes contain commas.

### Why keep Ubuntu as an exception scope?

Many enterprise Linux fleets are not perfectly homogeneous. The repository demonstrates how to handle exceptions without hiding them.

### Why include both Excel and HTML?

Excel is useful for CTO review and follow-up actions. HTML is better for read-only executive distribution and internal portals.

## 19. Contribution guide

Contributions should preserve public-safety rules:

1. Do not add real infrastructure data.
2. Do not add secrets or internal names.
3. Keep scripts deterministic and offline-compatible.
4. Keep Markdown GitHub-compatible.
5. Keep Ansible playbooks readable and idempotent.
6. Add tests or validation commands for new report generators.

## 20. Roadmap

- Add Molecule-based syntax validation for playbooks.
- Add optional Podman runtime checks.
- Add CIS benchmark mapping sheet.
- Add signed evidence archive manifest.
- Add GitLab CI pipeline for offline validation.
- Add role-based refactor for long-term reuse.
