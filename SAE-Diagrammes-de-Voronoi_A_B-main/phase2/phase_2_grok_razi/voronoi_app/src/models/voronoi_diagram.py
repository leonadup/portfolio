from dataclasses import dataclass
from src.models.point import Point

@dataclass
class VoronoiDiagram:
    """Contient le résultat complet du diagramme de Voronoï."""
    sites: list[Point]
    vertices: list[Point]          # sommets finis
    edges: list[tuple[Point, Point]]  # arêtes (finies ou rayon étendu)