import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt



### Constants #####
Max_puls = 196 #https://www.ntnu.no/cerg/hfmax 16.03.21
Min_puls = 35
N_fft =40248
window = 51
fps = 40
#######



raw_data = np.loadtxt("trans_2_ex/jonas_puls2_1.txt")
#raw_data = np.loadtxt("extracted/jonas4.txt")
#raw_data = np.loadtxt("rob_1_ex/jonas_puls7_2.txt") #

data=[]


for i in range(3):
    data.append(raw_data[:,i])
data = signal.detrend(data)







b, a = signal.butter(10, Max_puls/60, 'lp', analog=False, output="ba", fs=40) #filter away any noise outside the desiered range
data = signal.lfilter(b, a, data)  # finding the resolution and converting the bit value to the coresponding value in Volts
b, a = signal.butter(10, Min_puls/60, 'hp', analog=False, output="ba", fs=40)# filter away any noise outside the desiered range
data = signal.lfilter(b, a, data)  # finding the resolution and converting the bit value to the coresponding value in Volts

red = data[0]
green = data[1]
blue = data[2]

plt.plot(red,color = "r", label = "Red")
plt.plot(green,color = "g",label = "Green")
plt.plot(blue, color = "b", label = "Blue")
plt.legend()
plt.show()

data= data*signal.windows.hamming(len(raw_data))

fft_channel = blue





data_fft = np.fft.fft(fft_channel,len(fft_channel)*6) #Take the fast fourier transform with length 4 times sampling frequency og the complex vector array



data_log = 10*np.log10(np.abs(data_fft)**2)

freq = np.fft.fftfreq(n=round(len(data_log)), d=1/40)


freq_noise = []
data_noise =[]
data_signal =[]
for i in range(len(freq)-1,0,-1):
    if freq[i] <= Min_puls/60 or freq[i] >= Max_puls/60:
        freq_noise.append(freq[i])
        data_noise.append(data_fft[i])

        freq = np.delete(freq,i)



        data_log = np.delete(data_log,i)
        data_signal =np.delete(data_fft,i)
sorted = np.argsort(data_log)




print("######## The 10 frequency with the highest power:########")
for i in range(10):
    ind = sorted[-i-1]
    print("frequency[HZ]:",freq[ind],"Power[dB]:",data_log[ind],)
print("######################## \n")



plt.plot(freq,data_log)
plt.xlim(Min_puls/60,Max_puls/60)
plt.ylim(0,60)
plt.show()

f_D_index = np.argmax(data_log)
f_D = np.abs(freq[f_D_index])*60

print("Pulse is",f_D,"bpm")

print("######################## \n")

avg_signal = 10**(np.max(data_log)/10)
avg_noise = np.average(data_noise)


SNR=10*np.log(np.abs(avg_signal/avg_noise)**2)

print("SNR:",SNR)













