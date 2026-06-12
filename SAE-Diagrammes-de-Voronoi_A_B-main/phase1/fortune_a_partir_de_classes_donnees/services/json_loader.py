from domain.point import Point

def load_json(filename: str) -> dict:
    '''
    Charge un fichier JSON et le retourne sous forme de dictionnaire
    '''
    import json
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def convert_to_points(data: dict) -> list:
    '''
    Convertit une liste de dictionnaire en une liste de Point
    '''
    points = []
    #récupérer les clés et les valeurs {"1.0":"3.2"} et les convertir en Point(x,y)
    for d in data:
        key, value = list(d.items())[0]
        points.append(Point(float(key), float(value)))
    return points