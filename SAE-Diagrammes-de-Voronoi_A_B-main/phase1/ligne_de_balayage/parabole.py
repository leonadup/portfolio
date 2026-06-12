from point import Point
from droite import Droite
from config import screen, egalite_float
from math import sqrt
class Parabole():
    def __init__(self, foyer : Point, directrice : Droite):
        self._foyer = foyer
        self._directrice = directrice
        self._domaine = None
        self.calcul_domaine()

    @property
    def foyer(self) -> Point:
        return self._foyer
    
    @property
    def directrice(self) -> Droite:
        return self._directrice
    
    @property
    def domaine(self) -> tuple[int, int]:
        return self._domaine
    
    

    def calcul_domaine(self) -> None:
        a = self.foyer.x
        k = self.directrice.x
        # foyer et parabole à droite de la directrice
        if a > k: 
            self._domaine = (int((a + k) / 2), int(screen.get_width()))
        # foyer et parabole à gauche de la directrice
        else: 
            self._domaine = (int(0), int((a + k) / 2))
        

    def equation(self, x: float, branche: str) -> list[Point]:
        a = self.foyer.x
        b = self.foyer.y
        k = self.directrice.x

        # equation de départ pour une directrice verticale : 
        # (y - b)**2 = 2(a - k)*x + (k**2 - a**2)
        # la partie sous la racine carrée de droite doit être positive ou 
        # nulle pour que y soit réel
        
        discriminant = 2 * (a-k)*x + (k**2 - a**2)

        # verification si le discriminant est négatif
        if discriminant < 0:
            return None
        if branche == "superieure":
            y = b + sqrt(discriminant)
        elif branche == "inferieure":
            y = b - sqrt(discriminant)
        return Point(x, y)

            

    
    
    def intersection(self, parabole) -> list[Point]:
        points_intersection: list[Point] = []
        # On a k1 = k2 dans notre cas d'usage (car la directrice est la meme pour les 2 paraboles)
        a1: float = self.foyer.x #a1, b1 pour notre parabole
        b1: float = self.foyer.y
        a2: float = parabole.foyer.x #a2, b2 pour la parabole comparée
        b2: float = parabole.foyer.y
        k: float = self.directrice.x

        # SOLUTION 1 : superieure, superieure

        branche_parabole_1 = "superieure"
        branche_parabole_2 = "superieure"
        
        d = 2*(a1-a2)
        e = a2**2 - a1**2 - (b2 - b1)**2
        f = 2*(b2-b1)
        
        racines = self.solution_polynome(d, e, f, k, a2)
        if racines != None:
            for point in self.verification(racines[0], racines[1], branche_parabole_1, branche_parabole_2, parabole):
                points_intersection.append(point)
         
        # SOLUTION 2 : superieure inferieure

        branche_parabole_1 = "superieure"
        branche_parabole_2 = "inferieure"

        d = 2*(a1-a2)
        e = a2**2 - a1**2 - (b2-b1)**2
        f = (-2)*(b2-b1)

        if d == 0 and b2 > b1:
            x1 = (((b2-b1)/2)**2-(k**2-a1**2))/(2*(a1-k))
            racines = [x1, None]
        else:
            racines = self.solution_polynome(d, e, f, k, a2)
        if racines != None:
            for point in self.verification(racines[0], racines[1], branche_parabole_1, branche_parabole_2, parabole):
                points_intersection.append(point)

        # SOLUTION 3 : inferieure superieure

        branche_parabole_1 = "inferieure"
        branche_parabole_2 = "superieure"

        d = 2*(a1-a2)
        e = (b1-b2)**2 + a2**2 - a1**2
        f = 2*(b1-b2)

        if d == 0 and b1 > b2:
            x1 = (((b1-b2)/2)**2 - (k**2 - a1**2))/(2*(a1 - k))
            racines = [x1, None]
        else : 
            racines = self.solution_polynome(d, e, f, k, a1)
        if racines != None:
            for point in self.verification(racines[0], racines[1], branche_parabole_1, branche_parabole_2, parabole):
                points_intersection.append(point)

        # SOLUTION 4 : inferieure inferieure
        
        branche_parabole_1 = "inferieure"
        branche_parabole_2 = "inferieure"

        d = 2*(a2-a1)
        e = (b1-b2)**2 + a1**2 - a2**2
        f = (-2)*(b1-b2) 

        racines = self.solution_polynome(d, e, f, k, a2)
        if racines != None:
            for point in self.verification(racines[0], racines[1], branche_parabole_1, branche_parabole_2, parabole):
                points_intersection.append(point)
        
        return points_intersection
            
    def solution_polynome(self, d: float, e: float, f: float, k: float, a: float) -> list[float]:

        # On obtient une équation de la forme px^2 + qx + r = 0 (polynome 2nd degré)
        if d == 0: #pas de polynome du 2nd degré mais une solution quand meme a trouver
            return None
        p = d**2
        q = 2*d*e - 2*f**2*(a-k)
        r = e**2 - f**2*(k**2-a**2)

        # Vérification du discriminant
        delta = q**2 - 4*p*r
        if delta < 0:
            # Pas de solution réelle
            return None
        if delta == 0:
            # Résolution du polynome
            x1 = -q /(2*p)
            x2 = None
        else:
            # Résolution du polynome
            x1 = (-q + sqrt(q**2 - 4*p*r)) / (2*p)
            x2 = (-q - sqrt(q**2 - 4*p*r)) / (2*p)
        return [x1, x2]


    # VÉRIFICATION DE LA SOLUTION DANS LES 2 ÉQUATIONS DE PARABOLE
    def verification(self, x1 : float, x2 : float, branche_parabole_1: str, branche_parabole_2: str, parabole) -> list[Point]:
        
        points_intersection: list[Point] = []
        # Vérification du domaine de définition  
        if self.domaine[0] <= x1 <= self.domaine[1] or parabole.domaine[0] <= x1 <= parabole.domaine[1]:
            equation_x1_1 = self.equation(x1, branche_parabole_1)
            equation_x1_2 = parabole.equation(x1, branche_parabole_2)
            # On vérifie si les solutions existent
            if equation_x1_1 != None and equation_x1_2 != None: 
                # On vérifie que la solution est la même 
                # POUR LES BRANCHES TESTÉES
                if egalite_float(equation_x1_1.y, equation_x1_2.y):
                    points_intersection.append(equation_x1_1)
                    
        if x2 != None:
            if self.domaine[0] <= x2 <= self.domaine[1] or parabole.domaine[0] <= x2 <= parabole.domaine[1]:
                equation_x2_1 = self.equation(x2, branche_parabole_1)
                equation_x2_2 = parabole.equation(x2, branche_parabole_2)
                # On vérifie si les solutions existent
                if equation_x2_1 != None and equation_x2_2 != None: 
                    # On vérifie que la solution est la même 
                    # POUR LES BRANCHES TESTÉES
                    if egalite_float(equation_x2_1.y, equation_x2_2.y):
                        points_intersection.append(equation_x2_1)
        return points_intersection



    def tracer(self) -> None:
        # calcul du domaine de définition de x
        self.calcul_domaine()
        for abscisse in range(self.domaine[0], self.domaine[1] * 100):
            x = abscisse * 0.01
            points = [self.equation(x, "superieure"), self.equation(x, "inferieure")]
            if points != None:
                for point in points:
                    if point is not None:
                        point.tracer()
