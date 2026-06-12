from domain.circle import Circle
from services.parabole_service import *
from domain.segment import Segment
from typing import Union

class Beach():
    '''
    La plage formée par les arcs de paraboles
    '''
    def __init__ (self):
        self._liste_points: list[Point] = [] # c'est la plage formée par une suite de foyers
        self._liste_segments_en_cours: list[Segment] = [] # les intersections
        self._liste_segment_finis: list[Segment] = [] # quand les intersections se rejoingnent (cercle)

    def insert_point(self, point:Point):
        '''
        insère un point dans la plage
        '''
        if self._liste_points == []:
            self._liste_points.append(point)
        elif len(self._liste_points) == 1:
                self._liste_points.append(point)
                self._liste_points.append(self._liste_points[0])
                self._liste_segments_en_cours.append(Segment(Point(get_x(self._liste_points[0], point.y, point.x), point.y)))
                self._liste_segments_en_cours.append(Segment(Point(get_x(self._liste_points[0], point.y, point.x), point.y)))
        else:
            for i in range(len(self._liste_points)):
                    if i < len(self._liste_points)-1:
                        inter = intersection(self._liste_points[i], self._liste_points[i+1], point.x)
                        if inter.y < point.y and inter.x > self._liste_points[i].x and inter.x < self._liste_points[i+1].x:
                            continue
                        if inter.y > point.y:
                            self._liste_points.insert(i+1, point)
                            self._liste_points.insert(i+2, self._liste_points[i])
                            point_start_segment = Point(get_x(self._liste_points[i], point.y, point.x), point.y)
                            self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                            self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                            return
                    else:
                        self._liste_points.append(point)
                        self._liste_points.append(self._liste_points[i])
                        point_start_segment = Point(get_x(self._liste_points[i], point.y, point.x), point.y)
                        self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                        self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                        return
    
    
    def detecte_cercle_valable(self, nouveau_foyer:Point):
        '''
        teste les cercles valables autour de la plage
        '''
        cercles = []
        if len(self._liste_points) < 3:
            return []
        for i in range(len(self._liste_points)-2):
            if Circle.points_valid(self._liste_points[i], self._liste_points[i+1], self._liste_points[i+2]):
                cercles.append(Circle(self._liste_points[i], self._liste_points[i+1], self._liste_points[i+2]))
        return cercles
    
    def insert_cercle(self, cercle:Circle):
        '''
        insère un cercle dans la plage
        '''
        #trouver le point du cercle qui a le plus grand x
        A = cercle._A
        B = cercle._B
        C = cercle._C
        if A.x > B.x and A.x > C.x:
            point_droite = A
        elif B.x > A.x and B.x > C.x:
            point_droite = B
        else:
            point_droite = C

        circles = self.detecte_cercle_valable(point_droite)
        if circles != []:
            return circles
        return None

    def refermer_segments (self, cercle:Circle):
        centre = cercle.center
        #trouver le point du cercle qui a le plus grand x
        A = cercle._A
        B = cercle._B
        C = cercle._C
        #il faut parcourir les point de départ des segments et trouver les origines qui encadre le y du centre du cercle
        for i in range(len(self._liste_points)-2):
            if self._liste_points[i] == A and self._liste_points[i+1] == B and self._liste_points[i+2] == C:
                self._liste_segments_en_cours[i].finish(centre)
                self._liste_segments_en_cours[i+1].finish(centre)
                #il faut ajouter les deux segments dans la liste des segments finis
                self._liste_segment_finis.append(self._liste_segments_en_cours[i])
                self._liste_segment_finis.append(self._liste_segments_en_cours[i+1])
                #supprimer les 2 segments qu'on vient d'ajouter dans la liste des segments finis
                del self._liste_segments_en_cours[i]
                del self._liste_segments_en_cours[i]
                del self._liste_points[i+1]
                #on ajoute un segments pour boucher le trou             
                self._liste_segments_en_cours.insert(i,Segment(centre))
                
