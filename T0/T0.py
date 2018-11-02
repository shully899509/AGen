import numpy as np
import random
import math 
import sys
import time

print("ceva")
    
def rastrigin(s, x): return s + (x**2 - 10 * math.cos(2 * math.pi * x))
def ackley(s1, s2, x, c): return s1 + x**2, s2 + math.cos(c*x)

def executa(iterations, choose_function, dictionar):
    for iter in range(0, iterations):
        print('Iteratia ' + str(iter+1))
        n = 10    
        
        #Rastrigin
        if choose_function == 1:
            val=0
            s=0
            for i in range(1, n+1):
                x = np.random.uniform(-5.12, 5.12)
                #print('x' + str(i) + ' = ' + str(x))
                s = rastrigin(s, x) 
            val = 10*n + s
        
        #Ackley
        elif choose_function == 2:
            val=0; a=20; b=0.2; c=2*math.pi
            s1=0; s2=0
            for i in range(1, n+1):
                x = np.random.uniform(-15, 30)
                s1, s2 = ackley(s1, s2, x, c)
            val = -a*math.exp(-b*math.sqrt(1/n*s1))-math.exp(1/n*s2)+a+math.exp(1)
        
        #Beale
        elif choose_function == 3:
            x1, x2 = np.random.uniform(-4.5, 4.5), np.random.uniform(-4.5, 4.5)
            val = (1.5-x1*(1-x2))**2+(2.25-x1*(1-x2**2))**2+(2.625-x1*(1-x2**3))**2
        
        #Bohachevsky
        elif choose_function == 4:
            x1, x2 = np.random.uniform(-100, 100), np.random.uniform(-100, 100)
            f1 = x1**2+2*x2**2-0.3*math.cos(3*math.pi*x1)-0.4*math.cos(4*math.pi*x2)+0.7
            f2 = x1**2+2*x2**2-0.3*math.cos(3*math.pi*x1)*math.cos(4*math.pi*x2)+0.3
            f3 = x1**2+2*x2**2-0.3*math.cos(3*math.pi*x1+4*math.pi*x2)+0.3
            val = min(f1,f2,f3)
        
        
        if iter==0 or val<minim: minim = val; 
        print('{:<25}      {:<25}'.format('f(x): ' + str(val),'minimul: ' + str(minim)))
        
    print('\n\t\t Minimul final = ' + str(minim) + '\n\n')
    
    return minim
    
    
#iteratii = 20
#functia = 6 

while(1):
    print('>>>Pentru iesire Ctrl+C<<< \n Lista: ')
    
    dictionar = {1: 'Rastrigin', 2:'Ackley', 3:'Beale', 4:'Bohachevsky'}
    for cheie, valoare in dictionar.items():
        print(' ' + str(cheie) + ' - ' + valoare)
    
    try:
        functia = int(input('Functia dorita: '))
        if functia in dictionar.keys(): print('Functia ' + dictionar[functia] + '\n')
        else: raise ValueError
        iteratii = int(input('Nr de iteratii: '))
        nr_rulari = int(input('Nr de rulari: '))
    except ValueError:
        print('\n\t Inputul nu este corect \n\n')
    except KeyboardInterrupt:
        print('\n\t Exit \n\n')
        sys.exit(0)
    except Exception as e:
        print(e)
    else:
    
        min_val = sys.float_info.max
        max_val = sys.float_info.min
        total_vals = list()
        
        min_time = sys.float_info.max
        max_time = sys.float_info.min
        total_times = list()
        for repetari in range(nr_rulari):
            start_time = time.time()
            
            rezultat = executa(iteratii, functia, dictionar)
            if rezultat < min_val: min_val = rezultat
            if rezultat > max_val: max_val = rezultat
            total_vals += [rezultat]
            
            durata = time.time() - start_time
            if durata < min_time: min_time = durata
            if durata > max_time: max_time = durata
            total_times += [durata]
        print('Cel mai mic timp de executie: ' + str(min_time) + ' secunde')
        print('Cel mai mare timp de executie: ' + str(max_time) + ' secunde')
        print('Timp mediu de executie: ' + str(sum(total_times)/len(total_times)) + ' secunde')
        
        print('Cea mai buna solutie: ' + str(min_val))
        print('Cea mai slaba solutie: ' + str(max_val))
        print('Media solutiilor: ' + str(sum(total_vals)/len(total_vals)))
            

    

   