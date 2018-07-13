# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import matplotlib.pyplot as plt
import numpy as np

buf_s = 50
x_axs_l = 300
a = [0 for _ in range(x_axs_l)]
t = [i for i in range(x_axs_l)]
cntr_1 = 0

while cntr_2<30:
    if ser.is_open():
        a[buf_s*cntr_1:(cntr_1+1)*buf_s] = ser.read(buf_s)
        ser.close()
        plot(t, a)
        if cntr_1 < (x_axs_l/buf_s)-1:
            cntr_1 +=1
        elif cntr_1 == (x_axs_l/buf_s)-1:
            cntr_1 = 0
        
    ser = serial.Serial("COM5",9600)
    cntr_2 +=1
#print(a)

#x = [i for i in range(300)]
#y = [a[i] for i in range(300)]

#plt.plot(x,y)

