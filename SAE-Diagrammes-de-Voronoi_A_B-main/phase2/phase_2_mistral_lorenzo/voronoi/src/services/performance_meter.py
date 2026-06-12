import time
from typing import List, Callable
from models.point import Point

class PerformanceMeter:
    """Mesure le temps d'exécution d'une fonction en fonction du nombre de points."""

    @staticmethod
    def measure(func: Callable, points: List[Point]) -> float:
        """Mesure le temps d'exécution de la fonction `func` sur la liste de points."""
        start = time.time()
        func(points)
        end = time.time()
        return end - start
