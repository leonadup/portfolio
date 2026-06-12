"""
Tests unitaires pour les générateurs de diagrammes de Voronoï.
"""

import pytest
from src.models.point import Point
from src.algorithms.voronoi_generator import VoronoiGenerator
from src.algorithms.fortune_algorithm import FortuneAlgorithm


class TestVoronoiGenerator:
    """Tests pour l'interface VoronoiGenerator."""
    
    def test_abstract_class_cannot_be_instantiated(self):
        """Vérifie que l'interface abstraite ne peut pas être instanciée."""
        with pytest.raises(TypeError):
            VoronoiGenerator()
    
    def test_concrete_class_can_be_instantiated(self):
        """Vérifie qu'une classe concrète peut être instanciée."""
        generator = FortuneAlgorithm()
        assert isinstance(generator, VoronoiGenerator)


class TestFortuneAlgorithm:
    """Tests pour l'implémentation de l'algorithme de Fortune."""
    
    def setup_method(self):
        """Initialisation avant chaque test."""
        self.generator = FortuneAlgorithm()
    
    def test_generate_with_two_points(self):
        """Test la génération avec deux points."""
        points = [Point(0, 0), Point(10, 0)]
        edges = self.generator.generate(points)
        
        assert len(edges) > 0
        # Vérifie qu'il y a une arête (la médiatrice)
        has_bisector = False
        for edge in edges:
            if edge.site1 == points[0] and edge.site2 == points[1]:
                has_bisector = True
                # La médiatrice devrait être verticale à x=5
                if edge.start and edge.end:
                    assert abs(edge.start.x - 5) < 1e-10
                    assert abs(edge.end.x - 5) < 1e-10
                break
        
        assert has_bisector
    
    def test_generate_with_three_points(self):
        """Test la génération avec trois points."""
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        edges = self.generator.generate(points)
        
        assert len(edges) > 0
        # Devrait avoir au moins 3 paires de points
        assert len([e for e in edges if e.start and e.end]) >= 3
    
    def test_generate_with_single_point(self):
        """Test la génération avec un seul point (doit échouer)."""
        points = [Point(0, 0)]
        
        with pytest.raises(ValueError) as excinfo:
            self.generator.generate(points)
        
        assert "Au moins 2 points" in str(excinfo.value)
    
    def test_generate_with_empty_list(self):
        """Test la génération avec une liste vide."""
        with pytest.raises(ValueError) as excinfo:
            self.generator.generate([])
        
        assert "ne peut pas être vide" in str(excinfo.value)
    
    def test_generate_with_invalid_points(self):
        """Test la génération avec des points invalides."""
        with pytest.raises(TypeError):
            self.generator.generate([Point(0, 0), "not a point"])
    
    def test_bounding_box_calculation(self):
        """Test le calcul de la boîte englobante."""
        points = [Point(1, 2), Point(5, 7), Point(3, 4)]
        x_min, x_max, y_min, y_max = self.generator.get_bounding_box(points)
        
        assert x_min <= 1 - self.generator.bounding_box_padding
        assert x_max >= 5 + self.generator.bounding_box_padding
        assert y_min <= 2 - self.generator.bounding_box_padding
        assert y_max >= 7 + self.generator.bounding_box_padding
    
    def test_bounding_box_with_single_point(self):
        """Test la boîte englobante avec un seul point."""
        points = [Point(5, 5)]
        x_min, x_max, y_min, y_max = self.generator.get_bounding_box(points)
        
        assert x_min == 5 - self.generator.bounding_box_padding
        assert x_max == 5 + self.generator.bounding_box_padding
        assert y_min == 5 - self.generator.bounding_box_padding
        assert y_max == 5 + self.generator.bounding_box_padding
    
    def test_bounding_box_empty_list(self):
        """Test la boîte englobante avec liste vide."""
        x_min, x_max, y_min, y_max = self.generator.get_bounding_box([])
        
        assert x_min == 0
        assert x_max == 0
        assert y_min == 0
        assert y_max == 0
    
    def test_points_are_sorted_by_y(self):
        """Vérifie que les points sont triés par y."""
        points = [Point(1, 10), Point(2, 5), Point(3, 7)]
        edges = self.generator.generate(points)
        
        # L'implémentation devrait fonctionner quel que soit l'ordre
        assert len(edges) > 0
    
    def test_vertical_bisector(self):
        """Test la création d'une médiatrice verticale."""
        p1 = Point(0, 0)
        p2 = Point(10, 0)
        x_min, x_max, y_min, y_max = 0, 10, 0, 10
        
        edge = self.generator._create_bisector_edge(p1, p2, x_min, x_max, y_min, y_max)
        
        assert edge is not None
        assert edge.start is not None
        assert edge.end is not None
        assert abs(edge.start.x - 5) < 1e-10
        assert abs(edge.end.x - 5) < 1e-10
        assert edge.start.y == y_min
        assert edge.end.y == y_max
    
    def test_horizontal_bisector(self):
        """Test la création d'une médiatrice horizontale."""
        p1 = Point(0, 0)
        p2 = Point(0, 10)
        x_min, x_max, y_min, y_max = 0, 10, 0, 10
        
        edge = self.generator._create_bisector_edge(p1, p2, x_min, x_max, y_min, y_max)
        
        assert edge is not None
        assert edge.start is not None
        assert edge.end is not None
        assert abs(edge.start.y - 5) < 1e-10
        assert abs(edge.end.y - 5) < 1e-10
        assert edge.start.x == x_min
        assert edge.end.x == x_max