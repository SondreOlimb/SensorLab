import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import Read_Bin


### Constants #####
Max_puls = 196 #https://www.ntnu.no/cerg/hfmax 16.03.21
Min_puls = 40 #Us National library of medicine
N_fft =40248
window = 51
fps = 40
#######

def autocorr(x):
    AC =[]




    result = signal.fftconvolve(x, x[::-1], mode='full')

    l = len(result)//2


    return result[l:]


def read_pulse(file_location,x_min,x_max):
    """

    :param file_location:
    :param x_min:
    :param x_max:
    :return:
    """
    try:
        raw_data = np.loadtxt(file_location)
    except:
        print("File:", file_location,"dose not exist")

    data = []

    for i in range(3):
        data.append(raw_data[:, i])


    #steg 2: detrend
    data = signal.detrend(data)


    #steg 3- Lavpassfilter
    b, a = signal.butter(10, Max_puls / 60, 'lp', analog=False, output="ba",fs=40)
    data = signal.lfilter(b, a,data)

    #steg 4-høypassfilter
    b, a = signal.butter(10, Min_puls / 60, 'hp', analog=False, output="ba",fs=40)
    data = signal.lfilter(b, a,data)




#### plot av rådata #####
    red = data[0]
    green = data[1]
    blue = data[2]

    fig, axs = plt.subplots(3, 1)

    # Plot rødt signal
    n = 0
    axs[n].plot(red, color="red")

    axs[n].set_ylabel('Amplitude')
    axs[n].set_xlabel('Sample [n]')
    axs[n].grid(True)

    # Plot grønt signal
    n = 1
    axs[n].plot(green, color="green")


    axs[n].set_ylabel('Amplitude')
    axs[n].set_xlabel('Sample [n]')
    axs[n].grid(True)

    # Plot blått signal
    n = 2
    axs[n].plot(blue, color="blue")

    axs[n].set_ylabel('Amplitude')
    axs[n].set_xlabel('Sample [n]')
    axs[n].grid(True)
    plt.draw()
    color = ["Red", "Green", "Blue"]

##############




    

    #steg 5 Hammming window
    data = data * signal.windows.hamming(len(raw_data))



    # steg 6 FFT
    data_fft = np.fft.fft(data, len(data[0]) * 10)  # FFT som er ti ganger lengere en datasettet.

    data_log = 10 * np.log10(np.abs(data_fft)**2) #gjør om FFT signalet til decibel


    sorted = np.argsort(data_log, axis=-1, kind=None, order=None)


    freq = np.fft.fftfreq(n=round(len(data_log[0])), d=1/40)


    ##### finner alle signal som ikke
    freq_noise = []
    data_noise = []
    data_signal = []
    data_log_slized =[]
    for n in range(3):
        data_log_slized.append(data_log)

        for i in range(len(freq) - 1, 0, -1):
            if freq[i] <= Min_puls / 60 or freq[i] >= Max_puls / 60:
                freq_noise.append(freq[i])
                data_noise.append(data_fft[n,i])

                freq_slized = np.delete(freq, i)

                data_log_slized[n] = np.delete(data_log[n], i)


    ##### Plot av Power spektrumet ######

    fig, axs = plt.subplots(3, 1)

    #Plot red power spectrum
    n=0
    axs[n].plot(freq,data_log[n], color = "red")
    axs[n].set_xlim(x_min,x_max)
    axs[n].set_ylim(0, 50)
    axs[n].set_ylabel('Power[dB]')
    axs[n].set_xlabel('Frequency[Hz]')
    axs[n].grid(True)

    #Plot green power spectrum
    n = 1
    axs[n].plot(freq, data_log[n], color="green")

    axs[n].set_xlim(x_min,x_max)

    axs[n].set_ylim(0, 50)
    axs[n].set_ylabel('Power[dB]')
    axs[n].set_xlabel('Frequency[Hz]')
    axs[n].grid(True)

    #Plot blue power spectrum
    n=2
    axs[n].plot(freq, data_log[n], color="blue")
    axs[n].set_xlim(x_min,x_max)
    axs[n].set_ylim(0, 50)
    axs[n].set_ylabel('Power[dB]')
    axs[n].set_xlabel('Frequency[Hz]')
    axs[n].grid(True)
    plt.draw()
    color =["Red","Green","Blue"]


    ####


    for i in range(3):



        #steg 7-9: finner Pulsen
        f_D_index = np.argmax(data_log[i])

        pulse = np.abs(freq[f_D_index]) * 60
        data_noise = []


        #finner FFT- amplituden til alle frekvenser som ikke er hjertefrekvensen
        for k in range(len(freq) - 1, 0, -1):
            if freq[f_D_index] != freq[n]:
                data_noise.append(data_fft[i, k])



        print("######################## \n")
        print(color[i], "channel:")
        print("channel: Pulse is", pulse,"[bpm]")

        # Bergener SNR
        signal = np.max(data_log[i])

        avg_noise = 20*np.log10(np.abs(np.average(data_noise[i])))


        SNR = signal-avg_noise

        print("SNR:", SNR,"[dB]\n")

    plt.show()

    return None





#read_pulse("trans_2_ex/jonas_puls2_1.txt",Min_puls / 60, Max_puls / 60)
#read_pulse("data1_ex/jonas_puls5.txt",-Max_puls / 60,Max_puls / 60)
#read_pulse("rob_1_ex/jonas_puls7_3.txt",-Max_puls / 60,Max_puls / 60)
read_pulse("ref_4_ex/jonas_puls6_4.txt",Min_puls / 60,Max_puls / 60)