---
title: "BIOS 823 Homework 2: Number theory and a Google recruitment puzzle"
layout: post
date: 2021-09-12 22:48
# image: /assets/images/markdown.jpg
headerImage: false
# tag:
# - markdown
# - components
# - extra
category: blog
author: Caihan Wang
description: 823 HW2
---

# Number theory and a Google recruitment puzzle

Find the first 10-digit prime in the decimal expansion of 17π. 

The first 5 digits in the decimal expansion of π are 14159. The first 4-digit prime in the decimal expansion of π are 4159. You are asked to find the first 10-digit prime in the decimal expansion of 17π. First solve sub-problems (divide and conquer):

- Write a function to generate an arbitrary large expansion of a mathematical expression like π. Hint: You can use the standard library `decimal` or the 3rd party library `sympy` to do this
- Write a function to check if a number is prime. Hint: See Sieve of Eratosthenes
- Write a function to generate sliding windows of a specified width from a long iterable (e.g. a string representation of a number)

Write unit tests for each of these three functions. You are encouraged, but not required, to try [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development).

Now use these helper functions to write the function that you need.
Write a unit test for this final function, given that the first 10-digit prime in the expansion e is 7427466391. Finally, solve the given problem.  

---


## Solution
### 1. Function: expanding
I write a function named expanding which is to generate an arbitrary large expansion of a mathematical expression like π. I import sympy for those mathematical expression.  
The function has two input value: a and b. a is mathmetical expression, for example pi and E and b is the number of digits we need, which must be integer and larger than 0. If b is not an integer or larger than 0, there will be a ValueError.  
In this function, I use evalf to get first (b+1) digits of a and store the value in c. Then I convert c to a string and split the first b digits. Also, the type of the output is string.   
The reason why I do not using evalf to output first b digits directly is that the evalf function will round up the value. For example, the output of pi.evalf(4) is 3.142, but the value I expect is 3.141, which is not be rounded.  
The code is as following
```python
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
```

<br>  


### 2. Function: is_prime
This function is to check which the input value is a prime or not.  
Firstly, the number input must be an integer and larger than 1. If not, it will be a ValueError.  
Secondly, I check 2, which is a special prime. Every even number except 2 is not a prime. Therefore, the even number will be excluded.  
Finally, I check all the odd numbers from 3 to sqrt(x) to see whether it is a factor of x. If they all are not factor of x, x will be a prime. If not, x is not a prime.
```python
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
```

<br>

### 3. Function: sliding_window
This function is to generate sliding windows of a specified width from a long iterable.  
a is a long iterable and the type of a is string. b is the location. And c is the width of window.  
Firstly, if type of a is not a string, it will be a ValueError.  
Then, I use the b and (b+c) as index of a to output the window.
```python
def sliding_window(a, b, c):
    '''This function is to generate sliding windows of a specified width from a long iterable'''

    # a is a long iterable and the type of a is string
    if not isinstance(a, str):
        return ValueError("a must be a string")
    
    # b is the location
    # c is the width of window
    return a[b: b + c] # The type of the output is string
```

<br>

### 4. Function: find_prime
This function is to find the first prime of specific width for the iterable, whcih combines three functions above.  
thenumber is mathematical expression like π and width is the number of digits.  
The sliding window checks each number in the expansion of mathematical expression untill it finds that prime number
```python
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
```
---

## Answer
**The first 10-digit prime in the decimal expansion of 17π is 8649375157**

---
