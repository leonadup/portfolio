"""Algorithme complet de Voronoï (Delaunay brute-force + dual)."""
import itertools
import time
from typing import List, Tuple
from src.models.point import Point
from src.utils.geometry import circumcenter, get_outward_perp_direction
from src.models.voronoi_diagram import VoronoiDiagram

class VoronoiCalculator:
    """Responsabilité unique : calcul du diagramme de Voronoï."""

    @staticmethod
    def _is_empty_circle(points: List[Point], tri_idx: Tuple[int, int, int],
                         center: Point, radius: float) -> bool:
        for i, p in enumerate(points):
            if i not in tri_idx and p.distance_to(center) < radius - 1e-6:
                return False
        return True

    def compute(self, sites: List[Point]) -> VoronoiDiagram:
        """Calcule le diagramme complet (arêtes finies + rayons infinis étendus)."""
        if len(sites) < 2:
            raise ValueError("Au moins 2 points requis.")

        # 1. Delaunay brute-force
        delaunay = []
        for comb in itertools.combinations(range(len(sites)), 3):
            i, j, k = comb
            c = circumcenter(sites[i], sites[j], sites[k])
            if c is None:
                continue
            r = sites[i].distance_to(c)
            if self._is_empty_circle(sites, comb, c, r):
                delaunay.append((i, j, k, c))

        vertices = [tri[3] for tri in delaunay]

        # 2. Construction des arêtes Voronoï
        edges = []
        edge_to_tris = {}  # (sorted pair sites) -> list of triangle indices
        for t_idx, (i, j, k, _) in enumerate(delaunay):
            for pair in [(i, j), (i, k), (j, k)]:
                key = tuple(sorted(pair))
                if key not in edge_to_tris:
                    edge_to_tris[key] = []
                edge_to_tris[key].append(t_idx)

        LARGE = 1000.0  # extension des rayons
        for edge_sites, tris in edge_to_tris.items():
            a_idx, b_idx = edge_sites
            if len(tris) == 2:
                # arête finie
                v1 = vertices[tris[0]]
                v2 = vertices[tris[1]]
                edges.append((v1, v2))
            elif len(tris) == 1:
                # rayon infini (hull edge)
                t_idx = tris[0]
                tri = delaunay[t_idx]
                # trouver le third point
                third_idx = next(x for x in tri[:3] if x not in edge_sites)
                start = vertices[t_idx]
                dir_vec = get_outward_perp_direction(sites[a_idx], sites[b_idx],
                                                     sites[third_idx])
                end = Point(start.x + LARGE * dir_vec.x,
                            start.y + LARGE * dir_vec.y)
                edges.append((start, end))

        return VoronoiDiagram(sites=sites, vertices=vertices, edges=edges)

    def measure_performance(self, max_n: int = 30, trials: int = 5) -> dict:
        """Mesure temps d'exécution en fonction du nombre de points."""
        import random
        results = {}
        for n in range(3, max_n + 1, 2):
            times = []
            for _ in range(trials):
                points = [Point(random.uniform(0, 100), random.uniform(0, 100))
                          for _ in range(n)]
                start = time.perf_counter()
                self.compute(points)
                times.append(time.perf_counter() - start)
            results[n] = sum(times) / trials
        return results