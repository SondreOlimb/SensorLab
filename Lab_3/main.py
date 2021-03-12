import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import Read_Bin


### Constants #####
N_fft =40248
c = 3*10**8 #speed of ligth
f_0 = 24.125*10**9 #frequenzy of readar
w = c/f_0 #wavelangth
f_s=31250
#######

#Choose dataset
dataset = 2

fig, axs = plt.subplots(nrows=3, ncols=1)




file_name ="Raw_data_4/Dunkedata"+str(dataset)+".bin"

t, data, freq, spectrum,sample_period = Read_Bin.read_and_fft(file_name)

data = signal.detrend(data)

#Data[0] is the IF_I
#Data[1] is the IF_Q




x = data[0] + 1j*data[1] #Create a complex vector array of the to data streams from the radar

axs[0].plot(data[1])
axs[0].plot(data[0])
axs[0].set_xlabel("Sample[n]")
axs[0].set_ylabel("quantification[16-bit]")
axs[0].set_title("IF_Q and IF_I")
axs[0].set_xlim(2000,12000)
axs[0].grid(True)


x = x*signal.windows.hann(len(x)) #using a hamming window to reduce the sidelobes










"""
Solution 2
"""
data_fft = np.fft.fft(x,31250*6) #Take the fast fourier transform with length 4 times sampling frequency og the complex vector array


data_fft=np.trim_zeros(data_fft, trim='fb')

data_log = 10*np.log10(np.abs(data_fft)**2)
sorted = np.argsort(data_log, axis=-1, kind=None, order=None)


freq = np.fft.fftfreq(n=round(len(data_log)), d=sample_period)


print("######## The 10 frequency with the highest power:########")
for i in range(10):
    ind = sorted[-i-1]
    print("frequency[HZ]:",freq[ind],"Power[dB]:",data_log[ind],)
print("######################## \n")

#need to find the doopler frequenzy f_D
f_D_index = np.argmax(data_log)
f_D = freq[f_D_index]




v = f_D*w/2
print("the doppler frequency is",f_D,"Hz")
print("the velocity is:", np.round(v,2),"m/s",)






#plotting the PSD
axs[1].plot(freq,data_log)
axs[1].set_xlabel("Frequency [Hz]")
axs[1].set_ylabel("Power [dB]")
axs[1].set_xlim(-2000,2000)
axs[1].set_ylim(0,140)
axs[1].grid(True)


# Add a table at the bottom of the axes

data_stopw = [0,1.140,1.135,1.125,0.964,0.964,0.964,-1.081,-1.081,-1.081]

cell_text = [[np.round(2413/15*data_stopw[dataset-1],2),data_stopw[dataset-1]],[f_D,np.round(v,3)],[np.round(2413/15*data_stopw[dataset-1],2)-f_D,np.round(data_stopw[dataset-1]-np.round(v,3),3)]]



columns = ('Doppler freq [Hz]', 'Velocity [m/s]')
rows = ["Stopwatch","Radar","Deviation"]
the_table = axs[2].table(cellText=cell_text,
                      rowLabels=rows,
                      colLabels=columns,
                        loc = "center",
                         bbox = [0, -0.3, 1, 0.9]
                      )
axs[2].axis('tight')
axs[2].axis('off')






plt.subplots_adjust(hspace=0.5)
plt.show()

signal = np.max(data_log)


rms = 10*np.log10(np.sqrt(np.mean(np.abs(x)**2)))
snr = signal-rms


print("SNR:",snr )

cell_text = []
rows = []
for i in range(10):
    rows.append(i)
    ind = sorted[-i-1]
    cell_text.append([freq[ind],np.round(data_log[ind],2)])



columns = ('Frequency[HZ]', 'Power[dB]')

plt.figure()
plt.title("The ten frequency's withe the most Power")
plt.table(cellText=cell_text,
                      rowLabels=rows,
                      colLabels=columns,
                        loc = "top",
                    bbox = [0, -0.3, 1, 0.75]
                      )

plt.axis('tight')
plt.axis('off')
plt.tight_layout()

plt.show()





