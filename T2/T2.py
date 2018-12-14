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


def mutation(x):
    nBits = len(x[0])
    temp = list(''.join(x))
    random_bit = random.randint(0,len(temp)-1)
    temp[random_bit] = '1' if temp[random_bit] == '0' else '0'
    x1 = ''.join(temp)
    x_final = list(list())
    for iter in range(len(x)):
        x_final += [x1[iter * nBits:(iter+1) * nBits]]
    return x_final

def crossover(x, y):
    x_unified = ''.join(x); y_unified = ''.join(y)
    r = random.randint(1,len(x_unified)-2)
    x1 = x_unified[:r]; x1 += y_unified[r:]; y1 = y_unified[:r]; y1 += x_unified[r:]
    nBits = len(x[0])
    x_final = list(list()); y_final = list(list())
    for iter in range(len(x)):
        x_final += [x1[iter * nBits:(iter + 1) * nBits]]
        y_final += [y1[iter * nBits:(iter + 1) * nBits]]
    return (x_final,y_final)

def GA(function, dimension, pop_size, numberOfBits, a, b, g_limit, crossover_prob, mutation_prob):
    v = list(list())
    vReal = list(list())

    #generate population in bits
    for i in range(pop_size):
        individ = list(); individReal = list()
        for j in range(dimension):
            if function in [1,2,3]:
                individ += [bin(random.getrandbits(numberOfBits))[2:].zfill(numberOfBits)]
                individReal += [convertBinToReal(a, b, numberOfBits, individ[j])]
            else:
                individ += [bin(random.getrandbits(numberOfBits[j]))[2:].zfill(numberOfBits[j])]
                individReal += [convertBinToReal(a[j], b[j], numberOfBits[j], individ[j])]
        v += [individ]
        vReal += [individReal]

    #print(v); print(vReal)

    g = 0
    while g<g_limit:
        g+=1

        #Roata norocului
        select_vector = list()
        eval = [1/rastrigin(i) if function == 1 else 1/griewank(i) if function == 2 else 1/rosenbrock(i) if function == 3 else 1/(sixhump(i)+1.0316) for i in vReal]

        #print(min(eval))

        T = sum(eval)
        p = [i/T for i in eval]
        q = [0]
        for i in range(pop_size):
            q+=[q[i] + p[i]]

        for i in range(pop_size):
            r = random.uniform(0,1)
            j = 0
            while q[j] < r:
                j+=1
                if j==len(v): break
            j-=1
            select_vector += [v[j]]
        for i in range(0, len(select_vector), 2):
            if random.uniform(0,1) < crossover_prob: select_vector[i], select_vector[i+1] = crossover(select_vector[i], select_vector[i+1])
            if random.uniform(0,1) < mutation_prob: select_vector[i] = mutation(select_vector[i])
            if random.uniform(0,1) < mutation_prob: select_vector[i+1] = mutation(select_vector[i+1])


        indiviziReal = list(list())
        for i in range(len(select_vector)):
            if function in [1,2,3]:
                individReal = [convertBinToReal(a, b, numberOfBits, xB) for xB in select_vector[i]]
            else:
                individReal = [convertBinToReal(a[indiv], b[indiv], numberOfBits[indiv], select_vector[i][indiv]) for indiv in range(len(select_vector[i]))]
            indiviziReal += [individReal]


        v = select_vector.copy()
        vReal = indiviziReal.copy()

        #print(v)
        #print(vReal)

    #print(v)
    #print(vReal)

    results = [rastrigin(i) if function == 1 else griewank(i) if function == 2 else rosenbrock(i) if function == 3 else sixhump(i) for i in vReal]
    #print(results)


    print(min(results))
    return min(results)
    #print(vReal[results.index(min(results))])


# Rastrigin - 1
# Griewangk - 2
# Rosenbrock - 3
# Six-hump camel back - 4

function = 3
dimension = 30

precision = 8
if function==4: dimension = 2


if function in [1,2,3]:
    if function == 1:
        a = -5.12; b = 5.12
    elif function == 2:
        a = -600; b = 600
    else:
        a = -2.048; b = 2.048
    numberOfIntervals = (b - a) * math.pow(10, precision)
    numberOfBits = math.ceil(math.log(numberOfIntervals, 2))
else:
    a = [-3, -2]; b = [3, 2]
    numberOfIntervals = [(b[0] - a[0]) * math.pow(10, precision), (b[1] - a[1]) * math.pow(10, precision)]
    numberOfBits = [math.ceil(math.log(numberOfIntervals[0], 2)), math.ceil(math.log(numberOfIntervals[1], 2))]

crossover_prob = 0.8
mutation_prob = 0.05

g_limit = 5000
pop_size = 140

results = list()
for repeta in range(15):
    results += [GA(function, dimension, pop_size, numberOfBits, a, b, g_limit, crossover_prob, mutation_prob)]

print(min(results))
print(max(results))
print(sum(results)/len(results))