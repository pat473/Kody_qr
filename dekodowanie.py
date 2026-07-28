from stale import *

class Dekoder:
    def __init__(self, gotowa_matryca):
        self.matryca = gotowa_matryca
        self.usun_strefe_ochronna()
        self.rozmiar = len(gotowa_matryca)
        self.wersja = int(((self.rozmiar-21)/4)+1)

        self.poziom_korekcji = None
        self.nr_maski = None

    def usun_strefe_ochronna(self):
        rdzen_poziomy = self.matryca[4:-4]
        nowa_matryca = []
        for wiersz in rdzen_poziomy:
            rdzen_wiersza = wiersz[4:-4]
            nowa_matryca.append(rdzen_wiersza)
        self.matryca = nowa_matryca

    @staticmethod
    def _oblicz_odleglosc_hamminga(odczytane_bity, idealne_bity):
        roznic =0
        for b1, b2 in zip(odczytane_bity, idealne_bity):
            if b1 != b2:
                roznic +=1
        return roznic

    def sprawdzanie_bitow_korekcyjnych(self, odczytane_bity):
        najlepsza_wersja = None
        najmniejsza_odleglosc = 999

        for wersja, idealne_bity in ciag_bitow_dla_danej_wersji.items():
            odleglosc = self._oblicz_odleglosc_hamminga(odczytane_bity, idealne_bity)

            if odleglosc < najmniejsza_odleglosc:
                najmniejsza_odleglosc = odleglosc
                najlepsza_wersja = wersja
        return najlepsza_wersja, najmniejsza_odleglosc


    def odczytaj_info_o_wersji(self):
        if self.wersja >= 7:
            info_lewy_dol = ""
            for i in range(6):
                for j in range(3):
                    bit = str(self.matryca[self.rozmiar-11+j][i])
                    info_lewy_dol += bit
            info_prawa_gora = ""
            for i in range(6):
                for j in range(3):
                    bit = str(self.matryca[i][self.rozmiar-11+j])
                    info_prawa_gora += bit

            wersja_lewy_dol, bledy_lewy_dol = self.sprawdzanie_bitow_korekcyjnych(info_lewy_dol)
            wersja_prawa_gora, bledy_prawa_gora = self.sprawdzanie_bitow_korekcyjnych(info_prawa_gora)

            if bledy_lewy_dol <= bledy_prawa_gora and bledy_lewy_dol<=3:
                return wersja_lewy_dol
            elif bledy_prawa_gora <= bledy_lewy_dol and bledy_prawa_gora<=3:
                return wersja_prawa_gora
            else:
                raise TypeError("Kod jest zbyt uszkodzony.")

    def odczytaj_info_poziom_korekcji_i_maska(self):
        info_laczne = ""
        info_rozdzielne = ""













