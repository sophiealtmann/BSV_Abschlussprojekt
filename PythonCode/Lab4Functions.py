import numpy as np
from scipy import fftpack
from scipy import signal
import scipy
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

""" This function makes you choose beginning and end of a muscle activation with a plot by clicking.
    It is specifically made for the three BPK409 datasets (weights, mvc, fatigue)
    Input: mvc_emg_filtered, weights_emg_filtered, fatigue_emg_filtered
    Output: the 3 starts of the 3 mvc bursts, 3 ends of mvc burts, and same for weights fatigue
    mvc_start, mvc_end, weights_start, weights_end, fatigue_start, fatigue_end
   """
def get_bursts(emg_filtered):   
    def get_individual_burst(x):
        def tellme(s):
            print(s)
            plt.title(s, fontsize=16)
            plt.draw()
            
        plt.clf()
        plt.setp(plt.gca(), autoscale_on=True)
        plt.plot(x)
       
        tellme('Click once to start zoom') 
        plt.waitforbuttonpress()
        
        while True:
            tellme('Select two corners of zoom, enter/return key to finish')
            pts = plt.ginput(2, timeout=-1)
            if len(pts) < 2:
                break
            (x0, y0), (x1, y1) = pts
            xmin, xmax = sorted([x0, x1])
            ymin, ymax = sorted([y0, y1])
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
          
            
        tellme('Choose start of activity')    
        s = plt.ginput(1)
        tellme('Choose end of activity')   
        e = plt.ginput(1)
        s1 = s[0]
        e1 = e[0]
        start = int(s1[0].astype(int))
        end = int(e1[0].astype(int))
        plt.show()
        
        return start,end
    number_bursts = 5
    bursts_start = np.empty(number_bursts)
    bursts_end = np.empty(number_bursts)
    for i in range(number_bursts):
        bursts_start[i], bursts_end[i] = get_individual_burst(emg_filtered)
   
       
    bursts_start = bursts_start.astype(int)
    bursts_end = bursts_end.astype(int)
    
    
    return bursts_start, bursts_end

"""
This function gets the indices of the starts and ends of 3 0.5 sec sequencies in every burst of an EMG Data.
Those indices can be used to isolate the sequencies of the EMG-Data afterwards. 
Input:burst_start(array),burst_end(array),time(arraylike)
Output: index_s(array), index_e(array)
"""
def getindexforiso(burst_start,burst_end,time):
    start_s = np.zeros(len(burst_start))
    middle_s = np.zeros(len(burst_start))
    end_s = np.zeros(len(burst_start))

    start_e = np.zeros(len(burst_start))
    middle_e = np.zeros(len(burst_start))
    end_e = np.zeros(len(burst_start))

    for i in range(len(burst_start)):
        start_s[i]= time[burst_start[i]]+500
        tmp = burst_start[i]+((burst_end[i]-burst_start[i])/2)
        middle_s[i] = time[int(tmp)]
        end_s[i] = time[burst_end[i]]-1500
        start_e[i] = start_s[i]+500
        middle_e[i] = middle_s[i]+500
        end_e[i]= end_s[i]+500
    
    five_starts=[]
    five_ends=[]
    for j in range(len(burst_start)):
        five_starts.append(start_s[j])
        five_starts.append(middle_s[j])
        five_starts.append(end_s[j])
        five_ends.append(start_e[j])
        five_ends.append(middle_e[j])
        five_ends.append(end_e[j])

    five_starts= np.array(five_starts)
    five_ends= np.array(five_ends)

    index_s = np.zeros(len(five_starts))
    index_e = np.zeros(len(five_ends))
    
    for n in range(len(five_starts)):
        index_s[n] = np.argmin(np.abs(time-five_starts[n]))
        index_e[n] = np.argmin(np.abs(time-five_ends[n]))
    
    index_s = np.array(index_s,dtype= int)
    index_e = np.array(index_e,dtype= int)
    
    return index_s,index_e

def getmedian(index_s,index_e,emg_filtered):
    def get_power(data, sfreq):
        sig_fft = fftpack.fft(data)
    
        # And the power (sig_fft is of complex dtype)
        power = np.abs(sig_fft)
    
        # The corresponding frequencies
        sample_freq1 = fftpack.fftfreq(data.size, d=1/sfreq)
        frequencies = sample_freq1[sample_freq1 > 0]
        power = power[sample_freq1 > 0]
        return power, frequencies
    def getmedian(power,frequencies):
        area_freq= scipy.integrate.cumtrapz(power,frequencies, initial=0)
        total_power=area_freq[-1]
        median_freq= frequencies[np.where(area_freq >= total_power/2)[0][0]]
        return median_freq

    median_freqs=np.zeros(len(index_s))
    sampling=1000
    for i in range (len(index_s)):
        pwr,freq= get_power(emg_filtered[index_s[i]:index_e[i]],sampling)
        median_freqs[i]=getmedian(pwr,freq)

    return median_freqs