import pytest
from src.models import Point
from src.engine import VoronoiEngine

def test_point_distance():
    """Test de base de la formule de distance euclidienne."""
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert p1.distance_to(p2) == 5.0

def test_closest_point_logic():
    """Vérifie que l'algorithme identifie le bon germe."""
    points = [Point(0, 0), Point(10, 10)]
    engine = VoronoiEngine(points)
    
    # Un point à (1,1) doit être rattaché au point (0,0) -> index 0
    assert engine.get_closest_point_index(Point(1, 1)) == 0
    # Un point à (9,9) doit être rattaché au point (10,10) -> index 1
    assert engine.get_closest_point_index(Point(9, 9)) == 1

def test_adaptive_bounds():
    """Vérifie que les limites s'adaptent aux coordonnées des points."""
    points = [Point(10, 10), Point(20, 20)]
    padding = 5
    engine = VoronoiEngine(points, padding=padding)
    
    assert engine.min_x == 10 - padding
    assert engine.max_x == 20 + padding
    assert engine.min_y == 10 - padding
    assert engine.max_y == 20 + padding

def test_compute_map_shape():
    """Vérifie que la matrice générée a les bonnes dimensions."""
    points = [Point(0, 0), Point(10, 10)]
    engine = VoronoiEngine(points)
    resolution = 100
    grid, bounds = engine.compute_map(resolution=resolution)
    
    # Comme les points forment un carré, la grille doit être carrée
    assert len(grid) == resolution
    assert len(grid[0]) == resolution