"""
Module domain contenant les entités métier.

Ce module expose les classes fondamentales du domaine :
- Point : Représentation d'un point 2D
- VoronoiDiagram : Structure du diagramme de Voronoï
- VoronoiEdge : Arête du diagramme
- VoronoiCell : Cellule du diagramme
"""

from src.domain.point import Point
from src.domain.voronoi_diagram import (
    VoronoiDiagram,
    VoronoiEdge,
    VoronoiCell
)

__all__ = [
    'Point',
    'VoronoiDiagram',
    'VoronoiEdge',
    'VoronoiCell'
]