import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import Read_Bin


### Constants #####
N_fft =40248
window = 51
fps = 40
#######



#raw_data = np.loadtxt("data1_ex/puls1.txt")
raw_data = np.loadtxt("extracted/jonas4.txt")

data=[]

for i in range(3):
    data.append(raw_data[:,i])
data = signal.detrend(data)
data= data*signal.windows.hann(len(raw_data))


b, a = signal.butter(10,10, 'lp', analog=False, output="ba",fs=40)
raw_data = signal.lfilter(b, a, data, axis=- 1,zi=None)  # finding the resolution and converting the bit value to the coresponding value in Volts

    #b, a = signal.butter(1, 500, 'lp', analog=False, output="ba", fs=40)
    #data = signal.lfilter(b, a, data, axis=- 1,zi=None)  # finding the resolution and converting the bit value to the coresponding value in Volts


#data = signal.savgol_filter(data,51,3)


red = data[0]
green = data[1]
blue = data[2]
plt.plot(red,color = "r", label = "Red")
plt.plot(green,color = "g",label = "Green")
plt.plot(blue, color = "b", label = "Blue")
plt.legend()
plt.show()









data_fft = np.fft.fft(red,len(red)*6) #Take the fast fourier transform with length 4 times sampling frequency og the complex vector array



data_log = 10*np.log10(np.abs(data_fft)**2)
sorted = np.argsort(data_log, axis=-1, kind=None, order=None)

freq = np.fft.fftfreq(n=round(len(data_log)), d=1/40)

plt.plot(freq,data_log)
plt.show()

f_D_index = np.argmax(data_log)
f_D = freq[f_D_index]*60

print("Pulse is",f_D,"bpm")











