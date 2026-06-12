from typing import List, Tuple
from .models import Point
from .metrics import DistanceMetric, EuclideanDistance

class VoronoiEngine:
    def __init__(self, points: List[Point], padding: float = 2.0, metric: DistanceMetric = None):
        if not points:
            raise ValueError("Aucun point fourni.")
        
        # Nettoyage des doublons (Risque de précision)
        unique_map = {(p.x, p.y): p for p in points}
        self.points = list(unique_map.values())
        
        self.padding = padding
        self.metric = metric or EuclideanDistance()
        self.min_x, self.max_x, self.min_y, self.max_y = self._compute_bounds()

    def _compute_bounds(self):
        xs, ys = [p.x for p in self.points], [p.y for p in self.points]
        return min(xs)-self.padding, max(xs)+self.padding, min(ys)-self.padding, max(ys)+self.padding

    def compute_map(self, resolution: int = 500) -> Tuple[List[List[int]], tuple]:
        width_units = self.max_x - self.min_x
        height_units = self.max_y - self.min_y
        
        # Maintien du ratio d'aspect
        ratio = height_units / width_units
        w, h = (resolution, int(resolution * ratio)) if width_units > height_units else (int(resolution / ratio), resolution)

        grid = [[0 for _ in range(w)] for _ in range(h)]
        pts = [(p.x, p.y) for p in self.points] # Cache local pour performance

        # Boucle optimisée
        for j in range(h):
            real_y = self.min_y + (j / h) * height_units
            for i in range(w):
                real_x = self.min_x + (i / w) * width_units
                
                min_dist = float('inf')
                closest_idx = 0
                for idx, (px, py) in enumerate(pts):
                    # Calcul direct (vitesse max sur Python 3.14)
                    d_sq = (real_x - px)**2 + (real_y - py)**2
                    if d_sq < min_dist:
                        min_dist, closest_idx = d_sq, idx
                grid[j][i] = closest_idx
                
        return grid, (self.min_x, self.max_x, self.min_y, self.max_y)