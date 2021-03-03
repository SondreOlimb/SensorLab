import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import sys


import Read_Bin

t, data_voltage, freq, spectrum,s= Read_Bin.read_and_fft("RawData/wn.bin")






plot_color=["red","blue","green","purple","orange"]


for i in range(2,5):

    plt.subplot(2, 1, 1)
    plt.title("Time domain signal for ADC: "+str(i+1))
    plt.xlabel("Time [us]")
    plt.ylabel("Voltage")
    plt.plot(t[1000:5000], data_voltage[i][1000:5000],color=plot_color[i]) #slicing the array to make the signal readebol in the plot.
    #plt.plot(t_pre[100:2000], data_pre[i][1500:2000],color ="red",linestyle=":")


    plt.subplot(2, 1, 2)
    plt.title("Power spectrum of signal for ADC: "+str(i+1))
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power [dB]")

    plt.plot(freq, 20*np.log10(np.abs(spectrum[i])), color=plot_color[i]) # get the power spectrum
    plt.vlines(1000,0,100,label="1000Hz")
    plt.vlines(-1000, 0, 100)
    plt.xlim(-16000,16000)
    plt.legend()


    plt.show()



