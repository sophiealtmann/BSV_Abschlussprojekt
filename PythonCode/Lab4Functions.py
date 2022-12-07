import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import pandas as pd

""" 
This function imports five files of the Dead Hang experiment. It creates one variable for the EMG Data (emg_data)
and normalizes the time axis. The variables need to be in the working directory in the Data folder. 
name is the first name of the participant. name1, name2, name3, name4 ,name5 
A quite similar function was given for Lab 3 and edited for Lab 4 
Input: name(str), separator
Output: emg_data(df)

"""
def import_data(name,separator):
    """ This function is when you put together several datasets,
    but each dataset always starts with a time of 0.
    Input: dataframe that also has a column 't'
    Output: continuous time over all datasets
    """
    def time_norm(data):
        a = list(data.iloc[:]['t'])
        b = list(data.iloc[:]['t'])
        
        for u in range(len(a)-1):
            if a[u]>a[u+1]:
                if b[u]>b[u+1]:
                    offset = a[u]-a[u+1]+1
                    a[u+1] = offset + a[u+1]
                    u += 1
                else:
                    a[u+1] = offset + a[u+1]
                    u += 1
                      
        output = pd.DataFrame({'rechts': data.rechts,'links':data.links, 't': a})
        output.reset_index(inplace = True, drop = True)
        return output

    column_names = [
      'rechts',
      'links',
      't']
    # Creating an empty Dataframe with column names only
    emg_raw= pd.DataFrame(columns=column_names)

    # read all mvc, weight, and fatigue files 
    for i in range(5):
        # create string for path
        emg_string = './Data/' + str(name) + str(i+1) + '.txt'
        
        
        emg_raw = emg_raw.append(pd.read_csv(
            emg_string,
             sep=separator, names=column_names, skiprows= 50,
             skipfooter = 50
            ))

    # timing needs changing as the appended data starts from 0 again
    emg_data = time_norm(emg_raw)

    return emg_data