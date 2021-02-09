import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal


import Read_Bin

sampling = 31250

t, data, freq, spectrum = Read_Bin.read_and_fft("RawData/0_deg.bin")

def time_delay(m_1,m_2,f_s):
    """
    This fuction calculates the cross correlation of the signal m_1, and m_2

    It returns the time delay between the two singals in number of samples and in time
    :param m_1:
    :param m_2:
    :return:
    """

    upsamp_fact = 16

    upsampling_freq =len(m_1)*upsamp_fact

    m_1_upsampled = signal.resample(m_2,upsampling_freq)
    m_2_upsampled = signal.resample(m_1,upsampling_freq)
    r=np.correlate(m_1_upsampled,m_2_upsampled[7*upsamp_fact:-7*upsamp_fact] ,"valid")#Calculates the cross coreleation of the two arrays m_1 and m_2

    #r = np.correlate(m_1, m_2[7 :-7],"valid")  # Calculates the cross coreleation of the two arrays m_1 and m_2


    l = np.argmax(r) -7*upsamp_fact
    #l = np.argmax(r)

    delta_t = l/(f_s*16) #calculates the time delay in time [s]



    #plt.plot(m_1)
    #plt.show()
    #plt.plot(m_1_upsampled)
    #plt.show()
    plt.plot(r)
    plt.show()

    return delta_t,l


def get_angle(m_1,m_2,m_3):
    cros_m_1_m_2 = time_delay(m_1, m_2, sampling)
    cros_m_1_m_3 = time_delay(m_1, m_3, sampling)
    cros_m_2_m_3 = time_delay(m_2, m_3, sampling)

    n_21 = cros_m_1_m_2[1]
    n_31 = cros_m_1_m_3[1]
    n_32 = cros_m_2_m_3[1]

    teta = np.arctan2(np.sqrt(3)*(n_21+n_31),(n_21+n_31-2*n_32))


    return teta






cros_m_1_m_2 = time_delay(data[2],data[3],sampling)
cros_m_1_m_3 = time_delay(data[2],data[4],sampling)
cros_m_2_m_3 = time_delay(data[3],data[4],sampling)




#print(cros_m_1_m_2[0])
#print(cros_m_1_m_3[0])
#print(cros_m_2_m_3[0])

def from_file_to_angle(filename):

    t, data, freq, spectrum = Read_Bin.read_and_fft(filename)
    angle = get_angle(data[2],data[3],data[4])

    print("The angel of the sound is", np.degrees(get_angle(data[2],data[3],data[4])))
    return angle

#angle = from_file_to_angle("RawData/0_deg.bin")

angle_array=[]
for i in range(1,11):
    name = "data_1m/"+str(i)+".bin"
    angle = from_file_to_angle(name)
    angle_array.append(angle)

var = np.var(angle_array,ddof=1)
print(np.degrees(np.sqrt(var)))

