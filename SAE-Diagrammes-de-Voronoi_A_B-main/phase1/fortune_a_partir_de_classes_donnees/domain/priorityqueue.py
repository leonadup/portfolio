from domain.point import Point
from domain.circle import Circle
from typing import Union, Tuple

class PriorityQueue:
    def __init__(self):
        self._events = []  # liste des événements dans la file

    def empty(self) -> bool:
        return len(self._events) == 0

    def push(self, item:Union[Point, Circle]):
        '''
        Ajoute un evenement dans la file
        '''
        # recherche de l'indice d'insertion
        item_priority = self._get_priority(item)
        for i, e in enumerate(self._events):
            if item == e:
                # item déjà présent, abandon
                return
            e_priority = self._get_priority(e)
            if (e_priority[0] < item_priority[0]) or (e_priority[0] == item_priority[0]) and (e_priority[1] <= item_priority[1]): # e plus à gauche, passe au e suivant
                continue
            self._events.insert(i, item)
            return
        # tous les events sont prioritaire sur le nouvea
        self._events.append(item)

    def _get_priority(self, item:Union[Point, Circle]) -> Tuple[float, float]:
        '''
        renvoie la priorité de l'item qui est x d'abord puis y
        '''
        if type(item) == Point:
            return item.x, item.y
        # sinon c'est que c'est un cercle
        c = item.center
        return c.x + item.rayon, c.y

    def pop(self) -> Union[Point, Circle, None]:
        '''
        enlève et retourne le prochain item de la file
        '''
        if len(self._events) == 0:
            return None
        return self._events.pop(0)
    
    def __str__ (self):
        return "PriorityQueue(" + ", ".join(str(e) for e in self._events) + ")"
    
