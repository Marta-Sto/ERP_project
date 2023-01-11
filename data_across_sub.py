#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 21:36:28 2022

@author: stojanovic

"""

# Import function to load data per subject 
from data_per_sub import sub_data

# Data paths (for Marta's laptop/external hard drive)
data_path = '/Users/stojanovic/Downloads'
#data_path   = 'D:/ica_interpolated'
#data_path  = '/Volumes/New Volume/ica_interpolated'
# data_path = '/Users/stojanovic/Documents/Projects/Cambridge/Analyses/Adaptor/NewEEGFilesAdaptor'


def across_sub(data_path):
    """
    Load cropped data per repetition across subjects.

    Parameters
    ----------
    data_path : str
        Path to data files

    Returns
    -------
    cropped_ERP : dict of mne.Evoked concatenated across tones and subjects 
                per repetition

    """

    # Add complete subject list (check subject 08 for A500_0_bT in wake)
    subjects = ['01','02','03','04','05','06','07','17','19','20','21', 
                '23','24','25','26','27','28','29','30','31','32',
                '33','34','35','36','37','38']    

    ### Get evoked potentials per repetition across subjects in dictionary ###
    
    crop_tone_ERP = {}
    
    for subject in subjects:      
        sub_dict = sub_data(data_path, subject) 
        # Create dictionary for data across subjects 
        for k in sub_dict:
            # Append data per subject to dictionary 
            if k not in crop_tone_ERP:
                crop_tone_ERP[k] = []
            crop_tone_ERP[k].append(sub_dict[k])
                   
    return crop_tone_ERP
