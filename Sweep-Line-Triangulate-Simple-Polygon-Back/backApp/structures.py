from enum import Enum
from typing import Optional

import numpy as np


class Klasifikacija(Enum):
    LIJEVO = 0
    DESNO = 1
    IZAS = 2
    ISPREDS = 3
    POCETAKS = 4
    KRAJS = 5
    IZMEDJUS = 6


class Tacka:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, p):
        return (self.x < p.x) or ((self.x == p.x) and (self.y < p.y))

    def __gt__(self, p):
        return (self.x > p.x) or ((self.x == p.x) and (self.y > p.y))

    def __sub__(self, p):
        return Tacka(self.x - p.x, self.y - p.y)

    def __eq__(self, p):
        return (self.x == p.x) and (self.y == p.y)

    # Orjentacija tacaka
    def orjentacijaT(self, p1, p2):
        sTeta = (p2.x - p1.x) * (self.y - p1.y) - (self.x - p1.x) * (p2.y - p1.y)
        if sTeta > 0.0:
            return 1
        elif sTeta < 0.0:
            return -1
        return 0

    def moduoV(self):
        return np.sqrt(self.x**2 + self.y**2)

    def klasifikacijaT(self, p1, p2):
        p3 = self
        a: Tacka = p2 - p1
        b: Tacka = p3 - p1

        if p3.orjentacijaT(p1, p2) > 0.0:
            return Klasifikacija.LIJEVO
        elif p3.orjentacijaT(p1, p2) < 0.0:
            return Klasifikacija.DESNO
        elif a.x * b.x < 0.0 or a.y * b.y < 0.0:
            return Klasifikacija.IZAS
        elif a.moduoV() < b.moduoV():
            return Klasifikacija.ISPREDS
        elif p3 == p1:
            return Klasifikacija.POCETAKS
        elif p3 == p2:
            return Klasifikacija.KRAJS

        return Klasifikacija.IZMEDJUS


class Segment:
    def __init__(self, pocetakS: Tacka = None, krajS: Tacka = None):
        self.pocetakS = pocetakS
        self.krajS = krajS

    def koeficijentPravca(self):
        if self.pocetakS.x != self.krajS.x:
            return (self.krajS.y - self.pocetakS.y) / (self.krajS.x - self.pocetakS.x)
        return float("inf")

    def dajYKoord(self, x):
        return self.koeficijentPravca() * (x - self.pocetakS.x) + self.pocetakS.y


# Cvor klasa dvostruko povezana lista
class Cvor:
    def __init__(self):
        self.sljedeciC = self
        self.prethodniC = self

    def sljedeci(self):
        return self.sljedeciC

    def prethodni(self):
        return self.prethodniC

    def ubaci(self, b):
        c = self.sljedeciC
        b.sljedeciC = c
        b.prethodniC = self
        self.sljedeciC = b
        if c is not None:
            c.prethodniC = b
        return b

    def ukloni(self):
        if self.prethodniC is not None:
            self.prethodniC.sljedeciC = self.sljedeciC
        if self.sljedeciC is not None:
            self.sljedeciC.prethodniC = self.prethodniC
        return self

    def spoji(self, cvor):
        self.sljedeciC = cvor
        cvor.prethodniC = self


class Objekat:
    def __init__(self, tip):
        self.tip = tip  # 0 za ivicu, 1 za tacku

    def dajY(self, x):
        pass

    def Tip(self):
        return self.tip

    def dajIvicu(self):
        return Segment()

    def nagib(self):
        return 0.0


# Klasa vrh nasljedjuje klase Tacka i Cvor
class Vrh(Tacka, Cvor):
    def __init__(self, x: Optional[float] = 0.0, y: Optional[float] = 0.0):
        Cvor.__init__(self)
        Tacka.__init__(self, x, y)

    # Funkcija koja poredi vrhove
    def __lt__(self, p):
        return (
            (self.tackaVrha().y < p.tackaVrha().y)
            or (self.tackaVrha().y == p.tackaVrha().y)
            and (self.tackaVrha().x < p.tackaVrha().x)
        )

    def tackaVrha(self):
        return Tacka(self.x, self.y)

    def sKs(self):
        return self.sljedeci()

    def sSKs(self):
        return self.prethodni()

    def susjed(self, orjentacija):
        return self.sKs() if orjentacija < 0 else self.sSKs()

    def ubaciV(self, v):
        return self.ubaci(v)

    def spojiV(self, v):
        self.spoji(v)

    def jelKonveksanV(self):
        u = self.sSKs()
        w: Vrh = self.sKs()
        k = w.klasifikacijaT(self, u)
        return k == Klasifikacija.DESNO or k == Klasifikacija.IZAS

    def podijeliV(self, p):
        t = p.tackaVrha()
        tP = p.sSKs().ubaciV(Vrh(t.x, t.y))
        t = self.tackaVrha()
        a = self.ubaciV(Vrh(t.x, t.y))
        tP.spojiV(a)
        self.spojiV(p)
        return tP

    def podijeliVrh(self, p):
        t = p.tackaVrha()
        tP = p.ubaciV(Vrh(t.x, t.y))
        t = self.tackaVrha()
        a = self.sSKs().ubaciV(Vrh(t.x, t.y))
        p.spojiV(self)
        a.spojiV(tP)
        return tP


class Ivica(Objekat):
    def __init__(self, v: Vrh = None, r: int = 0, w: Vrh = None):
        super().__init__(0)
        self.v = v
        self.w = w
        self.r = r

    def dajIvicu(self):
        return Segment(self.v.tackaVrha(), self.v.sKs().tackaVrha())

    def dajY(self, xPL):
        return self.dajIvicu().dajYKoord(xPL)

    def nagib(self):
        return self.dajIvicu().koeficijentPravca()

    def azurirajW(self, w1):
        self.w = w1

    def __getitem__(self, i):
        return self.v if i == 0 else self.w

    def __setitem__(self, i, value):
        if i == 0:
            self.v = value
        elif i == 1:
            self.w = value

    def W(self):
        return self.w

    def V(self):
        return self.v

    def R(self):
        return self.r


class KrajIvice(Objekat):
    def __init__(self, t: Tacka):
        super().__init__(1)
        self.t = t

    def dajY(self, x):
        return self.t.y

    def tacka(self):
        return self.t
