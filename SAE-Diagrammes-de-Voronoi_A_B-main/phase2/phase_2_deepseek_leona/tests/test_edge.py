"""
Tests unitaires pour le modèle Edge.
"""

import pytest
from src.models.point import Point
from src.models.edge import Edge


class TestEdge:
    """Tests pour la classe Edge."""
    
    def test_create_valid_edge(self):
        """Test la création d'une arête valide."""
        start = Point(0, 0)
        end = Point(10, 10)
        site1 = Point(1, 1)
        site2 = Point(2, 2)
        
        edge = Edge(start, end, site1, site2)
        
        assert edge.start == start
        assert edge.end == end
        assert edge.site1 == site1
        assert edge.site2 == site2
        assert edge.is_infinite == False
    
    def test_create_infinite_edge(self):
        """Test la création d'une arête infinie."""
        start = Point(0, 0)
        site1 = Point(1, 1)
        site2 = Point(2, 2)
        
        edge = Edge(start, None, site1, site2, is_infinite=True)
        
        assert edge.start == start
        assert edge.end is None
        assert edge.is_infinite == True
    
    def test_create_edge_with_invalid_sites(self):
        """Test la création avec des sites invalides."""
        start = Point(0, 0)
        end = Point(10, 10)
        
        with pytest.raises(TypeError):
            Edge(start, end, "not a point", Point(2, 2))
        
        with pytest.raises(TypeError):
            Edge(start, end, Point(1, 1), "not a point")
    
    def test_create_edge_with_invalid_start(self):
        """Test la création avec un start invalide."""
        with pytest.raises(TypeError):
            Edge("not a point", Point(10, 10), Point(1, 1), Point(2, 2))
    
    def test_is_valid_method(self):
        """Test la méthode is_valid."""
        site1 = Point(1, 1)
        site2 = Point(2, 2)
        
        # Arête avec start et end
        edge1 = Edge(Point(0, 0), Point(10, 10), site1, site2)
        assert edge1.is_valid() == True
        
        # Arête avec seulement start
        edge2 = Edge(Point(0, 0), None, site1, site2)
        assert edge2.is_valid() == True
        
        # Arête avec seulement end
        edge3 = Edge(None, Point(10, 10), site1, site2)
        assert edge3.is_valid() == True
        
        # Arête sans extrémités
        edge4 = Edge(None, None, site1, site2)
        assert edge4.is_valid() == False
    
    def test_get_bounding_box(self):
        """Test le calcul de la boîte englobante."""
        site1 = Point(1, 1)
        site2 = Point(2, 2)
        
        # Arête avec les deux extrémités
        edge = Edge(Point(0, 0), Point(10, 10), site1, site2)
        x_min, x_max, y_min, y_max = edge.get_bounding_box()
        
        assert x_min == 0
        assert x_max == 10
        assert y_min == 0
        assert y_max == 10
        
        # Arête avec une seule extrémité
        edge2 = Edge(Point(5, 5), None, site1, site2)
        x_min, x_max, y_min, y_max = edge2.get_bounding_box()
        
        assert x_min == 5
        assert x_max == 5
        assert y_min == 5
        assert y_max == 5
        
        # Arête sans extrémités
        edge3 = Edge(None, None, site1, site2)
        x_min, x_max, y_min, y_max = edge3.get_bounding_box()
        
        assert x_min == 0
        assert x_max == 0
        assert y_min == 0
        assert y_max == 0
    
    def test_edge_immutability(self):
        """Test l'immuabilité des points (mais pas de l'arête elle-même)."""
        site1 = Point(1, 1)
        site2 = Point(2, 2)
        
        edge = Edge(Point(0, 0), Point(10, 10), site1, site2)
        
        # On peut modifier l'arête
        edge.is_infinite = True
        assert edge.is_infinite == True
        
        # Mais pas les points (ils sont immuables car Point est frozen)
        with pytest.raises(Exception):
            edge.start.x = 5
    
    def test_edge_representation(self):
        """Test la représentation string."""
        edge = Edge(Point(0, 0), Point(10, 10), Point(1, 1), Point(2, 2))
        # Pas de test spécifique, juste vérifier que ça ne plante pas
        assert repr(edge) is not None