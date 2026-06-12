# Voronoi Clean Code Project

Projet de génération de diagrammes de Voronoï respectant SOLID et Clean Code.

## Installation
1. Créer l'environnement virtuel :
   `python -m venv venv`
2. Activer l'environnement :
   - Windows : `venv\Scripts\activate`
   - Unix : `source venv/bin/activate`
3. Installer les dépendances :
   `pip install -r requirements.txt`

## Utilisation
Placer vos points dans un fichier `.txt` (format `x,y` ou `x y`).
Lancer l'application : `python main.py`

## Tests
Lancer la suite de tests avec : `pytest`

# Prompt pour Gemini
Rôle: 
Tu es un ingénieur en informatique et tu es très attaché aux principes du Clean Code. 

Consigne : 
Diagrammes de Voronoï → Votre équipe a été sollicitée pour proposer une application qui permet de déterminer un diagramme de Voronoï à partir d'une liste de points du plan, et permettre sa visualisation. Phase 1 Vous devrez vous acquitter de cette tâche en proposant une interface conviviale à partir de fichiers qui contiennent une liste de points sous forme de paire de nombres (les coordonnées) au rythme de une par ligne : 2,4 5.3,4.5 18,29 12.5,23.7 L'application permettra de visualiser le diagramme obtenu et éventuellement exporter le résultat sous forme de fichiers SVG ou image.
L'application fournie devra respecter le plus haut niveau de bonnes pratiques de programmation. Elle incluera donc aussi notamment une série de tests.

Spécifications : 
Tu ne dois pas utiliser la librairie intégrée à python qui trace directement le diagramme de voronoï mais bien recoder un algorithme complet avec seulement la librairie math de python.
Fais une arborescence cohérente en respectant les principes SOLID.
Inclus également un moyen de mesurer les performances de l’algorithme en fonction du nombre de points dans le fichier txt.
Le code doit inclure des docstrings clairs pour chaque classe et fonction, qui doivent par ailleurs avoir un nom explicite, ainsi que des commentaires pertinents.
Le projet doit contenir un README avec les instructions pour créer le venv python et installer les requirements etc…

Tests : 
Tu dois impérativement fournir une suite de tests unitaires pytest pour valider la lecture du fichier, la gestion des erreurs et la logique de calcul, en respectant les principes du TDD qui font partie du Clean Code.

Livrable attendu de ta part : 
Génère l'intégralité du code source structuré (tu dois diviser en plusieurs fichiers en indiquant les noms de fichiers et les imports).

# Correction des bugs
Problème version python 3.12 au lieu de 3.14, versions récentes matplotlib et pytest
Correction de la taille du graphique (hauteur max et largeur max) en fonction des germes, supression des constantes magiques (hardcoding)
Le moteur ne dépend plus d'une formule mathématique fixe. On peut lui passer n'importe quelle DistanceMetric.
Gère les fichiers vides, les points en double et les bugs de récursion.
L'utilisation de la distance au carré et le cache des tuples rend le calcul instantané pour de multiple points
Chaque fichier a une seule responsabilité (SRP)

# Temps pour le fonctionnement du projet
Environ 1h


# Comparaison avec la phase 1
Algortithme de balayage point par point, qui calcule le voisin le plus proche pour chaque zone
Complexité linéiare O(W * H * N) où W et H sont la largeur et la hauteur de l'image et N le nombre de germes. Il dépend de la résolution de l'image plus que du nombre de points
Rendu statique avec matplotlib