from pathlib import Path
from typing import List

from src.models.point import Point


class FileHandler:
    """
    Responsabilité : lecture/écriture des fichiers contenant les points (sites).
    """

    @staticmethod
    def read_points(file_path: str | Path) -> List[Point]:
        """
        Lit un fichier .txt contenant une liste de points au format :
            x,y
        une paire par ligne.

        Règles de parsing :
        - Ignore les lignes vides
        - Ignore les lignes commençant par #
        - Ignore tout ce qui suit # sur une ligne (commentaire en fin de ligne)
        - Tolère les espaces autour des nombres et de la virgule
        - Lève une ValueError explicite en cas de problème de format

        Args:
            file_path: chemin du fichier (str ou Path)

        Returns:
            Liste de Point

        Raises:
            FileNotFoundError: si le fichier n'existe pas
            ValueError: en cas de format invalide ou trop peu de points valides
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier non trouvé : {path}")

        points = []

        with path.open(encoding="utf-8") as f:
            for line_num, raw_line in enumerate(f, start=1):
                # Supprime le commentaire en fin de ligne
                line = raw_line.split('#', 1)[0]

                # Nettoyage : enlève espaces inutiles, tabs, etc.
                line = line.strip()

                if not line:
                    continue

                try:
                    # On split sur la virgule, puis on nettoie chaque partie
                    parts = [part.strip() for part in line.split(',')]

                    if len(parts) != 2:
                        raise ValueError(
                            "Format incorrect : exactement deux valeurs séparées par une virgule attendues"
                        )

                    if not parts[0] or not parts[1]:
                        raise ValueError("Une des coordonnées est vide après nettoyage")

                    x = float(parts[0])
                    y = float(parts[1])

                    points.append(Point(x, y))

                except ValueError as ve:
                    # On précise la ligne et le contenu pour aider au debug
                    raise ValueError(
                        f"Erreur de parsing ligne {line_num} : '{raw_line.strip()}' → {str(ve)}"
                    ) from ve
                except Exception as e:
                    raise ValueError(
                        f"Erreur inattendue ligne {line_num} : '{raw_line.strip()}' → {str(e)}"
                    ) from e

        if len(points) < 2:
            raise ValueError("Le fichier doit contenir au moins 2 points valides.")

        return points

    @staticmethod
    def save_points(points: List[Point], file_path: str | Path) -> None:
        """
        Sauvegarde une liste de points dans un fichier texte (format x,y par ligne).
        Utilisé éventuellement pour exporter ou sauvegarder une configuration.

        Args:
            points: liste de Point à sauvegarder
            file_path: chemin de destination
        """
        path = Path(file_path)
        with path.open("w", encoding="utf-8") as f:
            for p in points:
                f.write(f"{p.x},{p.y}\n")