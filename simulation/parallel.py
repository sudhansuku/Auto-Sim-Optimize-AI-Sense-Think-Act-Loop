from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed

from optimizer.evaluate import evaluate_process


def run_parallel(param_sets: list[dict], max_workers: int = 4) -> list[dict]:
    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(evaluate_process, p, f"batch_{i}") for i, p in enumerate(param_sets)]
        for fut in as_completed(futures):
            results.append(fut.result())
    return results
