import ReadFile as read
import numpy as np
import matplotlib.pyplot as plt


frek,ch1,ch2 = read.readnetwoek("RawData/frek-res.csv")


fig = plt.figure()
plt.plot(frek,ch1,color = "BLUE", label=r"$v_inn$",linewidth=1)
plt.plot(frek,ch2,color = "RED", label=r"$v_out$",linewidth=1)
plt.legend(bbox_to_anchor=(1,1),loc="upper right")
#plt.grid()
plt.xlabel("$Frekvens$ [Hz]")
plt.ylabel("$Demping$ [dB]")

plt.plot([6.5], [-3], 'o')
plt.annotate('(6.5,-3)', xy=(20, -3), xytext=(20, -4))
plt.savefig("frekvens")
plt.show()