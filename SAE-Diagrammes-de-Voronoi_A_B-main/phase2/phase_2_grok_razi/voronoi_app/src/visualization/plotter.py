import matplotlib.pyplot as plt
from src.models.voronoi_diagram import VoronoiDiagram
from src.models.point import Point

class VoronoiPlotter:
    """Responsabilité unique : visualisation et export."""

    @staticmethod
    def plot(diagram: VoronoiDiagram, title: str = "Diagramme de Voronoï") -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 8))
    
        if not diagram.sites:
            ax.text(0.5, 0.5, "Aucun site chargé", ha='center', va='center')
            return fig
    
        # ───────────────────────────────────────────────
        # Calcul des limites basé UNIQUEMENT sur les sites + marge
        # ───────────────────────────────────────────────
        xs = [p.x for p in diagram.sites]
        ys = [p.y for p in diagram.sites]
    
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
    
        # Marge relative (10–15 % selon la taille de la bounding box)
        x_range = xmax - xmin
        y_range = ymax - ymin
    
        if x_range < 1e-6:  # cas dégénéré (tous les points alignés verticalement)
            x_range = max(1.0, abs(ymax - ymin) * 0.5)
        if y_range < 1e-6:
            y_range = max(1.0, abs(xmax - xmin) * 0.5)
    
        margin = 0.12
        xmin -= x_range * margin
        xmax += x_range * margin
        ymin -= y_range * margin
        ymax += y_range * margin
    
        # Appliquer les limites
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
    
        # Sites
        ax.scatter(xs, ys, c='red', s=60, label='Sites', zorder=10, edgecolor='black')
    
        # Arêtes Voronoï (finies ou semi-infinies)
        for start, end in diagram.edges:
            ax.plot([start.x, end.x], [start.y, end.y],
                    color='blue', linewidth=1.4, alpha=0.85, zorder=5)
    
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(title)
        ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.35)
    
        # Option : aspect égal pour ne pas déformer les formes
        ax.set_aspect('equal', adjustable='box')
    
        return fig

    @staticmethod
    def save(fig: plt.Figure, filename: str) -> None:
        """Export SVG ou PNG selon extension."""
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)