import os.path as osp, numpy as np
import os

from guiqwt.plot import ImageDialog
from guiqwt.builder import make
from PyQt4 import QtCore, QtGui
import grattings
import json
import numpy

#res = grattings.r_of_lambda_and_t(save_file='sin.csv',**grattings.par_sin)

class MyImageDialog(ImageDialog):
    def __init__(self, directory):
        self.directory = directory
        super(MyImageDialog, self).__init__(edit=False, toolbar=True, wintitle="Cross sections test",
                      options=dict(show_xsection=True, show_ysection=True))
        self.resize(600, 600)
        
        self.lay = QtGui.QFormLayout()
        
        self.combo_n = QtGui.QComboBox()
        self.combo_eta = QtGui.QComboBox()
        self.combo_pol = QtGui.QComboBox()
        self.refresh_button = QtGui.QPushButton('refresh')
        self.refresh_button.clicked.connect(self.load_dir)
        self.layout().addWidget(self.refresh_button)
        
        self.lay.addRow(QtGui.QLabel('n'), self.combo_n)
        self.lay.addRow(QtGui.QLabel('eta'), self.combo_eta)
        self.lay.addRow(QtGui.QLabel('pol'), self.combo_pol)
        self.layout().addLayout(self.lay)
        
        self.image = None
        self.data = {}
        self.load_dir()
        
        self.combo_eta.currentIndexChanged.connect(self.display_data)
        self.combo_pol.currentIndexChanged.connect(self.display_data)
        self.combo_n.currentIndexChanged.connect(self.display_data)
        self.display_data()
        
    def display_data(self):
        n = float(self.combo_n.currentText())
        eta = float(self.combo_eta.currentText())
        pol = self.combo_pol.currentText()
        dat, kwds = self.data[self._str_data(n, eta, pol)]
        dat = 1.0-dat
        
        if not self.image:
            self.image = make.image(dat, title="Modified")
            self.get_plot().add_item(self.image)
            self.get_plot().set_axis_title(0, 'thickness')
            self.get_plot().set_axis_title(1, '1-R')
            self.get_plot().set_axis_title(2, 'llambda')
            self.plot_thicknesses()
            self.get_plot().legend()
        else:
            self.image.set_data(dat)
        self.image.set_xdata(kwds['llambda_min'], kwds['llambda_max'])
        self.image.set_ydata(kwds['t_min'], kwds['t_max'])
        self.get_plot().replot()
        self.get_plot().do_autoscale()

    def plot_thicknesses(self):
        llambda_min = 0.
        llambda_max = 2.
        
        for t, col in [(0.030, 'red'),(0.050,'green'),(0.100, 'black'),(0.200, 'blue')]:
            c = make.curve([llambda_min, llambda_max],[t, t], color=col, title='thickness=' + str(t))
            self.get_plot().add_item(c)
           
    def _str_data(self,  n, eta, pol):
        return str(n) + '_' + str(eta) + '_' + str(pol)
    
    def add_data(self, n, eta, pol, data, kwds):
        print 'adding data ', n, eta, pol
        self.data[self._str_data(n, eta, pol)] = (data, kwds)
        if self.combo_n.findText(str(n))==-1:       
            self.combo_n.addItem(str(n))
        if self.combo_eta.findText(str(eta))==-1:
            self.combo_eta.addItem(str(eta))
        if self.combo_pol.findText(str(pol))==-1:
            self.combo_pol.addItem(pol)
            
    def get_data(self, n, eta, pol):
        return self.data[self._str_data(n, eta, pol)]
    
    def load_dir(self, directory=None):
        if not directory:
            directory = self.directory
        for fname in os.listdir(directory):
            if fname.endswith('.csv'):
                with open(fname) as f:
                    kwds = json.loads(f.readline())
                    f.readline()
                    dat = numpy.loadtxt(f)
                    self.add_data(kwds['n_r'], kwds['eta'], kwds['pol'], dat, kwds)
        
import os.path as osp
import guidata
_app = guidata.qapplication()
win = MyImageDialog('D:/Dropbox/Theorie/grattings/RCWA/rodis')
win.show()
