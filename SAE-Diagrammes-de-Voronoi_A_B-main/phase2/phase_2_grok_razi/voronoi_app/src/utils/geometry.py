"""Utilitaires géométriques purs (seulement math)."""
import math
from src.models.point import Point, EPS

def circumcenter(p1: Point, p2: Point, p3: Point) -> Point | None:
    """Calcule le centre du cercle circonscrit à un triangle (formule analytique)."""
    ax, ay = p1.x, p1.y
    bx, by = p2.x, p2.y
    cx, cy = p3.x, p3.y

    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < EPS:
        return None  # points colinéaires

    ux = ((ax**2 + ay**2) * (by - cy) +
          (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / d

    uy = ((ax**2 + ay**2) * (cx - bx) +
          (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / d

    return Point(ux, uy)

def get_outward_perp_direction(a: Point, b: Point, third: Point) -> Point:
    """Direction unitaire du rayon Voronoï sortant (perp bissectrice)."""
    vx = b.x - a.x
    vy = b.y - a.y
    # Produit vectoriel pour déterminer le côté du third point
    cross = vx * (third.y - a.y) - vy * (third.x - a.x)

    # Rotation 90° CCW
    px, py = -vy, vx
    if cross > 0:          # third à gauche → inward = CCW → outward = opposé
        px, py = -px, -py

    length = math.hypot(px, py)
    if length < EPS:
        return Point(0, 0)
    return Point(px / length, py / length)