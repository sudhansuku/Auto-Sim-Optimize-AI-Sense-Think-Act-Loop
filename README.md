# Auto-Sim-Optimize-AI-Sense-Think-Act-Loop

Autonomous CIM optimization framework for orthodontic bracket injection molding with `openInjMoldSim` + Python.

## Project structure

- `optimizer/`: optimization and objective evaluation (`evaluate.py`, `nsga2_optimize.py`)
- `simulation/`: OpenFOAM dictionary editing, meshing, run orchestration, post-processing, and parallel execution
- `openfoam_case/`: base OpenFOAM case template that is cloned per evaluation
- `configs/`: YAML configuration for bounds and objective weights
- `results/`: generated case folders and Pareto exports
- `logs/`: meshing/solver logs
- `meshes/`: geometry assets and converted STL
- `scripts/`: optional entrypoints

## IGS -> STL -> snappyHexMesh workflow

1. Export CAD as ASCII `.igs` (millimeter units).
2. Convert with gmsh/FreeCAD/Salome to watertight STL.
3. Place STL under `openfoam_case/constant/triSurface/`.
4. If geometry is in mm, apply scale factor `1e-3` before meshing (meters in OpenFOAM).
5. Run `blockMesh`, `surfaceFeatureExtract`, `snappyHexMesh`, `checkMesh`.

## Numerical stability notes

- Keep consistent SI units (`Pa`, `K`, `m`) to avoid unrealistic Courant numbers.
- Start with conservative time-step controls; watch for divergence in pressure and alpha fields.
- Use cavity-only sampling files for short-shot detection to avoid background cell contamination.

## Install

```bash
pip install -r requirements.txt
```

## Run NSGA-II

```bash
python -m optimizer.nsga2_optimize
```
