from typing import List
from models.point import Point
from models.fortune_voronoi import FortuneVoronoi

class VoronoiBuilder:
    """Service pour construire un diagramme de Voronoï à partir d'une liste de points."""

    @staticmethod
    def build(points: List[Point]) -> FortuneVoronoi:
        """Construit et retourne un diagramme de Voronoï."""
        diagram = FortuneVoronoi(points)
        diagram.build()
        return diagram
