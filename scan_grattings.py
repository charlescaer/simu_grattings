##=======================================
##    runs python 2.2
##=======================================

from rodis import *
import time
from sys import stdout

def scan(name="",
         llambda_min=1.1/0.772, 
         llambda_max=2.5/0.772,
         n_llambdas=100,
         t_min=0.502/0.772,
         t_max=0.502/0.772,
         n_ts=1,
         n_r=3.2137,
         eta=0.77,
         n_orders=3,
         pol='TM'):
    reflectivity = []
    tic = time.time()
    step_llambda = (llambda_max - llambda_min)/n_llambdas
    step_ts = (t_max - t_min)/n_ts
    
    for j in range(n_ts): ###!%£^* Don't have numpy in python 2.2 !!!
        reflectivity_of_t = []
        for i in range(n_llambdas):
            llambda = llambda_min + step_llambda*i
            t = t_min + step_ts*j
            # rodis data
            set_lambda(1.064)
            set_N(n_orders)   
            set_polarisation(pol)
            
            # make device
            GaAs = Material(n_r)
            air  = Material(1.0)
            
            front  = Slab( air(llambda) )
            period = Slab( air(llambda*(1-eta)/2) + GaAs(llambda*eta) + air(llambda*(1-eta)/2))
            back   = Slab( air(llambda)  )
            
            grating = Stack( front(1.) + period(t) + back(1.))
            
            # start calculations
            grating.calc()
            
            reflectivity_of_t.append(grating.diffr_eff().R(0))
        reflectivity.append(reflectivity_of_t)

    for reflectivity_of_t in reflectivity:
        first = True
        for r in reflectivity_of_t:
            if not first:
                stdout.write(',')
            first = False
            stdout.write(str(r))
            
        stdout.write('\n')
    

if __name__=='__main__':
    import sys
    print """==="""
    kwds = {'llambda_min':float(sys.argv[1]),
            'llambda_max':float(sys.argv[2]),
            'n_llambdas':int(sys.argv[3]),
            't_min':float(sys.argv[4]),
            't_max':float(sys.argv[5]),
            'n_ts':int(sys.argv[6]),
            'n_r':float(sys.argv[7]),
            'eta':float(sys.argv[8]),
            'n_orders':int(sys.argv[9]),
            'pol':sys.argv[10]}
    scan(**kwds)