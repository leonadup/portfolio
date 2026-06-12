from typing import List
from models.fortune_voronoi import FortuneVoronoi
from models.edge import Edge

class SVGVisualizer:
    """Génère une représentation SVG d'un diagramme de Voronoï."""

    @staticmethod
    def visualize(diagram: FortuneVoronoi, output_path: str, width: int = 800, height: int = 600, padding: int = 20):
        """Génère un fichier SVG du diagramme de Voronoï."""
        edges = diagram.get_edges()
        points = diagram.points
        if not edges or not points:
            print("Aucune arête ou point à afficher.")
            return

        # Calcul des bornes
        min_x = min(p.x for p in points) - padding
        min_y = min(p.y for p in points) - padding
        max_x = max(p.x for p in points) + padding
        max_y = max(p.y for p in points) + padding

        # Échelle pour le SVG
        def scale_x(x: float) -> float:
            return ((x - min_x) / (max_x - min_x)) * (width - 2*padding) + padding

        def scale_y(y: float) -> float:
            return height - ((y - min_y) / (max_y - min_y)) * (height - 2*padding) - padding

        # Écriture du SVG
        with open(output_path, 'w') as f:
            f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background: white;">\n')

            # Dessiner les arêtes de Voronoï
            for edge in edges:
                # Gestion des arêtes infinies (tronquer aux limites du SVG)
                x1, y1 = edge.start.x, edge.start.y
                x2, y2 = edge.end.x, edge.end.y

                # Tronquer les coordonnées aux limites du SVG
                x1 = max(min_x, min(x1, max_x))
                y1 = max(min_y, min(y1, max_y))
                x2 = max(min_x, min(x2, max_x))
                y2 = max(min_y, min(y2, max_y))

                # Échelle
                sx1, sy1 = scale_x(x1), scale_y(y1)
                sx2, sy2 = scale_x(x2), scale_y(y2)

                f.write(f'  <line x1="{sx1}" y1="{sy1}" x2="{sx2}" y2="{sy2}" stroke="black" stroke-width="1" />\n')

            # Dessiner les points
            for point in points:
                x, y = scale_x(point.x), scale_y(point.y)
                f.write(f'  <circle cx="{x}" cy="{y}" r="3" fill="red" />\n')

            f.write('</svg>\n')
