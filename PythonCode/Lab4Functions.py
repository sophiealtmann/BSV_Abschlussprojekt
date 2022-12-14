import numpy as np
from scipy import fftpack
from scipy import signal
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
                      
        output = pd.DataFrame({'right': data.right,'left':data.left, 't': a})
        output.reset_index(inplace = True, drop = True)
        return output

    column_names = [
      'right',
      'left',
      't']
    # Creating an empty Dataframe with column names only

    emg_raw = pd.DataFrame(columns=column_names)

    for i in range(5):
        # create string for path
        emg_string = './Data/' + str(name) + str(i+1) + '.txt'
        
        
        emg_raw = emg_raw.append(pd.read_csv(
            emg_string,
             sep=separator, names=column_names, skiprows= 50,
             skipfooter = 50, engine='python'
            ))

    # timing needs changing as the appended data starts from 0 again
    emg_data = time_norm(emg_raw)

    return emg_data

"""
This function elimates the offset of the EMG-Data. It creates a new DataFrame which includes the columns right and left. 
The data stays the same except the elimination of the DC offset. The input has to be a Dataframe including the columns right and left. 
Input: emg(df)
Output: nooffset(df)
"""
def eliminateoffset(emg):
    nooffset_r = emg.right - np.mean(emg.right)
    nooffset_l= emg.left - np.mean(emg.left)
    nooffset=pd.DataFrame({'right':nooffset_r,'left':nooffset_l})
    return nooffset

"""
This function filters the EMG-Data with an Bandpass filter. It creates a new DataFrame which includes the columns right and left.
The Bandpass is between 20 and 450 Hz. Wn = cutoff-frequency devided by half of the samplingrate.  
The input has to be a Dataframe including the columns right and left.
Input: nooffset(df)
Output: emg_filtered(df)
"""
def filter(nooffset):
    b, a = signal.butter(4, 20/500 , "high", analog=False)
    emgr_filthigh= signal.filtfilt(b, a , nooffset.right)
    emgl_filthigh= signal.filtfilt(b, a , nooffset.left)

    d, c = signal.butter(4, 450/500 , "low", analog=False)
    emgr_filtered= signal.filtfilt(d, c , emgr_filthigh)
    emgl_filtered= signal.filtfilt(d, c , emgl_filthigh)

    emg_filtered= pd.DataFrame({'right':emgr_filtered,'left':emgl_filtered})
    
    return emg_filtered

"""
This Funtion rectifies the EMG-Data. All negative values are replaced by their absulte value. 
It creates a new DataFrame which includes the columns right and left. The input has to be a Dataframe including the columns right and left.
Input:emg_filtered(df)
Ouput:emg_rect(df)
"""
def rectify(emg_filtered):
    emgr_rect = []
    for i in range(len(emg_filtered.right)):
        if emg_filtered.right[i] <= 0:
            emgr_rect.append(abs(emg_filtered.right[i])) 
        else:
            emgr_rect.append(emg_filtered.right[i])
        
    emgr_rectified= np.array(emgr_rect)
    emgl_rect = []
    for i in range(len(emg_filtered.left)):
        if emg_filtered.left[i] <= 0:
            emgl_rect.append(abs(emg_filtered.left[i])) 
        else:
            emgl_rect.append(emg_filtered.left[i])
        
    emgl_rectified= np.array(emgl_rect)

    emg_rect= pd.DataFrame({'right':emgr_rectified,'left':emgl_rectified})
    
    return emg_rect

"""
This funtion creates the enveloping function of the EMG-Data. Therefore the rectified is filtered with a lowpass filter. 
It creates a new DataFrame which includes the columns right and left. The input emg_rect has to be a Dataframe including the columns right and left.
In order to create an enveloping function the Cutoff-Frequency should be about 3 Hz.
Input: emg_rect(df), co_freq(int)
Output: emg_env(df)
"""
def envelope(emg_rect, co_freq):
    b, a = signal.butter(4, co_freq/500 , "low", analog=False )
    emgr_env= signal.filtfilt(b, a , emg_rect.right)
    emgl_env= signal.filtfilt(b, a , emg_rect.left)

    emg_env=pd.DataFrame({'right':emgr_env,'left':emgl_env})
    return emg_env