import copy
from PIL import Image

from matematyka import OperacjeNaCieleGalois
from stale import *
from wspolne import SzablonQR
from wspolne import MetodyMasek

class KoderDanych:
    def __init__(self, dane_wejsciowe, poziom_korekcji):
        self.dane = dane_wejsciowe
        self.poziom_korekcji = poziom_korekcji
        self.tryb = None
        self.wersja = None
        self.rozmiar = None
        self.ciag_bitow = ""
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
                    self.rozmiar = ((self.wersja-1)*4)+21
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
                dlugosc_grupy = len(grupa)
                if dlugosc_grupy ==3:
                    na_ile_bitow = 10
                elif dlugosc_grupy ==2:
                    na_ile_bitow =7
                else:
                    na_ile_bitow=4

                liczba = bin(int(grupa))[2:].zfill(na_ile_bitow)
                self.ciag_bitow += liczba

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

    def _koduj_bajtowo(self):
            for znak in self.dane:
                liczba = bin(ord(znak))[2:].zfill(8)
                self.ciag_bitow += liczba

    def dodanie_paddingu(self):
            parametry = slowa_kodowe[(self.wersja, self.poziom_korekcji)]
            max_bajty = parametry["liczba_danych"]
            maksymalna_liczb_bitow = max_bajty * 8
            ile_brakuje_do_limitu = maksymalna_liczb_bitow - len(self.ciag_bitow)
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

    def przygotowanie_danych(self):
            for i in range(0,len(self.ciag_bitow),8):
                bajt = self.ciag_bitow[i:i+8]
                liczba = int(bajt,2)
                self.bajty_danych.append(liczba)

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

    def tworzenie_wielomianu_generujacego(self):
            generator = [1]
            parametry = slowa_kodowe[(self.wersja, self.poziom_korekcji)]
            liczba_iteracji = parametry["slowa_korekcyjne_na_blok"]
            for i in range(liczba_iteracji):
                nowa_lista1 = generator + [0]
                nowa_lista2 = [0]
                for liczba in generator:
                    pomnozona = OperacjeNaCieleGalois.mnozenie_gf(liczba, tabela_poteg[i])
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
                    wynik = OperacjeNaCieleGalois.mnozenie_gf(wyraz_wiodacy,generator[j])
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

    def przygotuj_wszystkie_dane(self):
        self.wybierz_tryb_kodowania()
        self.wybor_odpowiedniej_wersji()
        self.dodaj_wskaznik_liczby_znakow()
        self.zakoduj_dane()
        self.dodanie_paddingu()
        self.przygotowanie_danych()
        self.podzial_na_bloki()
        self.generuj_kod_korekcyjny()
        return self.podzial_na_bity()

class MajsterMatrycy:
    def __init__(self, gotowe_bity, wersja, rozmiar, poziom_korekcji):
        self.gotowe_bity = gotowe_bity
        self.wersja = wersja
        self.rozmiar = rozmiar
        self.poziom_korekcji = poziom_korekcji

        generator = SzablonQR(self.rozmiar,self.wersja)
        self.matryca = generator.wygeneruj()

        self.strefa_danych = generator.strefa_danych
        self.zmaskowane_matryce = []

    def umiesc_bity_danych(self, ciag_bitow):
        generator = SzablonQR(self.rozmiar,self.wersja)
        generator.wygeneruj()
        trasa = generator.pobierz_trase_wezyka2()

        lista_bitow = list(ciag_bitow)

        for y,x in trasa:
            # if not lista_bitow:
            #     break

            bit = int(lista_bitow.pop(0))
            self.matryca[y][x] = bit

    def nadanie_masek_dla_kopii_matrycy(self):
        self.zmaskowane_matryce = []
        for nr_maski in range(8):
            kopia_matrycy = copy.deepcopy(self.matryca)
            for y,x in self.strefa_danych:
                if MetodyMasek.czy_odwrocic_bit(nr_maski, y,x):
                    kopia_matrycy[y][x] ^= 1
            self.zmaskowane_matryce.append(kopia_matrycy)
        return self.zmaskowane_matryce

    def obliczenie_punktow_karnych(self, dana_zmaskowana_matryca):
        punkty_n1 =0
        punkty_n2 =0
        punkty_n3 =0
        punkty_n4 =0
        rozmiar = len(dana_zmaskowana_matryca)

        for wiersz in dana_zmaskowana_matryca:
            licznik =1
            for x in range(1, rozmiar):
                if wiersz[x] == wiersz[x-1]:
                    licznik +=1
                else:
                    if licznik >=5:
                        punkty_n1 +=3 + (licznik -5)
                    licznik=1
            if licznik >=5:
                punkty_n1+=3 + (licznik-5)

        for x in range(rozmiar):
            licznik =1
            for y in range(1, rozmiar):
                if dana_zmaskowana_matryca[y][x] == dana_zmaskowana_matryca[y-1][x]:
                    licznik+=1
                else:
                    if licznik >= 5:
                        punkty_n1 += 3 + (licznik - 5)
                    licznik = 1
            if licznik >= 5:
                punkty_n1 += 3 + (licznik - 5)

        for y in range(rozmiar-1):
            for x in range(rozmiar-1):
                if dana_zmaskowana_matryca[y][x] == dana_zmaskowana_matryca[y][x+1] == dana_zmaskowana_matryca[y+1][x] == dana_zmaskowana_matryca[y+1][x+1]:
                    punkty_n2 += 3

        kombinacja_do_znalezienia1 = [0,0,0,0,1,0,1,1,1,0,1]
        kombinacja_do_znalezienia2 = [1,0,1,1,1,0,1,0,0,0,0]
        for wiersz in dana_zmaskowana_matryca:
            for x in range(rozmiar-10):
                wycinek = wiersz[x:x+11]
                if wycinek == kombinacja_do_znalezienia1 or wycinek ==kombinacja_do_znalezienia2:
                    punkty_n3 +=40
        for x in range(rozmiar):
            for y in range(rozmiar-10):
                wycinek = []
                for i in range(11):
                    wycinek.append(dana_zmaskowana_matryca[y+i][x])
                if wycinek == kombinacja_do_znalezienia1 or wycinek ==kombinacja_do_znalezienia2:
                    punkty_n3 +=40

        calkowita_liczba_pixeli = rozmiar*rozmiar
        calkowita_liczba_czarnych_pixeli = 0
        for wiersz in dana_zmaskowana_matryca:
            for pixel in wiersz:
                if pixel==1:
                    calkowita_liczba_czarnych_pixeli+=1
        procent = (calkowita_liczba_czarnych_pixeli/calkowita_liczba_pixeli)*100
        odchylenie = abs(50-procent)
        punkty_n4 += (odchylenie//5)*10

        return punkty_n1 + punkty_n2 + punkty_n3 + punkty_n4

    def porownanie_punktow_karnych(self):
        self.nadanie_masek_dla_kopii_matrycy()
        punkty = {}

        for nr_maski, matryca in enumerate(self.zmaskowane_matryce):
            self.uzupelnienie_zarezerwowanych_miejsc(matryca, nr_maski)

            punkty[nr_maski] = self.obliczenie_punktow_karnych(matryca)

        najmniej_punktow = min(punkty, key=punkty.get)

        self.matryca = self.zmaskowane_matryce[najmniej_punktow]

    def wybranie_bitow_do_uzupelnienia(self, poziom_korekcji, maska):
        szukany_ciag = (poziom_korekcji, maska)
        return ciag_bitow_dla_maski_oraz_poziomu_korekcji_bledow[szukany_ciag]

    def bezpieczne_uzupelnienie_rezerwacji(self,matryca,y,x,bit):
        if matryca[y][x] == -1:
            matryca[y][x] = bit
            return True
        return False

    def uzupelnienie_zarezerwowanych_miejsc(self,matryca, maska):
        dane_do_wstawienia = self.wybranie_bitow_do_uzupelnienia(self.poziom_korekcji, maska)
        inddeks =0
        rozmiar = len(matryca)
        for i in range(9):
            if self.bezpieczne_uzupelnienie_rezerwacji(matryca,8,i,int(dane_do_wstawienia[inddeks])):
                inddeks +=1
        for i in range(7,-1,-1):
            if self.bezpieczne_uzupelnienie_rezerwacji(matryca,i, 8, int(dane_do_wstawienia[inddeks])):
                inddeks += 1
        inddeks = 0
        for i in range(7):
            if self.bezpieczne_uzupelnienie_rezerwacji(matryca,rozmiar-1-i,8,int(dane_do_wstawienia[inddeks])):
                inddeks +=1
        for i in range(rozmiar-8,rozmiar,1):
            if self.bezpieczne_uzupelnienie_rezerwacji(matryca, 8,i,int(dane_do_wstawienia[inddeks])):
                inddeks +=1
        inddeks=0

        if self.wersja >= 7:
            dane_dla_wyzszych_wersji_do_wstawienia = ciag_bitow_dla_danej_wersji[self.wersja]

            for i in range(6):
                for j in range(3):
                    if self.bezpieczne_uzupelnienie_rezerwacji(matryca,rozmiar-11+j,i,int(dane_dla_wyzszych_wersji_do_wstawienia[inddeks])):
                        inddeks+=1
            inddeks=0
            for i in range(6):
                for j in range(3):
                    if self.bezpieczne_uzupelnienie_rezerwacji(matryca, i, rozmiar-11+j,int(dane_dla_wyzszych_wersji_do_wstawienia[inddeks])):
                        inddeks+=1

    def dodaj_strefe_ochronna(self):
        stary_rozmiar = self.rozmiar
        nowa_szerokosc = stary_rozmiar + 8
        nowa_matryca = []
        for _ in range(4):
            nowa_matryca.append([0]* nowa_szerokosc)

        for wiersz in self.matryca:
            nowy_wiersz = [0,0,0,0] + wiersz + [0,0,0,0]
            nowa_matryca.append(nowy_wiersz)

        for _ in range(4):
            nowa_matryca.append([4]* nowa_szerokosc)

        self.matryca = nowa_matryca

    def wygeneruj_obraz(self, nazwa_pliku, skala):
        rozmiar = len(self.matryca)
        obraz = Image.new("RGB",(rozmiar,rozmiar), "white")
        pixele = obraz.load()

        for y in range(rozmiar):
            for x in range(rozmiar):
                if self.matryca[y][x] ==1:
                    pixele[x,y] = (0,0,0)
                else:
                    pixele[x,y] = (255,255,255)

        nowy_rozmiar = rozmiar * skala
        obraz = obraz.resize((nowy_rozmiar,nowy_rozmiar), Image.Resampling.NEAREST)

        obraz.save(nazwa_pliku)
        print(f"Kod QR powstal pod nazwa: {nazwa_pliku}")

    def zbuduj_pelna_matryce(self):
        self.umiesc_bity_danych(self.gotowe_bity)
        self.porownanie_punktow_karnych()
        self.dodaj_strefe_ochronna()

class GeneratorQR:
    def __init__(self, dane_wejsciowe, poziom_korekcji):
        self.koder = KoderDanych(dane_wejsciowe, poziom_korekcji)

    def wygeneruj(self,nazwa):
        gotowe_bity = self.koder.przygotuj_wszystkie_dane()
        wersja = self.koder.wersja
        rozmiar = self.koder.rozmiar

        self.budowniczy = MajsterMatrycy(gotowe_bity, wersja,rozmiar, self.koder.poziom_korekcji)

        self.budowniczy.zbuduj_pelna_matryce()
        self.budowniczy.wygeneruj_obraz(nazwa,10)




# if __name__ == "__main__":
#     dane_wejsciowe = input("Podaj dane do zakodowania: ")
#     poziom_korekcji_bledow = input("Podaj jaki tryb korekcji bledow chcesz wykorzystac (L,M,Q,H): ")
#     nazwa_pliku = input("Podaj nazwe pliku z kodem QR: ")
#     kodQR = GeneratorQR(dane_wejsciowe, poziom_korekcji_bledow)
#     kodQR.wygeneruj(nazwa_pliku)