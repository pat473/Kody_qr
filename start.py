from kodowanie import GeneratorQR
from dekodowanie import SkanerQR

def menu_glowne():
    print("MENU GLOWNE")
    print("1. Chce kodowac. ")
    print("2. Chce dekodowac. ")
    print("3. Wyjscie. ")
    wybor = input("Wybieram opcje: ")
    match wybor:
        case "1":
            dane_wejsciowe = input("Podaj dane do zakodowania: ")
            poziom_korekcji_bledow = input("Podaj jaki tryb korekcji bledow chcesz wykorzystac (L,M,Q,H): ")
            nazwa = input("Podaj nazwe pliku z kodem QR: ")
            kodQR = GeneratorQR(dane_wejsciowe, poziom_korekcji_bledow)
            kodQR.wygeneruj(nazwa)
        case "2":
            sciezka = input("Podaj sciezke do grafiki z kodem QR: ")
            skaner = SkanerQR(sciezka)
            zdekodowana_wiadomosc = skaner.zdekoduj()
            print(f"Zdekodowana wiadomosc: {zdekodowana_wiadomosc}")
        case "3":
            print("Zamykanie programu.")
            exit()
        case _:
            print("Wybrano nieprawidlowy znak.")


if __name__ == "__main__":
    while True:
        menu_glowne()
