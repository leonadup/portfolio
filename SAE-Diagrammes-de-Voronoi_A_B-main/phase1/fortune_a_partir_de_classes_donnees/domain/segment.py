from typing import Optional, Tuple
from domain.point import Point

class Segment:
    def __init__(self, A:Point, B:Optional[Point] = None):
        '''
        crée le segment [AB]
        '''
        self._A = A
        self._B = B

    def finish(self, p:Point):
        assert self._B == None, "L'extrémité ne peut être écrite qu'une seule fois !"
        self._B = p

    def __str__(self):
        if self._B is None:
            return f"[{str(self._A)} ; ?]"    
        return f"[{str(self._A)} ; {str(self._B)}]"

    def __repr__(self):
        if self._B is None:
            return f"Seg[{str(self._A)} ; ?]"    
        return f"Seg[{str(self._A)} ; {str(self._B)}]"

    @property
    def points(self) -> Tuple[Point, Point]:
        return self._A, self._B

    def copy(self) -> "Segment":
        return Segment(self._A, self._B)

    def rogner(self, left:float, right:float, top:float, bottom:float, prolonger:bool=False) -> Optional["Segment"]:
        '''
        Renvoie l'intersection du segment avec la boîte délimitée par les bords
        prolonger: indique s'il faut prolonger le côté end jusqu'à un bord
        '''
        assert left <= right and bottom <= top
       
        S = self._A
        E = self._B
        if S == E:
            return None
        S_in_box = S.in_box(left, right, top, bottom)
        E_in_box = E.in_box(left, right, top, bottom)
        if not prolonger and S_in_box and E_in_box:
            # rien à faire
            return self.copy()
        # traitement à part du cas self._B.x en -infini
        if self._B.x == float("-inf"):
            # on ne considère que le y de self._B
            y = self._B.y
            if not(bottom < y < top):
                return None
            if prolonger or self._B.x >= right:
                return Segment(Point(left,y), Point(right,y))
            if self._B.x <= left:
                return None
            return Segment(Point(left,y), self._B)
        # on poursuit avec les cas normaux
        # Sur l'axe gradué (S, SE) on cherche coordonnées k de toutes
        # les intersection avec les bords
        ks = [
            self.__k_for_x(left),
            self.__k_for_x(right),
            self.__k_for_y(top),
            self.__k_for_y(bottom),
        ]
        SE = E - S
        # on calcule les points correspondant en tenant compte que des k >= 0
        # et, si prolonge = False, k <= 1
        if prolonger:
            inters = {k:S + SE*k for k in ks if 0 <= k}
        else:
            inters = {k:S + SE*k for k in ks if 0 <= k <= 1}
        # on filtre encore pour ne retire que les intersections à l'intérieur du cadre (donc sur un bord)
        inters_in = {k:inters[k] for k in inters if inters[k].in_box(left, right, top, bottom)}
        if len(inters_in) == 0:
            # aucune intersection
            return None
        # On retient les points en allant du plus près de S au plus loin
        # il ne peut y en avoir que 0, 1 ou 2.
        pts = [inters_in[k] for k in sorted(inters_in.keys())]
        if S_in_box:
            nS = S
        else:
            #si S n'est pas dans la boîte, mais que la droite passe dans la boîte
            #alors le point d'entrée est forcément le plus proche de S
            nS = pts[0]
        if E_in_box and not prolonger:
            nE = E
        else:
            # si E est dehors ou que l'on souhaite prolonger,
            # le point de sortie est forcément le plus loin de S
            nE = pts[-1]
        return Segment(nS, nE)
    
    def __k_for_y(self, y:float) -> float:
        '''
        Soit S le point start et E le point end
        on peut considéré, à côté du repère Oxy, un repère (S, SE) donc juste un axe.
        On cherche sur cet axe la coordonnée k du point intersectant la droite horizontale
        en y du repère Oxy
        On ne veut que les k positifs. Si impossible, on renvoie -1
        '''
        S = self._A
        E = self._B
        assert E is not None and S.x != float("-inf")
        if S.y == E.y:
            return -1
        k = (y - S.y) / (E.y - S.y)
        if k < 0:
            return -1
        return k

    def __k_for_x(self, x:float) -> float:
        '''
        Soit S le point start et E le point end
        on peut considéré, à côté du repère Oxy, un repère (S, SE) donc juste un axe.
        On cherche sur cet axe la coordonnée k du point intersectant la droite verticale
        en x du repère Oxy
        On ne veut que les k positifs. Si impossible, on renvoie -1
        En cas d'impossibilité, renvoie -1
        '''
        S = self._A
        E = self._B
        assert E is not None and S.x != float("-inf")
        if S.x == E.x:
            return -1
        k = (x - S.x) / (E.x - S.x)
        if k <= 0:
            return -1
        return k
