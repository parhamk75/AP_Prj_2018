import serial
from queue import Queue


Serial_Port = "COM7"
Baud_Rate = 57600

Data_Recieve_is_True = True

Input_Buf = Queue()

def EMG_Read_Data( Serial_Port, Baud_Rate, Input_Buf, Data_Recieve_is_True):
    
    EMG_SER = serial.Serial( Serial_Port, Baud_Rate)

    while Data_Recieve_is_True:
        
        #EMG_SER.flushInput()
        #EMG_SER.reset_input_buffer()
        Input_Buf.put( EMG_SER.read(10) )
        
        print( "{}".format(Input_Buf.get())  )
        print("buf = {}".format(EMG_SER.in_waiting))
        
        
    EMG_SER.close()
    
