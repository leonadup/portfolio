"""
Module implémentant l'algorithme de Fortune pour le calcul de Voronoï.

Ce module contient une implémentation simplifiée de l'algorithme de Fortune
(sweep line algorithm) pour générer un diagramme de Voronoï.
Complexité théorique : O(n log n).
"""

import math
from typing import List, Set, Dict, Optional, Tuple
from src.domain.point import Point
from src.domain.voronoi_diagram import VoronoiDiagram, VoronoiEdge
from src.algorithms.geometry_utils import (
    calculate_circumcenter,
    calculate_perpendicular_bisector,
    line_intersection,
    clip_line_to_bbox
)


class FortuneAlgorithm:
    """
    Implémente l'algorithme de Fortune pour calculer un diagramme de Voronoï.
    
    Cette implémentation est une version simplifiée qui utilise
    une approche par triangulation de Delaunay et conversion en Voronoï.
    
    Attributes:
        sites (List[Point]): Les points générateurs.
    """
    
    def __init__(self, sites: List[Point]) -> None:
        """
        Initialise l'algorithme avec une liste de sites.
        
        Args:
            sites: Liste des points générateurs.
            
        Raises:
            ValueError: Si moins de 2 sites sont fournis.
        """
        if len(sites) < 2:
            raise ValueError("Au moins 2 sites sont nécessaires")
        
        self._sites = sorted(sites)  # Tri pour l'algorithme
        self._diagram: Optional[VoronoiDiagram] = None
    
    def compute(self) -> VoronoiDiagram:
        """
        Calcule le diagramme de Voronoï.
        
        Cette méthode est le point d'entrée principal de l'algorithme.
        
        Returns:
            Le diagramme de Voronoï calculé.
        """
        # Initialiser le diagramme
        self._diagram = VoronoiDiagram(self._sites)
        
        # Calculer la boîte englobante
        self._diagram.compute_bounding_box_from_sites(margin=10.0)
        
        # Cas particuliers
        if len(self._sites) == 2:
            self._handle_two_sites()
        elif len(self._sites) == 3:
            self._handle_three_sites()
        else:
            # Algorithme général via triangulation de Delaunay
            self._compute_via_delaunay()
        
        # Prolonger les segments ouverts jusqu'aux bords de la bbox
        self._close_open_edges()
        
        return self._diagram
    
    def _handle_two_sites(self) -> None:
        """
        Traite le cas particulier de deux sites.
        
        Pour deux sites, le diagramme est simplement la médiatrice.
        """
        p1, p2 = self._sites[0], self._sites[1]
        min_x, min_y, max_x, max_y = self._diagram.bounding_box
        
        # Calculer l'équation de la médiatrice
        a, b, c = calculate_perpendicular_bisector(p1, p2)
        
        # Trouver deux points sur la médiatrice aux bords de la bbox
        if abs(b) > 1e-10:  # La droite n'est pas verticale
            # Points aux extrémités verticales
            y1, y2 = min_y, max_y
            x1 = -(b * y1 + c) / a if abs(a) > 1e-10 else (min_x + max_x) / 2
            x2 = -(b * y2 + c) / a if abs(a) > 1e-10 else (min_x + max_x) / 2
            start = Point(x1, y1)
            end = Point(x2, y2)
        else:  # La droite est verticale
            x = -c / a
            start = Point(x, min_y)
            end = Point(x, max_y)
        
        # Clipper la ligne à la bbox
        clipped = clip_line_to_bbox(start, end, min_x, min_y, max_x, max_y)
        if clipped:
            start, end = clipped
            edge = VoronoiEdge(start, end, p1, p2)
            self._diagram.add_edge(edge)
    
    def _handle_three_sites(self) -> None:
        """
        Traite le cas particulier de trois sites.
        
        Pour trois sites, le sommet central est le centre du cercle circonscrit.
        """
        p1, p2, p3 = self._sites[0], self._sites[1], self._sites[2]
        
        # Calculer le centre du cercle circonscrit
        center = calculate_circumcenter(p1, p2, p3)
        
        if center is None:
            # Points colinéaires : deux médiatrices parallèles
            self._handle_collinear_sites()
            return
        
        self._diagram.add_vertex(center)
        min_x, min_y, max_x, max_y = self._diagram.bounding_box
        
        # Créer les trois arêtes partant du centre
        for i in range(3):
            site1 = self._sites[i]
            site2 = self._sites[(i + 1) % 3]
            
            # Direction perpendiculaire au segment
            dx = site2.x - site1.x
            dy = site2.y - site1.y
            
            # Vecteur perpendiculaire
            perp_x = -dy
            perp_y = dx
            
            # Normaliser
            length = math.sqrt(perp_x * perp_x + perp_y * perp_y)
            if length > 1e-10:
                perp_x /= length
                perp_y /= length
            
            # Point lointain dans la direction perpendiculaire
            far_point = Point(
                center.x + perp_x * 1000,
                center.y + perp_y * 1000
            )
            
            # Clipper à la bbox
            clipped = clip_line_to_bbox(center, far_point, 
                                       min_x, min_y, max_x, max_y)
            if clipped:
                start, end = clipped
                edge = VoronoiEdge(start, end, site1, site2)
                self._diagram.add_edge(edge)
    
    def _handle_collinear_sites(self) -> None:
        """
        Traite le cas où tous les sites sont colinéaires.
        
        Dans ce cas, les médiatrices sont toutes parallèles.
        """
        min_x, min_y, max_x, max_y = self._diagram.bounding_box
        
        for i in range(len(self._sites) - 1):
            p1 = self._sites[i]
            p2 = self._sites[i + 1]
            
            a, b, c = calculate_perpendicular_bisector(p1, p2)
            
            # Créer une ligne perpendiculaire
            if abs(b) > 1e-10:
                y1, y2 = min_y, max_y
                x1 = -(b * y1 + c) / a if abs(a) > 1e-10 else (min_x + max_x) / 2
                x2 = -(b * y2 + c) / a if abs(a) > 1e-10 else (min_x + max_x) / 2
                start = Point(x1, y1)
                end = Point(x2, y2)
            else:
                x = -c / a
                start = Point(x, min_y)
                end = Point(x, max_y)
            
            clipped = clip_line_to_bbox(start, end, min_x, min_y, max_x, max_y)
            if clipped:
                start, end = clipped
                edge = VoronoiEdge(start, end, p1, p2)
                self._diagram.add_edge(edge)
    
    def _compute_via_delaunay(self) -> None:
        """
        Calcule le diagramme via une triangulation de Delaunay simplifiée.
        
        Cette approche utilise le fait que le diagramme de Voronoï est
        le dual de la triangulation de Delaunay.
        """
        # Construction d'une triangulation simple (naïve)
        triangles = self._compute_delaunay_triangulation()
        
        min_x, min_y, max_x, max_y = self._diagram.bounding_box
        
        # Pour chaque paire de triangles adjacents, créer une arête de Voronoï
        processed_edges: Set[Tuple[Point, Point]] = set()
        
        for triangle in triangles:
            p1, p2, p3 = triangle
            
            # Centre du cercle circonscrit (sommet de Voronoï)
            center = calculate_circumcenter(p1, p2, p3)
            
            if center is None:
                continue
            
            self._diagram.add_vertex(center)
            
            # Pour chaque arête du triangle, chercher le triangle adjacent
            edges_of_triangle = [(p1, p2), (p2, p3), (p3, p1)]
            
            for edge in edges_of_triangle:
                edge_key = tuple(sorted([edge[0], edge[1]], key=lambda p: (p.x, p.y)))
                
                if edge_key in processed_edges:
                    continue
                
                # Trouver le triangle adjacent partageant cette arête
                adjacent_center = None
                for other_triangle in triangles:
                    if other_triangle == triangle:
                        continue
                    
                    # Vérifier si les deux triangles partagent l'arête
                    if edge[0] in other_triangle and edge[1] in other_triangle:
                        adjacent_center = calculate_circumcenter(*other_triangle)
                        break
                
                if adjacent_center:
                    # Créer une arête entre les deux centres
                    voronoi_edge = VoronoiEdge(center, adjacent_center, 
                                              edge[0], edge[1])
                    self._diagram.add_edge(voronoi_edge)
                    processed_edges.add(edge_key)
                else:
                    # Arête au bord : extrapoler vers l'infini
                    # Trouver le troisième point du triangle (celui qui n'est pas sur l'arête)
                    third_point = None
                    for pt in triangle:
                        if pt != edge[0] and pt != edge[1]:
                            third_point = pt
                            break
                    
                    if third_point is None:
                        continue
                    
                    dx = edge[1].x - edge[0].x
                    dy = edge[1].y - edge[0].y
                    
                    # Direction perpendiculaire
                    perp_x = -dy
                    perp_y = dx
                    
                    # Vérifier que la perpendiculaire pointe du bon côté
                    # Elle doit pointer à l'opposé du troisième point (vers l'extérieur)
                    mid_x = (edge[0].x + edge[1].x) / 2
                    mid_y = (edge[0].y + edge[1].y) / 2
                    
                    # Vecteur du milieu vers le troisième point
                    to_third_x = third_point.x - mid_x
                    to_third_y = third_point.y - mid_y
                    
                    # Produit scalaire
                    dot = perp_x * to_third_x + perp_y * to_third_y
                    
                    # Si positif, la perpendiculaire pointe vers le troisième point -> inverser
                    if dot > 0:
                        perp_x = -perp_x
                        perp_y = -perp_y
                    
                    # Normaliser
                    length = math.sqrt(perp_x * perp_x + perp_y * perp_y)
                    if length > 1e-10:
                        perp_x /= length
                        perp_y /= length
                    
                    far_point = Point(center.x + perp_x * 1000,
                                     center.y + perp_y * 1000)
                    
                    clipped = clip_line_to_bbox(center, far_point,
                                               min_x, min_y, max_x, max_y)
                    if clipped:
                        start, end = clipped
                        voronoi_edge = VoronoiEdge(start, end, edge[0], edge[1])
                        self._diagram.add_edge(voronoi_edge)
                    
                    processed_edges.add(edge_key)
    
    def _compute_delaunay_triangulation(self) -> List[Tuple[Point, Point, Point]]:
        """
        Calcule une triangulation de Delaunay naïve.
        
        Cette implémentation est simplifiée et a une complexité O(n^4).
        Pour de meilleures performances, une implémentation complète de
        l'algorithme de Fortune devrait être utilisée.
        
        Returns:
            Liste des triangles (chaque triangle est un tuple de 3 points).
        """
        n = len(self._sites)
        triangles: List[Tuple[Point, Point, Point]] = []
        
        # Algorithme naïf : tester toutes les combinaisons de 3 points
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    p1, p2, p3 = self._sites[i], self._sites[j], self._sites[k]
                    
                    # Calculer le centre du cercle circonscrit
                    center = calculate_circumcenter(p1, p2, p3)
                    
                    if center is None:
                        continue
                    
                    # Rayon du cercle circonscrit
                    radius = center.distance_to(p1)
                    
                    # Vérifier qu'aucun autre point n'est dans le cercle
                    is_delaunay = True
                    for m in range(n):
                        if m in (i, j, k):
                            continue
                        
                        dist = center.distance_to(self._sites[m])
                        if dist < radius - 1e-9:
                            is_delaunay = False
                            break
                    
                    if is_delaunay:
                        triangles.append((p1, p2, p3))
        
        return triangles
    
    def _close_open_edges(self) -> None:
        """
        Prolonge les arêtes ouvertes jusqu'aux bords de la bounding box.
        
        Pour chaque sommet avec seulement 1 ou 2 arêtes connectées,
        prolonge dans la direction appropriée jusqu'au bord.
        """
        min_x, min_y, max_x, max_y = self._diagram.bounding_box
        epsilon = 1e-9
        
        # Grouper les arêtes par sommet
        vertex_edges: Dict[Point, List[VoronoiEdge]] = {}
        
        for edge in self._diagram.edges:
            # Chercher si start existe déjà (avec tolérance)
            start_found = False
            for existing_vertex in vertex_edges.keys():
                if edge.start.distance_to(existing_vertex) < epsilon:
                    vertex_edges[existing_vertex].append(edge)
                    start_found = True
                    break
            if not start_found:
                vertex_edges[edge.start] = [edge]
            
            # Chercher si end existe déjà (avec tolérance)
            end_found = False
            for existing_vertex in vertex_edges.keys():
                if edge.end.distance_to(existing_vertex) < epsilon:
                    vertex_edges[existing_vertex].append(edge)
                    end_found = True
                    break
            if not end_found:
                vertex_edges[edge.end] = [edge]
        
        edges_to_add = []
        
        for vertex, edges in vertex_edges.items():
            num_edges = len(edges)
            
            if num_edges == 1:
                # Un seul segment : prolonger dans la même direction
                edge = edges[0]
                
                # Trouver l'autre extrémité
                if edge.start.distance_to(vertex) < epsilon:
                    other = edge.end
                else:
                    other = edge.start
                
                # Direction : du autre vers vertex
                dx = vertex.x - other.x
                dy = vertex.y - other.y
                length = math.sqrt(dx * dx + dy * dy)
                
                if length > epsilon:
                    dx /= length
                    dy /= length
                    
                    # Point lointain dans cette direction
                    far_point = Point(vertex.x + dx * 1000, vertex.y + dy * 1000)
                    
                    # Clipper à la bbox
                    clipped = clip_line_to_bbox(vertex, far_point, min_x, min_y, max_x, max_y)
                    
                    if clipped:
                        start, end = clipped
                        new_edge = VoronoiEdge(start, end, edge.left_site, edge.right_site)
                        edges_to_add.append(new_edge)
            
            elif num_edges == 2:
                # Deux segments : prolonger dans la direction de la bissectrice
                edge1, edge2 = edges[0], edges[1]
                
                # Trouver les autres extrémités
                if edge1.start.distance_to(vertex) < epsilon:
                    other1 = edge1.end
                else:
                    other1 = edge1.start
                
                if edge2.start.distance_to(vertex) < epsilon:
                    other2 = edge2.end
                else:
                    other2 = edge2.start
                
                # Vecteurs pointant vers les autres extrémités
                v1_x = other1.x - vertex.x
                v1_y = other1.y - vertex.y
                v2_x = other2.x - vertex.x
                v2_y = other2.y - vertex.y
                
                # Normaliser
                len1 = math.sqrt(v1_x * v1_x + v1_y * v1_y)
                len2 = math.sqrt(v2_x * v2_x + v2_y * v2_y)
                
                if len1 > epsilon and len2 > epsilon:
                    v1_x /= len1
                    v1_y /= len1
                    v2_x /= len2
                    v2_y /= len2
                    
                    # Bissectrice : direction opposée à la moyenne
                    bisect_x = -(v1_x + v2_x)
                    bisect_y = -(v1_y + v2_y)
                    
                    bisect_len = math.sqrt(bisect_x * bisect_x + bisect_y * bisect_y)
                    if bisect_len > epsilon:
                        bisect_x /= bisect_len
                        bisect_y /= bisect_len
                        
                        far_point = Point(vertex.x + bisect_x * 1000, vertex.y + bisect_y * 1000)
                        clipped = clip_line_to_bbox(vertex, far_point, min_x, min_y, max_x, max_y)
                        
                        if clipped:
                            start, end = clipped
                            
                            # Déterminer les sites
                            sites1 = {edge1.left_site, edge1.right_site}
                            sites2 = {edge2.left_site, edge2.right_site}
                            unique_to_1 = sites1 - sites2
                            unique_to_2 = sites2 - sites1
                            
                            if len(unique_to_1) == 1 and len(unique_to_2) == 1:
                                left_site = list(unique_to_1)[0]
                                right_site = list(unique_to_2)[0]
                                new_edge = VoronoiEdge(start, end, left_site, right_site)
                                edges_to_add.append(new_edge)
        
        # Ajouter les nouvelles arêtes
        for edge in edges_to_add:
            self._diagram.add_edge(edge)