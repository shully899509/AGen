import math
import random
import sys
import numpy as np

import matplotlib.pyplot as plt

def convertBinToReal(a, b, numberOfBits, xB): return a + int(xB, 2) * (b-a)/(2**numberOfBits - 1)

def rastrigin(x): return 10*len(x) + sum([xi ** 2 - 10 * math.cos(2 * math.pi * xi) for xi in x])
def griewank(x): return 1 + 1.0/4000 * sum([xi**2 for xi in x]) - np.prod([math.cos(x[i]/math.sqrt(i+1)) for i in range(len(x))])
def rosenbrock(x): return sum([100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x)-1)])
def sixhump(x): return (4 - 2.1*(x[0]**2) + (x[0]**4)/3.0)*(x[0]**2) + x[0]*x[1] + (-4 + 4*(x[1]**2))*(x[1]**2)


'''def dejong(x): return sum([xi**2 for xi in x])
def schwefel(x): return sum([-xi * math.sin(math.sqrt(abs(xi))) for xi in x])'''

#print(rosenbrock([1,1,1]))



