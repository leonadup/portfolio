from math import sqrt
from domain.point import Point
from typing import Tuple, Any

class Circle:
    def __init__(self, A:Point, B:Point, C:Point):
        '''
        cercle défini par 3 points
        '''
        self._A:Point = A
        self._B:Point = B
        self._C:Point = C
        self._center:Point = Point(0,0)
        self._rayon:float = 0.0
        if not Circle.points_valid(A, B, C):
            raise ValueError("Les trois points ne forment pas un cercle valide")
        self._calc_centre_rayon()

    @classmethod
    def points_valid(cls, A:Point, B:Point, C:Point) -> bool:
        '''
        Pour être un cercle valide A,B et C doivent être en sens trigo et non alignés
        '''
        AB = B - A
        AC = C - A
        return (AB.x * AC.y - AC.x * AB.y) < 0

    @property
    def rayon(self) -> float:
        return self._rayon
    
    @property
    def points(self) -> Tuple[Point, Point, Point]:
        return self._A, self._B, self._C

    @property
    def center(self) -> Point:
        return self._center
    
    def __str__(self):
        return f"cercle de centre {self._center}et de rayon rayon {self._rayon}"

    def __eq__(self, cercle2:Any) -> bool:
        equal = False
        if type(cercle2) != Circle:
            return equal
        if (self._A == cercle2._A and self._B == cercle2._B and self._C == cercle2._C):
            equal = True
        return equal

    def _calc_centre_rayon(self):
        '''
        Calcul le rayon et le centre du cercle circoncis du triangle formé par les trois points
        '''
        AB = self._B - self._A
        AC = self._C - self._A
        milieu_AB = (self._A + self._B)*0.5
        milieu_AC = (self._A + self._C)*0.5
        E = AB.x*milieu_AB.x + AB.y*milieu_AB.y
        F = AC.x*milieu_AC.x + AC.y*milieu_AC.y
        G = AB.x*AC.y - AB.y*AC.x

        if G == 0:
            raise ValueError("Points alignés !")

        ox = (AC.y*E - AB.y*F) / G
        oy = (AB.x*F - AC.x*E) / G

        self._center:Point = Point(ox, oy)
        self._rayon:float = sqrt((self._A.x-ox)**2 + (self._A.y-oy)**2)
