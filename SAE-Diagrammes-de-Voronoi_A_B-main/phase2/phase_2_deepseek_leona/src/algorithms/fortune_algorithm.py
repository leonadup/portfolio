"""
Implémentation de l'algorithme de Fortune pour les diagrammes de Voronoï.
"""

import math
from typing import List, Tuple, Optional
from src.models.point import Point
from src.models.edge import Edge
from .voronoi_generator import VoronoiGenerator
from .geometry_utils import GeometryUtils


class FortuneAlgorithm(VoronoiGenerator):
    """
    Implémentation de l'algorithme de Fortune pour générer des diagrammes de Voronoï.
    
    Cette implémentation utilise une approche simplifiée basée sur le balayage
    de ligne (sweep line) pour construire le diagramme.
    """
    
    def __init__(self, bounding_box_padding: float = 10.0):
        """
        Initialise l'algorithme de Fortune.
        
        Args:
            bounding_box_padding: Marge à ajouter autour des points pour la boîte englobante
        """
        self.bounding_box_padding = bounding_box_padding
        self.edges: List[Edge] = []
        self.geometry_utils = GeometryUtils()
    
    def generate(self, points: List[Point]) -> List[Edge]:
        """
        Génère le diagramme de Voronoï en utilisant l'algorithme de Fortune.
        
        Args:
            points: Liste des sites
            
        Returns:
            List[Edge]: Liste des arêtes du diagramme
            
        Note:
            Version simplifiée de l'algorithme pour la démonstration.
            Une implémentation complète nécessiterait plus de structures de données.
        """
        self.validate_points(points)
        
        # Tri des points par ordre croissant de y (pour le balayage)
        sorted_points = sorted(points, key=lambda p: p.y)
        
        # Boîte englobante
        x_min, x_max, y_min, y_max = self.get_bounding_box(sorted_points)
        
        # Génération simplifiée des arêtes (médiatrices)
        self._generate_simple_diagram(sorted_points, x_min, x_max, y_min, y_max)
        
        return self.edges
    
    def _generate_simple_diagram(self, points: List[Point], 
                                  x_min: float, x_max: float, 
                                  y_min: float, y_max: float) -> None:
        """
        Génère un diagramme simplifié basé sur les médiatrices.
        
        Args:
            points: Liste des points triés
            x_min, x_max, y_min, y_max: Limites de la boîte englobante
        """
        self.edges = []
        
        # Pour chaque paire de points, ajouter leur médiatrice
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                edge = self._create_bisector_edge(points[i], points[j], 
                                                  x_min, x_max, y_min, y_max)
                if edge and edge.is_valid():
                    self.edges.append(edge)
        
        # Ajout des arêtes aux limites
        self._add_boundary_edges(points, x_min, x_max, y_min, y_max)
    
    def _create_bisector_edge(self, p1: Point, p2: Point,
                              x_min: float, x_max: float,
                              y_min: float, y_max: float) -> Optional[Edge]:
        """
        Crée une arête correspondant à la médiatrice entre deux points.
        
        Args:
            p1, p2: Les deux points
            x_min, x_max, y_min, y_max: Limites de la boîte
            
        Returns:
            Optional[Edge]: L'arête créée ou None si impossible
        """
        # Calcul de la médiatrice
        midpoint = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        
        if abs(p2.y - p1.y) < 1e-10:
            # Points alignés horizontalement -> médiatrice verticale
            edge = self._create_vertical_bisector(midpoint, y_min, y_max)
        elif abs(p2.x - p1.x) < 1e-10:
            # Points alignés verticalement -> médiatrice horizontale
            edge = self._create_horizontal_bisector(midpoint, x_min, x_max)
        else:
            # Médiatrice avec pente
            slope = -(p2.x - p1.x) / (p2.y - p1.y)
            edge = self._create_sloped_bisector(midpoint, slope, x_min, x_max, y_min, y_max)
        
        if edge:
            edge.site1 = p1
            edge.site2 = p2
            
        return edge
    
    def _create_vertical_bisector(self, midpoint: Point, 
                                  y_min: float, y_max: float) -> Edge:
        """Crée une médiatrice verticale."""
        return Edge(
            start=Point(midpoint.x, y_min),
            end=Point(midpoint.x, y_max),
            site1=Point(0, 0),  # Temporaire
            site2=Point(0, 0)
        )
    
    def _create_horizontal_bisector(self, midpoint: Point,
                                    x_min: float, x_max: float) -> Edge:
        """Crée une médiatrice horizontale."""
        return Edge(
            start=Point(x_min, midpoint.y),
            end=Point(x_max, midpoint.y),
            site1=Point(0, 0),
            site2=Point(0, 0)
        )
    
    def _create_sloped_bisector(self, midpoint: Point, slope: float,
                                 x_min: float, x_max: float,
                                 y_min: float, y_max: float) -> Edge:
        """Crée une médiatrice avec une pente."""
        # Calcul des intersections avec la boîte
        start_x, start_y = self._find_boundary_intersection(
            midpoint, slope, x_min, y_min, y_max, direction=-1
        )
        end_x, end_y = self._find_boundary_intersection(
            midpoint, slope, x_max, y_min, y_max, direction=1
        )
        
        return Edge(
            start=Point(start_x, start_y) if start_x is not None else None,
            end=Point(end_x, end_y) if end_x is not None else None,
            site1=Point(0, 0),
            site2=Point(0, 0)
        )
    
    def _find_boundary_intersection(self, point: Point, slope: float,
                                    target_x: float, y_min: float, y_max: float,
                                    direction: int) -> Tuple[Optional[float], Optional[float]]:
        """
        Trouve l'intersection d'une ligne avec les limites de la boîte.
        
        Args:
            point: Point sur la ligne
            slope: Pente de la ligne
            target_x: Objectif x
            y_min, y_max: Limites y
            direction: Direction de recherche (-1 ou 1)
            
        Returns:
            Tuple[Optional[float], Optional[float]]: (x, y) de l'intersection
        """
        y = point.y + slope * (target_x - point.x)
        
        if y_min <= y <= y_max:
            return (target_x, y)
        
        # Intersection avec les limites horizontales
        if y < y_min:
            y_target = y_min
        else:
            y_target = y_max
            
        if abs(slope) > 1e-10:
            x = point.x + (y_target - point.y) / slope
            if y_min <= x <= y_max:
                return (x, y_target)
        
        return (None, None)
    
    def _add_boundary_edges(self, points: List[Point],
                            x_min: float, x_max: float,
                            y_min: float, y_max: float) -> None:
        """
        Ajoute les arêtes aux limites du diagramme.
        
        Args:
            points: Liste des points
            x_min, x_max, y_min, y_max: Limites
        """
        # Arêtes aux quatre coins
        corners = [
            Point(x_min, y_min),
            Point(x_max, y_min),
            Point(x_max, y_max),
            Point(x_min, y_max)
        ]
        
        for i in range(4):
            edge = Edge(
                start=corners[i],
                end=corners[(i + 1) % 4],
                site1=Point(0, 0),
                site2=Point(0, 0)
            )
            self.edges.append(edge)
    
    def get_bounding_box(self, points: List[Point]) -> Tuple[float, float, float, float]:
        """
        Calcule la boîte englobante des points avec une marge.
        
        Args:
            points: Liste des points
            
        Returns:
            Tuple[float, float, float, float]: (x_min, x_max, y_min, y_max)
        """
        if not points:
            return (0, 0, 0, 0)
        
        x_min = min(p.x for p in points) - self.bounding_box_padding
        x_max = max(p.x for p in points) + self.bounding_box_padding
        y_min = min(p.y for p in points) - self.bounding_box_padding
        y_max = max(p.y for p in points) + self.bounding_box_padding
        
        return (x_min, x_max, y_min, y_max)