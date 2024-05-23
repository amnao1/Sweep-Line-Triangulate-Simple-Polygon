import json

from backApp.services import (
    Poligon,
    dekompozicija,
    generisiRandomPoligon,
    triangulacijaMonotonihPoligona,
)
from backApp.structures import Tacka, Vrh
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def main(request):
    return JsonResponse({"name": "App started!"})


@csrf_exempt
def getName(request):
    return JsonResponse({"name": "Kompjutaciona geometrija"})


@csrf_exempt
def triangulate_polygon_view(request):
    data = json.loads(request.body)
    n = data["n"]
    p: Poligon = generisiRandomPoligon(n)
    # Ovdje iz nastalih poligona uzimaju se tacke kako bi se mogle proslijediti na front za crtanje
    vrhoviProstog = []
    vrhoviP = []
    vrhovi: list[Vrh] = []
    for _ in range(n):
        tVrh = p.dajTrenutniV()
        tacka: Tacka = tVrh.tackaVrha()
        vrhoviProstog.append((tacka.x, tacka.y))
        tVrh = p.pomjeriTrenutniV(-1)
        p.postaviTrenutniV(tVrh)

    poligoni: list[Poligon] = dekompozicija(p)

    for poligon in poligoni:
        vrhovi = []
        for _ in range(poligon.dajVelicinu()):
            tVrh = poligon.dajTrenutniV()
            tacka: Tacka = tVrh.tackaVrha()
            vrhovi.append((tacka.x, tacka.y))
            # print(tacka.x, tacka.y)
            tVrh = poligon.pomjeriTrenutniV(-1)
            poligon.postaviTrenutniV(tVrh)
        vrhoviP.append(vrhovi)

    dijagonale = triangulacijaMonotonihPoligona(poligoni)

    vrhoviD = []
    for i in range(len(dijagonale)):
        for j in range(len(dijagonale[i])):
            vrhoviD.append((dijagonale[i][j][0].x, dijagonale[i][j][0].y))
            vrhoviD.append((dijagonale[i][j][1].x, dijagonale[i][j][1].y))

    return JsonResponse(
        {"vrhovi": vrhoviProstog, "vrhoviP": vrhoviP, "vrhoviD": vrhoviD}
    )
