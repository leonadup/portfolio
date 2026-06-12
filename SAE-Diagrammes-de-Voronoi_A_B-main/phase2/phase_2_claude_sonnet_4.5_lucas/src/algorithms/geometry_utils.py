"""
Module contenant les utilitaires géométriques.

Ce module fournit des fonctions de calcul géométrique nécessaires
pour l'algorithme de Voronoï, en utilisant uniquement la librairie math.
"""

import math
from typing import Optional, Tuple
from src.domain.point import Point


def calculate_circumcenter(p1: Point, p2: Point, p3: Point) -> Optional[Point]:
    """
    Calcule le centre du cercle circonscrit à trois points.
    
    Le centre du cercle circonscrit est équidistant des trois points
    et correspond à un sommet du diagramme de Voronoï.
    
    Args:
        p1: Premier point.
        p2: Deuxième point.
        p3: Troisième point.
        
    Returns:
        Le centre du cercle circonscrit, ou None si les points sont colinéaires.
    """
    # Coordonnées des points
    ax, ay = p1.x, p1.y
    bx, by = p2.x, p2.y
    cx, cy = p3.x, p3.y
    
    # Calcul des différences
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    
    # Si d est proche de 0, les points sont colinéaires
    if abs(d) < 1e-10:
        return None
    
    # Calcul des coordonnées du centre
    ux = ((ax * ax + ay * ay) * (by - cy) + 
          (bx * bx + by * by) * (cy - ay) + 
          (cx * cx + cy * cy) * (ay - by)) / d
    
    uy = ((ax * ax + ay * ay) * (cx - bx) + 
          (bx * bx + by * by) * (ax - cx) + 
          (cx * cx + cy * cy) * (bx - ax)) / d
    
    return Point(ux, uy)


def calculate_circle_center_from_two_points(p1: Point, p2: Point) -> Point:
    """
    Calcule le centre de la médiatrice entre deux points.
    
    La médiatrice est la droite perpendiculaire au segment [p1, p2]
    passant par son milieu.
    
    Args:
        p1: Premier point.
        p2: Deuxième point.
        
    Returns:
        Le point milieu entre p1 et p2.
    """
    center_x = (p1.x + p2.x) / 2.0
    center_y = (p1.y + p2.y) / 2.0
    return Point(center_x, center_y)


def calculate_perpendicular_bisector(p1: Point, p2: Point) -> Tuple[float, float, float]:
    """
    Calcule l'équation de la médiatrice entre deux points.
    
    La médiatrice est représentée par l'équation : ax + by + c = 0
    
    Args:
        p1: Premier point.
        p2: Deuxième point.
        
    Returns:
        Un tuple (a, b, c) représentant l'équation de la médiatrice.
        
    Raises:
        ValueError: Si les deux points sont identiques.
    """
    if p1 == p2:
        raise ValueError("Les deux points ne peuvent pas être identiques")
    
    # Point milieu
    mid_x = (p1.x + p2.x) / 2.0
    mid_y = (p1.y + p2.y) / 2.0
    
    # Vecteur directeur du segment
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    
    # Vecteur normal (perpendiculaire) : (-dy, dx)
    # Équation : -dy * (x - mid_x) + dx * (y - mid_y) = 0
    # Soit : -dy * x + dx * y + (dy * mid_x - dx * mid_y) = 0
    a = -dy
    b = dx
    c = dy * mid_x - dx * mid_y
    
    return (a, b, c)


def line_intersection(a1: float, b1: float, c1: float,
                      a2: float, b2: float, c2: float) -> Optional[Point]:
    """
    Calcule l'intersection de deux droites.
    
    Les droites sont représentées par leurs équations :
    - Droite 1 : a1*x + b1*y + c1 = 0
    - Droite 2 : a2*x + b2*y + c2 = 0
    
    Args:
        a1, b1, c1: Coefficients de la première droite.
        a2, b2, c2: Coefficients de la deuxième droite.
        
    Returns:
        Le point d'intersection, ou None si les droites sont parallèles.
    """
    det = a1 * b2 - a2 * b1
    
    # Si le déterminant est proche de 0, les droites sont parallèles
    if abs(det) < 1e-10:
        return None
    
    # Calcul du point d'intersection
    x = (b1 * c2 - b2 * c1) / det
    y = (a2 * c1 - a1 * c2) / det
    
    return Point(x, y)


def point_on_segment(point: Point, seg_start: Point, seg_end: Point) -> bool:
    """
    Vérifie si un point est sur un segment.
    
    Args:
        point: Le point à tester.
        seg_start: Point de début du segment.
        seg_end: Point de fin du segment.
        
    Returns:
        True si le point est sur le segment, False sinon.
    """
    epsilon = 1e-9
    
    # Vérifie si le point est dans la boîte englobante du segment
    min_x = min(seg_start.x, seg_end.x) - epsilon
    max_x = max(seg_start.x, seg_end.x) + epsilon
    min_y = min(seg_start.y, seg_end.y) - epsilon
    max_y = max(seg_start.y, seg_end.y) + epsilon
    
    if not (min_x <= point.x <= max_x and min_y <= point.y <= max_y):
        return False
    
    # Vérifie la colinéarité avec le produit vectoriel
    dx1 = point.x - seg_start.x
    dy1 = point.y - seg_start.y
    dx2 = seg_end.x - seg_start.x
    dy2 = seg_end.y - seg_start.y
    
    cross_product = abs(dx1 * dy2 - dy1 * dx2)
    
    return cross_product < epsilon


def clip_line_to_bbox(p1: Point, p2: Point, 
                      min_x: float, min_y: float,
                      max_x: float, max_y: float) -> Optional[Tuple[Point, Point]]:
    """
    Coupe une ligne pour qu'elle reste dans une boîte englobante.
    
    Utilise l'algorithme de Cohen-Sutherland pour le clipping.
    
    Args:
        p1: Premier point de la ligne.
        p2: Deuxième point de la ligne.
        min_x: Coordonnée x minimale de la boîte.
        min_y: Coordonnée y minimale de la boîte.
        max_x: Coordonnée x maximale de la boîte.
        max_y: Coordonnée y maximale de la boîte.
        
    Returns:
        Un tuple de deux points (clippés), ou None si la ligne est entièrement
        en dehors de la boîte.
    """
    # Codes de région pour Cohen-Sutherland
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000
    
    def compute_code(x: float, y: float) -> int:
        """Calcule le code de région d'un point."""
        code = INSIDE
        if x < min_x:
            code |= LEFT
        elif x > max_x:
            code |= RIGHT
        if y < min_y:
            code |= BOTTOM
        elif y > max_y:
            code |= TOP
        return code
    
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    
    accept = False
    
    while True:
        # Les deux points sont à l'intérieur
        if code1 == 0 and code2 == 0:
            accept = True
            break
        
        # Les deux points sont du même côté à l'extérieur
        elif (code1 & code2) != 0:
            break
        
        # Au moins un point est à l'extérieur
        else:
            # Choisir un point à l'extérieur
            code_out = code1 if code1 != 0 else code2
            
            # Trouver le point d'intersection avec le bord de la boîte
            if code_out & TOP:
                x = x1 + (x2 - x1) * (max_y - y1) / (y2 - y1)
                y = max_y
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (min_y - y1) / (y2 - y1)
                y = min_y
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (max_x - x1) / (x2 - x1)
                x = max_x
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (min_x - x1) / (x2 - x1)
                x = min_x
            
            # Remplacer le point extérieur par le point d'intersection
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)
    
    if accept:
        return (Point(x1, y1), Point(x2, y2))
    else:
        return None


def calculate_angle(p1: Point, center: Point, p2: Point) -> float:
    """
    Calcule l'angle entre trois points.
    
    Args:
        p1: Premier point.
        center: Point central.
        p2: Troisième point.
        
    Returns:
        L'angle en radians entre les vecteurs (center->p1) et (center->p2).
    """
    dx1 = p1.x - center.x
    dy1 = p1.y - center.y
    dx2 = p2.x - center.x
    dy2 = p2.y - center.y
    
    angle1 = math.atan2(dy1, dx1)
    angle2 = math.atan2(dy2, dx2)
    
    angle = angle2 - angle1
    
    # Normaliser l'angle entre -π et π
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    
    return angle


def are_collinear(p1: Point, p2: Point, p3: Point, epsilon: float = 1e-9) -> bool:
    """
    Vérifie si trois points sont colinéaires.
    
    Args:
        p1: Premier point.
        p2: Deuxième point.
        p3: Troisième point.
        epsilon: Tolérance pour la comparaison (défaut: 1e-9).
        
    Returns:
        True si les points sont colinéaires, False sinon.
    """
    # Calcul du produit vectoriel
    dx1 = p2.x - p1.x
    dy1 = p2.y - p1.y
    dx2 = p3.x - p1.x
    dy2 = p3.y - p1.y
    
    cross_product = abs(dx1 * dy2 - dy1 * dx2)
    
    return cross_product < epsilon