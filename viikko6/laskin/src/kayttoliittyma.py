from enum import Enum
from tkinter import ttk, constants, StringVar

class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class KomentoRajapinta:
    def suorita(self):
        raise NotImplementedError

    def kumoa(self):
        raise NotImplementedError


class Summa(KomentoRajapinta):
    def __init__(self, logiikka, input_reader):
        self._logiikka = logiikka
        self._input_reader = input_reader
        self._edellinen = None

    def suorita(self):
        self._edellinen = self._logiikka.arvo()
        self._logiikka.plus(self._input_reader())
        return self._logiikka.arvo()

    def kumoa(self):
        self._logiikka.aseta_arvo(self._edellinen)
        return self._logiikka.arvo()


class Erotus(KomentoRajapinta):
    def __init__(self, logiikka, input_reader):
        self._logiikka = logiikka
        self._input_reader = input_reader
        self._edellinen = None

    def suorita(self):
        self._edellinen = self._logiikka.arvo()
        self._logiikka.miinus(self._input_reader())
        return self._logiikka.arvo()

    def kumoa(self):
        self._logiikka.aseta_arvo(self._edellinen)
        return self._logiikka.arvo()


class Nollaus(KomentoRajapinta):
    def __init__(self, logiikka):
        self._logiikka = logiikka
        self._edellinen = None

    def suorita(self):
        self._edellinen = self._logiikka.arvo()
        self._logiikka.nollaa()
        return self._logiikka.arvo()

    def kumoa(self):
        self._logiikka.aseta_arvo(self._edellinen)
        return self._logiikka.arvo()


class Kumoa(KomentoRajapinta):
    def __init__(self, historia):
        self._historia = historia

    def suorita(self):
        if not self._historia:
            return None

        komento = self._historia.pop()
        return komento.kumoa()

    def kumoa(self):
        # Ei palauteta kumottua kumoa-komentoa
        return None

class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        self._historia = []
        self.komennot = {}

    def _lue_syote(self):
        arvo = 0
        try:
            arvo = int(self._syote_kentta.get())
        except Exception:
            pass
        return arvo

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        # Luodaan komennot vasta kun syötekenttä on olemassa
        self.komennot = {
            Komento.SUMMA: Summa(self._sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: Erotus(self._sovelluslogiikka, self._lue_syote),
            Komento.NOLLAUS: Nollaus(self._sovelluslogiikka),
            Komento.KUMOA: Kumoa(self._historia),
        }

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _suorita_komento(self, komento):
        komento_olio = self.komennot[komento]

        if komento == Komento.KUMOA:
            komento_olio.suorita()
        else:
            komento_olio.suorita()
            self._historia.append(komento_olio)

        self._kumoa_painike["state"] = constants.NORMAL if self._historia else constants.DISABLED
        self._nollaus_painike["state"] = constants.DISABLED if self._sovelluslogiikka.arvo() == 0 else constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())
