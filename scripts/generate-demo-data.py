#!/usr/bin/env python3
"""Generate deterministic synthetic demo CSV data for the public-safe baseline repository."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CREATE_SCRIPT = ROOT.parent / "create_ansible_managed_dc_baseline_v11.py"

if CREATE_SCRIPT.exists():
    subprocess.run([sys.executable, str(CREATE_SCRIPT)], check=True)
else:
    print("Demo data is already committed. Re-run report builders to refresh derived outputs.")
