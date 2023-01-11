
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

    # Create path to subject file (based on subject id)
    #subject_setfile_wake_n = data_path + '/EEG_' + subj_id + '_wake.set'
    subject_setfile_sleep = data_path + '/EEG_' + subj_id + '_sleep.set' 
    
    
    # Read epochs from file
    # epochs = mne.read_epochs_eeglab(subject_setfile_wake_n)
    epochs = mne.read_epochs_eeglab(subject_setfile_sleep)
    #epochs = mne.read_epochs_eeglab(subject_setfile_wake_m)

        
    # Define list of repetitions
    repetitions = ['0_bT', '1_bT', '2_bT', '3_bT', '4_bT'] # before T500s
    #repetitions = ['0', '1', '2', '3', '4'] # not before T500s
    
    
    # Create dictionary to store contents of loop
    cropped_evoked  = {}

    for rep in repetitions    
        # tones = ['T500'] 
        tones = ['A500'] # change prefix based on sleep stage aka conscious state
        # tones = ['T650','T845','T1098','T1856','T2413','T3137','T4079','T5302']


    # Concatenate across tones
        for tone in tones:
            evoked_list = []
            miniblock = tone + '_' + rep 
            evoked_list.append(epochs[miniblock])
        
        epochs_rep = mne.concatenate_epochs(evoked_list)
                
    # Store data per repetition across subjects for selected channels
    cropped_evoked[rep] = epochs_rep.average(picks = ['E6', 'E13', 'E112', 'E7', 'E106'])

      
    return cropped_evoked
