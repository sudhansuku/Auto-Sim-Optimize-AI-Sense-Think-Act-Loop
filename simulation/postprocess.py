from __future__ import annotations

from pathlib import Path
import numpy as np


def _latest_time_dir(case_dir: Path) -> Path:
    time_dirs = [p for p in case_dir.iterdir() if p.is_dir() and p.name.replace('.', '', 1).isdigit()]
    if not time_dirs:
        raise FileNotFoundError("No time directories found")
    return sorted(time_dirs, key=lambda p: float(p.name))[-1]


def extract_fill_time(case_dir: Path) -> float:
    return float(_latest_time_dir(case_dir).name)


def detect_short_shot(case_dir: Path, threshold: float = 0.995) -> bool:
    alpha_csv = case_dir / "postProcessing" / "alphaMeltInternal.csv"
    if not alpha_csv.exists():
        return True
    arr = np.loadtxt(alpha_csv, delimiter=",", skiprows=1)
    return float(np.mean(arr[:, -1])) < threshold


def compute_shrinkage(case_dir: Path) -> float:
    rho_file = case_dir / "postProcessing" / "density_summary.csv"
    if not rho_file.exists():
        return 1.0
    arr = np.loadtxt(rho_file, delimiter=",", skiprows=1)
    rho0, rhof = arr[0, 1], arr[-1, 1]
    return max(0.0, 1.0 - rho0 / rhof)


def extract_weldline_metrics(case_dir: Path) -> dict:
    weld_file = case_dir / "postProcessing" / "weldline_metrics.csv"
    if not weld_file.exists():
        return {"severity": 1.0, "confidence_low": 1.0}
    arr = np.loadtxt(weld_file, delimiter=",", skiprows=1)
    return {"severity": float(arr[-1, 1]), "confidence_low": float(arr[-1, 2])}
