from enum import Enum

class rodzaj_trybu(Enum):
    Numeryczny = "0001"
    Alfanumeryczny ="0010"
    Bajtowy = "0100"

#kolejno wersje od 1 do 9, od 10 do 26, od 27 do 40
wskaznik_liczby_znakow = {
    "alfanumeryczny":(9, 11, 13), #alfanumeryczny
    "numeryczny":(10, 12, 14), #numeryczny
    "bajtowy":(8, 16, 16) #bajtowy
}

#(wersja,rodzaj_korekcji): pojemnosc_znaków
pojemnosc_alfanumeryczna ={
    (1,"L"):25, (2,"L"):47, (3,"L"):77 , (4,"L"):114,
    (1,"M"):20, (2,"M"):38, (3,"M"):61 , (4,"M"):90,
    (1,"Q"):16, (2,"Q"):29, (3,"Q"):47 , (4,"Q"):67,
    (1,"H"):10, (2,"H"):20, (3,"H"):35 , (4,"H"):50,
}

pojemnosc_numeryczna ={
    (1, "L"): 41, (2, "L"): 77, (3, "L"): 127, (4, "L"): 187,
    (1, "M"): 34, (2, "M"): 63, (3, "M"): 101, (4, "M"): 149,
    (1, "Q"): 27, (2, "Q"): 48, (3, "Q"): 77, (4, "Q"): 111,
    (1, "H"): 17, (2, "H"): 34, (3, "H"): 58, (4, "H"): 82,
}

pojemnosc_bajtowa={
    (1, "L"): 17, (2, "L"): 32, (3, "L"): 53, (4, "L"): 78,
    (1, "M"): 14, (2, "M"): 26, (3, "M"): 42, (4, "M"): 62,
    (1, "Q"): 11, (2, "Q"): 20, (3, "Q"): 32, (4, "Q"): 46,
    (1, "H"): 7, (2, "H"): 14, (3, "H"): 24, (4, "H"): 34,
}

#tablica alfanumerycznych wartosci dla danego znaku
alfanumeryczne_wartosci ={
"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6,
"7":7, "8":8, "9":9, "A":10, "B":11, "C":12, "D":13,
"E":14, "F":15, "G":16, "H":17, "I":18, "J":19, "K":20,
"L":21, "M":22, "N":23, "O":24, "P":25, "Q":26, "R":27,
"T":29, "U":30, "V":31, "W":32, "X":33, "Y":34, "Z":35, " ":36, #spacja
"$":37, "%":38, "*":39, "+":40, "-":41, ".":42, "/":43, ":":44
}

#tablica slow kodowych (bajtow danych) wymaganych dla danego kodu qr
slowa_kodowe = {
    (1, 'L'): {'liczba_danych': 19, 'slowa_korekcyjne_na_blok': 7, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 19, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (1, 'M'): {'liczba_danych': 16, 'slowa_korekcyjne_na_blok': 10, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 16, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (1, 'Q'): {'liczba_danych': 13, 'slowa_korekcyjne_na_blok': 13, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 13, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (1, 'H'): {'liczba_danych': 9, 'slowa_korekcyjne_na_blok': 17, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 9, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},

    (2, 'L'): {'liczba_danych': 34, 'slowa_korekcyjne_na_blok': 10, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 34, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (2, 'M'): {'liczba_danych': 28, 'slowa_korekcyjne_na_blok': 16, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 28, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (2, 'Q'): {'liczba_danych': 22, 'slowa_korekcyjne_na_blok': 22, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 22, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (2, 'H'): {'liczba_danych': 16, 'slowa_korekcyjne_na_blok': 28, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 16, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},

    (3, 'L'): {'liczba_danych': 55, 'slowa_korekcyjne_na_blok': 15, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 55, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (3, 'M'): {'liczba_danych': 44, 'slowa_korekcyjne_na_blok': 26, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 44, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (3, 'Q'): {'liczba_danych': 34, 'slowa_korekcyjne_na_blok': 18, 'bloki_w_grupie1': 2, 'liczba_slow_danych_dla_blokow_grupy1': 17, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (3, 'H'): {'liczba_danych': 26, 'slowa_korekcyjne_na_blok': 22, 'bloki_w_grupie1': 2, 'liczba_slow_danych_dla_blokow_grupy1': 13, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},

    (4, 'L'): {'liczba_danych': 80, 'slowa_korekcyjne_na_blok': 20, 'bloki_w_grupie1': 1, 'liczba_slow_danych_dla_blokow_grupy1': 80, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (4, 'M'): {'liczba_danych': 64, 'slowa_korekcyjne_na_blok': 18, 'bloki_w_grupie1': 2, 'liczba_slow_danych_dla_blokow_grupy1': 32, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (4, 'Q'): {'liczba_danych': 48, 'slowa_korekcyjne_na_blok': 26, 'bloki_w_grupie1': 2, 'liczba_slow_danych_dla_blokow_grupy1': 24, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
    (4, 'H'): {'liczba_danych': 36, 'slowa_korekcyjne_na_blok': 16, 'bloki_w_grupie1': 4, 'liczba_slow_danych_dla_blokow_grupy1': 9, 'bloki_w_grupie2': 0, 'liczba_slow_danych_dla_blokow_grupy2': 0},
}


tabela_logarytmow = [0] * 256
tabela_poteg = [0] * 256

wartosc = 1

for potega in range(255):
    tabela_poteg[potega] = wartosc
    tabela_logarytmow[wartosc] = potega

    wartosc = wartosc * 2

    if wartosc >= 256:
        wartosc = wartosc ^ 285

tabela_poteg[255] = tabela_logarytmow[0]


#bity reszty
#wersjaQR: wymagane bity reszty
slownik_bitow_reszty = {
    1:0,
    2:7, 3:7, 4:7, 5:7, 6:7,
    7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0,
    14:3, 15:3, 16:3, 17:3, 18:3, 19:3, 20:3,
    21:4, 22:4, 23:4, 24:4, 25:4, 26:4, 27:4,
    28:3, 29:3, 30:3, 31:3, 32:3, 33:3, 34:3,
    35:0, 36:0, 37:0, 38:0, 39:0, 40:0
}

wzor_wyszukiwajacy = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1]
]

#wersja kodu : lista wspolrzednych, gdzie nalezy umiescic wzorzec wyrownania
slownik_wzorcow_wyrownania = {
    1:[],
    2:[6,18],
    3:[6,22],
    4:[6,26],
    5:[6,30],
    6:[6,34],
    7:[6,22,38],
    8:[6,24,42],
    9:[6,26,46],
    10:[6,28,50],
    11:[6,30,54],
    12:[6,32,58],
    13:[6,34,62],
    14:[6,26,46,66],
    15:[6,26,48,70],
    16:[6,26,50,74],
    17:[6,30,54,78],
    18:[6,30,56,82],
    19:[6,30,58,86],
    20:[6,34,62,90],
    21:[6,28,50,72,94],
    22:[6,26,50,74,98],
    23:[6,30,54,78,102],
    24:[6,28,54,80,106],
    25:[6,32,58,84,110],
    26:[6,30,58,86,114],
    27:[6,34,62,90,118],
    28:[6,26,50,74,98,122],
    29:[6,30,54,78,102,126],
    30:[6,26,52,78,104,130],
    31:[6,30,56,82,108,134],
    32:[6,34,60,86,112,138],
    33:[6,30,58,86,114,142],
    34:[6,34,62,90,118,146],
    35:[6,30,54,78,102,126,150],
    36:[6,24,50,76,102,128,154],
    37:[6,28,54,80,106,132,158],
    38:[6,32,58,84,110,138,166],
    39:[6,26,54,82,110,138,166],
    40:[6,30,58,86,114,142,170]
}

wzor_wyrownania = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

ciag_bitow_dla_danej_wersji = {
7:"000111110010010100",
8:"001000010110111100",
9:"001001101010011001",
10:"001010010011010011",
11:"001011101111110110",
12:"001100011101100010",
13:"001101100001000111",
14:"001110011000001101",
15:"001111100100101000",
16:"010000101101111000",
17:"010001010001011101",
18:"010010101000010111",
19:"010011010100110010",
20:"010100100110100110",
21:"010101011010000011",
22:"010110100011001001",
23:"010111011111101100",
24:"011001000111100001",
26:"011010111110101011",
27:"011011000010001110",
28:"011100110000011010",
29:"011101001100111111",
30:"011110110101110101",
31:"011111001001010000",
32:"100000100111010101",
33:"100001011011110000",
34:"100010100010111010",
35:"100011011110011111",
36:"100100101100001011",
37:"100101010000101110",
38:"100110101001100100",
39:"100111010101000001",
40:"101000110001101001"
}

ciag_bitow_dla_maski_oraz_poziomu_korekcji_bledow = {
    ("L",0):"111011111000100",
    ("L",1):"111001011110011",
    ("L",2):"111110110101010",
    ("L",3):"111100010011101",
    ("L",4):"110011000101111",
    ("L",5):"110001100011000",
    ("L",6):"110110001000001",
    ("L",7):"110100101110110",
    ("M",0):"101010000010010",
    ("M",1):"101000100100101",
    ("M",2):"101111001111100",
    ("M",3):"101101101001011",
    ("M",4):"100010111111001",
    ("M",5):"100000011001110",
    ("M",6):"100111110010111",
    ("M",7):"100101010100000",
    ("Q",0):"011010101011111",
    ("Q",1):"011000001101000",
    ("Q",2):"011111100110001",
    ("Q",3):"011101000000110",
    ("Q",4):"010010010110100",
    ("Q",5):"010000110000011",
    ("Q",6):"010111011011010",
    ("Q",7):"010101111101101",
    ("H",0):"001011010001001",
    ("H",1):"001001110111110",
    ("H",2):"001110011100111",
    ("H",3):"001100111010000",
    ("H",4):"000011101100010",
    ("H",5):"000001001010101",
    ("H",6):"000110100001100",
    ("H",7):"000100000111011"
}