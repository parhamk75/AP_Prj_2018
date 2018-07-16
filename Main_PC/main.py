# new data processing -> new thread for hystersys
import serial
from queue import Queue
from threading import Thread
import re

# for sleep
from time import sleep

#to run the game:
import os
import sys

sys.path.append(os.path.join(os.getcwd(),".\\Chrome-T-Rex-Rush-master\\"))
sys.path.append(os.path.join(os.getcwd(),".\\Chrome-T-Rex-Rush-master\\sprite"))

import pyGame



from PyQt5 import uic

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

################## Serial ####################

Serial_Port = "COM1"
Baud_Rate = 57600

Input_Buf = Queue()

#Data_Buf_Raw = Queue()

Extracted_Data_Buf_2_Show = Queue()
Extracted_Data_Buf = Queue()


Packet_ID_RE = re.compile('165,90,([0-9]{1,3}),([0-9]{1,3}),([0-9]{1,3}),([0-9]{1,3}),1,')
#       Please Don't omit the last comma (',') in the RE above because it
#   asures us that the last '1' is really a '1' not a '1' from
#   the next byte! (It's so important to be asure of that because
#   the next byte is '165' in normal state so it has a '1' at the beginning!)

temp_packet_number = 2000
tmp_cnst_1 = 40 + 7 * temp_packet_number
print("getting {} packets".format( int(temp_packet_number/7)) )

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
        #while i<tmp_cnst_1:            
        while True:
            Input_Buf.put( SER.read() )
            i += 1
            
        SER.close()


class pckt_xtrctr_thrd(Thread):
    def __init__( self ):
        Thread.__init__( self, name="Packet_Extractor_Thread")
        
    def run( self ):
        tmp_1 = ''
        cntr_2 = 0
        i = 0
        #while i<tmp_cnst_1:
        while True:
            tmp_1 += '{},'.format( ord(Input_Buf.get(block=True)) )           
            tmp_2 = Packet_ID_RE.findall(tmp_1)            
            
            if len(tmp_2) > 0:
#                Data_Buf_Raw.put(tmp_2[0])                
                tmp_1 = ''        
#                Unpacking the raw data to the processed data queue
                num = int( (tmp_2[0])[0] )*256 + int( (tmp_2[0])[1] )
                amp = int( (tmp_2[0])[2] )*256 + int( (tmp_2[0])[3] )
                
                if cntr_2 > 10:
                    Extracted_Data_Buf_2_Show.put( amp )
                    cntr_2 = 0
                
                
                Extracted_Data_Buf.put( ( num, amp) )
                cntr_2 += 1
#                print(Extracted_Data_Buf_2_Show.get())
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
       
        self.ax.set_ylim([-100,1500])
        self.canvas = FigureCanvas(self.fig)
        self.navi = NavigationToolbar( self.canvas, self)
        
        self.points_x = []
        self.points_y = []
        self.line, = self.ax.plot(  self.points_x, self.points_y)
        
        l = QVBoxLayout(self.Plt_Wdgt)
        l.addWidget(self.canvas)
        l.addWidget(self.navi)
        
    def Tmp_Run_Bttn_Func(self):
<<<<<<< HEAD
        
        
=======
<<<<<<< HEAD
        
        
=======
        pyGame.main()
>>>>>>> 8d947eb032b476e2a3b657b264d4aa2ae767d8de
>>>>>>> 2eb6ede671e83e2a4ac09b21d937abe080b4b941
        print("Ich liebe sie!")

    
        EMG_Shield_Serial_Reader.start()
        EMG_Data_Packet_Extractor.start()
        EMG_Process_Act.start()

        print("PyGame passed!!!")
        
        time_x = 0
        while True :
            tmp_amp = Extracted_Data_Buf_2_Show.get(block=True)
            self.points_x.append(time_x)
            self.points_y.append(tmp_amp)
            self.line.set_data(self.points_x, self.points_y)
            self.ax.set_xlim([time_x-300,time_x+300])
            self.fig.canvas.draw()
            pltr_app.processEvents()
            time_x += 1
        
###########################################


############ Data Processing ##############
threshould = 480
packet_number = 2

class dt_prcss(Thread):
    __strength__ = 0
    __current_state__ = False
    
    def __init__( self):
        Thread.__init__(self, name = "hystersis for values Thread")
    
    def run( self ):
        print("Data Process Started!")
        while True:
            if Extracted_Data_Buf.qsize() > (packet_number):
#                print("processing one group")
                amps = []
                for i in range(packet_number):
                    a,b = Extracted_Data_Buf.get()
                    amps.append(b)
                self.__strength__ = sum(amps) / packet_number
                #print("summation = {}".format(self.__strength__))
                if self.__current_state__ == False:
                    if self.__strength__ > threshould:
                        self.__current_state__ = True
                        print("got HIGH")
                        # here should emit
                        pyGame.set_high()
                else:
                    if self.__strength__ < threshould:
                        self.__current_state__ = False
                        print("got LOW")
                        #here should emit
                        pyGame.set_low()
            else:
                sleep(0.1)

###########################################    
        
############## Main Thread ################

EMG_Shield_Serial_Reader = sril_thrd( Serial_Port, Baud_Rate)
EMG_Shield_Serial_Reader.setDaemon(True)


EMG_Data_Packet_Extractor = pckt_xtrctr_thrd()
EMG_Data_Packet_Extractor.setDaemon(True)


EMG_Process_Act = dt_prcss()
EMG_Process_Act.setDaemon(True)





#EMG_Shield_Serial_Reader.join()
#EMG_Data_Packet_Extractor.join()


#for i in range(Extracted_Data_Buf_2_Show.qsize()):
#    print(Extracted_Data_Buf_2_Show.get())
        

pltr_app = QApplication(sys.argv)
pltr_w = Ploter()
pltr_w.show()

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 2eb6ede671e83e2a4ac09b21d937abe080b4b941
def Game_Opener():
    pyGame.main()
    
t = Thread(target = Game_Opener)
t.setDaemon(True)
t.start()
<<<<<<< HEAD
=======
=======
>>>>>>> 8d947eb032b476e2a3b657b264d4aa2ae767d8de
>>>>>>> 2eb6ede671e83e2a4ac09b21d937abe080b4b941


sys.exit( pltr_app.exec_() )
        
###########################################    
    
