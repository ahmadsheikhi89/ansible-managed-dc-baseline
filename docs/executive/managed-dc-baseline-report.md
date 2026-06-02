# AtlasForge Bank - Managed DC Baseline Executive Report

This executive report is generated from deterministic synthetic evidence for public training only.

## Executive summary

| KPI | Value |
|---|---:|
| Total managed hosts | 22 |
| Final OK hosts | 22 |
| Rocky Linux hosts | 19 |
| Ubuntu exception hosts | 3 |
| Docker active hosts | 22 |
| Time synchronized hosts | 22 |
| External repository references | 0 |
| Average Rocky hardening index | 81.2 |

## Firewall control status

| status | count |
| --- | --- |
| OK | 17 |
| ACCEPTED_EXCEPTION | 2 |
| UBUNTU_EXCEPTION | 3 |

## Operational exceptions

| inventory_hostname | ansible_host | service_name | exception_type | owner_team | risk_level | approval_status | reason | review_cycle | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| af-gitlab-01 | 10.44.30.11 | gitlab-server | FIREWALLD_DOCKER_DESIGN | Digital Infrastructure Engineering | Medium | Accepted for demo baseline | Docker-based GitLab and GitLab Runner require SOC-approved Docker/firewalld design before enabling host firewalld. | Quarterly | Synthetic public-safe exception record |
| af-gitlab-runner-01 | 10.44.30.12 | gitlab-runner | FIREWALLD_DOCKER_DESIGN | Digital Infrastructure Engineering | Medium | Accepted for demo baseline | Docker-based GitLab and GitLab Runner require SOC-approved Docker/firewalld design before enabling host firewalld. | Quarterly | Synthetic public-safe exception record |

## Sample final baseline rows

| inventory_hostname | ansible_host | service_name | real_hostname | os | version | scope | hub_hosts_entry | git_hosts_entry | package_manager | external_repo_refs | time_service | time_sync | chrony_source | selinux | firewalld | firewall_control | docker | final_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| af-api-gw-out-01 | 10.44.20.11 | api-gateway-outbound | af-api-gw-out-01.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-api-gw-out-02 | 10.44.20.12 | api-gateway-outbound | af-api-gw-out-02.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-api-gw-out-03 | 10.44.20.13 | api-gateway-outbound | af-api-gw-out-03.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-api-gw-in-01 | 10.44.20.21 | api-gateway-inbound | af-api-gw-in-01.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-api-gw-in-02 | 10.44.20.22 | api-gateway-inbound | af-api-gw-in-02.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-api-gw-in-03 | 10.44.20.23 | api-gateway-inbound | af-api-gw-in-03.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-app-dev-01 | 10.44.20.31 | application-dev | af-app-dev-01.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |
| af-app-stg-01 | 10.44.20.32 | application-staging | af-app-stg-01.atlasforge.example | Rocky | 9.4 | Application | yes | yes | dnf | 0 | chronyd | yes | ntp01.atlasforge.example | Enforcing | active | OK | active | OK | All baseline controls passed in synthetic evidence set |

## Charts

- `docs/executive/charts/os-distribution.svg`
- `docs/executive/charts/firewall-control.svg`
- `docs/executive/charts/control-readiness.svg`
