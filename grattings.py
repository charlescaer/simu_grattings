"""
module that can be run with python 2.7
"""
import subprocess
from StringIO import StringIO
import numpy
from numpy import linspace
import pylab
import json

def r_of_llambda_and_t(llambda_min=1.1/0.772, 
                     llambda_max=2.5/0.772,
                     n_llambdas=100,
                     t_min=0.1/0.772,
                     t_max=0.9/0.772,
                     n_ts=100,
                     n_r=3.2137,
                     eta=0.77,
                     n_orders=3,
                     pol='TM',
                     save_file=None,
                     plot=True):
    
    kwds = {'llambda_min':llambda_min, 
           'llambda_max':llambda_max,
           'n_llambdas':n_llambdas,
           't_min':t_min,
           't_max':t_max,
            'n_ts':n_ts,
            'n_r':n_r,
            'eta':eta,
            'n_orders':n_orders,
            'pol':pol
           }
    res = subprocess.check_output(['C:/python22/python.exe', 'D:/Dropbox/Theorie/grattings/RCWA/rodis/scan_grattings.py', 
                            str(llambda_min),
                            str(llambda_max),
                            str(n_llambdas),
                            str(t_min),
                            str(t_max),
                            str(n_ts),
                            str(n_r),
                            str(eta),
                            str(n_orders),
                            str(pol)])
    string = StringIO(res.split('===')[1])

    x = numpy.linspace(llambda_min, llambda_max, n_llambdas)
    y = numpy.linspace(t_min, t_max, n_ts)
    c = numpy.loadtxt(string, delimiter=',')
    if plot:
        fig = pylab.figure()
        pylab.pcolor(x,y,c)
        pylab.xlabel('llambda (um)')
        pylab.ylabel('t (um)')
        pylab.title("n_r=" + str(n_r) + " eta=" + str(eta) + " n_orders=" + str(n_orders) + " pol=" + pol)
        if save_file:
            fig.savefig(save_file + '.png')
    if save_file:
        with open(save_file, 'w') as f:
            json.dump(kwds, f)
            f.write('\n')
            f.write('[DATA]')
            f.write('\n')
            numpy.savetxt(f, numpy.array(c))
    return x, y, c


def r_of_llambda(llambda_min=1.1/0.772, 
                 llambda_max=2.5/0.772,
                 n_llambdas=100,
                 t=0.1/0.772,
                 n_r=3.2137,
                 eta=0.77,
                 n_orders=3,
                 pol='TM',
                 plot=True):
    t_min = t
    t_max = t
    n_ts = 1
    res = subprocess.check_output(['C:/python22/python.exe', 'D:/Dropbox/Theorie/grattings/RCWA/rodis/scan_grattings.py', 
                            str(llambda_min),
                            str(llambda_max),
                            str(n_llambdas),
                            str(t_min),
                            str(t_max),
                            str(n_ts),
                            str(n_r),
                            str(eta),
                            str(n_orders),
                            str(pol)])
    string = StringIO(res.split('===')[1])

    x = numpy.linspace(llambda_min, llambda_max, n_llambdas)
    c = numpy.loadtxt(string, delimiter=',')
    if plot:
        pylab.plot(x, c)
    return x, c

par_broadband = {'llambda_min':1.1/0.772, 
                 'llambda_max':2.5/0.772,
                 'n_llambdas':100,
                 't_min':0.1,
                 't_max':3.,
                 'n_ts':100,
                 'n_r':3.2137,
                 'eta':0.77,
                 'n_orders':3,
                 'pol':'TM'}

par_sin = {'llambda_min':0.5, 
           'llambda_max':1.7,
                 'n_llambdas':100,
                 't_min':0.01,
                 't_max':1.,
                 'n_ts':100,
                 'n_r':2.0,
                 'eta':0.3,
                 'n_orders':3,
                 'pol':'TE'
            }


par_res = {'llambda_min':1.4/0.716, 
           'llambda_max':2./0.716,
           'n_llambdas':100,
           't_min':0.1,
            't_max':3.,
                 'n_ts':100,
                 'n_r':3.48,
                 'eta':0.7,
                 'n_orders':3,
                 'pol':'TE'
           }


par_fig2 = {'llambda_min':0.01, 
            'llambda_max':3.,
                 'n_llambdas':100,
                 't_min':0.1,
                 't_max':3.,
                 'n_ts':100,
                 'n_r':3.48,
                 'eta':0.7,
                 'n_orders':3,
                 'pol':'TE'
            }
def calc_sin():
    for eta in linspace(0.1, 0.9, 10):
        for pol in ['TM', 'TE']:
            par_sin['pol'] = pol
            par_sin['eta'] = eta
            r_of_llambda_and_t(save_file=pol+'_eta'+str(eta)+'.csv',**par_sin)

def dummy():
    #r_of_lambda_and_t(save_file='fig1.csv',**par_broadband)
    #r_of_lambda_and_t(save_file='fig2.csv',**par_fig2)
    t_res = 1.494/0.716
    t_broadband = 0.502/0.772
    r_of_lambda_and_t(save_file='fig1.csv',**par_broadband)
    pylab.plot([1.0,3.5], [t_broadband,t_broadband])
    
    r_of_lambda_and_t(save_file='fig1_res.csv',**par_res)
    pylab.plot([-1.,3.5], [t_res,t_res])
    
    #par_broadband['n_r'] = 2.
    #r_of_lambda_and_t(save_file='sin.csv',**par_broadband)
    
    pylab.figure()
    par_broadband.pop('n_ts')
    par_broadband.pop('t_min')
    par_broadband.pop('t_max')
    par_broadband['t'] = t_broadband
    r_of_lambda(**par_broadband)
    par_res.pop('n_ts')
    par_res.pop('t_min')
    par_res.pop('t_max')
    par_res['t'] = t_res
    r_of_lambda(**par_res)
    
    
