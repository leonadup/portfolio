import time
import random
from typing import List, Dict
from .models import Point
from .engine import VoronoiEngine

class VoronoiBenchmark:
    """
    Composant dédié à l'analyse des performances de l'algorithme.
    Permet de valider la scalabilité de la solution.
    """

    @staticmethod
    def generate_random_points(n: int, min_val: float = 0, max_val: float = 100) -> List[Point]:
        """Génère un jeu de données aléatoire pour les tests de charge."""
        return [
            Point(random.uniform(min_val, max_val), random.uniform(min_val, max_val))
            for _ in range(n)
        ]

    def run_suite(self, sizes: List[int], resolution: int = 300) -> Dict[int, float]:
        """
        Exécute une série de tests pour différentes tailles de données.
        Retourne un dictionnaire {nombre_de_points: temps_en_secondes}.
        """
        results = {}
        print(f"{'Points':<10} | {'Temps (s)':<10}")
        print("-" * 25)

        for size in sizes:
            points = self.generate_random_points(size)
            engine = VoronoiEngine(points)
            
            start_time = time.perf_counter()
            # On exécute le calcul lourd
            engine.compute_map(resolution=resolution)
            end_time = time.perf_counter()
            
            duration = end_time - start_time
            results[size] = duration
            print(f"{size:<10} | {duration:.4f}s")
            
        return results