from sympy import *

def expanding(a, b):
    '''this function is to generate an arbitrary large expansion of a mathematical expression'''
    # a is mathmetical expression, for example pi and E
    # b is the number of digits we need, b must be integer and larger than 0
    if b <= 0:
        return ValueError("b must be larger than 0")
    if not isinstance(b, int):
        return ValueError("b must be an integer")
    
    # Using evalf function to expand a to (b+1) digits
    c = a.evalf(b+1)

    # Split first b digits 
    d = str(c)[0:b+1]
    return d # type of d is string



def is_prime(x):
    '''this function is to check whether the number x is a prime or not'''
    # Firstly, we need to check whether the input number is a integer, because only integer can be a prime
    if isinstance(x, int):
        if x <= 1:
            return ValueError("Input number must be greater than 1")
        # 2 is the smallest and special prime, we need to check it in advance
        if x == 2:
            return "It is a prime"

        # If the number is an even number, it cannot be a prime
        elif x % 2 == 0:
            return "It isn't a prime"

        # We check whether each two number from 3 to sqrt(x) is the factor of x
        for i in range(3, int(x**0.5+1), 2):
            # If it is factor of x, x will not be a prime
            if x % i == 0:
                return "It isn't a prime"
        return "It is a prime"

    # If the number is not a integer, it shouldn't be considered   
    else:
        return ValueError("Input number must be an integer")


def sliding_window(a, b, c):
    '''This function is to generate sliding windows of a specified width from a long iterable'''

    # a is a long iterable and the type of a is string
    if not isinstance(a, str):
        return ValueError("a must be a string")
    
    # b is the location
    # c is the width of window
    return a[b: b + c] # The type of the output is string


def find_prime(thenumber, width):
    '''This function is to find the first prime of specific width for the iterable'''

    # Set an empty list to store the prime number
    result = []

    # Set index
    digits = width
    i = 0

    while result == []:
        
        # generate a expansion of thenumber
        x = expanding(thenumber, digits)

        # check whether the number(y) split from x is a prime or not 
        y = sliding_window(x, i, width)
        
        # if y is start from 0, we should not consider it
        if y[0] != '0':
            # After we found the first prime which meet our request, we will end the loop
             if is_prime(eval(y)) == "It is a prime":
                 result.append(y)
        
        digits += 1
        i += 1

    return eval(result[0])

                    
   
      
            

if __name__ == '__main__':

    answer = find_prime(17*pi,10)

    print("The first 10-digit prime in the decimal expansion of 17π is", answer)
    
    