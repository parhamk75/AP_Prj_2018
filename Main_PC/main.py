import serial
from queue import Queue
from threading import Thread
import re

import os
import sys

from PyQt5 import uic

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

################## Serial ####################

Serial_Port = "COM11"
Baud_Rate = 57600

Input_Buf = Queue()

#Data_Buf_Raw = Queue()

Data_Buf_Processed = Queue()


Packet_ID_RE = re.compile('165,90,([0-9]{1,3}),([0-9]{1,3}),([0-9]{1,3}),([0-9]{1,3}),1,')
#       Please Don't omit the last comma (',') in the RE above because it
#   asures us that the last '1' is really a '1' not a '1' from
#   the next byte! (It's so important to be asure of that because
#   the next byte is '165' in normal state so it has a '1' at the beginning!)

tmp_cnst_1 = 20000

class sril_thrd(Thread):
    def __init__( self, Serial_Port, Baud_Rate ):
        Thread.__init__( self, name="Serial_Thread")
        self.Serial_Port_ = Serial_Port
        self.Baud_Rate_ = Baud_Rate
        
    
    def run( self ):
        print("Serial Port is: {}".format(self.Serial_Port_))
        print("Serial Port is: {}".format(self.Baud_Rate_))
        SER = serial.Serial( self.Serial_Port_, self.Baud_Rate_)
        SER.flushInput()
        
        i = 0
        while i<tmp_cnst_1:            
            Input_Buf.put( SER.read() )
            i += 1
            
        SER.close()


class pckt_xtrctr_thrd(Thread):
    def __init__( self ):
        Thread.__init__( self, name="Packet_Extractor_Thread")
        
    def run( self ):
        tmp_1 = ''
        
        i = 0
        while i<tmp_cnst_1:
            tmp_1 += '{},'.format( ord(Input_Buf.get(block=True)) )           
            tmp_2 = Packet_ID_RE.findall(tmp_1)            
            
            if len(tmp_2) > 0:
#                Data_Buf_Raw.put(tmp_2[0])                
                tmp_1 = ''        
#                Unpacking the raw data to the processed data queue
                num = int( (tmp_2[0])[0] )*256 + int( (tmp_2[0])[1] )
                amp = int( (tmp_2[0])[2] )*256 + int( (tmp_2[0])[3] )
                Data_Buf_Processed.put( ( num, amp) )
#                print(Data_Buf_Processed.get())
            i += 1
            
        print(tmp_1)
###########################################
        
################## GUI ####################
        
Forms = uic.loadUiType( os.path.join( os.getcwd(), 'Ploter.ui') )
    
class Ploter( Forms[0], QMainWindow):
    def __init__(self):
        Forms[0].__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        
        self.Tmp_Run_Bttn.clicked.connect(self.Tmp_Run_Bttn_Func)
        
        self.fig = Figure()
        self.ax = self.fig.add_axes([ 0.1, 0.1, 0.8, 0.8])
        self.canvas = FigureCanvas(self.fig)
        self.navi = NavigationToolbar( self.canvas, self)
        
        l = QVBoxLayout(self.Plt_Wdgt)
        l.addWidget(self.canvas)
        l.addWidget(self.navi)
        
    def Tmp_Run_Bttn_Func(self):
        print("Ich liebe sie!")
        
###########################################



############## Main Thread ################

EMG_Shield_Serial_Reader = sril_thrd( Serial_Port, Baud_Rate)
EMG_Shield_Serial_Reader.start()

EMG_Data_Packet_Extractor = pckt_xtrctr_thrd()
EMG_Data_Packet_Extractor.start()


EMG_Shield_Serial_Reader.join()
EMG_Data_Packet_Extractor.join()


for i in range(Data_Buf_Processed.qsize()):
    print(Data_Buf_Processed.get())
        

pltr_app = QApplication(sys.argv)
pltr_w = Ploter()
pltr_w.show()

sys.exit( pltr_app.exec_() )
        
###########################################    
    
