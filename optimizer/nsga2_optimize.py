from __future__ import annotations

import numpy as np
import pandas as pd
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

from optimizer.evaluate import evaluate_process


class CIMProblem(ElementwiseProblem):
    def __init__(self) -> None:
        super().__init__(n_var=4, n_obj=3, n_ieq_constr=2, xl=np.array([80, 430, 300, 0]), xu=np.array([160, 510, 370, 2]))
        self.cavity_options = [3, 4, 7]

    def _evaluate(self, x, out, *args, **kwargs):
        cavity = self.cavity_options[int(round(x[3]))]
        result = evaluate_process({"pressure": float(x[0]), "melt_temp": float(x[1]), "mold_temp": float(x[2]), "cavity_count": cavity}, run_id=f"gen{kwargs.get('algorithm').n_gen}_id{np.random.randint(1_000_000)}")
        out["F"] = [result["fill_time"], result["shrinkage"], result["confidence_low"]]
        out["G"] = [float(result["short_shot"]) - 0.3, float(result["weldline_severity"] > 0.3) - 0.3]


def run_nsga2() -> None:
    algorithm = NSGA2(pop_size=16)
    res = minimize(CIMProblem(), algorithm, ("n_gen", 10), seed=7, verbose=True)
    df = pd.DataFrame(res.F, columns=["fill_time", "shrinkage", "confidence_low"])
    df.to_csv("results/pareto_front.csv", index=False)


if __name__ == "__main__":
    run_nsga2()
