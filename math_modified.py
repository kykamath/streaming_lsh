'''
Created on Jun 14, 2011

@author: kykamath
'''

import math, numpy

def modified_log(i):
    if i==0: return 1
    else: return math.log(i)
    
def exponentialDecay(currentValue, decayCoefficient, timeDifference):
    '''
    The function V_n = V_o*D**t
    '''
    return currentValue*(decayCoefficient**timeDifference)

def isPrime(number):
    '''
    A quick hack to see if a number is prime or not.
    The code for this method was obtained from:
    http://rebrained.com/?p=458
    The original author can be contacted at nolfonzo@gmail.com
    '''
    return number in filter(lambda num: (num % numpy.arange(2,1+int(math.sqrt(num)))).all(), range(2,number+1))

def getLargestPrimeLesserThan(number):
    '''
    For details see isPrime description.
    '''
    return filter(lambda num: (num % numpy.arange(2,1+int(math.sqrt(num)))).all(), range(2,number+1))[-1]

def getSmallestPrimeNumberGreaterThan(number):
    '''
    For details see isPrime description.
    '''
    while not isPrime(number): number+=1
    return number
        

class ModularArithmetic:
    @staticmethod
    def gcd(numA, numB):
        '''
        The method to determine greatest common divisor by Andrew Pociu
        http://www.geekpedia.com/code120_Find-The-Greatest-Common-Divisor.html
        '''
        while numB != 0:
            numRem = numA % numB
            numA, numB = numB, numRem
        return numA
    @staticmethod
    def gcdExtended(a, b):
        '''
        Calculates gcd along with the co-efficients for
        linear combinations of numA and numB.
        Returns (gcd, x, y) such that gcd = numA*x + numB*y
        
        Thomas H. Cormen, Clifford Stein, Ronald L. Rivest, and Charles E. Leiserson. 2001. Introduction to Algorithms (2nd ed.). McGraw-Hill Higher Education.
        Implements the EXTENDED-EUCLID algorithm on pg. 860.
        '''
        if b == 0: return (a,1,0)
        (d_, x_, y_) = ModularArithmetic.gcdExtended(b, a%b)
        (d,x,y)=(d_, y_, x_-(a//b)*y_)
        return (d,x,y)
    
class DateTimeAirthematic:
    @staticmethod
    def getDifferenceInTimeUnits(time1, time2, timeUnitInSeconds):
        if time1<time2: return (time2-time1).seconds/timeUnitInSeconds
        return (time1-time2).seconds/timeUnitInSeconds