from __future__ import annotations

from pathlib import Path
from typing import Any

from simulation.config import SOLVER, WEIGHTS
from simulation.dictionary_editor import update_material_properties, update_pressure, update_temperature
from simulation.mesh_pipeline import clone_case, run_mesh
from simulation.postprocess import compute_shrinkage, detect_short_shot, extract_fill_time, extract_weldline_metrics
from simulation.runner import run_simulation


def evaluate_process(params: dict[str, Any], run_id: str) -> dict[str, Any]:
    case_dir = clone_case(SOLVER.case_template_dir, Path("results") / f"case_{run_id}")
    update_pressure(case_dir, params["pressure"])
    update_temperature(case_dir, params["melt_temp"], params["mold_temp"])
    if "cross_wlf" in params:
        update_material_properties(case_dir, params["cross_wlf"])

    run_mesh(case_dir, Path("logs") / f"mesh_{run_id}.log")
    sim = run_simulation(case_dir, SOLVER.solver_binary, SOLVER.timeout_s, Path("logs") / f"solver_{run_id}.log")
    if sim["status"] != "success":
        return {"fitness": -1e9, "fill_time": 1e9, "shrinkage": 1.0, "short_shot": True, "status": "failure"}

    fill_time = extract_fill_time(case_dir)
    shrinkage = compute_shrinkage(case_dir)
    short_shot = detect_short_shot(case_dir)
    weld = extract_weldline_metrics(case_dir)

    penalty = WEIGHTS.short_shot_penalty if short_shot else 0.0
    fitness = -(WEIGHTS.shrinkage * shrinkage + WEIGHTS.fill_time * fill_time + WEIGHTS.confidence_low * weld["confidence_low"] + penalty)

    return {
        "fitness": fitness,
        "fill_time": fill_time,
        "shrinkage": shrinkage,
        "short_shot": short_shot,
        "weldline_severity": weld["severity"],
        "confidence_low": weld["confidence_low"],
        "status": "success",
    }
