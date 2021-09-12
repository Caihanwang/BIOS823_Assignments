#Problem 6
import numpy as np 
def diff_square():
    '''build a list which contains natural numbers from 1 to 100'''
    x = np.arange(101)

    '''Calculate sum of squares and square of sum'''
    y1 = sum(x)**2
    y2 = sum(list(map(lambda x:x**2, x)))

    '''Calculate the difference'''
    print(y1 - y2)

if __name__ == '__main__':
    diff_square()

#Problem 56

import numpy as np

def digit_sum():
    results = []

    for a in range(100):
        for b in range(100):
            c = a**b
            d = sum(list(map(int,list(str(c)))))
            results.append(d)

    result = max(results)

    print(result)

if __name__ == '__main__':
    digit_sum()

#Problem 119

def power_sum():
    results = []

    for i in range(100):
        for j in range(100):
            if i**j > 10:
                if sum(list(map(int,list(str(i**j))))) == i:
                    results.append(i**j)

    print(sorted(results)[29])


if __name__ == '__main__':
    power_sum()