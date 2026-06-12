import time
from typing import List
from voronoi.domain.point import Point
from .voronoi_algorithm import VoronoiAlgorithm


class PerformanceAnalyzer:
    """
    Measures execution time of the Voronoï algorithm.
    """

    def measure(self, points: List[Point]) -> float:
        algorithm = VoronoiAlgorithm()

        start = time.perf_counter()
        algorithm.compute(points)
        end = time.perf_counter()

        return end - start