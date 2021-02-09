import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import sys


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


# Import data from bin file
sample_period, data = raspi_import('RawData/d.bin')

#data = signal.detrend(data, axis=0)  # removes DC component for each channel
sample_period *= 1e-6  # change unit to micro seconds

# Generate time axis
num_of_samples = data.shape[0]  # returns shape of matrix
t = np.linspace(start=0, stop=num_of_samples*sample_period, num=num_of_samples)

# Generate frequency axis and take FFT
freq = np.fft.fftfreq(n=num_of_samples, d=sample_period)
spectrum = np.fft.fft(data, axis=0)  # takes FFT of all channels

data_voltage = 3.3/(2**12)*data  # finding the resolution and converting the bit value to the coresponding value in Volts
print("Resolution is:",3.3/(2**12))


# Plot the results in two subplots
# NOTICE: This lazily plots the entire matrixes. All the channels will be put into the same plots.
# If you want a single channel, use data[:,n] to get channel n
plot_color=["red","blue","green","purple","orange"]
for i in range(5):

    plt.subplot(2, 1, 1)
    plt.title("Time domain signal for ADC: "+str(i+1))
    plt.xlabel("Time [us]")
    plt.ylabel("Voltage")
    plt.plot(t[:1000], data_voltage[:,i][:1000],color=plot_color[i]) #slicing the array to make the signal readebol in the plot.


    plt.subplot(2, 1, 2)
    plt.title("Power spectrum of signal for ADC: "+str(i+1))
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power [dB]")

    plt.plot(freq, 20*np.log10(np.abs(spectrum[:,i])), color=plot_color[i]) # get the power spectrum
    plt.vlines(1000,0,100,label="1000Hz")
    plt.vlines(-1000, 0, 100)
    plt.xlim(-2000,2000)
    plt.legend()


    plt.show()



