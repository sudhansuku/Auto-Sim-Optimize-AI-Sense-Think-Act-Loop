from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ParameterBounds:
    pressure_mpa: tuple[float, float] = (80.0, 160.0)
    melt_temp_k: tuple[float, float] = (430.0, 510.0)
    mold_temp_k: tuple[float, float] = (300.0, 370.0)
    cavity_count: tuple[int, ...] = (3, 4, 7)


@dataclass(frozen=True)
class ObjectiveWeights:
    shrinkage: float = 0.45
    fill_time: float = 0.35
    confidence_low: float = 0.20
    short_shot_penalty: float = 5.0


@dataclass(frozen=True)
class SolverConfig:
    case_template_dir: Path = Path("openfoam_case")
    solver_binary: str = "openInjMoldSim"
    timeout_s: int = 3600
    logs_dir: Path = Path("logs")
    results_dir: Path = Path("results")


BOUNDS = ParameterBounds()
WEIGHTS = ObjectiveWeights()
SOLVER = SolverConfig()
