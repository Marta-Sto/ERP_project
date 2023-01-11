#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 01:50:56 2023

@author: stojanovic
"""

# Imports
import mne
import numpy as np
from data_across_sub import across_sub
#from scripttoplot import plot_cluster_results
from plot_clusters import plot_cluster_results


############ PIPELINE ############

data_path = '/Users/stojanovic/Documents/Projects/Cambridge/Analyses/Adaptor/NewEEGFilesAdaptor'

# Load dict of two lists, average for each subject for first and last repetition
ERP = across_sub(data_path) 

### Get array to pass to permutation cluster test using list comprehension ###
X = np.vstack([first.data.mean(axis=0) - last.data.mean(axis=0) for first,last in zip(ERP['0'],ERP['4'])]) # can change to 3

diff_stat = mne.stats.permutation_cluster_1samp_test(X) 

### Plot cluster results ###
cluster_results = plot_cluster_results(ERP, diff_stat)
