from stale import rodzaj_trybu, pojemnosc_numeryczna, pojemnosc_alfanumeryczna, pojemnosc_bajtowa, \
    alfanumeryczne_wartosci, slowa_kodowe, tabela_poteg, tabela_logarytmow, slownik_bitow_reszty, wzor_wyszukiwajacy, \
    slownik_wzorcow_wyrownania
from stale import wskaznik_liczby_znakow, wzor_wyrownania

class GeneratorQR:
    def __init__(self, dane_wejsciowe, poziom_korekcji):
        self.dane = dane_wejsciowe
        self.poziom_korekcji = poziom_korekcji
        self.ciag_bitow =""
        self.tryb = None
        self.wersja = None
        self.bajty_danych = []
        self.bloki_danych = []


    def wybierz_tryb_kodowania(self):
        if all(znak.isdigit() for znak in self.dane):
            self.tryb = rodzaj_trybu.Numeryczny.name
            self.ciag_bitow += rodzaj_trybu.Numeryczny.value
            return

        znaki_alfanumeryczne = list(alfanumeryczne_wartosci.keys())

        if all(znak in znaki_alfanumeryczne for znak in self.dane):
            self.tryb = rodzaj_trybu.Alfanumeryczny.name
            self.ciag_bitow += rodzaj_trybu.Alfanumeryczny.value
            return

        self.tryb = rodzaj_trybu.Bajtowy.name
        self.ciag_bitow += rodzaj_trybu.Bajtowy.value
        return

    def wybor_odpowiedniej_wersji(self):
        dlugosc = len(self.dane)
        if self.tryb == rodzaj_trybu.Numeryczny.name:
            tabela = pojemnosc_numeryczna
        elif self.tryb == rodzaj_trybu.Alfanumeryczny.name:
            tabela = pojemnosc_alfanumeryczna
        else:
            tabela = pojemnosc_bajtowa

        for wersja in range(1,4):
            limit = tabela[wersja, self.poziom_korekcji]
            if dlugosc <= limit:
                self.wersja = wersja
                print(f"Dobrana wersja: {wersja}")
                return

        raise ValueError("Dane są za długie, program nie obsłuży tak wielkich danych.")

    def dodaj_wskaznik_liczby_znakow(self):

        if self.tryb == rodzaj_trybu.Numeryczny.name:
            liczba_znakow = wskaznik_liczby_znakow["numeryczny"]
        elif self.tryb == rodzaj_trybu.Alfanumeryczny.name:
            liczba_znakow = wskaznik_liczby_znakow["alfanumeryczny"]
        else:
            liczba_znakow = wskaznik_liczby_znakow["bajtowy"]

        if 1<=self.wersja<=9:
            liczba_zn = liczba_znakow[0]
        elif 10<= self.wersja <=26:
            liczba_zn = liczba_znakow[1]
        else:
            liczba_zn = liczba_znakow[2]

        print(f"Wskaznik liczby znakow wynosi: {liczba_zn}")

        liczba = bin(len(self.dane))[2:].zfill(liczba_zn)
        self.ciag_bitow += liczba


    def zakoduj_dane(self):
        if self.tryb == rodzaj_trybu.Numeryczny.name:
            self._koduj_numerycznie()
        elif self.tryb == rodzaj_trybu.Alfanumeryczny.name:
            self._koduj_alfanumerycznie()
        else:
            self._koduj_bajtowo()

    def _koduj_numerycznie(self):

        for i in range(0,len(self.dane),3):
            grupa = self.dane[i:i+3]
            print(grupa)
            dlugosc_grupy = len(grupa)
            if dlugosc_grupy ==3:
                na_ile_bitow = 10
            elif dlugosc_grupy ==2:
                na_ile_bitow =7
            else:
                na_ile_bitow=4

            liczba = bin(int(grupa))[2:].zfill(na_ile_bitow)
            self.ciag_bitow += liczba
        print(f"Aktualny ciag bitow: {self.ciag_bitow}")

    def _koduj_alfanumerycznie(self):
        for i in range(0,len(self.dane),2):
            grupa = self.dane[i:i+2]
            dlugosc_grupy = len(grupa)
            if dlugosc_grupy == 2:
                wartosc1 = alfanumeryczne_wartosci[grupa[0]]
                wartosc2 = alfanumeryczne_wartosci[grupa[1]]
                wynik = (wartosc1*45)+wartosc2
                na_ile_bitow = 11
            else:
                wynik = alfanumeryczne_wartosci[grupa[0]]
                na_ile_bitow = 6

            liczba = bin(wynik)[2:].zfill(na_ile_bitow)
            self.ciag_bitow += liczba
        print(f"Aktualny ciag bitow: {self.ciag_bitow}")

    def _koduj_bajtowo(self):
        for znak in self.dane:
            liczba = bin(ord(znak))[2:].zfill(8)
            self.ciag_bitow += liczba
        print(f"Aktualny ciag bitow: {self.ciag_bitow}")

    def dodanie_paddingu(self):
        parametry = slowa_kodowe[(self.wersja, self.poziom_korekcji)]
        max_bajty = parametry["liczba_danych"]
        maksymalna_liczb_bitow = max_bajty * 8
        ile_brakuje_do_limitu = maksymalna_liczb_bitow - len(self.ciag_bitow)
        print(ile_brakuje_do_limitu)
        if ile_brakuje_do_limitu >= 4:
            self.ciag_bitow += "0"*4
        elif 0<ile_brakuje_do_limitu < 4:
            self.ciag_bitow += "0"* ile_brakuje_do_limitu

        while len(self.ciag_bitow) % 8 !=0:
            self.ciag_bitow += "0"

        czy_pierwszy_bajt = True

        while len(self.ciag_bitow) <maksymalna_liczb_bitow:
            if czy_pierwszy_bajt:
                self.ciag_bitow += "11101100"
            else:
                self.ciag_bitow += "00010001"

            czy_pierwszy_bajt = not czy_pierwszy_bajt
        print(f"Aktualny ciag bitow: {self.ciag_bitow}")

    def przygotowanie_danych(self):
        for i in range(0,len(self.ciag_bitow),8):
            bajt = self.ciag_bitow[i:i+8]
            liczba = int(bajt,2)
            self.bajty_danych.append(liczba)
        print(self.bajty_danych)

    def podzial_na_bloki(self):
        obecny_ind = 0

        parametry = slowa_kodowe[(self.wersja, self.poziom_korekcji)]
        for _ in range(parametry["bloki_w_grupie1"]):
            wielkosc_blokow = parametry["liczba_slow_danych_dla_blokow_grupy1"]
            blok = self.bajty_danych[obecny_ind:obecny_ind+wielkosc_blokow]
            self.bloki_danych.append(blok)
            obecny_ind += wielkosc_blokow

        for _ in range(parametry["bloki_w_grupie2"]):
            wielkosc_blokow = parametry["liczba_slow_danych_dla_blokow_grupy2"]
            blok = self.bajty_danych[obecny_ind:obecny_ind+wielkosc_blokow]
            self.bloki_danych.append(blok)
            obecny_ind += wielkosc_blokow

        print(self.bloki_danych)

    def mnozenie_gf(self,a,b):
        if a == 0 or b == 0:
            return 0
        suma_poteg = tabela_logarytmow[a] + tabela_logarytmow[b]
        suma_poteg = suma_poteg % 255
        return tabela_poteg[suma_poteg]

    def tworzenie_wielomianu_generujacego(self):
        generator = [1]
        parametry = slowa_kodowe[(self.wersja, self.poziom_korekcji)]
        liczba_iteracji = parametry["slowa_korekcyjne_na_blok"]
        for i in range(liczba_iteracji):
            nowa_lista1 = generator + [0]
            nowa_lista2 = [0]
            for liczba in generator:
                pomnozona = self.mnozenie_gf(liczba, tabela_poteg[i])
                nowa_lista2.append(pomnozona)
            wynik = []
            for j in range(0, len(nowa_lista2)):
                wynik.append(nowa_lista1[j] ^ nowa_lista2[j])
            generator = wynik
        return generator

    def oblicz_bajty_korekcyjne(self, blok_danych, generator):
        bajty_korekcyjne = len(generator)-1
        wiadomosc = blok_danych +(bajty_korekcyjne*[0])
        for i in range(len(blok_danych)):
            wyraz_wiodacy = wiadomosc[i]

            if wyraz_wiodacy ==0:
                continue

            for j in range(0,len(generator)):
                wynik = self.mnozenie_gf(wyraz_wiodacy,generator[j])
                wiadomosc[i +j] = wiadomosc[i+j]^wynik
        return wiadomosc[-bajty_korekcyjne:]

    def generuj_kod_korekcyjny(self):
        generator = self.tworzenie_wielomianu_generujacego()

        self.bloki_korekcyjne = []

        for blok in self.bloki_danych:
            reszta = self.oblicz_bajty_korekcyjne(blok, generator)

            self.bloki_korekcyjne.append(reszta)

    def zrob_przeplot(self):
        max_dlugosc_danych = max(len(blok) for blok in self.bloki_danych)
        max_dlugosc_korekcji = max(len(blok) for blok in self.bloki_korekcyjne)
        przetasowane_dane =[]
        przetasowane_korekcje = []

        for i in range(max_dlugosc_danych):
            for blok in self.bloki_danych:
                if i < len(blok):
                    przetasowane_dane.append(blok[i])

        for i in range(max_dlugosc_korekcji):
            for blok in self.bloki_korekcyjne:
                if i < len(blok):
                    przetasowane_korekcje.append(blok[i])

        ostateczna_wiadomosc = przetasowane_dane + przetasowane_korekcje
        return ostateczna_wiadomosc

    def podzial_na_bity(self):
        do_podzialu = self.zrob_przeplot()
        przekonwertowane_gotowe_dane = ""
        for liczba in do_podzialu:
            bit = bin(liczba)[2:].zfill(8)
            przekonwertowane_gotowe_dane += bit

        bity_reszty = slownik_bitow_reszty[self.wersja]
        przekonwertowane_gotowe_dane += "0"* bity_reszty
        return przekonwertowane_gotowe_dane

    def tworzenie_matrycy(self):
        rozmiar = ((self.wersja-1)*4)+21
        self.matryca = []
        for y in range(rozmiar):
            wiersz = []
            for x in range(rozmiar):
                wiersz.append(None)
            self.matryca.append(wiersz)

    def wklej_dany_wzor(self,wzor, start_x, start_y):
        wysokosc = len(wzor)
        szerokosc = len(wzor[0])
        for y in range(wysokosc):
            for x in range(szerokosc):
                self.matryca[start_y+y][start_x+x] = wzor[x][y]


    def matryca_tworzenie_wzorcow_wyszukiwania(self):
        wzor = wzor_wyszukiwajacy
        rozmiar = len(self.matryca)
        self.wklej_dany_wzor(wzor,0,0)
        self.wklej_dany_wzor(wzor,rozmiar -7,0)
        self.wklej_dany_wzor(wzor,0,rozmiar-7)

    def matryca_tworzenie_separatorow(self):
        rozmiar = len(self.matryca)
        for i in range(8):
            self.matryca[7][i] = 0
            self.matryca[i][7] = 0

            self.matryca[7][rozmiar-1-i] = 0
            self.matryca[i][rozmiar-8] = 0

            self.matryca[rozmiar-1-i][7] = 0
            self.matryca[rozmiar-8][i] = 0


    def matryca_tworzenie_wzorcow_wyrownania(self):
        if self.wersja ==1:
            return

        rozmiar = len(self.matryca)
        wspolrzedne = slownik_wzorcow_wyrownania[self.wersja]

        for srodek_x in wspolrzedne:
            for srodek_y in wspolrzedne:

                if srodek_x < 10 and srodek_y < 10:
                    continue
                if srodek_x > rozmiar - 10 and srodek_y<10:
                    continue
                if srodek_x < 10 and srodek_y > rozmiar - 10:
                    continue

                start_x = srodek_x -2
                start_y = srodek_y -2

                self.wklej_dany_wzor(wzor_wyrownania,start_x,start_y)


    def matryca_tworzenie_wzorcow_czasowych(self):
        rozmiar = len(self.matryca)
        pasek_poziomy_start_x = 8
        pasek_poziomy_start_y = 6
        pasek_pionowy_start_x = 6
        pasek_pionowy_start_y = 8
        dlugosc_paska = rozmiar - 16
        czarne_pole = True
        for i in range(dlugosc_paska):
            if czarne_pole:
                self.matryca[pasek_poziomy_start_y][pasek_poziomy_start_x+i] = 1
                self.matryca[pasek_pionowy_start_y+i][pasek_pionowy_start_x] = 1
            else:
                self.matryca[pasek_poziomy_start_y][pasek_poziomy_start_x+i] = 0
                self.matryca[pasek_pionowy_start_y+i][pasek_pionowy_start_x] = 0
            czarne_pole = True

    def matryca_tworzenie_ciemnego_modulu(self):
        self.matryca[(4*self.wersja)+9][8] = 1

    def bezpieczna_rezerwacja(self,y,x):
        if self.matryca[y][x] is None:
            self.matryca[y][x] = -1


    def matryca_tworzenie_miejsc_zarezerwowanych(self):
        rozmiar = len(self.matryca)
        for i in range(9):
            self.bezpieczna_rezerwacja(8,i)
            self.bezpieczna_rezerwacja(i,8)

        for i in range(8):
            self.bezpieczna_rezerwacja(8,rozmiar-1-i)
            self.bezpieczna_rezerwacja(rozmiar-1-i,8)

        if self.wersja >= 7:
            for i in range(3):
                for j in range(6):
                    self.bezpieczna_rezerwacja(j,rozmiar-9-i)
                    self.bezpieczna_rezerwacja(rozmiar-9-i,j)







daneWejsciowe = input("Podaj dane do zakodowania: ")
poziom_korekcji_bledow = input("Podaj jaki tryb korekcji bledow chcesz wykorzystac (L,M,Q,H): ")

kod_qr = GeneratorQR(daneWejsciowe, poziom_korekcji_bledow)
print(f"Stworzono obiekt generatora!")

kod_qr.wybierz_tryb_kodowania()

kod_qr.wybor_odpowiedniej_wersji()

kod_qr.dodaj_wskaznik_liczby_znakow()

kod_qr.zakoduj_dane()

kod_qr.dodanie_paddingu()

kod_qr.przygotowanie_danych()

kod_qr.podzial_na_bloki()

kod_qr.generuj_kod_korekcyjny()

kod_qr.zrob_przeplot()

kod_qr.podzial_na_bity()



