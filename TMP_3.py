import serial
from queue import Queue
from threading import Thread
import re


Serial_Port = "COM7"
Baud_Rate = 57600

Input_Buf = Queue()

Data_Buf = Queue()

Packet_ID_RE = re.compile('165,90,([0-9]{1,3}),([0-9]{1,3}),([0-9]{1,3}),([0-9]{1,3}),1,')
#       Please Don't omit the last comma (',') in the RE above because it
#   asures us that the last '1' is really a '1' not a '1' from
#   the next byte! (It's so important to be asure of that because
#   the next byte is '165' in normal state so it has a '1' at the beginning!)

tmp_cnst_1 = 1000

class sril_thrd(Thread):
    def __init__( self, Serial_Port, Baud_Rate ):
        Thread.__init__( self, name="Serial_Thread")
        self.Serial_Port_ = Serial_Port
        self.Baud_Rate_ = Baud_Rate
        
    
    def run( self ):
        print("Serial Port is: {}".format(self.Serial_Port_))
        print("Serial Port is: {}".format(self.Baud_Rate_))
        SER = serial.Serial( self.Serial_Port_, self.Baud_Rate_)
        i = 0
        while i<tmp_cnst_1:            
            Input_Buf.put( SER.read() )
            i += 1
#            EMG_SER.close()

class pckt_xtrctr_thrd(Thread):
    def __init__( self ):
        Thread.__init__( self, name="Packet_Extractor_Thread")
        
    def run( self ):
        tmp_1 = ''
        i = 0
        while i<tmp_cnst_1:
            tmp_1 += '{},'.format( ord(Input_Buf.get()) )
#            print(tmp_1)
#            a = tmp_1.split(',')
#            print(a)
            
            i += 1
            
        print(Packet_ID_RE.findall(tmp_1))
        Extrctd_Data = 0
        Data_Buf.put(Extrctd_Data)



EMG_Shield_Serial_Reader = sril_thrd("COM7", 57600)
EMG_Shield_Serial_Reader.start()

EMG_Data_Packet_Extractor = pckt_xtrctr_thrd()
EMG_Data_Packet_Extractor.start()


EMG_Shield_Serial_Reader.join()
EMG_Data_Packet_Extractor.join()



            
        
    
    
