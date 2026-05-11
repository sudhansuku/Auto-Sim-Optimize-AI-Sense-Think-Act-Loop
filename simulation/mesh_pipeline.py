from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def convert_igs_to_stl(igs_path: Path, stl_path: Path, scale_mm_to_m: bool = True) -> None:
    """Use gmsh CLI for deterministic conversion.

    Example command:
    gmsh part.igs -0 -format stl -o part.stl
    """
    stl_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["gmsh", str(igs_path), "-0", "-format", "stl", "-o", str(stl_path)], check=True)
    if scale_mm_to_m:
        # If CAD was in mm, apply 1e-3 scale with surfaceTransformPoints at case level.
        pass


def run_mesh(case_dir: Path, log_file: Path) -> None:
    commands = [
        ["blockMesh", "-case", str(case_dir)],
        ["surfaceFeatureExtract", "-case", str(case_dir)],
        ["snappyHexMesh", "-overwrite", "-case", str(case_dir)],
        ["checkMesh", "-case", str(case_dir)],
    ]
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("w", encoding="utf-8") as f:
        for cmd in commands:
            subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.STDOUT)


def clone_case(template: Path, destination: Path) -> Path:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(template, destination)
    return destination
