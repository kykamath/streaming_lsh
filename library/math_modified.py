'''
Created on Jun 14, 2011

@author: kykamath
'''

import math, numpy

def modified_log(i):
    if i==0: return 1
    else: return math.log(i)

def isPrime(number):
    '''
    A quick hack to see if a number is prime or not.
    The code for this method was obtained from:
    http://rebrained.com/?p=458
    The original author can be contacted at nolfonzo@gmail.com
    '''
    return number in filter(lambda num: (num % numpy.arange(2,1+int(math.sqrt(num)))).all(), range(2,number+1))