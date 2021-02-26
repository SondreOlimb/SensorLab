import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import Read_Bin

N_fft =40248
c = 3*10**8 #speed of ligth
f_0 = 24.125*10**9 #frequenzy of readar
w = c/f_0 #wavelangth
f_s=31250
print(w)

plt.ion()



t, data, freq, spectrum,sample_period = Read_Bin.read_and_fft("Raw_data/Dunkedata8.bin")

#Data[0] is the IF_I
#Data[1] is the IF_Q




x = data[1] + 1j*data[0]

x = x*signal.windows.hamming(len(x))

#need to find the doopler frequenzy f_D

f,periodogram_x = signal.periodogram(x,31250,nfft=len(data[0])*6)



index_f_D = np.argmax(periodogram_x)

f_D = f[index_f_D]


plt.plot(data[0][5000:7000])
plt.plot(data[1][5000:7000])
plt.show()






v = f_D*w/2

"""
Solution 1

tester = 10*np.log10(np.abs(periodogram_x)**2)
sorted = np.argsort(tester, axis=-1, kind=None, order=None)

print("######## The 10 frequency with the highest power:########")
for i in range(10):
    ind = sorted[-i-1]
    print("frequency[HZ]:",f[ind],"Power[dB]:",tester[ind],)
print("######################## \n")


print("the frequency is:",f_D)
print("the velocity is:", v)

"""

"""
Solution 2
"""
data_fft = np.fft.fft(x,31250*4)


data_fft=np.trim_zeros(data_fft, trim='fb')

tester = 10*np.log10(np.abs(data_fft)**2)
sorted = np.argsort(tester, axis=-1, kind=None, order=None)


freq = np.fft.fftfreq(n=round(len(tester)), d=sample_period)
print("######## The 10 frequency with the highest power:########")
for i in range(10):
    ind = sorted[-i-1]
    print("frequency[HZ]:",freq[ind],"Power[dB]:",tester[ind],)
print("######################## \n")
f_D_index = np.argmax(tester)
f_D = freq[f_D_index]




v = f_D*w/2
print("the doppler frequency is",f_D,"Hz")
print("the velocity is:", v,"m/s")









#plt.plot(f,10*np.log10(periodogram_x))
#plt.xlim(-2000,2000)
#plt.show()





#plotting the PSD
plt.plot(freq,tester)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Power [dB]")
#plt.xlim(-2000,2000)
#plt.xlim(170,200)
plt.show()

signal = np.max(tester)


rms = 10*np.log10(np.sqrt(np.mean(np.abs(x)**2)))
snr = signal-rms


print("SNR:",snr )








