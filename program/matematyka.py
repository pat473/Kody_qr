from program.stale import tabela_logarytmow, tabela_poteg

# Wszystkie metody gf sa przeprowadzane w CG(256)
class OperacjeNaCieleGalois:
    @staticmethod
    def mnozenie_gf(a,b):
            if a == 0 or b == 0:
                return 0
            suma_poteg = tabela_logarytmow[a] + tabela_logarytmow[b]
            suma_poteg = suma_poteg % 255
            return tabela_poteg[suma_poteg]

    @staticmethod
    def dzielenie_gf(a,b):
        if b ==0:
            raise ZeroDivisionError("Dzielenie przez zero w Ciele Galois")
        if a ==0:
            return 0
        roznica_poteg = tabela_logarytmow[a] - tabela_logarytmow[b]
        roznica_poteg = ( roznica_poteg+255)%255
        return tabela_poteg[roznica_poteg]

    @staticmethod
    def mnozenie_wielomianow_gf(w1,w2):
        rozmiar_wyniku = len(w1) + len(w2) -1
        wynik = [0] * rozmiar_wyniku
        for i in range(len(w1)):
            for j in range(len(w2)):
                wynik[i+j] ^= OperacjeNaCieleGalois.mnozenie_gf(w1[i],w2[j])
        return wynik

    @staticmethod
    def pochodna_wielomianu_gf(wielomian):
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

class MatematykaInna:
    @staticmethod
    def podstawienie_x_do_wielomianu(x,wielomian):
        wynik = 0
        for i in wielomian:
            wynik = OperacjeNaCieleGalois.mnozenie_gf(wynik,x)
            wynik = wynik ^ i
        return wynik

    @staticmethod
    def zamiana_na_bajty(ciag_danych):
        bajty_dziesietne = []
        for i in range(0,len(ciag_danych),8):
            bajt = ciag_danych[i:i+8]
            if len(bajt)==8:
                liczba = int(bajt,2)
                bajty_dziesietne.append(liczba)
        return bajty_dziesietne

    @staticmethod
    def zamiana_na_bity(dane):
        wynik = ""
        for bajt in dane:
            wynik += f"{bajt:08b}"
        return wynik