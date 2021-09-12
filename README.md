---
title: "BIOS 823 Homework 1: Math is fun"
layout: post
date: 2021-09-3 22:48
# image: /assets/images/markdown.jpg
headerImage: false
# tag:
# - markdown
# - components
# - extra
category: blog
author: Caihan Wang
description: 823 HW1
---



## Problem 6 

[Problem 6](https://projecteuler.net/problem=6) has been Currently solved by 496349 people. The problem is as following:
![Screen Shot 2021-09-03 at 10.38.03 PM.png](https://i.loli.net/2021/09/04/T5rhIayVPn1t2z8.png)  

### Solution
My solution is to build a list which contains natural numbers from 1 to 100, and then, we could calculate the sum of squares and square of sum. After that, we can get the difference of them.  
My answer is 25164150
<br>   

Firsly, I used numpy to generate a natural number list
```python
import numpy as np 

def diff_square():
    '''build a list which contains natural numbers from 1 to 100'''
    x = np.arange(101)
```


Secondly, I can calculate sum of squares and square of sum and get the difference between them
```python
    '''Calculate sum of squares and square of sum'''
    y1 = sum(x)**2
    y2 = sum(list(map(lambda x:x**2, x)))

    '''Calculate the difference'''
    print(y1 - y2)

if __name__ == '__main__':
    diff_square()
```


---

## Problem 56
[Problem 56](https://projecteuler.net/problem=56) has been Currently solved by 58489 people. The problem is as following:
![Screen Shot 2021-09-03 at 10.57.46 PM.png](https://i.loli.net/2021/09/04/N6yM7VT9HU2wtji.png) 
### Solution
To calculate the maximum digit sum of a^b, where a, b<100, I choose to use two loops to solve the question.   
First loop for a from 1 to 99 and second loop for b from 1 to 99. We can calculte digit sum of each a^b and storage the results in a list. To calculate digit sum, I choose to convert the int to the string, and convert each string to number and add together to get the digit sum.   
In the end, we can use max function to find the largest one.  
My answer is 972
<br>

```python
import numpy as np

def digit_sum():

    '''set an empty list to storage the results'''
    results = []

    '''two loops for a and b'''
    for a in range(100):
        for b in range(100):

            '''calculate the a^b'''
            c = a**b

            '''calculate the sum of digits'''
            d = sum(list(map(int,list(str(c)))))

            '''store in list'''
            results.append(d)

    '''find the max'''
    result = max(results)

    print(result)

if __name__ == '__main__':
    digit_sum()
```
---

## Problem 119
[Problem 119](https://projecteuler.net/problem=119) has been Currently solved by 12212 people. The problem is as following:
![Screen Shot 2021-09-03 at 11.24.12 PM.png](https://i.loli.net/2021/09/04/6mWG4lB17TiYrZd.png)
### Solution
I use two loops to find numbers meet this condition. First loop for i range from 0~99 and second loop for j range from 0~99 and then calculate i^j.  
According to the problem, the number must contain at least two digits, so i^j must larger than 10. I use if to set this condition.  
Then, if the sum digits of i^j equal to i, the i^j is what we want. We can put it in the results list.  
In the end, I find the No.30 result in the list.  
My answer is 248155780267521
<br>

```python
def power_sum():
    '''set an empty list to storage the results'''
    results = []

    '''use two loops'''
    for i in range(100):
        for j in range(100):

            '''i^j must have at least two digits'''
            if i**j > 10:

                '''if the sum digits of i^j equal to i, the i^j is what we want'''
                if sum(list(map(int,list(str(i**j))))) == i:
                    results.append(i**j)

    '''We need the No.30 result'''
    print(sorted(results)[29])


if __name__ == '__main__':
    power_sum()
```
---
