Synthetic baseline evidence was generated and reviewed for the AtlasForge Bank managed datacenter demo scope.

Summary:
- 22 managed hosts checked.
- 19 Rocky Linux hosts passed SELinux enforcing baseline.
- 3 Ubuntu hosts documented as exception scope.
- Docker runtime active on all hosts.
- Time synchronization validated against ntp01.atlasforge.example.
- External repository references are zero.
- GitLab and GitLab Runner firewalld exceptions are documented for SOC design review.

Evidence package:
- Final CSV: reports/final/99-managed-dc-baseline-readonly.csv
- CTO Excel: reports/final/managed-dc-baseline-cto.xlsx
- HTML report: docs/executive/managed-dc-baseline-report.html
