"""
Module définissant l'interface de base pour les exporteurs.

Ce module fournit une classe abstraite que tous les exporteurs
doivent implémenter (principe Open/Closed de SOLID).
"""

from abc import ABC, abstractmethod
from src.domain.voronoi_diagram import VoronoiDiagram


class BaseExporter(ABC):
    """
    Classe abstraite définissant l'interface des exporteurs.
    
    Cette classe respecte les principes SOLID :
    - Open/Closed : Ouverte à l'extension, fermée à la modification
    - Interface Segregation : Interface minimale et spécifique
    - Liskov Substitution : Toutes les implémentations sont substituables
    """
    
    @abstractmethod
    def export(self, diagram: VoronoiDiagram, output_path: str) -> None:
        """
        Exporte un diagramme vers un fichier.
        
        Args:
            diagram: Le diagramme de Voronoï à exporter.
            output_path: Chemin vers le fichier de sortie.
            
        Raises:
            ExporterError: Si l'export échoue.
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Retourne l'extension de fichier pour cet exporteur.
        
        Returns:
            L'extension (ex: '.svg', '.png').
        """
        pass


class ExporterError(Exception):
    """Exception de base pour les erreurs d'export."""
    pass