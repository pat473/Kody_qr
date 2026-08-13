from matematyka import OperacjeNaCieleGalois, MatematykaInna
from stale import *
from wspolne import SzablonQR, MetodyMasek, Przygotowanie
from PIL import Image

class DeMajsterMatrycy:
    def __init__(self, gotowa_matryca):
        self.matryca = gotowa_matryca
        self.usun_strefe_ochronna()
        self.rozmiar = len(self.matryca)
        self.wersja = int(((self.rozmiar-21)/4)+1)
        self.wzorzec_matryca = SzablonQR(self.rozmiar, self.wersja)
        self.wzorzec_matryca.wygeneruj()

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
        trasa = self.wzorzec_matryca.pobierz_trase_wezyka2()
        odcztane_dane = ""
        for y,x in trasa:
            bit = str(self.matryca[y][x])
            odcztane_dane += bit
        return odcztane_dane

    def zdemajstruj_matryce(self):
        self.odczytaj_dane()
        self.odmaskowanie()
        return self.odczytanie_ciagu_danych()


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

        self.tryb_danych = ""
        self.wskaznik_liczby_znakow = ""

        self.nadmiarowe_marginesy = ""
        self.odczytany_tekst = ""

    def antyprzeplot(self):
        liczba_danych, bloki_1, bloki_2, wielkosc_1, wielkosc_2, wielkosc_korekcji = Przygotowanie.pobierz_parametry_qr(self.wersja,self.poziom_korekcji, "liczba_danych", "bloki_w_grupie1", "bloki_w_grupie2", "liczba_slow_danych_dla_blokow_grupy1", "liczba_slow_danych_dla_blokow_grupy2", "slowa_korekcyjne_na_blok")

        liczba_wszystkich_blokow = bloki_1 + bloki_2

        rozrzucone_dane = self.bajty_dziesietne[:liczba_danych]
        rozrzucone_korekcje = self.bajty_dziesietne[liczba_danych:]

        for _ in range(bloki_1):
            blok_d = []
            blok_k = []
            self.bloki_danych.append(blok_d)
            self.bloki_korekcyjne.append(blok_k)

        for _ in range(bloki_2):
            blok_d = []
            blok_k = []
            self.bloki_danych.append(blok_d)
            self.bloki_korekcyjne.append(blok_k)

        while len(rozrzucone_dane)>0:
            dodano_cos = False
            for i in range(liczba_wszystkich_blokow):
                if i < bloki_1:
                    aktualny_limit = wielkosc_1
                else:
                    aktualny_limit = wielkosc_2

                if aktualny_limit > 0 and len(self.bloki_danych[i]) < aktualny_limit:
                    self.bloki_danych[i].append(rozrzucone_dane.pop(0))
                    dodano_cos = True

            if not dodano_cos:
                break

        while len(rozrzucone_korekcje)>0:
            dodano_cos = False
            for i in range(liczba_wszystkich_blokow):

                if len(self.bloki_korekcyjne[i]) < wielkosc_korekcji:
                    self.bloki_korekcyjne[i].append(rozrzucone_korekcje.pop(0))
                    dodano_cos = True

            if not dodano_cos:
                break

        gotowy_ciag = []
        for i in self.bloki_danych:
            gotowy_ciag.append(i)
        for j in self.bloki_korekcyjne:
            gotowy_ciag.append(j)
        self.bajty_danych_i_korekcji = gotowy_ciag

    def obliczanie_syndromow(self, liczba_bajtow_korekcyjnych, gotowy_ciag):
        wyrazy_ciagu = len(gotowy_ciag)

        for syndrom in range(liczba_bajtow_korekcyjnych):
            wynik = 0
            for i in range(wyrazy_ciagu):
                mnozenie = OperacjeNaCieleGalois.mnozenie_gf(wynik,tabela_poteg[syndrom])
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
                    iloczyn = OperacjeNaCieleGalois.mnozenie_gf(glowny_wielomian[i],self.lista_syndromow[aktualna_iteracja-i])
                    suma_iloczynow = suma_iloczynow ^ iloczyn
            rozbieznosc = rozbieznosc ^ suma_iloczynow

            if rozbieznosc ==0:
                licznik_przesuniecia +=1
            else:
                    tymczasowa_kopia = glowny_wielomian.copy()
                    skorygowana_kopia = []
                    for element in kopia_wielomianu:
                        pomnozony = OperacjeNaCieleGalois.mnozenie_gf(element,rozbieznosc)
                        podzielony = OperacjeNaCieleGalois.dzielenie_gf(pomnozony,ostatnia_wartosc_rozbieznosci)
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
            wynik = MatematykaInna.podstawienie_x_do_wielomianu(wielomian,mnoznik_alfa)
            if wynik == 0:
                pozycje_bledow.append(i)
            if len(pozycje_bledow) == liczba_bledow:
                return pozycje_bledow
            raise ValueError(f"Uszkodzenie! Oczekiwano {liczba_bledow} błędów, znaleziono {len(pozycje_bledow)}.")

    def algorytm_forneya(self, gotowy_ciag):
        wielomian = self.algorytm_berlekampa_masseya()
        uszkodzone_pozycje = self.wyszukiwanie_chiena(gotowy_ciag)
        ewaluator_bledow = OperacjeNaCieleGalois.mnozenie_wielomianow_gf(wielomian,self.lista_syndromow)
        pochodna_wielomianu = OperacjeNaCieleGalois.pochodna_wielomianu_gf(wielomian)

        for pozycja in uszkodzone_pozycje:

            x = tabela_poteg[(255-pozycja)%255]
            wartosc_ewaluatora = MatematykaInna.podstawienie_x_do_wielomianu(ewaluator_bledow,x)
            wartosc_pochodnej = MatematykaInna.podstawienie_x_do_wielomianu(pochodna_wielomianu,x)

            surowa_maska_bledu = OperacjeNaCieleGalois.dzielenie_gf(wartosc_ewaluatora, wartosc_pochodnej)
            ostateczna_maska_bledu = OperacjeNaCieleGalois.mnozenie_gf(surowa_maska_bledu,tabela_poteg[pozycja])

            wadliwy_bajt = gotowy_ciag[pozycja]
            naprawiony_bajt = wadliwy_bajt ^ ostateczna_maska_bledu

            gotowy_ciag[pozycja] = naprawiony_bajt

        return gotowy_ciag

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

    def ustal_tryb_kodowania(self, ciag_danych):
        znacznik_trybu = ciag_danych[:4]
        match znacznik_trybu:
            case "0001":
                self.tryb_danych = "Numeryczny"
            case "0010":
                self.tryb_danych = "Alfanumeryczny"
            case "0100":
                self.tryb_danych = "Bajtowy"

        self.odczytany_tekst = self.odczytany_tekst[4:]

    def wykorzystaj_wskaznik_liczby_znakow(self):
        if self.tryb_danych == rodzaj_trybu.Numeryczny.name:
            liczba_znakow = wskaznik_liczby_znakow["numeryczny"]
        elif self.tryb_danych == rodzaj_trybu.Alfanumeryczny.name:
            liczba_znakow = wskaznik_liczby_znakow["alfanumeryczny"]
        else:
            liczba_znakow = wskaznik_liczby_znakow["bajtowy"]

        if 1 <= self.wersja <= 9:
            liczba_zn = liczba_znakow[0]
        elif 10 <= self.wersja <= 26:
            liczba_zn = liczba_znakow[1]
        else:
            liczba_zn = liczba_znakow[2]

        kawalek_bitow = self.odczytany_tekst[: liczba_zn]
        self.odczytany_tekst = self.odczytany_tekst[liczba_zn:]
        dlugosc_danych = int(kawalek_bitow,2)
        return dlugosc_danych


    def dlugosc_samej_wiadomosci(self):
        dlugosc_danych = self.wykorzystaj_wskaznik_liczby_znakow()
        if self.tryb_danych == rodzaj_trybu.Bajtowy.name:
            wskaznik_dlugosci_danych = dlugosc_danych * 8
            return wskaznik_dlugosci_danych
        elif self.tryb_danych == rodzaj_trybu.Numeryczny.name:
            wskaznik_dlugosci_danych = (dlugosc_danych // 3)*10
            if dlugosc_danych % 3 == 1:
                wskaznik_dlugosci_danych += 4
            elif dlugosc_danych % 3 == 2:
                wskaznik_dlugosci_danych += 7
            return wskaznik_dlugosci_danych
        else:
            wskaznik_dlugosci_danych = (dlugosc_danych // 2) * 11
            if dlugosc_danych % 2 == 1:
                wskaznik_dlugosci_danych +=6
            return wskaznik_dlugosci_danych

    def rozdzielenie_wiadomosci_od_paddingu(self):
        indeks_ciecia = self.dlugosc_samej_wiadomosci()
        self.nadmiarowe_marginesy = self.odczytany_tekst[indeks_ciecia:]
        self.odczytany_tekst = self.odczytany_tekst[:indeks_ciecia]

    def dekodowanie(self):
        tekst_koncowy = ""
        if self.tryb_danych == rodzaj_trybu.Bajtowy.name:
            for i in range(0,len(self.odczytany_tekst),8):
                kawalek = self.odczytany_tekst[i:i+8]
                liczba = int(kawalek,2)
                tekst_koncowy += chr(liczba)

        elif self.tryb_danych == rodzaj_trybu.Numeryczny.name:
            for i in range(0,len(self.odczytany_tekst),10):
                kawalek = self.odczytany_tekst[i:i+10]
                liczba = int(kawalek,2)
                if len(kawalek) == 10:
                    liczba = f"{liczba:03d}"
                elif len(kawalek) == 7:
                    liczba = f"{liczba:02d}"
                elif len(kawalek) == 4:
                    liczba = f"{liczba:01d}"
                tekst_koncowy += liczba
        else:
            for i in range(0,len(self.odczytany_tekst),11):
                kawalek = self.odczytany_tekst[i:i+11]
                liczba = int(kawalek,2)
                if len(kawalek) == 11:
                    indeks_1 = liczba // 45
                    indeks_2 = liczba % 45
                    tekst_koncowy += alfanumeryczne_wartosci[indeks_1]
                    tekst_koncowy += alfanumeryczne_wartosci[indeks_2]
                elif len(kawalek) ==6:
                    liczba = int(kawalek)
                    tekst_koncowy += alfanumeryczne_wartosci[liczba]

        self.odczytany_tekst = tekst_koncowy

    def zdekoduj_dane(self):
        self.bajty_dziesietne = MatematykaInna.zamiana_na_bajty(self.ciag_danych)

        self.antyprzeplot()
        self.odwrotny_reed_solomon()

        self.odczytany_tekst = MatematykaInna.zamiana_na_bity(self.dane)

        self.ustal_tryb_kodowania(self.odczytany_tekst)
        self.rozdzielenie_wiadomosci_od_paddingu()
        self.dekodowanie()

class CzytnikMatryc:
    def __init__(self,sciezka):
        self.sciezka = sciezka

    def obraz_na_matryce(self):
        # 1. Wczytanie obrazu i konwersja do odcieni szarości (L = Luminance)
        obraz = Image.open(self.sciezka).convert('L')
        piksele = obraz.load()
        szerokosc, wysokosc = obraz.size

        # 2. Szukanie granic kodu (odcinamy biały margines - Quiet Zone)
        # Znajdujemy pierwsze i ostatnie czarne piksele z każdej strony
        min_x, min_y = szerokosc, wysokosc
        max_x, max_y = 0, 0

        for y in range(wysokosc):
            for x in range(szerokosc):
                if piksele[x, y] < 128:  # Próg dla czarnego piksela
                    if x < min_x: min_x = x
                    if y < min_y: min_y = y
                    if x > max_x: max_x = x
                    if y > max_y: max_y = y

        # 3. Obliczenie rozmiaru jednego modułu (kratki)
        # Badamy górną krawędź lewego górnego oka (od min_x w prawo).
        # Zgodnie ze standardem, to oko ma dokładnie 7 kratek szerokości.
        dlugosc_oka_w_pikselach = 0
        for x in range(min_x, max_x + 1):
            if piksele[x, min_y] < 128:
                dlugosc_oka_w_pikselach += 1
            else:
                break  # Dotarliśmy do białej przerwy

        rozmiar_modulu = dlugosc_oka_w_pikselach / 7.0

        # 4. Obliczenie docelowego rozmiaru całej matrycy (np. 21x21)
        szerokosc_kodu_piksele = (max_x - min_x) + 1
        wymiar_matrycy = int(round(szerokosc_kodu_piksele / rozmiar_modulu))

        matryca = []

        # 5. Próbkowanie siatki (czytanie wartości z samego środka kratek)
        for wiersz in range(wymiar_matrycy):
            rzad = []
            for kolumna in range(wymiar_matrycy):
                # Przesuwamy się o 'wiersz' i 'kolumna', ale dodajemy 0.5,
                # by celować dokładnie w ŚRODEK pikselowy danej kratki (omijamy rozmyte brzegi)
                srodek_x = min_x + int((kolumna + 0.5) * rozmiar_modulu)
                srodek_y = min_y + int((wiersz + 0.5) * rozmiar_modulu)

                # Bezpiecznik na wypadek błędów zaokrągleń przy samym brzegu
                srodek_x = min(srodek_x, szerokosc - 1)
                srodek_y = min(srodek_y, wysokosc - 1)

                jasnosc = piksele[srodek_x, srodek_y]

                # Standard QR: Ciemny moduł = 1 (True), Jasny moduł = 0 (False)
                bit = 1 if jasnosc < 128 else 0
                rzad.append(bit)

            matryca.append(rzad)

        nowa_szerokosc = wymiar_matrycy + 8
        pusty_wiersz = [0] * nowa_szerokosc

        matryca_z_marginesem = []

        # 1. Dodajemy 4 puste (białe) wiersze na samej górze
        for _ in range(4):
            matryca_z_marginesem.append(pusty_wiersz.copy())

        # 2. Bierzemy nasze sczytane rzędy kodu i po bokach dodajemy po 4 zera
        for rzad in matryca:
            nowy_rzad = [0] * 4 + rzad + [0] * 4
            matryca_z_marginesem.append(nowy_rzad)

        # 3. Dodajemy 4 puste wiersze na samym dole
        for _ in range(4):
            matryca_z_marginesem.append(pusty_wiersz.copy())

        return matryca_z_marginesem

class SkanerQR:
    def __init__(self, sciezka_do_obrazu):
        self.sciezka = sciezka_do_obrazu

    def zdekoduj(self):

        czytnik = CzytnikMatryc(self.sciezka)
        surowa_matryca = czytnik.obraz_na_matryce()

        demajster = DeMajsterMatrycy(surowa_matryca)
        surowy_ciag_bitow = demajster.zdemajstruj_matryce()
        wersja = demajster.wersja
        poziom_korekcji = demajster.poziom_korekcji

        dekoder = DekoderDanych(surowy_ciag_bitow,wersja,poziom_korekcji)
        dekoder.zdekoduj_dane()

        finalowa_wiadomosc = dekoder.odczytany_tekst

        return finalowa_wiadomosc



# if __name__ == "__main__":
#     sciezka_pliku = input("Podaj sciezke pliku do grafiki z kodem: ")
#     skaner = SkanerQR(sciezka_pliku)
#     zdekodowana_wiadomosc = skaner.zdekoduj()
#     print(zdekodowana_wiadomosc)
#
