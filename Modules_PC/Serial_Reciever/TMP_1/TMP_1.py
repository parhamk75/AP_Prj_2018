import serial


def EMG_Read_Data_CL():
    
    EMG_SER = serial.Serial("COM7", 57600)
    
    EMG_SER.flushInput()
    
    
    a = EMG_SER.read(490)
    
    EMG_SER.close()
    
    
    for i in range(len(a)):
        if a[i] == 165:
            if a[i+1] == 90: 
                print("\n package #{} :".format(i/7))
        print("{} => ".format(i%7),int(a[i]))
        
def EMG_Read_Data_NC():
    EMG_SER = serial.Serial("COM7", 57600)
    
    for _ in range(10):
        
        
        EMG_SER.flushInput()
        
        
        a = EMG_SER.read(490)
        
        
        for i in range(len(a)):
            if a[i] == 165:
                if a[i+1] == 90: 
                    print("\n package #{} :".format(i/7))
            print("{} => ".format(i%7),int(a[i]))        
            
    EMG_SER.close()
    

    