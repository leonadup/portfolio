from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence
import random, time
from ..domain.geometry import Point
from ..domain.voronoi import compute_voronoi_diagram

@dataclass
class BenchmarkResult:
    n_points: int
    avg_time_ms: float

def run_benchmark(points: Sequence[Point], steps: int, repeat: int) -> List[BenchmarkResult]:
    if steps < 1 or repeat < 1:
        raise ValueError("steps and repeat must be >= 1.")
    n_total = len(points)
    if n_total < 2:
        raise ValueError("Need at least two points.")
    max_step = min(steps, n_total)
    results: List[BenchmarkResult] = []
    for k in range(1, max_step + 1):
        n_points = max(2, int(round(k * n_total / max_step)))
        n_points = min(n_points, n_total)
        rnd = random.Random(k)
        idx = list(range(n_total))
        rnd.shuffle(idx)
        subset = [points[i] for i in idx[:n_points]]
        total = 0.0
        for _ in range(repeat):
            t0 = time.perf_counter()
            compute_voronoi_diagram(subset)
            t1 = time.perf_counter()
            total += (t1 - t0)
        results.append(BenchmarkResult(n_points=n_points, avg_time_ms=(total/repeat)*1000.0))
    return results

def format_benchmark_table(results: Sequence[BenchmarkResult]) -> str:
    lines = ["n_points    avg_time_ms"]
    for r in results:
        lines.append(f"{r.n_points:<11d}{r.avg_time_ms:.3f}")
    return "\n".join(lines)
