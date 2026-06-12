# Diagramme de Voronoï - Application Python

## Description

Application professionnelle de génération et visualisation de diagrammes de Voronoï, développée selon les principes du Clean Code et SOLID.

Cette application permet de :
- Charger des points depuis un fichier texte
- Calculer le diagramme de Voronoï avec un algorithme custom (Fortune's algorithm)
- Visualiser le résultat de manière interactive
- Exporter en SVG ou PNG
- Mesurer les performances de l'algorithme

## Architecture

Le projet suit les principes SOLID :
- **Single Responsibility** : Chaque classe a une responsabilité unique
- **Open/Closed** : Extensions via interfaces (exporters)
- **Liskov Substitution** : Polymorphisme des exporters
- **Interface Segregation** : Interfaces spécifiques
- **Dependency Inversion** : Dépendances via abstractions

## Prérequis

- Python 3.8 ou supérieur
- Windows (testé sur Windows 10/11)

## Installation

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd voronoi-diagram
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Sur Windows :**
```bash
venv\Scripts\activate
```

**Sur PowerShell (si erreur de politique d'exécution) :**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Format des fichiers d'entrée

Les fichiers de points doivent contenir une paire de coordonnées par ligne :

```
2,4
5.3,4.5
18,29
12.5,23.7
```

Format accepté : `x,y` où x et y sont des nombres (entiers ou décimaux).

## Utilisation

### Exécution de l'application

```bash
python main.py
```

L'application propose un menu interactif :
1. Charger un fichier de points
2. Calculer et visualiser le diagramme
3. Exporter en SVG
4. Exporter en PNG
5. Analyser les performances
6. Quitter

### Exemples de commandes

```bash
# Lancer l'application
python main.py

# Exécuter les tests
pytest tests/ -v

# Exécuter les tests avec couverture
pytest tests/ --cov=src --cov-report=html

# Analyser les performances
python -m src.services.performance_analyzer
```

## Structure du projet

```
voronoi-diagram/
├── src/                    # Code source
│   ├── domain/            # Entités métier (Point, Diagram)
│   ├── algorithms/        # Algorithme de Voronoï
│   ├── services/          # Services métier
│   ├── exporters/         # Exportation (SVG, PNG)
│   └── ui/                # Interface utilisateur
├── tests/                 # Tests unitaires
├── data/                  # Fichiers de données d'exemple
└── output/                # Fichiers générés
```

## Tests

Le projet utilise pytest avec une couverture complète :

```bash
# Lancer tous les tests
pytest

# Tests avec verbosité
pytest -v

# Tests avec couverture
pytest --cov=src --cov-report=term-missing

# Tests d'un module spécifique
pytest tests/test_file_reader.py -v
```

## Analyse de performance

L'application inclut un analyseur de performance qui mesure :
- Temps d'exécution en fonction du nombre de points
- Complexité algorithmique
- Utilisation mémoire

```bash
python -m src.services.performance_analyzer
```

## Principes de Clean Code appliqués

- **Noms explicites** : Variables et fonctions auto-documentées
- **Fonctions courtes** : Une responsabilité par fonction
- **DRY** : Pas de duplication de code
- **Tests unitaires** : Couverture complète avec pytest
- **Documentation** : Docstrings pour toutes les classes/méthodes
- **Gestion d'erreurs** : Exceptions spécifiques et informatives
- **Types hints** : Annotations de types partout

## Dépendances principales

- `pytest` : Framework de tests
- `pytest-cov` : Couverture de code
- `matplotlib` : Visualisation
- `Pillow` : Export d'images
- `numpy` : Calculs numériques (utilisé minimalement)

## Limitations et notes

- L'algorithme implémenté est l'algorithme de Fortune (sweep line)
- Complexité théorique : O(n log n)
- Les librairies scipy.spatial.Voronoi ne sont PAS utilisées
- Seule la librairie `math` standard Python est utilisée pour les calculs géométriques

## Auteur

Développé selon les principes du Clean Code et SOLID.

## Licence

MIT License