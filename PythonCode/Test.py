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
plt.plot(verena_data.t,verena_data.links,label='links')
plt.plot(verena_data.t,verena_data.rechts,label='rechts')
plt.legend(loc="best",frameon=True)
plt.show()
