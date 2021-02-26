import numpy as np

import scipy.signal as signal
import matplotlib.pyplot as plt



###Constants####

Bit_depth = 2**12
V_ref = 3.3 #[V]
Sampling_freq = 31250


################


def raspi_import(path, channels=5):
    """
    Import data produced using adc_sampler.c.
    Returns sample period and ndarray with one column per channel.
    Sampled data for each channel, in dimensions NUM_SAMPLES x NUM_CHANNELS.
    """

    with open(path, 'r') as fid:
        sample_period = np.fromfile(fid, count=1, dtype=float)[0]
        data = np.fromfile(fid, dtype=np.uint16)
        data = data.reshape((-1, channels))
    return sample_period, data

def autocorr(x):
    AC =[]


    for i in range(5):
        sig = x[i]


        result = signal.fftconvolve(sig, sig[::-1], mode='full')

        l = len(result)//2

        AC.append(result[l:])
    return AC







def read_and_fft(path):
    """
    Calls on the function raspi_import to fetch the binary file and coverte it to readable data.

    It converts the data from bit to voltage and shifts it so x-axsis is the center of the resolution.
    It return the time axis and the corrected data

    Further it takes the FFT og the data and corrects the frequenzy axis befor it return the freq and FFT og the data


    """
    sample_period, data = raspi_import(path)
    sample_period *= 1e-6  # change unit to micro seconds
    # Generate time axis

    d = []
    for i in range(5):
        d.append(data[:,i][6000:])
    data = d


    data = signal.detrend(data)  # removes DC component for each channel
    #####num_of_samples = data.shape[0]  # returns shape of matrix
    num_of_samples = len(data[1])
    t = np.linspace(start=0, stop=num_of_samples * sample_period, num=num_of_samples)
    b, a = signal.butter(4,150, 'highpass', analog=False, output="ba",fs=Sampling_freq)
    data = signal.lfilter(b, a, data, axis=- 1,zi=None)  # finding the resolution and converting the bit value to the coresponding value in Volts

    b, a = signal.butter(6, 250, 'lowpass', analog=False, output="ba", fs=Sampling_freq)
    data = signal.lfilter(b, a, data, axis=- 1,zi=None)  # finding the resolution and converting the bit value to the coresponding value in Volts


    #data = autocorr(data)
    # Generate frequency axis and take FFT



    data_pre = data
    t_pre = t
    '''
    downsampling_factor =1
    data = signal.decimate(data,downsampling_factor)
    num_of_samples_after = round(len(data[1]))
    t = np.linspace(start=0, stop=num_of_samples * sample_period, num=num_of_samples_after)
    print(len(data[1]), len(t))

    
    '''
    #data = autocorr(data)


    #data = signal.fftconvolve(data, data[::-1], mode='full') ###takes the autocorelation of the signal to remove noice

    freq = np.fft.fftfreq(n=num_of_samples, d=sample_period)
    ####spectrum = np.fft.fft(data, axis=0)  # takes FFT of all channels

    spectrum = np.fft.fft(data)  # takes FFT of all channels




    return t, data,freq,spectrum,sample_period