import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import csv

data= pd.read_csv('./Data/V5.txt',
                sep=';',
                header=None,
                names=["rechts",
                "links",
                "t"])

    
plt.plot(data.t,data.links,label='links')
plt.plot(data.t,data.rechts,label='rechts')
plt.legend(loc="best",frameon=True)
plt.show()
