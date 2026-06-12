"""
Module de construction de diagrammes de Voronoï.

Ce module fournit un service de haut niveau pour orchestrer
la construction d'un diagramme de Voronoï.
"""

from typing import List
from src.domain.point import Point
from src.domain.voronoi_diagram import VoronoiDiagram
from src.algorithms.fortune_algorithm import FortuneAlgorithm


class DiagramBuilderError(Exception):
    """Exception levée lors d'erreurs de construction du diagramme."""
    pass


class DiagramBuilder:
    """
    Service de construction de diagrammes de Voronoï.
    
    Ce service orchestre l'algorithme de calcul et fournit
    une interface simple pour générer des diagrammes.
    
    Principles SOLID respectés :
    - Single Responsibility : Construction de diagrammes uniquement
    - Dependency Inversion : Dépend de l'abstraction (algorithme)
    """
    
    def __init__(self) -> None:
        """Initialise le constructeur de diagrammes."""
        pass
    
    def build_diagram(self, points: List[Point]) -> VoronoiDiagram:
        """
        Construit un diagramme de Voronoï depuis une liste de points.
        
        Args:
            points: Liste des points générateurs.
            
        Returns:
            Le diagramme de Voronoï calculé.
            
        Raises:
            DiagramBuilderError: Si la construction échoue.
            ValueError: Si la liste de points est invalide.
        """
        # Validation
        if not points:
            raise ValueError("La liste de points ne peut pas être vide")
        
        if len(points) < 2:
            raise ValueError("Au moins 2 points sont nécessaires")
        
        # Supprimer les doublons
        unique_points = self._remove_duplicates(points)
        
        if len(unique_points) < 2:
            raise ValueError(
                "Au moins 2 points distincts sont nécessaires "
                f"(doublons supprimés : {len(points)} -> {len(unique_points)})"
            )
        
        try:
            # Créer et exécuter l'algorithme
            algorithm = FortuneAlgorithm(unique_points)
            diagram = algorithm.compute()
            
            return diagram
            
        except Exception as e:
            raise DiagramBuilderError(
                f"Erreur lors de la construction du diagramme : {str(e)}"
            )
    
    def _remove_duplicates(self, points: List[Point]) -> List[Point]:
        """
        Supprime les points en double de la liste.
        
        Args:
            points: Liste de points potentiellement avec doublons.
            
        Returns:
            Liste de points sans doublons.
        """
        seen = set()
        unique = []
        
        for point in points:
            # Utiliser le hash du point pour détecter les doublons
            point_hash = hash(point)
            if point_hash not in seen:
                seen.add(point_hash)
                unique.append(point)
        
        return unique
    
    def validate_points(self, points: List[Point]) -> bool:
        """
        Valide une liste de points pour la construction d'un diagramme.
        
        Args:
            points: Liste de points à valider.
            
        Returns:
            True si les points sont valides, False sinon.
        """
        if not points or len(points) < 2:
            return False
        
        unique_points = self._remove_duplicates(points)
        return len(unique_points) >= 2
    
    def get_statistics(self, diagram: VoronoiDiagram) -> dict:
        """
        Calcule des statistiques sur un diagramme.
        
        Args:
            diagram: Le diagramme à analyser.
            
        Returns:
            Dictionnaire contenant les statistiques.
        """
        return {
            'num_sites': len(diagram.sites),
            'num_edges': len(diagram.edges),
            'num_vertices': len(diagram.vertices),
            'bounding_box': diagram.bounding_box,
            'avg_edges_per_site': len(diagram.edges) / len(diagram.sites) if diagram.sites else 0
        }