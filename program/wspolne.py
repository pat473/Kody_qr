from program.stale import *

class SzablonQR:
    def __init__(self,rozmiar, wersja,):
        self.rozmiar = rozmiar
        self.wersja = wersja
        self.szablon = []
        self.tworzenie_pustej_matrycy()
        self.strefa_danych = []

    def tworzenie_pustej_matrycy(self):
        for y in range(self.rozmiar):
            wiersz = []
            for x in range(self.rozmiar):
                wiersz.append(None)
            self.szablon.append(wiersz)

    def wygeneruj(self):
        self.tworzenie_wzorcow_wyszukiwania()
        self.tworzenie_separatorow()
        self.tworzenie_wzorcow_wyrownania()
        self.tworzenie_wzorcow_czasowych()
        self.tworzenie_ciemnego_modulu()
        self.tworzenie_miejsc_zarezerwowanych()
        self.zapamietanie_strefy_danych()

        return self.szablon

    def _wklej_dany_wzor(self,wzor, start_x, start_y):
        wysokosc = len(wzor)
        szerokosc = len(wzor[0])
        for y in range(wysokosc):
            for x in range(szerokosc):
                self.szablon[start_y+y][start_x+x] = wzor[y][x]

    def tworzenie_wzorcow_wyszukiwania(self):
        wzor = wzor_wyszukiwajacy
        self._wklej_dany_wzor(wzor,0,0)
        self._wklej_dany_wzor(wzor,self.rozmiar -7,0)
        self._wklej_dany_wzor(wzor,0,self.rozmiar-7)

    def tworzenie_separatorow(self):
        for i in range(8):
            self.szablon[7][i] = 0
            self.szablon[i][7] = 0

            self.szablon[7][self.rozmiar-1-i] = 0
            self.szablon[i][self.rozmiar-8] = 0

            self.szablon[self.rozmiar-1-i][7] = 0
            self.szablon[self.rozmiar-8][i] = 0

    def tworzenie_wzorcow_wyrownania(self):
        if self.wersja ==1:
            return

        wspolrzedne = slownik_wzorcow_wyrownania[self.wersja]

        for srodek_x in wspolrzedne:
            for srodek_y in wspolrzedne:

                if srodek_x < 10 and srodek_y < 10:
                    continue
                if srodek_x > self.rozmiar - 10 and srodek_y<10:
                    continue
                if srodek_x < 10 and srodek_y > self.rozmiar - 10:
                    continue

                start_x = srodek_x -2
                start_y = srodek_y -2

                self._wklej_dany_wzor(wzor_wyrownania,start_x,start_y)

    def tworzenie_wzorcow_czasowych(self):
        pasek_poziomy_start_x = 8
        pasek_poziomy_start_y = 6
        pasek_pionowy_start_x = 6
        pasek_pionowy_start_y = 8
        dlugosc_paska = self.rozmiar - 16
        czarne_pole = True
        for i in range(dlugosc_paska):
            if czarne_pole:
                self.szablon[pasek_poziomy_start_y][pasek_poziomy_start_x+i] = 1
                self.szablon[pasek_pionowy_start_y+i][pasek_pionowy_start_x] = 1
            else:
                self.szablon[pasek_poziomy_start_y][pasek_poziomy_start_x+i] = 0
                self.szablon[pasek_pionowy_start_y+i][pasek_pionowy_start_x] = 0
            czarne_pole = not czarne_pole

    def tworzenie_ciemnego_modulu(self):
        self.szablon[(4*self.wersja)+9][8] = 1

    def bezpieczna_rezerwacja(self,y,x):
        if self.szablon[y][x] is None:
            self.szablon[y][x] = -1

    def tworzenie_miejsc_zarezerwowanych(self):
        for i in range(9):
            self.bezpieczna_rezerwacja(8,i)
            self.bezpieczna_rezerwacja(i,8)

        for i in range(8):
            self.bezpieczna_rezerwacja(8,self.rozmiar-1-i)
            self.bezpieczna_rezerwacja(self.rozmiar-1-i,8)

        if self.wersja >= 7:
            for i in range(3):
                for j in range(6):
                    self.bezpieczna_rezerwacja(j,self.rozmiar-9-i)
                    self.bezpieczna_rezerwacja(self.rozmiar-9-i,j)

    def zapamietanie_strefy_danych(self):
        for y in range(len(self.szablon)):
            for x in range(len(self.szablon)):
                if self.szablon[y][x] is None:
                    self.strefa_danych.append((y,x))

    def pobierz_trase_wezyka(self, czy_w_gore, indeks_x):
        trasa_odcinka = []
        if czy_w_gore:
            for y in range(self.rozmiar-1,-1,-1):
                for i in range(2):
                    aktualny_x = indeks_x - i
                    if self.szablon[y][aktualny_x] is None:
                        trasa_odcinka.append((y, aktualny_x))
        else:
            for y in range(0, self.rozmiar,1):
                for i in range(2):
                    aktualny_x = indeks_x - i
                    if self.szablon[y][aktualny_x] is None:
                        trasa_odcinka.append((y,aktualny_x))

        return trasa_odcinka, not czy_w_gore

    def pobierz_trase_wezyka2(self):
        indeks_x = self.rozmiar-1
        czy_w_gore = True
        pelna_trasa = []
        while indeks_x >=0:
            if indeks_x ==6:
                indeks_x -= 1

            nowy_odcinek, czy_w_gore = self.pobierz_trase_wezyka(czy_w_gore,indeks_x)
            pelna_trasa.extend(nowy_odcinek)

            indeks_x -=2
        return pelna_trasa

class MetodyMasek:
    @staticmethod
    def czy_odwrocic_bit(nr_maski, y, x):
        if nr_maski == 0:
            return (y + x) % 2 == 0
        elif nr_maski == 1:
            return y % 2 == 0
        elif nr_maski == 2:
            return x % 3 == 0
        elif nr_maski == 3:
            return (y + x) % 3 == 0
        elif nr_maski == 4:
            return ((y // 2) + (x // 3)) % 2 == 0
        elif nr_maski == 5:
            return ((y * x) % 2) + ((y * x) % 3) == 0
        elif nr_maski == 6:
            return (((y * x) % 2) + ((y * x) % 3)) % 2 == 0
        elif nr_maski == 7:
            return (((y + x) % 2) + ((y * x) % 3)) % 2 == 0

class Przygotowanie:
    @staticmethod
    def pobierz_parametry_qr(wersja, korekcja, *wybrane_klucze):
        parametry = slowa_kodowe[wersja, korekcja]
        wynik = []
        for klucz in wybrane_klucze:
            wynik.append(parametry[klucz])
        return wynik



