import math
from typing import List, Tuple, Dict, Set
from models.point import Point
from models.edge import Edge

class Event:
    """Représente un événement (site ou cercle) pour l'algorithme de Fortune."""
    def __init__(self, x: float, y: float, is_site: bool, point: Point = None):
        self.x = x
        self.y = y
        self.is_site = is_site
        self.point = point

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

class Arc:
    """Représente un arc de parabole dans le front de balayage."""
    def __init__(self, point: Point, prev: 'Arc' = None, next: 'Arc' = None):
        self.point = point
        self.prev = prev
        self.next = next
        self.edge = None
        self.event = None

class FortuneVoronoi:
    """Implémente l'algorithme de Fortune pour générer un diagramme de Voronoï."""

    def __init__(self, points: List[Point]):
        self.points = points
        self.edges: List[Edge] = []
        self.beachline = None
        self.events = []
        self.sweep_line_y = 0

    def build(self):
        """Construit le diagramme de Voronoï."""
        if len(self.points) < 2:
            return

        # 1. Initialiser les événements
        for point in self.points:
            self.events.append(Event(point.x, point.y, True, point))

        # 2. Trier les événements par ordre de balayage
        self.events.sort()

        # 3. Traiter les événements
        while self.events:
            event = self.events.pop(0)
            self.sweep_line_y = event.y

            if event.is_site:
                self._handle_site_event(event)
            else:
                self._handle_circle_event(event)

        # 4. Finaliser les arêtes
        self._finalize_edges()

    def _handle_site_event(self, event: Event):
        """Gère l'ajout d'un nouveau site (point)."""
        if not self.beachline:
            self.beachline = Arc(event.point)
            return

        # Trouver l'arc au-dessus du nouveau point
        arc = self.beachline
        while arc.next and self._intersect(arc.next.point, event.point) < event.x:
            arc = arc.next

        # Créer un nouvel arc
        new_arc = Arc(event.point, arc, arc.next)
        if arc.next:
            arc.next.prev = new_arc
        arc.next = new_arc

        # Vérifier les événements de cercle
        self._check_circle_event(arc)
        self._check_circle_event(new_arc)

    def _handle_circle_event(self, event: Event):
        """Gère la disparition d'un arc (événement de cercle)."""
        arc = event.arc
        if not arc:
            return

        # Supprimer l'arc
        if arc.prev:
            arc.prev.next = arc.next
            arc.prev.edge = arc.edge
        if arc.next:
            arc.next.prev = arc.prev
            arc.next.edge = arc.edge

        # Finaliser l'arête
        if arc.edge:
            arc.edge.end = Point(event.x, event.y)
            self.edges.append(arc.edge)

        # Vérifier les nouveaux événements de cercle
        if arc.prev:
            self._check_circle_event(arc.prev)
        if arc.next:
            self._check_circle_event(arc.next)

    def _check_circle_event(self, arc: Arc):
        """Vérifie si un nouvel événement de cercle doit être créé."""
        if not arc.prev or not arc.next:
            return

        # Calculer le centre du cercle circonscrit
        a = arc.prev.point
        b = arc.point
        c = arc.next.point
        center = self._circumcenter(a, b, c)
        if not center:
            return

        # Calculer le rayon
        radius = math.sqrt((a.x - center.x)**2 + (a.y - center.y)**2)
        if radius == 0:
            return

        # Calculer l'événement de cercle
        y = center.y + radius
        if y <= self.sweep_line_y:
            return

        # Créer l'événement
        event = Event(center.x, y, False)
        event.arc = arc
        arc.event = event
        self.events.append(event)
        self.events.sort()

    def _circumcenter(self, a: Point, b: Point, c: Point) -> Point:
        """Calcule le centre du cercle circonscrit."""
        d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
        if d == 0:
            return None

        ux = ((a.x**2 + a.y**2) * (b.y - c.y) + (b.x**2 + b.y**2) * (c.y - a.y) + (c.x**2 + c.y**2) * (a.y - b.y)) / d
        uy = ((a.x**2 + a.y**2) * (c.x - b.x) + (b.x**2 + b.y**2) * (a.x - c.x) + (c.x**2 + c.y**2) * (b.x - a.x)) / d
        return Point(ux, uy)

    def _intersect(self, a: Point, b: Point) -> float:
        """Calcule l'intersection des deux paraboles."""
        if a.y == b.y:
            return (a.x + b.x) / 2

        # Résolution de l'équation des deux paraboles
        # (simplifiée pour la ligne de balayage)
        return (b.x - a.x) / (a.y - b.y) * (self.sweep_line_y - (a.y + b.y) / 2) + (a.x + b.x) / 2

    def _finalize_edges(self):
        """Finalise les arêtes restantes."""
        arc = self.beachline
        while arc:
            if arc.edge:
                # Étendre l'arête à l'infini
                if arc.prev:
                    start = Point(-1000, arc.prev.point.y + 1000)
                else:
                    start = Point(1000, arc.point.y + 1000)
                if arc.next:
                    end = Point(1000, arc.next.point.y + 1000)
                else:
                    end = Point(-1000, arc.point.y + 1000)
                arc.edge.end = end
                self.edges.append(arc.edge)
            arc = arc.next

    def get_edges(self) -> List[Edge]:
        return self.edges
