
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 24 12:41:51 2021

Function to crop plotted cluster results to significant time intervals per subject.
Currently loads data per subject for A500s before, and A500s not before T500s.

@author: marta
"""

# Imports
import mne


# Data paths (for Marta's laptop/external hard drive)
data_path = '/Users/stojanovic/Downloads'
# data_path = '/Users/stojanovic/Documents/Projects/Cambridge/Analyses/Adaptor/NewEEGFilesAdaptor'

# Channels of interest
channels = ['E6', 'E13', 'E112', 'E7', 'E106']


def sub_data(data_path, subj_id):
    """
    Load epoch data per subject, concatenate across tones and return evoked array 
    per repetition of shape (n_channels, n_timepoints) for significant time interval.


    Parameters
    ----------
    data_path: str
        Path to folder containing .set data
    subj_id : str
        Name of subject to load

    Returns
    -------
    cropped_evoked : dict of mne.Evoked
        Dictionary of evoked points for sthe ignificant time interval 
        identified with plotted cluster test results

    """

    # Path to files
    
    #subject_setfile_wake_n = data_path + '/EEG_' + subj_id + '_wake.set'
    subject_setfile_sleep = data_path + '/EEG_' + subj_id + 'sleep.set' 
    
    
    # Read epochs from file 
    
    # epochs = mne.read_epochs_eeglab(subject_setfile_wake_n)
    epochs = mne.read_epochs_eeglab(subject_setfile_sleep)
    #epochs = mne.read_epochs_eeglab(subject_setfile_wake_m)

        
    # Define list of repetitions
    repetitions = ['0_bT', '1_bT', '2_bT', '3_bT', '4_bT'] # before T500s
    #repetitions = ['0', '1', '2', '3', '4'] # not before T500s
    
    
    # Create dictionary to store contents of loop
    cropped_evoked  = {}

    
    for rep in repetitions:
        
    # tones = ['T500'] 
        tones = ['A500']
    # tones = ['T650','T845','T1098','T1856','T2413','T3137','T4079','T5302']


    # Concatenate across tones
    # mean_across_chan = [] 
    
        for tone in tones:

        # Concatenate across tones
            evoked_list = []
            miniblock = tone + '_' + rep 
            evoked_list.append(epochs[miniblock])
        
        epochs_rep = mne.concatenate_epochs(evoked_list)
                
        # Grand averages for each repetition across subjects
    cropped_evoked[rep] = epochs_rep.average(picks = ['E6', 'E13', 'E112', 'E7', 'E106'])

      
    return cropped_evoked











##############################################################################

### 
# Questions/unclarities: I have the 'int' files here, whereas now I'm using the 
# referenced. I don't know whether this will make a difference in future analyses.

# For reading events from EEGLAB: 
# 'pip install pymatreader'
# conda install -c conda-forge pymatreader'



    
    #subject_setfile_wake_n = data_path + '/s_' + subj_id + '_wake_night_referenced.set'
    #subject_setfile_sleep  = data_path + '/s_' + subj_id + '_sleep_int.set'
    #subject_setfile_wake_m = data_path + '/s_' + subj_id + '_wake_morning_int.set'



    #     miniblock = tone + '_' + rep
    #     ev = epochs[miniblock].crop(tmin = -0.01, tmax = 0.448)
        
    #     # Select five fronto-central electrodes
    #     mean = ev.average(picks = ['E6', 'E13', 'E112', 'E7', 'E106'])
        
    #     # Average over the 5 channels
    #     mean_across_chan = mean.data.mean(axis = 0)
    #     mean_across_chan = mean.tolist()

    # # Store mean per repetition in dictionary
    # cropped_evoked[rep] = mean_across_chan




#tones = ['T650','T845','T1098','T1428','T1856','T2413','T3137','T4079','T5302']
#tones = ['N2T650','N2T845','N2T1098','N2T1856','N2T2413','N2T3137','N2T4079','N2T5302']
#tones = ['N3T650','N3T845','N3T1098','N3T1856','N3T2413','N3T3137','N3T4079','N3T5302']
#tones = ['RpT650','RpT845','RpT1098','RpT1856','RpT2413','RpT3137','RpT4079','RpT5302', 
        #'RtT650','RtT845','RtT1856','RtT2413','RtT4079','RtT5302']
 
#sig_interval = epochs[miniblock].crop(tmin = 0.000, tmax = 0.076) # N1 
#sig_interval = epochs[miniblock].crop(tmin = 0.000, tmax = 0.160) # N1 # contains 16 time points 
#sig_interval = epochs[miniblock].crop(tmin = 0.160, tmax = 0.275) # P2
#sig_interval = epochs[miniblock].crop(tmin = 0.315, tmax = 0.435) # N4
                
                