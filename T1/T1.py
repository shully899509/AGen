import math
import random
import sys
import numpy as np

import matplotlib.pyplot as plt


def convertBinToReal(a, b, numberOfBits, xB): return a + int(xB, 2) * (b-a)/(2**numberOfBits - 1)

def rastrigin(x): return 10*len(x) + sum([xi ** 2 - 10 * math.cos(2 * math.pi * xi) for xi in x])
def dejong(x): return sum([xi**2 for xi in x])
def schwefel(x): return sum([-xi * math.sin(math.sqrt(abs(xi))) for xi in x])
def sixhump(x): return (4 - 2.1*(x[0]**2) + (x[0]**4)/3.0)*(x[0]**2) + x[0]*x[1] + (-4 + 4*(x[1]**2))*(x[1]**2)




#1 - Rastrigin
#2 - De Jong
#3 - Schwefel
#4 - Six-hump camel back

#improvement: 1 - first(stop after finding first better neighbour), 2 - best
def execHC(iterations, function, improvement, n, f, numberOfBits, testNo):
    if function in [1,2,3,4]:
        f.write('\n\n\n**********  TEST NUMBER ' + str(testNo) + '  **********\n\n')

        listOfResults = list()
        listOfVcs = list()
        listOfVcsReal = list()

        for iter in range(iterations):
            better = sys.float_info.max
            local = False
            vc = list()

            #generate list of random vars
            for parameter in range(n):
                if function==4:
                    vc += [bin(random.getrandbits(numberOfBits[parameter]))[2:].zfill(numberOfBits[parameter])]
                else:
                    vc += [bin(random.getrandbits(numberOfBits))[2:].zfill(numberOfBits)]

            vcReal = [convertBinToReal(a[i],b[i],numberOfBits[i],vc[i]) for i in range(len(vc))] if function==4 else [convertBinToReal(a,b,numberOfBits,xB) for xB in vc]

            #evaluate vc
            eval1 = rastrigin(vcReal) if function == 1 else dejong(vcReal) if function == 2 else schwefel(vcReal) if function == 3 else sixhump(vcReal)
            if eval1<better: better = eval1

            while not local:
            #implement Improve(Neighbourhood(vc))
                found_better = False
                for param_iter in range(len(vc)):
                    vn = vc
                    var = vc[param_iter]
                    bit_iter = 0

                    while bit_iter < len(var):
                        #flip one bit at a time
                        temp = list(var)
                        temp[bit_iter] = '1' if temp[bit_iter] == '0' else '0'
                        #update vn with a var's neighbor
                        vn[param_iter] = ''.join(temp)
                        vnReal = [convertBinToReal(a[i],b[i],numberOfBits[i],vn[i]) for i in range(len(vn))] if function==4 else [convertBinToReal(a,b,numberOfBits,xB) for xB in vn]
                        eval2 = rastrigin(vnReal) if function == 1 else dejong(vnReal) if function == 2 else schwefel(vnReal) if function == 3 else sixhump(vnReal)
                        if eval2 < better:
                            vc2=vn
                            vcReal2 = vnReal
                            better = eval2

                            # condition for first improvement
                            found_better = True
                            if improvement == 1: break

                        bit_iter += 1

                    # condition for first improvement
                    if improvement == 1 and found_better:
                        break
                if better < eval1:
                    vc=vc2
                    vcReal=vcReal2
                    eval1=better
                else:
                    local=True

            #    local = True

            '''
            print('**************ITERATION ' + str(iter + 1))
            print(vc)
            print(vcReal)
            print(better)
            '''
            f.write('ITERATION ' + str(iter+1) + ' result: ' + str(better))
            f.write('\n========================\n')
            for i in range(len(vn)):
                f.write(vn[i] + ' = ' + str(vnReal[i]) + '\n')
            f.write('\n\n')


            listOfResults += [eval1]
            listOfVcs += [vc]
            listOfVcsReal += [vcReal]




        bestRes = str(min(listOfResults))
        bestVc = listOfVcs[listOfResults.index(min(listOfResults))]
        bestVcReal = listOfVcsReal[listOfResults.index(min(listOfResults))]

        f.write('###################### RESULTS FOR TEST NUMBER ' + str(testNo) + '\n')
        f.write('BEST RESULT: ' + bestRes + ' @iteration ' + str(listOfResults.index(min(listOfResults))+1) + '\n')
        for i in range(len(bestVc)):
            f.write(str(bestVc[i]) + ' = ' + str(bestVcReal[i]) + '\n')
        f.write('\n')

        worstRes = str(max(listOfResults))
        worstVc = listOfVcs[listOfResults.index(max(listOfResults))]
        worstVcReal = listOfVcsReal[listOfResults.index(max(listOfResults))]
        f.write('WORST RESULT: ' + worstRes + ' @iteration ' + str(listOfResults.index(max(listOfResults))+1) + '\n')
        for i in range(len(worstVc)):
            f.write(str(worstVc[i]) + ' = ' + str(worstVcReal[i]) + '\n')
        f.write('\n')

        import statistics
        f.write('MEAN: ' + str(sum(listOfResults)/len(listOfResults)) + '\n')
        f.write('STANDARD DEVIATION: ' + str(statistics.stdev(listOfResults)) + '\n\n\n\n')

        '''
        if testNo==1:
            fig = plt.figure()
            ax = plt.axes()

            x = [i for i in range(1, iterations+1)]
            y = listOfResults

            ax.plot(x, y)
            plt.show()
            '''





''' pseudocod:
begin
  t := 0
  initialize the temperature T
  select a current candidate solution (bitstring) vc at random
  evaluate vc
  repeat
    repeat
      select at random vn - a neighbor of vc
      if eval(vn) is better than eval(vc)
        then vc := vn
        else if random[0,1) < exp(-|eval(vn)-eval(vc)|/T)
          then vc := vn
    until (termination-condition)
    T := g(T; t)
    t := t + 1
  until (halting-criterion)
end
'''
def execSA(function, n, T, T_step, T_limit, numberOfBits, testNo, f):
    f.write('\n\n\n**********  TEST NUMBER ' + str(testNo) + '  **********\n\n')
    listOfResults = list()
    listOfVcs = list()
    listOfVcsReal = list()

    if function in [1,2,3,4]:
        better = sys.float_info.max
        vc = list()

        # generate list of random vars
        for parameter in range(n):
            if function == 4:
                vc += [bin(random.getrandbits(numberOfBits[parameter]))[2:].zfill(numberOfBits[parameter])]
            else:
                vc += [bin(random.getrandbits(numberOfBits))[2:].zfill(numberOfBits)]

        vcReal = [convertBinToReal(a[i], b[i], numberOfBits[i], vc[i]) for i in range(len(vc))] if function == 4 else [convertBinToReal(a, b, numberOfBits, xB) for xB in vc]

        # evaluate vc
        eval1 = rastrigin(vcReal) if function == 1 else dejong(vcReal) if function == 2 else schwefel(vcReal) if function == 3 else sixhump(vcReal)
        if eval1 < better: better = eval1

        vcPeBune = vc
        vcRealPeBune = vcReal
        betterPeBune = better

        t = 0
        while T > T_limit:
            #print(T)
            maxIterations = random.randint(30, 90)
            for iter in range(maxIterations):
                #print(iter)
                #select at random vn - a neighbor of vc
                vn = vc

                '''
                numberOfVarsToChange = random.randint(1, n)
                randomListOfVars = random.sample([i for i in range(numberOfVarsToChange)],random.randint(1,numberOfVarsToChange))
                for varNb in randomListOfVars:
                    randomBit = random.randint(0, numberOfBits[varNb]-1) if function==4 else random.randint(0, numberOfBits-1)
                    # flip one random bit from one random var
                    temp = list(vc[varNb])
                    temp[randomBit] = '1' if temp[randomBit] == '0' else '0'
                    # update vn with a var's neighbor
                    vn[varNb] = ''.join(temp)
                '''

                randomVar = random.randint(0, n-1)
                randomBit = random.randint(0, numberOfBits[randomVar]-1) if function==4 else random.randint(0, numberOfBits-1)
                # flip one random bit from one random var
                temp = list(vc[randomVar])
                temp[randomBit] = '1' if temp[randomBit] == '0' else '0'
                # update vn with a var's neighbor
                vn[randomVar] = ''.join(temp)

                vnReal = [convertBinToReal(a[i], b[i], numberOfBits[i], vn[i]) for i in range(len(vn))] if function == 4 else [convertBinToReal(a, b, numberOfBits, xB) for xB in vn]
                eval2 = rastrigin(vnReal) if function == 1 else dejong(vnReal) if function == 2 else schwefel(vnReal) if function == 3 else sixhump(vnReal)
                if eval2 < better:
                    #print('am gasit')
                    vc = vn
                    vcReal = vnReal
                    better = eval2

                    vcPeBune = vn
                    vcRealPeBune = vnReal
                    betterPeBune = eval2

                # random[0,1) < exp(-|eval(vn)-eval(vc)|/T)
                elif random.random() < math.exp(-abs(eval2-better)/T):
                    #print('nu am gasit sol bun')
                    vc = vn
                    vcReal = vnReal
                    better = eval2

            f.write('ITERATION ' + str(t + 1) + ' result: ' + str(better))
            f.write('\n========================\n')
            for i in range(len(vc)):
                f.write(vc[i] + ' = ' + str(vcReal[i]) + '\n')
            f.write('\n\n')
            listOfResults += [better]
            listOfVcs += [vc]
            listOfVcsReal += [vcReal]

            t+=1
            T *= (1-T_step)


        #print(vc)
        #print(vcReal)
        #print(better)

        #print(vcPeBune)
        #print(vcRealPeBune)
        #print(betterPeBune)


        f.write('###################### RESULTS FOR TEST NUMBER ' + str(testNo) + '\n')
        bestRes = str(min(listOfResults))
        bestVc = listOfVcs[listOfResults.index(min(listOfResults))]
        bestVcReal = listOfVcsReal[listOfResults.index(min(listOfResults))]
        f.write('BEST RESULT: ' + bestRes + ' @iteration ' + str(listOfResults.index(min(listOfResults))+1) + '\n')
        for i in range(len(bestVc)):
            f.write(str(bestVc[i]) + ' = ' + str(bestVcReal[i]) + '\n')
        f.write('\n')

        worstRes = str(max(listOfResults))
        worstVc = listOfVcs[listOfResults.index(max(listOfResults))]
        worstVcReal = listOfVcsReal[listOfResults.index(max(listOfResults))]
        f.write('WORST RESULT: ' + worstRes + ' @iteration ' + str(listOfResults.index(max(listOfResults))+1) + '\n')
        for i in range(len(worstVc)):
            f.write(str(worstVc[i]) + ' = ' + str(worstVcReal[i]) + '\n')
        f.write('\n')

        import statistics
        f.write('MEAN: ' + str(sum(listOfResults) / len(listOfResults)) + '\n')
        f.write('STANDARD DEVIATION: ' + str(statistics.stdev(listOfResults)) + '\n\n\n\n')











################## SET PARAMETERS AND RUN






#number of parameters (dimensions)
n = 5
precision = 8

#1 - Rastrigin
#2 - De Jong
#3 - Schwefel
#4 - Six-hump camel back
function = 4
if function==4: n = 2

iterations = 30


#MODE: 1 - first improvement (stop after finding first better neighbour), 2 - best improvement, 3 - Simulated Annealing
mode = 3

if mode==3:
    temperature = 100
    temp_step = 0.1
    temp_limit = 10**(-20)


if function in [1, 2, 3]:
    function_name = 'Rastrigin' if function == 1 else 'DeJong' if function == 2 else 'Schwefel'
    mode_name = 'First' if mode==1 else 'Best' if mode==2 else 'SA'
    function_name += '_' + mode_name
    function_name += '_' + str(n) + '.txt'
else:
    function_name = 'SixHump'
    mode_name = 'First' if mode == 1 else 'Best' if mode == 2 else 'SA'
    function_name += '_' + mode_name
    function_name += '_' + str(n) + '.txt'


#file handler
f = open(function_name, 'w')
f.write('INFO\n')

implementation = 'First Improvement' if mode==1 else 'Best Improvement' if mode==3 else 'Simulated Annealing'
f.write('Implementation: ' + implementation + '\n')

f.write('Number of parameters: ' + str(n) + '\n')

search_space = '[-5.12, 5.12]' if function in [1,2] else '[-500, 500]' if function == 3 else '[-3, 3] for x1, [-2, 2] for x2'
f.write('Search space: ' + search_space + '\n')


# function init domain space
if function in [1,2]:
    a = -5.12
    b = 5.12
elif function == 3:
    a = -500
    b = 500
elif function == 4:
    first_improv_flag = False
    a = [-3, -2]
    b = [3, 2]
    numberOfIntervals = [(b[0] - a[0]) * math.pow(10, precision), (b[1] - a[1]) * math.pow(10, precision)]
    numberOfBits = [math.ceil(math.log(numberOfIntervals[0], 2)), math.ceil(math.log(numberOfIntervals[1], 2))]
    f.write('Number of subintervals: ' + str(int(numberOfIntervals[0])) + ' for x1, ' + str(int(numberOfIntervals[1])) + ' for x2\n')
    f.write('Number of bits: ' + str(numberOfBits[0]) + ' for x1, ' + str(numberOfBits[1]) + ' for x2\n')

if function in [1,2,3]:
    numberOfIntervals = (b - a) * math.pow(10, precision)
    numberOfBits = math.ceil(math.log(numberOfIntervals, 2))
    f.write('Number of subintervals: ' + str(int(numberOfIntervals)) + '\n')
    f.write('Number of bits: ' + str(numberOfBits) + '\n')


iterationsNo = str(iterations) if mode in [1,2] else ' varies between 30 and 100'
f.write('Number of iterations per test: ' + iterationsNo + '\n')



for testNo in range(1):
    if mode in [1,2]:
        execHC(iterations=iterations, function=function, improvement=mode, n=n, f=f, numberOfBits=numberOfBits, testNo=testNo+1)
    else:
        execSA(function=function, n=n, T=temperature, T_step=temp_step, T_limit = temp_limit, f=f, numberOfBits=numberOfBits, testNo=testNo+1)
print('Created ' + function_name)