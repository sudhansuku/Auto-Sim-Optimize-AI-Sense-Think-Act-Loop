from __future__ import annotations

import subprocess
from pathlib import Path


def run_simulation(case_dir: Path, solver: str, timeout_s: int, log_file: Path) -> dict:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [solver, "-case", str(case_dir)]
    try:
        with log_file.open("w", encoding="utf-8") as f:
            completed = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, timeout=timeout_s)
        return {"status": "success" if completed.returncode == 0 else "failure", "returncode": completed.returncode}
    except subprocess.TimeoutExpired:
        return {"status": "failure", "reason": "timeout", "returncode": -1}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failure", "reason": str(exc), "returncode": -2}
