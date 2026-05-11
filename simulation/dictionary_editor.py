from __future__ import annotations

from pathlib import Path
from typing import Mapping

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def _write_dict(path: Path, updater) -> None:
    foam = ParsedParameterFile(str(path))
    updater(foam)
    foam.writeFile()


def update_pressure(case_dir: Path, pressure_mpa: float) -> None:
    u_file = case_dir / "0" / "U"

    def _update(foam) -> None:
        foam["boundaryField"]["inlet"]["type"] = "fixedValue"
        # Pressure-to-velocity proxy; replace with calibrated relation for CIM feedstock
        foam["boundaryField"]["inlet"]["value"] = f"uniform ({pressure_mpa * 1e3:.6f} 0 0)"

    _write_dict(u_file, _update)


def update_temperature(case_dir: Path, melt_temp_k: float, mold_temp_k: float) -> None:
    t_file = case_dir / "0" / "T"
    tp_file = case_dir / "constant" / "transportProperties"

    def _t_update(foam) -> None:
        foam["boundaryField"]["inlet"]["value"] = f"uniform {melt_temp_k:.3f}"

    def _tp_update(foam) -> None:
        foam["moldTemperature"] = mold_temp_k

    _write_dict(t_file, _t_update)
    _write_dict(tp_file, _tp_update)


def update_material_properties(case_dir: Path, cross_wlf: Mapping[str, float]) -> None:
    tp_file = case_dir / "constant" / "transportProperties"

    def _update(foam) -> None:
        coeffs = foam.setdefault("CrossWLFCoeffs", {})
        for key in ("n", "tauStar", "D1", "D2", "D3", "A1", "A2"):
            if key in cross_wlf:
                coeffs[key] = cross_wlf[key]

    _write_dict(tp_file, _update)
