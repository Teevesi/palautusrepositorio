import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()


        self.varasto_mock = Mock()

        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 10)
            if tuote_id == 3:
                return Tuote(3, "voi", 20)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_kaksi_tuotetta_ostaessa_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 15)

    def test_kaksi_samaa_tuotetta_ostaessa_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 10)

    def test_loppunutta_tuotetta_ostaessa_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

        # tehdään toiset ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("matti", "54321")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikein
        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "54321", ANY, 10)

    def test_uusi_viitenumero_jokaiselle_maksulle(self):
        
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # määritellään että metodi palauttaa ensimmäisellä kutsulla 1, toisella 2 ja kolmannella 3
        viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        kauppa = Kauppa(self.varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että nyt käytössä ensimmäinen viite
        pankki_mock.tilisiirto.assert_called_with("pekka", 1, "12345", ANY, 5)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("matti", "123456")

        # ...toinen viite
        pankki_mock.tilisiirto.assert_called_with("matti", 2, "123456", ANY, 5)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("jaakko", "1234567")

        # ...ja kolmas viite
        pankki_mock.tilisiirto.assert_called_with("jaakko", 3, "1234567", ANY, 5)

    def test_poista_tuote_korista_palauttaa_tuotteen_varastoon(self):
        
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)

        # varmistetaan, että palautetaan_varastoon metodia on kutsuttu
        self.varasto_mock.palauta_varastoon.assert_called()