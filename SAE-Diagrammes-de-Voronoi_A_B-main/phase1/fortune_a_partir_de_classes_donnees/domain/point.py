from typing import Any

class Point:
    def __init__(self, x:float, y:float):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __add__(A:"Point", B:"Point") -> "Point":
        '''
        Ajoute deux vecteurs
        '''
        x = A.x + B.x
        y = A.y + B.y
        return Point(x, y)

    def __eq__(A:"Point", B:Any) -> bool:
        """ Fonction pour tester l'unicité"""
        equal = False
        if type(B) != Point:
            return equal
        if A.x == B.x and A.y == B.y:
            return not equal

    def __sub__(A:"Point", B:"Point") -> "Point":
        '''
        Soustraction de deux points, aussi coordonnées du vecteur AB
        '''
        x = A.x - B.x
        y = A.y - B.y
        return Point(x, y)

    def __mul__(A:"Point", k:float) -> "Point":
        '''
        Multiplication par un scalaire k
        '''
        x = A.x * k
        y = A.y * k
        return Point(x,y)

    def __str__(self) -> str:
        return f"({self._x} ; {self._y})"
    
    def __repr__(self) -> str:
        return f"Point[{self._x} ; {self._y}]"

    def in_box(self, left:int, right:int, top:int, bottom:int) -> bool:
        '''
        renvoie True si le point est dans la boite
        '''
        return left <= self._x <= right and bottom <= self._y <= top
