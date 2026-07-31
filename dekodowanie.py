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

        self.bajty_dziesietne = []
        self.bloki_danych = []
        self.bloki_korekcyjne = []

        self.bajty_danych_i_korekcji = []

        self.lista_syndromow = []
        self.dane = []


        self.odczytany_tekst = ""

    def podzial_na_liczby(self):
        for i in range(0,self.ciag_danych,8):
            bajt = self.ciag_danych[i:i+8]
            if len(bajt)==8:
                liczba = int(bajt,2)
                self.bajty_dziesietne.append(liczba)


    def antyprzeplot(self):
        parametry = slowa_kodowe[self.wersja, self.poziom_korekcji]
        liczba_danych = parametry["liczba_danych"]
        bloki_w_grupie_1 = parametry["bloki_w_grupie1"]
        bloki_w_grupie_2 = parametry["bloki_w_grupie2"]
        wielkosc_blokow = parametry["liczba_slow_danych_dla_blokow_grupy1"]
        wielkosc_blokow2 = parametry["liczba_slow_danych_dla_blokow_grupy2"]
        wielkosc_korekcji = parametry["slowa_korekcyjne_na_blok"]
        liczba_wszystkich_blokow = bloki_w_grupie_1 + bloki_w_grupie_2


        rozrzucone_dane = self.bajty_dziesietne[:liczba_danych]
        rozrzucone_korekcje = self.bajty_dziesietne[liczba_danych:]

        for _ in range(bloki_w_grupie_1):
            blok_d = []
            blok_k = []
            self.bloki_danych.append(blok_d)
            self.bloki_korekcyjne.append(blok_k)

        for _ in range(bloki_w_grupie_2):
            blok_d = []
            blok_k = []
            self.bloki_danych.append(blok_d)
            self.bloki_korekcyjne.append(blok_k)

        while len(rozrzucone_dane)>0:
            for i in range(liczba_wszystkich_blokow):
                if i < bloki_w_grupie_1:
                    aktualny_limit = wielkosc_blokow
                else:
                    aktualny_limit = wielkosc_blokow2

                if aktualny_limit > 0 and len(self.bloki_danych[i]) < aktualny_limit:
                    self.bloki_danych[i].append(rozrzucone_dane.pop(0))

        while len(rozrzucone_korekcje)>0:
            for i in range(liczba_wszystkich_blokow):

                if len(self.bloki_korekcyjne[i]) < wielkosc_korekcji:
                    self.bloki_korekcyjne[i].append(rozrzucone_korekcje.pop(0))

        gotowy_ciag = []
        for i in self.bloki_danych:
            gotowy_ciag.append(i)
        for j in self.bloki_korekcyjne:
            gotowy_ciag.append(j)
        self.bajty_danych_i_korekcji = gotowy_ciag

    def mnozenie_gf(self,a,b):
            if a == 0 or b == 0:
                return 0
            suma_poteg = tabela_logarytmow[a] + tabela_logarytmow[b]
            suma_poteg = suma_poteg % 255
            return tabela_poteg[suma_poteg]

    def dzielenie_gf(self,a,b):
        if b ==0:
            raise ZeroDivisionError("Dzielenie przez zero w Ciele Galois")
        if a ==0:
            return 0
        roznica_poteg = tabela_logarytmow[a] - tabela_logarytmow[b]
        roznica_poteg = ( roznica_poteg+255)%255
        return tabela_poteg[roznica_poteg]

    def obliczanie_syndromow(self, liczba_bajtow_korekcyjnych, gotowy_ciag):
        wyrazy_ciagu = len(gotowy_ciag)

        for syndrom in range(liczba_bajtow_korekcyjnych):
            wynik = 0
            for i in range(wyrazy_ciagu):
                mnozenie = self.mnozenie_gf(wynik,tabela_poteg[syndrom])
                dodawanie = mnozenie ^ gotowy_ciag[i]
                wynik = dodawanie
            self.lista_syndromow.append(wynik)
        for element in self.lista_syndromow:
            if element != 0:
                return False
        return True


    def algorytm_berlekampa_masseya(self):
        glowny_wielomian = [1]
        kopia_wielomianu = [1]
        licznik_zakladanej_liczby_bledow = 0
        licznik_przesuniecia = 1
        ostatnia_wartosc_rozbieznosci = 1
        for aktualna_iteracja in range(len(self.lista_syndromow)):
            rozbieznosc = self.lista_syndromow[aktualna_iteracja]
            suma_iloczynow = 0

            for i in range(1, len(glowny_wielomian)):
                if aktualna_iteracja - i >= 0:
                    iloczyn = self.mnozenie_gf(glowny_wielomian[i],self.lista_syndromow[aktualna_iteracja-i])
                    suma_iloczynow = suma_iloczynow ^ iloczyn
            rozbieznosc = rozbieznosc ^ suma_iloczynow


            if rozbieznosc ==0:
                licznik_przesuniecia +=1
            else:
                    tymczasowa_kopia = glowny_wielomian.copy()
                    skorygowana_kopia = []
                    for element in kopia_wielomianu:
                        pomnozony = self.mnozenie_gf(element,rozbieznosc)
                        podzielony = self.dzielenie_gf(pomnozony,ostatnia_wartosc_rozbieznosci)
                        skorygowana_kopia.append(podzielony)
                    kopia_wielomianu = skorygowana_kopia

                    for _ in range(licznik_przesuniecia):
                        kopia_wielomianu.insert(0,0)

                    nowy_wielomian = []
                    max_dlugosc = max(len(glowny_wielomian), len(kopia_wielomianu))

                    for i in range(max_dlugosc):
                        wartosc_glowna = glowny_wielomian[i] if i < len(glowny_wielomian) else 0
                        wartosc_z_kopii = kopia_wielomianu[i] if i < len(kopia_wielomianu) else 0

                        nowy_wielomian.append(wartosc_glowna ^ wartosc_z_kopii)

                    glowny_wielomian = nowy_wielomian

                    if 2*licznik_zakladanej_liczby_bledow<=aktualna_iteracja:
                        licznik_zakladanej_liczby_bledow = aktualna_iteracja+1- licznik_zakladanej_liczby_bledow
                        kopia_wielomianu = tymczasowa_kopia
                        ostatnia_wartosc_rozbieznosci = rozbieznosc
                        licznik_przesuniecia = 1
                    else:
                        licznik_przesuniecia +=1

        return glowny_wielomian

    def wyszukiwanie_chiena(self, gotowy_ciag):
        wielomian = self.algorytm_berlekampa_masseya()
        liczba_bledow = len(wielomian)-1
        pozycje_bledow = []
        for i in range(len(gotowy_ciag)):
            mnoznik_alfa = tabela_poteg[255-i]
            wynik = self.podstawienie_x_do_wielomianu(wielomian,mnoznik_alfa)
            if wynik == 0:
                pozycje_bledow.append(i)
            if len(pozycje_bledow) == liczba_bledow:
                return pozycje_bledow

    def podstawienie_x_do_wielomianu(self,wspolczynniki,x):
        wynik = 0
        for i in wspolczynniki:
            wynik = self.mnozenie_gf(wynik,x)
            wynik = wynik ^ i
        return wynik

    def algorytm_forneya(self, gotowy_ciag):
        wielomian = self.algorytm_berlekampa_masseya()
        uszkodzone_pozycje = self.wyszukiwanie_chiena(gotowy_ciag)
        ewaluator_bledow = self.mnozenie_wielomianow_gf(wielomian,self.lista_syndromow)
        pochodna_wielomianu = self.pochodna_wielomianu_gf(wielomian)

        for pozycja in uszkodzone_pozycje:

            x = tabela_poteg[(255-pozycja)%255]
            wartosc_ewaluatora = self.podstawienie_x_do_wielomianu(ewaluator_bledow,x)
            wartosc_pochodnej = self.podstawienie_x_do_wielomianu(pochodna_wielomianu,x)

            surowa_maska_bledu = self.dzielenie_gf(wartosc_ewaluatora, wartosc_pochodnej)
            ostateczna_maska_bledu = self.mnozenie_gf(surowa_maska_bledu,tabela_poteg[pozycja])

            wadliwy_bajt = gotowy_ciag[pozycja]
            naprawiony_bajt = wadliwy_bajt ^ ostateczna_maska_bledu

            gotowy_ciag[pozycja] = naprawiony_bajt

        return gotowy_ciag


    def mnozenie_wielomianow_gf(self,w1,w2):
        rozmiar_wyniku = len(w1) + len(w2) -1
        wynik = [0] * rozmiar_wyniku
        for i in range(len(w1)):
            for j in range(len(w2)):
                wynik[i+j] += wynik[i+j] ^ self.mnozenie_gf(w1[i],w2[j])
        return wynik

    def pochodna_wielomianu_gf(self,wielomian):
        wynik =[]
        for i in range(len(wielomian)-1):
            potega = len(wielomian)-1-i
            if potega %2 != 0:
                wynik.append(wielomian[i])
            else:
                wynik.append(0)

        if not wynik:
            return[0]
        return wynik

    def odwrotny_reed_solomon(self):
        parametry = slowa_kodowe[self.wersja, self.poziom_korekcji]
        wielkosc_korekcji = parametry["slowa_korekcyjne_na_blok"]

        naprawione_dane = []

        for blok_d, blok_k in zip(self.bloki_danych,self.bloki_korekcyjne):
            gotowy_ciag = blok_d + blok_k

            self.lista_syndromow = []

            if not self.obliczanie_syndromow(wielkosc_korekcji,gotowy_ciag):
                gotowy_ciag = self.algorytm_forneya(gotowy_ciag)

            czyste_dane = gotowy_ciag[:len(blok_d)]
            naprawione_dane.extend(czyste_dane)

        self.dane = naprawione_dane












