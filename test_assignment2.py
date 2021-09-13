from assignment2 import *
from sympy import *


def test_expanding():
    a = pi
    b = 8
    assert expanding(a, b) == "3.1415926"

    a = E
    b = 5
    assert expanding(a, b) == "2.7182"

def test_is_prime():
    n = 3
    assert is_prime(n) == "It is a prime"

    n = 88
    assert is_prime(n) == "It isn't a prime"

    n = 87
    assert is_prime(n) == "It isn't a prime"

def test_sliding_window():
    a = "3.1312413524"
    b = 0
    c = 4
    assert sliding_window(a, b, c) == "3.13"

    a = "3.1312413524"
    b = 1
    c = 3
    assert sliding_window(a, b, c) == ".13"

def test_find_prime():
    thenumber = E
    width = 10
    assert find_prime(thenumber, width) == 7427466391

    thenumber = pi
    width = 5
    assert find_prime(thenumber, width) == 14159

    thenumber = pi
    width = 4
    assert find_prime(thenumber, width) == 4159


if __name__ == '__main__':
    test_expanding()
    test_is_prime()
    test_sliding_window()
    test_find_prime()
    print("pass all the tests")