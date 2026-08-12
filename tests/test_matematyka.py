import pytest

from program.matematyka import MatematykaInna
from program.matematyka import OperacjeNaCieleGalois

@pytest.mark.parametrize("a,b,oczekiwany_wynik",[
    (15,81,24),
    (4,4,16),
    (25,10,250),
    (25,11,227),
])
def test_mnozenie_gf(a,b, oczekiwany_wynik):
    assert OperacjeNaCieleGalois.mnozenie_gf(a,b) ==oczekiwany_wynik, "Mnozenie w gf zwraca nieprawidlowe wartosci. "

@pytest.mark.parametrize("a, b, oczekiwany_wynik", [
    (16, 4, 4),
    (15, 15, 1),
    (0, 4, 0),
    (255, 254, 127),
])
def test_dzielenie_gf_poprawne(a, b, oczekiwany_wynik):
    assert OperacjeNaCieleGalois.dzielenie_gf(a, b) == oczekiwany_wynik, "Dzielenie w GF zwróciło zły wynik."

def test_dzielenie_gf_przez_zero():
    with pytest.raises(ZeroDivisionError):
        OperacjeNaCieleGalois.dzielenie_gf(4, 0)


@pytest.mark.parametrize("a,b,oczekiwany_wynik", [
    ([1,0,1],[1,1],[1,1,1,1]),  # Zwykle mnozenie wielomianow
    ([0],[4,3,2,1,5,6,7,8,9],[0] * 9), # Mnozenie wielomianu przez zero
    ([5,4,0,0,0,0],[2,3,0,0,0,0,0],[10,7,12,0,0,0,0,0,0,0,0,0]), # Mnozenie z wykorzystaniem wlasciwosci ciala Galois
])
def test_mnozenie_wielomianow_gf(a,b,oczekiwany_wynik):
    assert OperacjeNaCieleGalois.mnozenie_wielomianow_gf(a,b) == oczekiwany_wynik, "Mnozenie wielomianow dziala nieprawidlowo. "

@pytest.mark.parametrize("wielomian,oczekiwany_wynik", [
    ([5,5,5,5],[5,0,5]), # Dodawanie odbywa sie w CG przez operacje XOR
    ([1],[0]), # Pochodna rowna zero
    ([3,2],[3]) # Pochodna niezerowa
])
def test_pochodna_wielomianu_gf(wielomian,oczekiwany_wynik):
    assert OperacjeNaCieleGalois.pochodna_wielomianu_gf(wielomian) == oczekiwany_wynik, "Pochodna wielomianu jest blednie obliczona. "

@pytest.mark.parametrize("x, wielomian, oczekiwany_wynik", [
    (0,[5,5,5,5,5,5],5), # Podstawienie 0
    (253,[1,0,9,5,4],17), # Podstawienie konkretnej wartosci
    (-3,[1,0,9,5,4],17), # Podstawienie tej samej wartosci w swiecie mod 256
    (2,[1,0,0,100],108), # Podstawienie innej wartosci
])
def test_podstawienie_x_do_wielomianu(x, wielomian, oczekiwany_wynik):
    assert MatematykaInna.podstawienie_x_do_wielomianu(x, wielomian) == oczekiwany_wynik, "Podstawianie wartosci przebiega blednie. "