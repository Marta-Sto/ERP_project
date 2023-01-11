#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 23:12:01 2023

@author: stojanovic

Function to plot significant clusters in time points
between the first and last tone repetition across subjects.

@author: marta
"""

import mne
import matplotlib.pyplot as plt 

def plot_cluster_results(ERP, cluster_stat): 
    """
    Plot results of cluster test with significant clusters.    

    Parameters
    ----------
    ERP : dict
        Evoked objects across subjects per repetition.
    cluster_stat : tuple
        T-statistics, list of significant clusters, p-statistic for significant
        cluster, and number of permutations.

    Returns
    -------
    Plot with shaded area for significant time points.

    """
    
    mne.viz.plot_compare_evokeds(ERP, combine = 'mean',
                                      title = 'Evoked potential across first five repetitions') 
    ax = plt.gca() # get current axis 
    
    cluster_times = cluster_stat[1]
    p_values = cluster_stat[2] 
    
    for t, p in zip(cluster_times, p_values):
        if p < 0.05:
            start = ERP['0_bT'][0].times[t[0][0]]
            end   = ERP['0_bT'][0].times[t[0][-1]]
            print(start)
            print(end)
            print(p)
            #import pdb; pdb.set_trace()
            ax.axvspan(start, end, alpha = 0.3, facecolor='black')
            
    plt.show()
    
