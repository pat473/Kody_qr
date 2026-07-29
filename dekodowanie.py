from stale import *
from wspolne import SzablonQR, MetodyMasek


class DeMajsterMatrycy:
    def __init__(self, gotowa_matryca):
        self.matryca = gotowa_matryca
        self.usun_strefe_ochronna()
        self.rozmiar = len(gotowa_matryca)
        self.wersja = int(((self.rozmiar-21)/4)+1)
        self.wzorzec_matryca = SzablonQR(self.rozmiar,self.wersja).wygeneruj()

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

    def sprawdzanie_bitow_korekcyjnych(self, odczytane_bity, slownik):
        najlepsza_wersja = None
        najmniejsza_odleglosc = 999

        for wersja, idealne_bity in slownik.items():
            odleglosc = self._oblicz_odleglosc_hamminga(odczytane_bity, idealne_bity)

            if odleglosc < najmniejsza_odleglosc:
                najmniejsza_odleglosc = odleglosc
                najlepsza_wersja = wersja
        return najlepsza_wersja, najmniejsza_odleglosc

    def _wybierz_zwyciezce(self, ciag_1, ciag_2, slownik):
        wynik_1, bledy_1 = self.sprawdzanie_bitow_korekcyjnych(ciag_1, slownik)
        wynik_2, bledy_2 = self.sprawdzanie_bitow_korekcyjnych(ciag_2, slownik)

        if bledy_1 <= bledy_2 and bledy_1 <= 3:
            return wynik_1
        elif bledy_2 <= bledy_1 and bledy_2 <=3:
            return wynik_2
        else:
            raise ValueError("Kod jest zbyt uszkodzony.")

    def odczytaj_dane(self):
        info_laczne = ""
        info_rozdzielne = ""

        for i in range(9):
            if i != 6:
                bit = str(self.matryca[8][i])
                info_laczne += bit
        for i in range(7,-1,-1):
            if i != 6 :
                bit = str(self.matryca[i][8])
                info_laczne += bit
        for i in range(7):
            bit = str(self.matryca[self.rozmiar-1-i][8])
            info_rozdzielne += bit
        for i in range(7,-1,-1):
            bit = str(self.matryca[8][self.rozmiar-1-i])
            info_rozdzielne += bit

        format_wynik = self._wybierz_zwyciezce(info_laczne, info_rozdzielne,ciag_bitow_dla_maski_oraz_poziomu_korekcji_bledow)
        self.poziom_korekcji = format_wynik[0]
        self.nr_maski = format_wynik[1]

        if self.wersja >=7:
            info_lewy_dol = ""
            info_prawa_gora = ""
            for i in range(6):
                for j in range(3):
                    bit_ld = str(self.matryca[self.rozmiar - 11 + j][i])
                    info_lewy_dol += bit_ld
                    bit_pg = str(self.matryca[i][self.rozmiar-11+j])
                    info_prawa_gora += bit_pg

            self.wersja = self._wybierz_zwyciezce(info_lewy_dol, info_prawa_gora, ciag_bitow_dla_danej_wersji)

    def odmaskowanie(self):
        mapa_samych_danych = self.wzorzec_matryca.strefa_danych
        for y,x in mapa_samych_danych:
            if MetodyMasek.czy_odwrocic_bit(self.nr_maski,y,x):
                self.matryca[y][x] ^=1

    def odczytanie_ciagu_danych(self):
        generator = SzablonQR(self.rozmiar,self.wersja)
        trasa = generator.pobierz_trase_wezyka2()
        odcztane_dane = ""
        for y,x in trasa:
            bit = str(self.matryca[y][x])
            odcztane_dane += bit
        return odcztane_dane

    def zbierz_dane_z_matrycy(self):
        self.odczytaj_dane()
        self.odmaskowanie()
        return self.odczytanie_ciagu_danych()


    # def zamien_obraz_na_matryce(self):

class DekoderDanych:

    def __init__(self, ciag_danych, wersja, poziom_korekcji):
        self.ciag_danych = ciag_danych
        self.wersja = wersja
        self.poziom_korekcji = poziom_korekcji



        self.odczytany_tekst = ""



    def antyprzeplot(self):

    def podzial_na_liczby(self):

