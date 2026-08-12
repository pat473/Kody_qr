import pytest

@pytest.fixture
def pusta_matryca_21x21():
    """
    Fixtura dostarczająca czystą matrycę o rozmiarze Wersji 1.
    Przydatna do testowania nakładania masek i wzorców wyszukiwania.
    """
    rozmiar = 21
    # Generuje listę 21 list, z których każda ma 21 zer
    return [[0 for _ in range(rozmiar)] for _ in range(rozmiar)]

@pytest.fixture
def krotki_ciag_bitow():
    """
    Fixtura dostarczająca przykładowy, surowy strumień bitów
    (np. reprezentujący literę 'H' i literę 'E' w ASCII)
    """
    return [0, 1, 0, 0, 1, 0, 0, 0,  # 'H' (72)
            0, 1, 0, 0, 0, 1, 0, 1]  # 'E' (69)