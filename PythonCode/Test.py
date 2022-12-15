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
dbursts_start =[1048,19325,32549,43313,52553]
dbursts_end = [17209,30266,41206,50635,59900]