import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab4Functions as l4f
import csv

# data= pd.read_csv('./Data/validierung_beidseitig.txt',   # Bei Validierung: A0 --> links, A --> rechts
#                 sep=';',
#                 header=None,
#                 names=["links",
#                 "rechts",
#                 "t"])

    
# plt.plot(data.t,data.links,label='links')
# plt.plot(data.t,data.rechts,label='rechts')
# plt.legend(loc="best",frameon=True)
# plt.show()


# data= pd.read_csv('./Data/V5.txt',                  # Bei Experiment: A0 --> rechts, A1 --> links
#                 sep=';',
#                 header=None,
#                 names=["rechts",
#                 "links",
#                 "t"])

verena_data= l4f.import_data('verena',';')  

# fig, (ax1, ax2) = plt.subplots(1,2)
# ax1.plot(verena_data.t,verena_data.left)
# ax2.plot(verena_data.t,verena_data.right)
# plt.show()

# plt.plot(verena_data.t,verena_data.left,label='left')
# plt.plot(verena_data.t,verena_data.right,label='right')
# plt.legend(loc="best",frameon=True)
# plt.show()
 
david_data= l4f.import_data('david',';')  

# fig, (ax1, ax2) = plt.subplots(1,2)
# ax1.plot(david_data.t,david_data.left)
# ax2.plot(david_data.t,david_data.right)
# plt.show()

# plt.plot(david_data.t,david_data.left,label='left')
# plt.plot(david_data.t,david_data.right,label='right')
# plt.legend(loc="best",frameon=True)
# plt.show()

v_elmoffset = l4f.eliminateoffset(verena_data)
d_elmoffset = l4f.eliminateoffset(david_data)

v_filtered=l4f.filter(v_elmoffset)
d_filtered=l4f.filter(d_elmoffset)

v_rect= l4f.rectify(v_filtered)
d_rect= l4f.rectify(d_filtered)

v_env=l4f.envelope(v_rect,3)
d_env=l4f.envelope(d_rect,3)

# fig, axs = plt.subplots(5,2)
# axs[0,0].plot(verena_data.t,verena_data.right)
# axs[0,1].plot(verena_data.t,verena_data.left)
# axs[1,0].plot(verena_data.t,v_elmoffset.right)
# axs[1,1].plot(verena_data.t,v_elmoffset.left)
# axs[2,0].plot(verena_data.t,v_filtered.right)
# axs[2,1].plot(verena_data.t,v_filtered.left)
# axs[3,0].plot(verena_data.t,v_rect.right)
# axs[3,1].plot(verena_data.t,v_rect.left)
# axs[4,0].plot(verena_data.t,v_env.right)
# axs[4,1].plot(verena_data.t,v_env.left)
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

# vbursts_start, vbursts_end = l4f.get_bursts(v_filtered)
# print (vbursts_start,vbursts_end)
# dbursts_start, dbursts_end = l4f.get_bursts(d_filtered)
# print (dbursts_start,dbursts_end)

vbursts_start = [1108,13650,24295,34420,42619]
vbursts_end = [11777,22163,32263,40556,48638]
dbursts_start = [1048,19325,32549,43313,52553]
dbursts_end = [17209,30266,41206,50635,59900]

vindex_s, vindex_e = l4f.getindexforiso(vbursts_start,vbursts_end,verena_data.t)
dindex_s, dindex_e = l4f.getindexforiso(dbursts_start,dbursts_end,david_data.t)

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
# ax1.set_xlabel('Time within experiment')
# ax1.set_ylabel('Median Frequency (Hz)')
# ax1.legend(loc='best',frameon=True)
# ax1.set_title('Rechts')
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
# ax2.set_xlabel('Time within experiment')
# ax2.legend(loc='best',frameon=True)
# ax2.set_title('Links')
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
# ax1.set_xlabel('Time within experiment')
# ax1.set_ylabel('Median Frequency (Hz)')
# ax1.legend(loc='best',frameon=True)
# ax1.set_title('Rechts')
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
# ax2.set_xlabel('Time within experiment')
# ax2.legend(loc='best',frameon=True)
# ax2.set_title('Links')

# plt.show()

# plt.plot(verena_data.t,v_filtered.right)
# plt.plot(verena_data.t[vindex_s[0]:vindex_e[0]],v_filtered.right[vindex_s[0]:vindex_e[0]],color='red')
# plt.plot(verena_data.t[vindex_s[1]:vindex_e[1]],v_filtered.right[vindex_s[1]:vindex_e[1]],color='red')
# plt.plot(verena_data.t[vindex_s[2]:vindex_e[2]],v_filtered.right[vindex_s[2]:vindex_e[2]],color='red')
# plt.plot(verena_data.t[vindex_s[3]:vindex_e[3]],v_filtered.right[vindex_s[3]:vindex_e[3]],color='red')
# plt.plot(verena_data.t[vindex_s[4]:vindex_e[4]],v_filtered.right[vindex_s[4]:vindex_e[4]],color='red')
# plt.plot(verena_data.t[vindex_s[5]:vindex_e[5]],v_filtered.right[vindex_s[5]:vindex_e[5]],color='red')
# plt.plot(verena_data.t[vindex_s[6]:vindex_e[6]],v_filtered.right[vindex_s[6]:vindex_e[6]],color='red')
# plt.plot(verena_data.t[vindex_s[7]:vindex_e[7]],v_filtered.right[vindex_s[7]:vindex_e[7]],color='red')
# plt.plot(verena_data.t[vindex_s[8]:vindex_e[8]],v_filtered.right[vindex_s[8]:vindex_e[8]],color='red')
# plt.plot(verena_data.t[vindex_s[9]:vindex_e[9]],v_filtered.right[vindex_s[9]:vindex_e[9]],color='red')
# plt.plot(verena_data.t[vindex_s[10]:vindex_e[10]],v_filtered.right[vindex_s[10]:vindex_e[10]],color='red')
# plt.plot(verena_data.t[vindex_s[11]:vindex_e[11]],v_filtered.right[vindex_s[11]:vindex_e[11]],color='red')
# plt.plot(verena_data.t[vindex_s[12]:vindex_e[12]],v_filtered.right[vindex_s[12]:vindex_e[12]],color='red')
# plt.plot(verena_data.t[vindex_s[13]:vindex_e[13]],v_filtered.right[vindex_s[13]:vindex_e[13]],color='red')
# plt.plot(verena_data.t[vindex_s[14]:vindex_e[14]],v_filtered.right[vindex_s[14]:vindex_e[14]],color='red')
# plt.show()