#!/usr/bin/env python3
"""Generate deterministic synthetic demo reports for AtlasForge Bank.

This script intentionally produces fictional public-safe evidence. It performs no
network access and does not inspect the local host.
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

HOSTS = [
    ("af-api-gw-out-01", "10.44.20.11", "api-gateway-outbound", "Rocky", "9.4", "Application"),
    ("af-api-gw-out-02", "10.44.20.12", "api-gateway-outbound", "Rocky", "9.4", "Application"),
    ("af-api-gw-out-03", "10.44.20.13", "api-gateway-outbound", "Rocky", "9.4", "Application"),
    ("af-api-gw-in-01", "10.44.20.21", "api-gateway-inbound", "Rocky", "9.4", "Application"),
    ("af-api-gw-in-02", "10.44.20.22", "api-gateway-inbound", "Rocky", "9.4", "Application"),
    ("af-api-gw-in-03", "10.44.20.23", "api-gateway-inbound", "Rocky", "9.4", "Application"),
    ("af-app-dev-01", "10.44.20.31", "application-dev", "Rocky", "9.4", "Application"),
    ("af-app-stg-01", "10.44.20.32", "application-staging", "Rocky", "9.4", "Application"),
    ("af-app-prd-01", "10.44.20.33", "application-production", "Rocky", "9.4", "Application"),
    ("af-gitlab-01", "10.44.30.11", "gitlab-server", "Rocky", "9.4", "Platform"),
    ("af-gitlab-runner-01", "10.44.30.12", "gitlab-runner", "Rocky", "9.4", "Platform"),
    ("af-nexus-01", "10.44.30.13", "artifact-repository", "Rocky", "9.4", "Platform"),
    ("af-push-01", "10.44.30.21", "push-service", "Ubuntu", "22.04", "Ubuntu Exception"),
    ("af-pwa-01", "10.44.20.41", "pwa-service", "Rocky", "9.4", "Application"),
    ("af-payment-dev-01", "10.44.20.51", "payment-dev", "Rocky", "9.4", "Application"),
    ("af-payment-stg-01", "10.44.20.52", "payment-staging", "Rocky", "9.4", "Application"),
    ("af-payment-prd-01", "10.44.20.53", "payment-production", "Rocky", "9.4", "Application"),
    ("af-vehicle-01", "10.44.20.61", "vehicle-service", "Ubuntu", "22.04", "Ubuntu Exception"),
    ("af-services-01", "10.44.20.62", "shared-services", "Rocky", "9.4", "Application"),
    ("af-sentry-01", "10.44.40.11", "sentry-observability", "Ubuntu", "22.04", "Ubuntu Exception"),
    ("af-hub-01", "10.44.30.31", "container-registry", "Rocky", "9.4", "Platform"),
    ("af-api-common-01", "10.44.20.71", "api-common", "Rocky", "9.4", "Application"),
]

FIREWALL_EXCEPTIONS = {"af-gitlab-01", "af-gitlab-runner-01"}


def write_pipe_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="|")
        writer.writerow(header)
        writer.writerows(rows)


def build_final_baseline() -> None:
    header = [
        "inventory_hostname", "ansible_host", "service_name", "real_hostname", "os", "version",
        "scope", "hub_hosts_entry", "git_hosts_entry", "package_manager", "external_repo_refs",
        "time_service", "time_sync", "chrony_source", "selinux", "firewalld", "firewall_control",
        "docker", "final_status", "notes",
    ]
    rows = []
    for hostname, ip, service, os_name, version, scope in HOSTS:
        is_ubuntu = os_name == "Ubuntu"
        if hostname in FIREWALL_EXCEPTIONS:
            firewalld = "inactive"
            firewall_control = "ACCEPTED_EXCEPTION"
            notes = "SOC-approved operational exception documented for Docker/firewalld design review"
        elif is_ubuntu:
            firewalld = "ufw-managed"
            firewall_control = "UBUNTU_EXCEPTION"
            notes = "Ubuntu exception host tracked outside Rocky SELinux/firewalld baseline"
        else:
            firewalld = "active"
            firewall_control = "OK"
            notes = "All baseline controls passed in synthetic evidence set"
        rows.append([
            hostname,
            ip,
            service,
            f"{hostname}.atlasforge.example",
            os_name,
            version,
            scope,
            "yes",
            "yes",
            "apt" if is_ubuntu else "dnf",
            0,
            "chronyd" if not is_ubuntu else "systemd-timesyncd+chrony-client",
            "yes",
            "ntp01.atlasforge.example",
            "NotApplicable" if is_ubuntu else "Enforcing",
            firewalld,
            firewall_control,
            "active",
            "OK",
            notes,
        ])
    write_pipe_csv(REPO_ROOT / "reports/final/99-managed-dc-baseline-readonly.csv", header, rows)


def build_exceptions() -> None:
    header = ["inventory_hostname", "ansible_host", "service_name", "exception_type", "owner_team", "risk_level", "approval_status", "reason", "review_cycle", "notes"]
    rows = []
    lookup = {h[0]: h for h in HOSTS}
    for hostname in ["af-gitlab-01", "af-gitlab-runner-01"]:
        h = lookup[hostname]
        rows.append([
            hostname,
            h[1],
            h[2],
            "FIREWALLD_DOCKER_DESIGN",
            "Digital Infrastructure Engineering",
            "Medium",
            "Accepted for demo baseline",
            "Docker-based GitLab and GitLab Runner require SOC-approved Docker/firewalld design before enabling host firewalld.",
            "Quarterly",
            "Synthetic public-safe exception record",
        ])
    write_pipe_csv(REPO_ROOT / "reports/exceptions/74-firewalld-operational-exceptions.csv", header, rows)


def build_firewall_report() -> None:
    header = ["inventory_hostname", "ansible_host", "service_name", "docker", "firewalld", "required_action", "control_status", "notes"]
    rows = [
        ["af-gitlab-01", "10.44.30.11", "gitlab-server", "active", "inactive", "Design SOC-approved Docker/firewalld policy", "ACCEPTED_EXCEPTION", "Synthetic GitLab firewalld evidence"],
        ["af-gitlab-runner-01", "10.44.30.12", "gitlab-runner", "active", "inactive", "Design SOC-approved Docker/firewalld policy", "ACCEPTED_EXCEPTION", "Synthetic Runner firewalld evidence"],
    ]
    write_pipe_csv(REPO_ROOT / "reports/firewall/73-gitlab-firewalld-readonly-report.csv", header, rows)


def build_repo_cleanup_report() -> None:
    header = ["inventory_hostname", "ansible_host", "os", "package_manager", "external_repo_refs", "status", "notes"]
    rows = []
    for hostname, ip, service, os_name, version, scope in HOSTS:
        rows.append([hostname, ip, os_name, "apt" if os_name == "Ubuntu" else "dnf", 0, "OK", "Only AtlasForge internal repository references found"])
    write_pipe_csv(REPO_ROOT / "reports/repo-cleanup/69-external-repo-refs-report.csv", header, rows)


def build_lynis_summary() -> None:
    header = ["inventory_hostname", "ansible_host", "service_name", "real_hostname", "os", "version", "hardening_index", "tests_done", "warnings", "suggestions", "status", "notes"]
    rows = []
    hardening = [82, 81, 83, 80, 84, 82, 79, 80, 82, 78, 79, 83, 81, 80, 82, 84, 79, 83, 81]
    warnings = [1, 1, 0, 2, 0, 1, 2, 2, 1, 3, 2, 1, 1, 2, 1, 0, 2, 1, 1]
    suggestions = [26, 25, 23, 29, 22, 24, 31, 30, 27, 35, 32, 24, 26, 30, 27, 22, 31, 24, 28]
    rocky_hosts = [h for h in HOSTS if h[3] == "Rocky"]
    for idx, h in enumerate(rocky_hosts):
        hostname, ip, service, os_name, version, _scope = h
        rows.append([hostname, ip, service, f"{hostname}.atlasforge.example", os_name, version, hardening[idx], 248 + (idx % 9), warnings[idx], suggestions[idx], "OK", "Synthetic Lynis/CIS-like evidence for training"])
    write_pipe_csv(REPO_ROOT / "reports/61-lynis-rocky-summary.csv", header, rows)


def build_sample_lynis_dat() -> None:
    path = REPO_ROOT / "reports/lynis/sample-host-lynis-report.dat"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("""# Synthetic Lynis report data for public training only
hostid=af-api-gw-out-01
os=Rocky Linux 9.4
hardening_index=82
warnings=1
suggestions=26
lynis_version=3.1.0-demo
report_generation=synthetic
""", encoding="utf-8")


def main() -> None:
    build_final_baseline()
    build_exceptions()
    build_firewall_report()
    build_repo_cleanup_report()
    build_lynis_summary()
    build_sample_lynis_dat()
    print("Synthetic demo report data generated successfully.")


if __name__ == "__main__":
    main()
