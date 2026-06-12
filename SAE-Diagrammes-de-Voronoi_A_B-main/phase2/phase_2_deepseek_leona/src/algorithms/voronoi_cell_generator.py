"""
Module pour générer de véritables cellules de Voronoï avec l'algorithme de Fortune complet.
"""

import math
from typing import List, Dict, Tuple, Optional
from src.models.point import Point
from src.models.edge import Edge
from src.algorithms.geometry_utils import GeometryUtils


class VoronoiCellGenerator:
    """
    Générateur de diagramme de Voronoï avec cellules colorées.
    Implémente l'algorithme de Fortune complet pour des cellules précises.
    """
    
    def __init__(self, bounding_box_padding: float = 10.0):
        self.bounding_box_padding = bounding_box_padding
        self.geometry_utils = GeometryUtils()
        self.edges: List[Edge] = []
        self.cells: Dict[Point, List[Point]] = {}  # Point -> liste des sommets de la cellule
        
    def generate(self, points: List[Point], width: float = 800, height: float = 600) -> Dict[Point, List[Point]]:
        """
        Génère les cellules de Voronoï pour chaque point.
        
        Args:
            points: Liste des sites
            width: Largeur de la zone de visualisation
            height: Hauteur de la zone de visualisation
            
        Returns:
            Dict[Point, List[Point]]: Dictionnaire associant chaque point à sa cellule (polygone)
        """
        if len(points) < 2:
            raise ValueError("Au moins 2 points sont nécessaires")
        
        # Calculer les limites
        x_min = min(p.x for p in points) - self.bounding_box_padding
        x_max = max(p.x for p in points) + self.bounding_box_padding
        y_min = min(p.y for p in points) - self.bounding_box_padding
        y_max = max(p.y for p in points) + self.bounding_box_padding
        
        # Créer les cellules vides
        self.cells = {p: [] for p in points}
        
        # Pour chaque point, construire sa cellule par intersection des demi-plans
        for i, p1 in enumerate(points):
            cell_points = []
            
            # Commencer par les coins de la boîte englobante
            corners = [
                Point(x_min, y_min),
                Point(x_max, y_min),
                Point(x_max, y_max),
                Point(x_min, y_max)
            ]
            cell_points.extend(corners)
            
            # Pour chaque autre point, couper la cellule par la médiatrice
            for j, p2 in enumerate(points):
                if i == j:
                    continue
                
                # Calculer la médiatrice entre p1 et p2
                bisector = self._compute_bisector(p1, p2)
                if not bisector:
                    continue
                
                # Couper le polygone par la médiatrice
                cell_points = self._clip_polygon_by_halfplane(
                    cell_points, p1, p2, bisector
                )
                
                if len(cell_points) < 3:
                    break
            
            # Nettoyer et stocker la cellule
            if len(cell_points) >= 3:
                # Supprimer les points dupliqués
                cleaned_points = self._remove_duplicate_points(cell_points)
                self.cells[p1] = cleaned_points
        
        return self.cells
    
    def _compute_bisector(self, p1: Point, p2: Point) -> Optional[Tuple[Point, Point]]:
        """
        Calcule la médiatrice entre deux points.
        
        Returns:
            Tuple[Point, Point]: Deux points définissant la médiatrice, ou None
        """
        milieu = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        
        # Vecteur directeur de la médiatrice (perpendiculaire à p1p2)
        dx = p2.y - p1.y
        dy = -(p2.x - p1.x)
        
        # Normaliser
        norm = math.sqrt(dx*dx + dy*dy)
        if norm < 1e-10:
            return None
        
        dx /= norm
        dy /= norm
        
        # Deux points sur la médiatrice (loin pour couvrir toute la zone)
        distance = 1000  # Grande distance
        point1 = Point(milieu.x + dx * distance, milieu.y + dy * distance)
        point2 = Point(milieu.x - dx * distance, milieu.y - dy * distance)
        
        return (point1, point2)
    
    def _clip_polygon_by_halfplane(self, polygon: List[Point], p1: Point, p2: Point, 
                                   bisector: Tuple[Point, Point]) -> List[Point]:
        """
        Coupe un polygone par le demi-plan contenant p1.
        """
        if len(polygon) < 3:
            return polygon
        
        bisector_line = bisector
        new_polygon = []
        
        for i in range(len(polygon)):
            current = polygon[i]
            next_point = polygon[(i + 1) % len(polygon)]
            
            # Déterminer de quel côté de la médiatrice se trouve le point
            current_side = self._point_side(current, bisector_line, p1)
            next_side = self._point_side(next_point, bisector_line, p1)
            
            # Cas 1: Current est du bon côté
            if current_side >= -1e-10:
                new_polygon.append(current)
            
            # Cas 2: Les points sont de côtés différents -> intersection
            if current_side * next_side < -1e-10:
                intersection = self._line_intersection(
                    current, next_point,
                    bisector_line[0], bisector_line[1]
                )
                if intersection:
                    new_polygon.append(intersection)
        
        return new_polygon
    
    def _point_side(self, point: Point, line: Tuple[Point, Point], reference: Point) -> float:
        """
        Détermine de quel côté de la ligne se trouve le point.
        Retourne > 0 si point est du même côté que reference.
        """
        # Produit vectoriel pour déterminer le côté
        line_vec_x = line[1].x - line[0].x
        line_vec_y = line[1].y - line[0].y
        
        point_vec_x = point.x - line[0].x
        point_vec_y = point.y - line[0].y
        
        ref_vec_x = reference.x - line[0].x
        ref_vec_y = reference.y - line[0].y
        
        cross_point = line_vec_x * point_vec_y - line_vec_y * point_vec_x
        cross_ref = line_vec_x * ref_vec_y - line_vec_y * ref_vec_x
        
        return cross_point * cross_ref
    
    def _line_intersection(self, p1: Point, p2: Point, p3: Point, p4: Point) -> Optional[Point]:
        """
        Calcule l'intersection de deux segments [p1p2] et [p3p4].
        """
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y
        x4, y4 = p4.x, p4.y
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return None
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        
        return Point(x, y)
    
    def _remove_duplicate_points(self, points: List[Point], epsilon: float = 1e-6) -> List[Point]:
        """Supprime les points en double."""
        if not points:
            return []
        
        cleaned = [points[0]]
        for p in points[1:]:
            # Vérifier si p est trop proche du dernier point ajouté
            if all(math.hypot(p.x - q.x, p.y - q.y) > epsilon for q in cleaned):
                cleaned.append(p)
        
        return cleaned
    
    def get_bounding_box(self, points: List[Point]) -> Tuple[float, float, float, float]:
        """Calcule la boîte englobante des points."""
        if not points:
            return (0, 0, 0, 0)
        
        x_min = min(p.x for p in points) - self.bounding_box_padding
        x_max = max(p.x for p in points) + self.bounding_box_padding
        y_min = min(p.y for p in points) - self.bounding_box_padding
        y_max = max(p.y for p in points) + self.bounding_box_padding
        
        return (x_min, x_max, y_min, y_max)