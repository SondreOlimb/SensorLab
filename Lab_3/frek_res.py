import ReadFile as read
import numpy as np
import matplotlib.pyplot as plt


frek,ch1,ch2 = read.readnetwoek("Raw_data/frek-res.csv")



print(frek)

frek = 10*np.log10(frek)
x_ticks_lable = 10**(frek/10)




fig = plt.figure()
plt.plot(frek[15:],ch1[15:],color = "BLUE", label=r"$V_{inn}$",linewidth=1)
plt.plot(frek[15:],ch2[15:],color = "RED", label=r"$V_{out}$",linewidth=1)

plt.legend(bbox_to_anchor=(1,1),loc="upper right")
plt.xlabel("$Frekvens$ [Hz]")
plt.ylabel("$Forsterking$ [dB]")
plt.xscale("linear")
plt.grid()
plt.xticks(frek[15::12],labels=round(x_ticks_lable[15::12],2))






#plt.plot([3.5], [19], 'o')
#plt.annotate('(3.5,19)', xy=(20, 19), xytext=(20, -4))
plt.savefig("frekvens")
#plt.tight_layout()
plt.show()