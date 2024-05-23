import math
import random
from enum import Enum
from typing import Optional

from backApp.rsp import RandomiziranoStablo
from backApp.structures import Ivica, Klasifikacija, KrajIvice, Objekat, Tacka, Vrh


# Smjer pokretne linije
class Smjer(Enum):
    LIJEVODESNO = 0
    DESNOLIJEVO = 1


# Dogadjaji
class Dogadjaj(Enum):
    Pocetak = 0
    Prevoj = 1
    Kraj = 2


# Lanac monotonog poligona
class Lanac(Enum):
    GORNJI = 0
    DONJI = 1


# Strana
class Strana(Enum):
    LIJEVO = 0
    DESNO = 1


smjerPL = Smjer.LIJEVODESNO  # smjer pokretne linije
tipVrha = Dogadjaj.Pocetak  # tip vrha
xPL = 0  # x koordinata pokretne linije
krajT = False  # je li kraj triangulacije


# Funckija za inicijalizaciju pokretne linije
def inicijalizacijaPL():
    sweepline = RandomiziranoStablo(poredjenjeObjekata)
    strazar = Tacka(0, -1e10)
    sweepline.ubaci(Ivica(Vrh(strazar.x, strazar.y), 0, Vrh(strazar.x, strazar.y)))
    return sweepline


# Raspored tacaka a i b
def lijevaPrijeDesne(a: Tacka, b: Tacka):
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        return 0


# Klasa poligon
class Poligon:
    def __init__(self, trenutniVrh: Optional[Vrh] = None, velicinaP: Optional[int] = 0):
        self.trenutniVrh: Vrh = trenutniVrh
        self.velicinaP: int = velicinaP
        self.azurirajVelicinuP()

    def ispis(self):
        for _ in range(self.dajVelicinu()):
            tVrh = self.dajTrenutniV()
            tacka: Tacka = tVrh.tackaVrha()
            print(tacka.x, tacka.y)
            tVrh = self.pomjeriTrenutniV(-1)
            self.postaviTrenutniV(tVrh)

    def azurirajVelicinuP(self):
        if self.trenutniVrh is None:
            self.velicinaP = 0
        else:
            v = self.trenutniVrh.sKs()
            self.velicinaP = 1
            while v != self.trenutniVrh:
                self.velicinaP += 1
                v = v.sKs()

    # Funkcija za podjelu poligona na dva poligona
    def podijeliP(self, b: Vrh):
        bp = self.trenutniVrh.podijeliVrh(b)
        self.azurirajVelicinuP()
        return Poligon(bp)

    def podijeliP1(self, b: Vrh):
        bp = self.trenutniVrh.podijeliV(b)
        self.azurirajVelicinuP()
        return Poligon(bp)

    def tackaTrenutnogV(self):
        if self.trenutniVrh is not None:
            return self.trenutniVrh.tackaVrha()

    def dajVelicinu(self):
        return self.velicinaP

    def ubaci(self, t: Tacka):
        if self.velicinaP == 0:
            self.trenutniVrh = Vrh(t.x, t.y)
        else:
            self.trenutniVrh = self.trenutniVrh.ubaciV(Vrh(t.x, t.y))

        self.velicinaP += 1
        return self.trenutniVrh

    def dajTrenutniV(self):
        return self.trenutniVrh

    def postaviTrenutniV(self, novi):
        self.trenutniVrh = novi
        return self.trenutniVrh

    def pomjeriTrenutniV(self, orjentacija):
        self.trenutniVrh = self.trenutniVrh.susjed(orjentacija)
        return self.trenutniVrh


# Funkcija koja racuna centroid tacaka
def izracunaj_centroid(tacke: list[Tacka]):
    centroid = Tacka(0, 0)
    for tacka in tacke:
        centroid.x += tacka.x
        centroid.y += tacka.y
    centroid.x /= len(tacke)
    centroid.y /= len(tacke)

    return centroid


# Funkcija koja na pocetku sortira random tacke kako bi se mogao nacrtati poligon
def sortTackePoPolarnomUglu(tacke: list[Tacka]):
    centroid = izracunaj_centroid(tacke)
    tacke.sort(key=lambda tacka: math.atan2(tacka.y - centroid.y, tacka.x - centroid.x))
    return tacke


# Funkcija koja generiše random tačke poligona
def generisiRandomPoligon(velicina):
    p: Poligon = Poligon()
    if velicina >= 3:
        # tacke = [
        #     Tacka(random.randint(0, 1000), random.randint(0, 520))
        #     for _ in range(velicina)
        # ]
        # tacke = [
        #     Tacka(100, 400),
        #     Tacka(250, 300),
        #     Tacka(340, 200),
        #     Tacka(400, 110),
        #     Tacka(900, 250),
        #     Tacka(830, 420),
        #     Tacka(820, 490),
        #     Tacka(800, 380),
        #     Tacka(700, 290),
        #     Tacka(550, 390),
        # ]
        tacke = [
            Tacka(116, 256),
            Tacka(362, 42),
            Tacka(876, 27),
            Tacka(988, 37),
            Tacka(955, 274),
            Tacka(934, 383),
            Tacka(576, 486),
            Tacka(572, 372),
            Tacka(471, 472),
            Tacka(279, 334),
        ]
        # tacke = [
        #     Tacka(24, 231),
        #     Tacka(402, 95),
        #     Tacka(520, 146),
        #     Tacka(526, 235),
        #     Tacka(627, 111),
        #     Tacka(925, 184),
        #     Tacka(997, 454),
        #     Tacka(993, 257),
        #     Tacka(492, 515),
        #     Tacka(186, 490),
        # ]
        # tacke = [
        #     Tacka(23, 247),
        #     Tacka(122, 123),
        #     Tacka(107, 83),
        #     Tacka(150, 91),
        #     Tacka(694, 53),
        #     Tacka(798, 7),
        #     Tacka(686, 142),
        #     Tacka(993, 257),
        #     Tacka(580, 222),
        #     Tacka(742, 282),
        #     Tacka(535, 216),
        #     Tacka(578, 305),
        #     Tacka(118, 430),
        # ]
        tacke = sortTackePoPolarnomUglu(tacke)
    for i in range(velicina):
        p.ubaci(tacke[i])
    p.ispis()
    return p


# Funkcija koja sortira vrhove poligona zavisno od smjera pokretne linije
def sortVrhovePoligona(poligon: Poligon, smjer):
    vrhovi: list[Vrh] = []
    if poligon.dajVelicinu() > 1:
        for _ in range(poligon.dajVelicinu()):
            vrhovi.append(poligon.dajTrenutniV())
            poligon.postaviTrenutniV(poligon.pomjeriTrenutniV(-1))

        if smjer == Smjer.LIJEVODESNO:
            sort_vrhovi = sorted(
                vrhovi, key=lambda t: [t.tackaVrha().x, t.tackaVrha().y]
            )

        else:
            sort_vrhovi = sorted(
                vrhovi, key=lambda t: [t.tackaVrha().x, t.tackaVrha().y], reverse=True
            )
    return sort_vrhovi


# Funkcija kriterija poredjenja objekata u randomiziranom stablu tj. pokretnoj liniji
def poredjenjeObjekata(o1: Objekat, o2: Objekat):
    # Poredjenje na osnovu y koordinate
    yO1, yO2 = o1.dajY(xPL), o2.dajY(xPL)

    if yO1 < yO2:
        return -1
    elif yO1 > yO2:
        return 1

    if o1.Tip() == 1 and o2.Tip() == 1:
        return 0
    elif o1.Tip() == 1:
        return -1
    elif o2.Tip() == 1:
        return 1

    znak = 1
    if (smjerPL == Smjer.LIJEVODESNO and tipVrha == Dogadjaj.Pocetak) or (
        smjerPL == Smjer.DESNOLIJEVO and tipVrha == Dogadjaj.Kraj
    ):
        znak = -1

    # Poredjenje na osnovu nagiba
    nO1, nO2 = o1.nagib(), o2.nagib()
    if nO1 < nO2:
        return znak
    elif nO1 > nO2:
        return -znak

    return 0


# Odredjuje tip dogadjaja vrha u odnosu na smjer pokretne linije
def tipDogadjaja(vrh: Vrh, smjer):
    if smjer == Smjer.LIJEVODESNO:
        a = lijevaPrijeDesne(vrh.tackaVrha(), vrh.sKs().tackaVrha())
        b = lijevaPrijeDesne(vrh.tackaVrha(), vrh.sSKs().tackaVrha())
    else:
        a = lijevaPrijeDesne(vrh.sKs().tackaVrha(), vrh.tackaVrha())
        b = lijevaPrijeDesne(vrh.sSKs().tackaVrha(), vrh.tackaVrha())
    if a <= 0 and b <= 0:
        return Dogadjaj.Kraj
    elif a > 0 and b > 0:
        return Dogadjaj.Pocetak
    else:
        return Dogadjaj.Prevoj


# Funkcija koja obradjuje dogadjaj pocetak
def procesirajPocetak(v: Vrh, pokretnaL: RandomiziranoStablo):
    kI = KrajIvice(v.tackaVrha())
    a: Ivica = pokretnaL.lociraj(kI)
    if not v.jelKonveksanV():
        # Obradi split vrh
        w = a.W()
        wp: Vrh = v.podijeliV(w)
        pokretnaL.ubaci(Ivica(wp.sKs(), -1, wp.sKs()))
        pokretnaL.ubaci(Ivica(v.sSKs(), 1, v))

        if smjerPL == Smjer.LIJEVODESNO:
            a[1] = v
        else:
            a[1] = wp.sKs()
    else:
        # Obradi start vrh
        pokretnaL.ubaci(Ivica(v.sSKs(), 1, v))
        pokretnaL.ubaci(Ivica(v, -1, v))
        a[1] = v


# Funkcija koja obradjuje dogadjaj prevoj
def procesirajPrevoj(v: Vrh, pokretnaL: RandomiziranoStablo):
    kI = KrajIvice(v.tackaVrha())
    a: Ivica = pokretnaL.lociraj(kI)
    b: Ivica = pokretnaL.sljedeci()
    if a is not None and b is not None:
        a[1] = v
        b[1] = v
        b[0] = b[0].susjed(b.R())


# Funkcija koja obradjuje dogadjaj kraj
def procesirajKraj(v: Vrh, pokretnaL: RandomiziranoStablo, poligoni):
    kI = KrajIvice(v.tackaVrha())
    a = pokretnaL.lociraj(kI)
    b = pokretnaL.sljedeci()
    c = pokretnaL.sljedeci()

    if a is not None and b is not None and c is not None:
        # Obradi end vrh
        if v.jelKonveksanV():
            p = Poligon(v)
            poligoni.append(p)
        # Obradi merge vrh
        else:
            a[1] = v

        pokretnaL.ukloniE(b)
        pokretnaL.ukloniE(c)


# Kreiranje monotonih poligona od prostog poligona p
def kreirajMonotonePoligone(p: Poligon, smjer, poligoni):
    sortirani_vrhovi = sortVrhovePoligona(p, smjer)
    global smjerPL
    global xPL
    global tipVrha
    smjerPL = smjer
    pokretnaLinija = inicijalizacijaPL()
    for i in range(0, len(sortirani_vrhovi)):
        t = sortirani_vrhovi[i]
        xPL = t.tackaVrha().x
        tipVrha = tipDogadjaja(t, smjerPL)
        if tipVrha == Dogadjaj.Pocetak:
            procesirajPocetak(t, pokretnaLinija)
        elif tipVrha == Dogadjaj.Prevoj:
            procesirajPrevoj(t, pokretnaLinija)
        else:
            procesirajKraj(t, pokretnaLinija, poligoni)


# Glavna funkcija podjele prostog poligona na monotone poligone
def dekompozicija(p):
    # Kreira parcijalo monotone iduci sa lijeva na desno
    parcijalnoMonotoni = []
    kreirajMonotonePoligone(p, Smjer.LIJEVODESNO, parcijalnoMonotoni)

    xMonotoni = []

    # Kreira monotone iduci sa desna na lijevo
    for poligon in parcijalnoMonotoni:
        kreirajMonotonePoligone(poligon, Smjer.DESNOLIJEVO, xMonotoni)

    return xMonotoni


# Provjerava da li su dva vrha spojena ivicom
def susjedan(a: Vrh, b: Vrh):
    return b.tackaVrha() == a.sKs().tackaVrha() or b.tackaVrha() == a.sSKs().tackaVrha()


# Vraca najljevlji vrh poligona
def vratiNajmanjiV(p: Poligon, f):
    najV = p.dajTrenutniV()
    p.pomjeriTrenutniV(-1)
    for _ in range(1, p.dajVelicinu()):
        if f(p.dajTrenutniV().tackaVrha(), najV.tackaVrha()) > 0:
            najV = p.dajTrenutniV()
        p.pomjeriTrenutniV(-1)
    p.postaviTrenutniV(najV)
    return najV


# Vraca vrh lanca i vrstu lanca
def vratiVrhLanca(vD: Vrh, vG: Vrh):
    lanac = 2
    vrhGornjegLanca = vG.sKs()
    vrhDonjegLanca = vD.sSKs()
    if vrhGornjegLanca.tackaVrha().x < vrhDonjegLanca.tackaVrha().x:
        lanac = Lanac.GORNJI
        return vrhGornjegLanca, lanac
    elif vrhGornjegLanca.tackaVrha() == vrhDonjegLanca.tackaVrha():
        return vrhGornjegLanca, lanac
    else:
        lanac = Lanac.DONJI
        return vrhDonjegLanca, lanac


# Funkcija koja pravi dijagonale iz jedne tacke prema ostalim tackama poligona
def napraviDijagonale(p: Poligon, dijagonale):
    tv = p.dajTrenutniV()
    v1 = tv.sKs()
    for i in range(0, p.dajVelicinu() - 1):
        if krajT is True and i == 0:
            v1 = v1.sKs()
            continue
        else:
            dijagonale.append((tv.tackaVrha(), v1.tackaVrha()))
            v1 = v1.sKs()


# Glavna funkcija za triangulaciju monotonog poligona
def triangulacijaMonotonogPoligona(p: Poligon):
    dijagonale = []
    q = []
    stek: list[Vrh] = []
    global krajT
    krajT = False
    vratiNajmanjiV(p, lijevaPrijeDesne)
    vD = p.dajTrenutniV()
    vG = p.dajTrenutniV()
    stek.append(vD)
    pom, lanac = vratiVrhLanca(vD, vG)
    if lanac == Lanac.GORNJI:
        vG = pom
    else:
        vD = pom
    stek.append(pom)
    while True:
        pom, lanac = vratiVrhLanca(vD, vG)
        if lanac == 2:
            krajT = True
        elif lanac == Lanac.GORNJI:
            vG = pom
        else:
            vD = pom

        # Prva opcija
        if susjedan(pom, stek[-1]) and not susjedan(pom, stek[0]):
            strana = (
                Klasifikacija.DESNO if lanac == Lanac.GORNJI else Klasifikacija.LIJEVO
            )

            a = stek[-1]
            b = stek[-2]

            while (
                b.tackaVrha().klasifikacijaT(pom.tackaVrha(), a.tackaVrha()) == strana
            ):
                if lanac == Lanac.GORNJI:
                    p.postaviTrenutniV(pom)
                    q = p.podijeliP(b)
                    napraviDijagonale(q, dijagonale)

                else:
                    p.postaviTrenutniV(b)
                    q = p.podijeliP(pom)
                    napraviDijagonale(q, dijagonale)

                stek.pop()

                if len(stek) <= 1:
                    break

                a = stek[-1]
                b = stek[-2]

            stek.append(pom)

        # Druga opcija
        elif susjedan(pom, stek[0]) and not susjedan(pom, stek[-1]):
            v = stek.pop()

            if lanac == Lanac.GORNJI:
                p.postaviTrenutniV(v)
                q = p.podijeliP1(pom)
                napraviDijagonale(q, dijagonale)

            else:
                p.postaviTrenutniV(v)
                q = p.podijeliP(pom)
                napraviDijagonale(q, dijagonale)

            while not len(stek) == 0:
                stek.pop()

            stek.append(v)
            stek.append(pom)

        # Treca opcija
        else:
            p.postaviTrenutniV(pom)
            napraviDijagonale(p, dijagonale)
            break

    while not len(stek) == 0:
        stek.pop()

    return dijagonale


# Funkcija koja vrsi triangulaciju svih monotonih poligona unutar prostog poligona
def triangulacijaMonotonihPoligona(poligoni):
    dijagonale = []
    for poligon in poligoni:
        dijagonale.append(triangulacijaMonotonogPoligona(poligon))
    return dijagonale
