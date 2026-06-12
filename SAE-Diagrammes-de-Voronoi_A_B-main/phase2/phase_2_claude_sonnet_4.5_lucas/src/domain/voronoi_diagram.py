"""
Module définissant la structure du diagramme de Voronoï.

Ce module contient les classes représentant le diagramme de Voronoï
et ses composants (arêtes, cellules).
"""

from typing import List, Tuple, Dict, Set
from src.domain.point import Point


class VoronoiEdge:
    """
    Représente une arête du diagramme de Voronoï.
    
    Une arête relie deux points et sépare deux sites (points générateurs).
    
    Attributes:
        start (Point): Point de départ de l'arête.
        end (Point): Point d'arrivée de l'arête.
        left_site (Point): Site à gauche de l'arête.
        right_site (Point): Site à droite de l'arête.
    """
    
    def __init__(self, start: Point, end: Point, 
                 left_site: Point, right_site: Point) -> None:
        """
        Initialise une arête du diagramme de Voronoï.
        
        Args:
            start: Point de départ de l'arête.
            end: Point d'arrivée de l'arête.
            left_site: Site générateur à gauche.
            right_site: Site générateur à droite.
        """
        self._start = start
        self._end = end
        self._left_site = left_site
        self._right_site = right_site
    
    @property
    def start(self) -> Point:
        """Retourne le point de départ de l'arête."""
        return self._start
    
    @property
    def end(self) -> Point:
        """Retourne le point d'arrivée de l'arête."""
        return self._end
    
    @property
    def left_site(self) -> Point:
        """Retourne le site générateur à gauche."""
        return self._left_site
    
    @property
    def right_site(self) -> Point:
        """Retourne le site générateur à droite."""
        return self._right_site
    
    def length(self) -> float:
        """
        Calcule la longueur de l'arête.
        
        Returns:
            La longueur euclidienne de l'arête.
        """
        return self._start.distance_to(self._end)
    
    def __repr__(self) -> str:
        """Retourne une représentation string de l'arête."""
        return f"VoronoiEdge({self._start} -> {self._end})"


class VoronoiCell:
    """
    Représente une cellule du diagramme de Voronoï.
    
    Une cellule est la région associée à un site (point générateur).
    Elle est délimitée par un ensemble d'arêtes.
    
    Attributes:
        site (Point): Le site générateur de cette cellule.
        vertices (List[Point]): Les sommets de la cellule (dans l'ordre).
    """
    
    def __init__(self, site: Point) -> None:
        """
        Initialise une cellule de Voronoï.
        
        Args:
            site: Le point générateur de cette cellule.
        """
        self._site = site
        self._vertices: List[Point] = []
    
    @property
    def site(self) -> Point:
        """Retourne le site générateur de la cellule."""
        return self._site
    
    @property
    def vertices(self) -> List[Point]:
        """Retourne les sommets de la cellule."""
        return self._vertices.copy()
    
    def add_vertex(self, vertex: Point) -> None:
        """
        Ajoute un sommet à la cellule.
        
        Args:
            vertex: Le sommet à ajouter.
        """
        self._vertices.append(vertex)
    
    def is_bounded(self) -> bool:
        """
        Vérifie si la cellule est bornée.
        
        Returns:
            True si la cellule a au moins 3 sommets, False sinon.
        """
        return len(self._vertices) >= 3
    
    def __repr__(self) -> str:
        """Retourne une représentation string de la cellule."""
        return f"VoronoiCell(site={self._site}, vertices={len(self._vertices)})"


class VoronoiDiagram:
    """
    Représente un diagramme de Voronoï complet.
    
    Le diagramme contient les sites générateurs, les arêtes,
    les sommets et les cellules du diagramme de Voronoï.
    
    Attributes:
        sites (List[Point]): Les points générateurs du diagramme.
        edges (List[VoronoiEdge]): Les arêtes du diagramme.
        vertices (Set[Point]): Les sommets du diagramme.
        cells (Dict[Point, VoronoiCell]): Les cellules indexées par site.
    """
    
    def __init__(self, sites: List[Point]) -> None:
        """
        Initialise un diagramme de Voronoï.
        
        Args:
            sites: La liste des points générateurs.
            
        Raises:
            ValueError: Si la liste de sites est vide.
        """
        if not sites:
            raise ValueError("La liste de sites ne peut pas être vide")
        
        self._sites = sites.copy()
        self._edges: List[VoronoiEdge] = []
        self._vertices: Set[Point] = set()
        self._cells: Dict[Point, VoronoiCell] = {
            site: VoronoiCell(site) for site in sites
        }
        self._bounding_box: Tuple[float, float, float, float] = (0, 0, 0, 0)
    
    @property
    def sites(self) -> List[Point]:
        """Retourne la liste des sites générateurs."""
        return self._sites.copy()
    
    @property
    def edges(self) -> List[VoronoiEdge]:
        """Retourne la liste des arêtes du diagramme."""
        return self._edges.copy()
    
    @property
    def vertices(self) -> Set[Point]:
        """Retourne l'ensemble des sommets du diagramme."""
        return self._vertices.copy()
    
    @property
    def cells(self) -> Dict[Point, VoronoiCell]:
        """Retourne le dictionnaire des cellules."""
        return self._cells.copy()
    
    @property
    def bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Retourne la boîte englobante du diagramme.
        
        Returns:
            Un tuple (min_x, min_y, max_x, max_y).
        """
        return self._bounding_box
    
    def add_edge(self, edge: VoronoiEdge) -> None:
        """
        Ajoute une arête au diagramme.
        
        Args:
            edge: L'arête à ajouter.
        """
        self._edges.append(edge)
        self._vertices.add(edge.start)
        self._vertices.add(edge.end)
    
    def add_vertex(self, vertex: Point) -> None:
        """
        Ajoute un sommet au diagramme.
        
        Args:
            vertex: Le sommet à ajouter.
        """
        self._vertices.add(vertex)
    
    def set_bounding_box(self, min_x: float, min_y: float, 
                         max_x: float, max_y: float) -> None:
        """
        Définit la boîte englobante du diagramme.
        
        Args:
            min_x: Coordonnée x minimale.
            min_y: Coordonnée y minimale.
            max_x: Coordonnée x maximale.
            max_y: Coordonnée y maximale.
        """
        self._bounding_box = (min_x, min_y, max_x, max_y)
    
    def compute_bounding_box_from_sites(self, margin: float = 1.0) -> None:
        """
        Calcule automatiquement la boîte englobante depuis les sites.
        
        Args:
            margin: Marge à ajouter autour des sites (défaut: 1.0).
        """
        if not self._sites:
            return
        
        x_coords = [site.x for site in self._sites]
        y_coords = [site.y for site in self._sites]
        
        # Calculer les limites de base
        min_x = min(x_coords) - margin
        max_x = max(x_coords) + margin
        min_y = min(y_coords) - margin
        max_y = max(y_coords) + margin
        
        # Ajouter une marge supplémentaire pour couvrir toute la zone de tracé
        # (le visualizer ajoute 10% de marge, on doit inclure ça dans la bbox)
        range_x = max_x - min_x
        range_y = max_y - min_y
        extra_margin = 0.15 * max(range_x, range_y)  # 15% pour être sûr de tout couvrir
        
        min_x -= extra_margin
        max_x += extra_margin
        min_y -= extra_margin
        max_y += extra_margin
        
        self._bounding_box = (min_x, min_y, max_x, max_y)
    
    def get_cell(self, site: Point) -> VoronoiCell:
        """
        Retourne la cellule associée à un site.
        
        Args:
            site: Le site dont on veut la cellule.
            
        Returns:
            La cellule correspondante.
            
        Raises:
            KeyError: Si le site n'existe pas dans le diagramme.
        """
        if site not in self._cells:
            raise KeyError(f"Le site {site} n'existe pas dans le diagramme")
        return self._cells[site]
    
    def __repr__(self) -> str:
        """Retourne une représentation string du diagramme."""
        return (f"VoronoiDiagram(sites={len(self._sites)}, "
                f"edges={len(self._edges)}, "
                f"vertices={len(self._vertices)})")