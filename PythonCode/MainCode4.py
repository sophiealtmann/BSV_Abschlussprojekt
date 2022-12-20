import numpy as np
import matplotlib.pyplot as plt
import Lab4Functions as l4f
import pandas as pd
import csv

"""
Dieser Code dient zur Analyse der im Dead Hang Experiment aufgenommenen Daten. Die Validierung unseres Systems,
sowie das Erstellen aller Plots wurde einmal durchgeführt und danach auskommentiert. 
Das auskommentieren der Plots dient zur einfacheren Weiterverarbeitung. 
Damit der Code funktioniert muss die Datei Lab4Functoins im selben ordner sein. 
"""

#Validierung unseres Mess-Systems

# data= pd.read_csv('./Data/validierung_beidseitig.txt',   # Bei Validierung: A0 --> links, A --> rechts
#                 sep=';',
#                 header=None,
#                 names=["links","rechts",
#                 "t"])

# rechts= pd.read_csv('./Data/validierung_rechts.txt',
#                   sep=";",
#                   header=None,
#                   names=[ "rechts",
#                   "t"])
# links= pd.read_csv('./Data/validierung_links.txt',   
#                   sep=';',
#                   header=None,
#                   names=[ "links",
#                   "t"])

# plt.plot(data.t/1000, data.links, label="Left")
# plt.plot(data.t/1000, data.rechts, label="Right")
# plt.xlabel('Time / s')
# plt.legend()
# plt.ylabel('Voltage / mV')
# plt.savefig("./Plots/validierung_beidseitig.svg")
# plt.show()

# fig, (ax1, ax2) = plt.subplots(1,2)
# ax1.plot(links.t/1000, links.links,)
# ax2.plot(rechts.t/1000, rechts.rechts,color='orange')
# ax1.set_ylim([1350,1650])
# ax2.set_ylim([1350,1650])
# ax1.set_xlabel('Time / s')
# ax2.set_xlabel('Time / s')
# ax1.set_ylabel('Voltage / mV')
# ax1.set_title("Left")
# ax2.set_title("Right")
# plt.savefig("./Plots/validierung.svg")
# plt.show()


# data= pd.read_csv('./Data/V5.txt',                  # Bei Experiment: A0 --> rechts, A1 --> links
#                 sep=';',
#                 header=None,
#                 names=["rechts",
#                 "links",
#                 "t"])

# Import der EMG-Daten 
verena_data= l4f.import_data('verena',';')  
david_data= l4f.import_data('david',';')  

# Vorverarbeitung der Datensätze 

v_elmoffset = l4f.eliminateoffset(verena_data)
d_elmoffset = l4f.eliminateoffset(david_data)

v_filtered=l4f.filter(v_elmoffset)
d_filtered=l4f.filter(d_elmoffset)

v_rect= l4f.rectify(v_filtered)
d_rect= l4f.rectify(d_filtered)

v_env=l4f.envelope(v_rect,3)
d_env=l4f.envelope(d_rect,3)

# fig, axs = plt.subplots(5,2)
# axs[0,0].plot(verena_data.t/1000,verena_data.right)
# axs[0,0].set_title('Right')
# axs[0,1].plot(verena_data.t/1000,verena_data.left)
# axs[0,1].set_title('Left')
# axs[1,0].plot(verena_data.t/1000,v_elmoffset.right)
# axs[1,1].plot(verena_data.t/1000,v_elmoffset.left)
# axs[2,0].plot(verena_data.t/1000,v_filtered.right)
# axs[2,0].set_ylabel('Voltage / mV')
# axs[2,1].plot(verena_data.t/1000,v_filtered.left)
# axs[3,0].plot(verena_data.t/1000,v_rect.right)
# axs[3,1].plot(verena_data.t/1000,v_rect.left)
# axs[4,0].plot(verena_data.t/1000,v_env.right)
# axs[4,0].set_xlabel('Time / s')
# axs[4,1].plot(verena_data.t/1000,v_env.left)
# axs[4,1].set_xlabel('Time / s')
# fig.align_ylabels(axs) 
# plt.subplots_adjust(left=0.125,
#                     bottom=0.1, 
#                     right=0.9, 
#                     top=0.9, 
#                     wspace=0.2, 
#                     hspace=0.35)
# plt.savefig('./Plots/vorverarbeitung.svg')
# plt.show()

# fig, axs = plt.subplots(5,2)
# axs[0,0].plot(david_data.t,david_data.right)
# axs[0,1].plot(david_data.t,david_data.left)
# axs[1,0].plot(david_data.t,d_elmoffset.right)
# axs[1,1].plot(david_data.t,d_elmoffset.left)
# axs[2,0].plot(david_data.t,d_filtered.right)
# axs[2,1].plot(david_data.t,d_filtered.left)
# axs[3,0].plot(david_data.t,d_rect.right)
# axs[3,1].plot(david_data.t,d_rect.left)
# axs[4,0].plot(david_data.t,d_env.right)
# axs[4,1].plot(david_data.t,d_env.left)
# plt.show()

# Auswählen der Aktivitäts-Bursts

# vbursts_start, vbursts_end = l4f.get_bursts(v_filtered)   # Zur Vereinfachung wurde dies Funktion nur einmalausgeführt 
# print (vbursts_start,vbursts_end)                         # und danach in den folgenden Variablen abgespeichert
# dbursts_start, dbursts_end = l4f.get_bursts(d_filtered)
# print (dbursts_start,dbursts_end)

vbursts_start = [1108,13650,24295,34420,42619]
vbursts_end = [11777,22163,32263,40556,48638]
dbursts_start = [1048,19325,32549,43313,52553]
dbursts_end = [17209,30266,41206,50635,59900]

# Berechnung der Dauer der Übungen
v_duration=[]
d_duration=[]
for x in range(5):
   v_duration.append((verena_data.t[vbursts_end[x]]-verena_data.t[vbursts_start[x]])/1000)
   d_duration.append((david_data.t[dbursts_end[x]]-david_data.t[dbursts_start[x]])/1000)

bursts=[1,2,3,4,5]

# duration_values=[['Proband','1.Runde Dauer / s','2.Runde Dauer / s','3.Runde Dauer / s','4.Runde Dauer / s','5.Runde Dauer / s'],  
#         ['1 - Rechtshaender',int(v_duration[0]),int(v_duration[1]),int(v_duration[2]),int(v_duration[3]),int(v_duration[4])],                                   
#         ['2 - Linkshaender',int(d_duration[0]),int(d_duration[1]),int(d_duration[2]),int(d_duration[3]),int(d_duration[4])]]
# with open('./Plots/duration.csv','w') as file: 
#     writer=csv.writer(file)
#     for row in duration_values:
#         writer.writerow(row)
#     file.close()

# plt.scatter(bursts,v_duration,marker='*')
# plt.plot(bursts,v_duration,label='Subject 1')
# plt.scatter(bursts,d_duration,marker='*')
# plt.plot(bursts,d_duration,label='Subject 2')
# plt.xticks(bursts)
# plt.xlabel('Repetition')
# plt.ylabel('Duration / s')
# plt.legend(loc='best',frameon=True)
# plt.savefig('./Plots/duration.svg')
# plt.show()

# Berechnung der mittleren Muskelkontraktion während eines Bursts.

vmean_right=[]
vmean_left=[]
dmean_right=[]
dmean_left=[]

for i in range(5):
   vmean_right.append(np.mean(v_env.right[vbursts_start[i]:vbursts_end[i]]))
   vmean_left.append(np.mean(v_env.left[vbursts_start[i]:vbursts_end[i]]))
   dmean_right.append(np.mean(d_env.right[dbursts_start[i]:dbursts_end[i]]))
   dmean_left.append(np.mean(d_env.left[dbursts_start[i]:dbursts_end[i]]))

v_meanoverall_r= np.mean(vmean_right)
v_meanoverall_l= np.mean(vmean_left)
d_meanoverall_r= np.mean(dmean_right)
d_meanoverall_l= np.mean(dmean_left)

v_mean= (v_meanoverall_r+v_meanoverall_l)/2
d_mean= (d_meanoverall_r+d_meanoverall_l)/2

 
# mean_values=[['Proband','Links / mV','Rechts / mV','Global / mV'],  
#         ['1 - Rechtshaender',round(v_meanoverall_l,2),round(v_meanoverall_r,2),round(v_mean,2)],                                   
#         ['2 - Linkshaender',round(d_meanoverall_l,2), round(d_meanoverall_r,2), round( d_mean,2)]]
# with open('./Plots/mean_contraction.csv','w') as file: 
#     writer=csv.writer(file)
#     for row in mean_values:
#         writer.writerow(row)
#     file.close()


# plt.scatter(bursts,(vmean_right/v_mean)*100,marker='*')
# plt.plot(bursts,(vmean_right/v_mean)*100,label='Right')
# plt.scatter(bursts,(vmean_left/v_mean)*100,marker='*')
# plt.plot(bursts,(vmean_left/v_mean)*100,label='Left')
# plt.xticks(bursts)
# plt.xlabel('Repetition')
# plt.ylabel('Musclecontraction / % of average')
# plt.legend(loc='best',frameon=True)
# plt.savefig('./Plots/verena_aktivität.svg')
# plt.show()

# plt.scatter(bursts,(dmean_right/d_mean)*100,marker='*')
# plt.plot(bursts,(dmean_right/d_mean)*100,label='Right')
# plt.scatter(bursts,(dmean_left/d_mean)*100,marker='*')
# plt.plot(bursts,(dmean_left/d_mean)*100,label='Left')
# plt.xticks(bursts)
# plt.xlabel('Repetition')
# plt.ylabel('Musclecontraction / % of average')
# plt.legend(loc='best',frameon=True)
# plt.savefig('./Plots/david_aktivität.svg')
# plt.show()


vindex_s, vindex_e = l4f.getindexforiso(vbursts_start,vbursts_end,verena_data.t)
dindex_s, dindex_e = l4f.getindexforiso(dbursts_start,dbursts_end,david_data.t)
pwr,freq= l4f.get_power(v_filtered.right[vindex_s[9]:vindex_e[9]],1000)
median=l4f.get_indivmedian(pwr,freq)
pwrfilt= l4f.freqfilt(pwr)

# plt.plot(freq,pwr/10,label='Unfiltered Power')
# plt.plot(freq,pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=median,color='green',label='Median')
# plt.xlabel('Frequency / Hz')
# plt.ylabel('Power / dB')
# plt.legend(loc="best",frameon=True)
# plt.savefig('./Plots/frequenzanalyse.svg')
# plt.show()

vrmedian_freqs = l4f.getmedian(vindex_s,vindex_e,v_filtered.right)
vrburst1_median = vrmedian_freqs[0:3]
vrburst2_median = vrmedian_freqs[3:6]
vrburst3_median = vrmedian_freqs[6:9]
vrburst4_median = vrmedian_freqs[9:12]
vrburst5_median = vrmedian_freqs[12:15]

vlmedian_freqs = l4f.getmedian(vindex_s,vindex_e,v_filtered.left)
vlburst1_median = vlmedian_freqs[0:3]
vlburst2_median = vlmedian_freqs[3:6]
vlburst3_median = vlmedian_freqs[6:9]
vlburst4_median = vlmedian_freqs[9:12]
vlburst5_median = vlmedian_freqs[12:15]

drmedian_freqs = l4f.getmedian(dindex_s,dindex_e,d_filtered.right)
drburst1_median = drmedian_freqs[0:3]
drburst2_median = drmedian_freqs[3:6]
drburst3_median = drmedian_freqs[6:9]
drburst4_median = drmedian_freqs[9:12]
drburst5_median = drmedian_freqs[12:15]

dlmedian_freqs = l4f.getmedian(dindex_s,dindex_e,d_filtered.left)
dlburst1_median = dlmedian_freqs[0:3]
dlburst2_median = dlmedian_freqs[3:6]
dlburst3_median = dlmedian_freqs[6:9]
dlburst4_median = dlmedian_freqs[9:12]
dlburst5_median = dlmedian_freqs[12:15]

median_time=['start','middle','end']

# fig,(ax1,ax2)=plt.subplots(1,2)
# ax1.scatter(median_time,vrburst1_median,marker='*')
# ax1.plot(median_time,vrburst1_median,label="1st cycle")
# ax1.scatter(median_time,vrburst2_median,marker='*')
# ax1.plot(median_time,vrburst2_median,label="2nd cycle")
# ax1.scatter(median_time,vrburst3_median,marker='*')
# ax1.plot(median_time,vrburst3_median,label="3rd cycle")
# ax1.scatter(median_time,vrburst4_median,marker='*')
# ax1.plot(median_time,vrburst4_median,label="4th cycle")
# ax1.scatter(median_time,vrburst5_median,marker='*')
# ax1.plot(median_time,vrburst5_median,label="5th cycle")
# ax1.set_xlabel('Time within one repetition')
# ax1.set_ylabel('Median Frequency / Hz')
# ax1.legend(loc='best',frameon=True)
# ax1.set_title('Right')
# ax2.scatter(median_time,vlburst1_median,marker='*')
# ax2.plot(median_time,vlburst1_median,label="1st cycle")
# ax2.scatter(median_time,vlburst2_median,marker='*')
# ax2.plot(median_time,vlburst2_median,label="2nd cycle")
# ax2.scatter(median_time,vlburst3_median,marker='*')
# ax2.plot(median_time,vlburst3_median,label="3rd cycle")
# ax2.scatter(median_time,vlburst4_median,marker='*')
# ax2.plot(median_time,vlburst4_median,label="4th cycle")
# ax2.scatter(median_time,vlburst5_median,marker='*')
# ax2.plot(median_time,vlburst5_median,label="5th cycle")
# ax2.set_xlabel('Time within one repetition')
# ax2.set_title('Left')
# ax1.set_ylim([100,240])
# ax2.set_ylim([100,240])
# plt.savefig('./Plots/verena_mediane.svg')
# plt.show()

# fig,(ax1,ax2)=plt.subplots(1,2)
# ax1.scatter(median_time,drburst1_median,marker='*')
# ax1.plot(median_time,drburst1_median,label="1st cycle")
# ax1.scatter(median_time,drburst2_median,marker='*')
# ax1.plot(median_time,drburst2_median,label="2nd cycle")
# ax1.scatter(median_time,drburst3_median,marker='*')
# ax1.plot(median_time,drburst3_median,label="3rd cycle")
# ax1.scatter(median_time,drburst4_median,marker='*')
# ax1.plot(median_time,drburst4_median,label="4th cycle")
# ax1.scatter(median_time,drburst5_median,marker='*')
# ax1.plot(median_time,drburst5_median,label="5th cycle")
# ax1.set_xlabel('Time within one repetition')
# ax1.set_ylabel('Median Frequency / Hz')
# ax1.legend(loc='best',frameon=True)
# ax1.set_title('Right')
# ax2.scatter(median_time,dlburst1_median,marker='*')
# ax2.plot(median_time,dlburst1_median,label="1st cycle")
# ax2.scatter(median_time,dlburst2_median,marker='*')
# ax2.plot(median_time,dlburst2_median,label="2nd cycle")
# ax2.scatter(median_time,dlburst3_median,marker='*')
# ax2.plot(median_time,dlburst3_median,label="3rd cycle")
# ax2.scatter(median_time,dlburst4_median,marker='*')
# ax2.plot(median_time,dlburst4_median,label="4th cycle")
# ax2.scatter(median_time,dlburst5_median,marker='*')
# ax2.plot(median_time,dlburst5_median,label="5th cycle")
# ax2.set_xlabel('Time within one repetition')
# ax2.legend(loc='best',frameon=True)
# ax1.set_ylim([90,200])
# ax2.set_ylim([90,200])
# ax2.set_title('Left')
# plt.savefig('./Plots/david_mediane.svg')
# plt.show()

# plt.plot(verena_data.t/1000,v_filtered.right,label='filtered data')
# plt.plot(verena_data.t[vindex_s[0]:vindex_e[0]]/1000,v_filtered.right[vindex_s[0]:vindex_e[0]],color='red',label='isolated timeslots')
# plt.plot(verena_data.t[vindex_s[1]:vindex_e[1]]/1000,v_filtered.right[vindex_s[1]:vindex_e[1]],color='red')
# plt.plot(verena_data.t[vindex_s[2]:vindex_e[2]]/1000,v_filtered.right[vindex_s[2]:vindex_e[2]],color='red')
# plt.plot(verena_data.t[vindex_s[3]:vindex_e[3]]/1000,v_filtered.right[vindex_s[3]:vindex_e[3]],color='red')
# plt.plot(verena_data.t[vindex_s[4]:vindex_e[4]]/1000,v_filtered.right[vindex_s[4]:vindex_e[4]],color='red')
# plt.plot(verena_data.t[vindex_s[5]:vindex_e[5]]/1000,v_filtered.right[vindex_s[5]:vindex_e[5]],color='red')
# plt.plot(verena_data.t[vindex_s[6]:vindex_e[6]]/1000,v_filtered.right[vindex_s[6]:vindex_e[6]],color='red')
# plt.plot(verena_data.t[vindex_s[7]:vindex_e[7]]/1000,v_filtered.right[vindex_s[7]:vindex_e[7]],color='red')
# plt.plot(verena_data.t[vindex_s[8]:vindex_e[8]]/1000,v_filtered.right[vindex_s[8]:vindex_e[8]],color='red')
# plt.plot(verena_data.t[vindex_s[9]:vindex_e[9]]/1000,v_filtered.right[vindex_s[9]:vindex_e[9]],color='red')
# plt.plot(verena_data.t[vindex_s[10]:vindex_e[10]]/1000,v_filtered.right[vindex_s[10]:vindex_e[10]],color='red')
# plt.plot(verena_data.t[vindex_s[11]:vindex_e[11]]/1000,v_filtered.right[vindex_s[11]:vindex_e[11]],color='red')
# plt.plot(verena_data.t[vindex_s[12]:vindex_e[12]]/1000,v_filtered.right[vindex_s[12]:vindex_e[12]],color='red')
# plt.plot(verena_data.t[vindex_s[13]:vindex_e[13]]/1000,v_filtered.right[vindex_s[13]:vindex_e[13]],color='red')
# plt.plot(verena_data.t[vindex_s[14]:vindex_e[14]]/1000,v_filtered.right[vindex_s[14]:vindex_e[14]],color='red')
# plt.xlabel('Time / s')
# plt.ylabel('Voltage / mV')
# plt.legend(loc='best', frameon=True)
# plt.savefig('./Plots/isolate.svg')
# plt.show()