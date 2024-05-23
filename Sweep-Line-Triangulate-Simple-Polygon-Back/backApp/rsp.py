import random

from backApp.structures import Cvor, Ivica


class RSP_Cvor(Cvor):
    def __init__(self, podatak, sjeme=-1):
        Cvor.__init__(self)
        if sjeme != -1:
            random.seed(sjeme)  # Random number generator
        self.prioritet = random.random()
        self.podatak = podatak
        self.roditelj = None
        self.lijevoDijete = None
        self.desnoDijete = None

    def rotiraj_udesno(self):
        y = self
        x = y.lijevoDijete
        r = y.roditelj

        T2 = x.desnoDijete
        y.lijevoDijete = T2

        if y.lijevoDijete is not None:
            y.lijevoDijete.roditelj = y

        if r is not None:
            if r.desnoDijete == y:
                r.desnoDijete = x
            else:
                r.lijevoDijete = x

        x.roditelj = r
        x.desnoDijete = y
        y.roditelj = x

    def rotiraj_ulijevo(self):
        x = self
        y = x.desnoDijete
        r = x.roditelj

        T2 = y.lijevoDijete
        x.desnoDijete = T2

        if x.desnoDijete is not None:
            x.desnoDijete.roditelj = x
        if r is not None:
            if r.lijevoDijete == x:
                r.lijevoDijete = y
            else:
                r.desnoDijete = y

        y.roditelj = r
        y.lijevoDijete = x
        x.roditelj = y

    def istisniNagore(self):
        r = self.roditelj
        if r is not None:
            if self.prioritet < r.prioritet:
                if self == r.lijevoDijete:
                    r.rotiraj_udesno()
                else:
                    r.rotiraj_ulijevo()
                self.istisniNagore()

    def istisniNadole(self):
        prioritetLijevogD = self.lijevoDijete.prioritet if self.lijevoDijete else 2.0
        prioritetDesnogD = self.desnoDijete.prioritet if self.desnoDijete else 2.0
        minPrioritet = min(prioritetLijevogD, prioritetDesnogD)

        if self.prioritet <= minPrioritet:
            return

        if prioritetLijevogD < prioritetDesnogD:
            self.rotiraj_udesno()
        else:
            self.rotiraj_ulijevo()

        self.istisniNadole()


class RandomiziranoStablo:
    def __init__(self, fP):
        self.funkcijaPoretka = fP
        self.korijen: RSP_Cvor = None
        self.trenutniP: RSP_Cvor = None

    def ubaci(self, podatak):
        rez = 1
        k = self.korijen
        if k is None:
            self.trenutniP = RSP_Cvor(podatak, 42)
            self.korijen = self.trenutniP
            self.korijen.prioritet = -1.0
            return podatak
        d = self.korijen.desnoDijete

        while d is not None:
            k = d
            rez = self.funkcijaPoretka(podatak, k.podatak)
            if rez < 0:
                d = k.lijevoDijete
            elif rez > 0:
                d = k.desnoDijete
            else:
                return Ivica()
        self.trenutniP = RSP_Cvor(podatak, 42)
        self.trenutniP.roditelj = k

        if rez < 0:
            k.lijevoDijete = self.trenutniP
            k.prethodni().ubaci(self.trenutniP)
        else:
            k.desnoDijete = self.trenutniP
            k.ubaci(self.trenutniP)

        self.trenutniP.istisniNagore()
        return podatak

    def pronadji(self, e):
        d = self.korijen.desnoDijete
        while d is not None:
            rez = self.funkcijaPoretka(e, d.podatak)
            if rez < 0:
                d = d.lijevoDijete
            elif rez > 0:
                d = d.desnoDijete
            else:
                self.trenutniP = d
                return self.trenutniP.podatak
        return None

    def lociraj(self, podatak):
        k = self.korijen
        d = k.desnoDijete

        while d is not None:
            rez = self.funkcijaPoretka(podatak, d.podatak)
            if rez < 0:
                d = d.lijevoDijete
            elif rez > 0:
                k = d
                d = d.desnoDijete
            else:
                self.trenutniP = d
                return self.trenutniP.podatak

        self.trenutniP = k
        return self.trenutniP.podatak

    def ukloniS(self, cvor: RSP_Cvor):
        cvor.prioritet = 1.5
        cvor.istisniNadole()
        r = cvor.roditelj
        if r.lijevoDijete == cvor:
            r.lijevoDijete = None
        else:
            r.desnoDijete = None
        if self.trenutniP == cvor:
            self.trenutniP = cvor.prethodni()
        cvor.ukloni()

    def ukloni(self):
        if self.trenutniP != self.korijen:
            self.ukloniS(self.trenutniP)

    def ukloniE(self, e):
        el = self.pronadji(e)
        if el is not None:
            self.ukloni()

    def sljedeci(self):
        self.trenutniP = self.trenutniP.sljedeci()
        return self.trenutniP.podatak

    def prethodni(self):
        self.trenutniP = self.trenutniP.prethodni()
        return self.trenutniP.podatak

    def ispisi(self, cvor: RSP_Cvor):
        if cvor is None:
            return
        else:
            self.ispisi(cvor.lijevoDijete)
            print(
                "cvor",
                "v",
                cvor.podatak.V().tackaVrha().x,
                "v",
                cvor.podatak.V().tackaVrha().y,
                "r",
                cvor.podatak.R(),
                "w",
                cvor.podatak.W().tackaVrha().x,
                "w",
                cvor.podatak.W().tackaVrha().y,
            )
            self.ispisi(cvor.desnoDijete)
