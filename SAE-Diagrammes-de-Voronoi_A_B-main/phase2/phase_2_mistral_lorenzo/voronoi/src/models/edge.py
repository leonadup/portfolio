from models.point import Point

class Edge:
    """Représente une arête d'un diagramme de Voronoï, définie par deux points."""

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Edge({self.start}, {self.end})"
