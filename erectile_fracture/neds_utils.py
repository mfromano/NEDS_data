from __future__ import print_function
from __future__ import division

import os
import os.path
import sys
import csv
import numpy as np
import logging
import re
import math
import scipy.special


''' 
    The next function returns a list containing the data types for each column
    of the NEDS Core data file
'''
def get_data_type():
    data_labels = {}
    data_type = []
    with open('raw_data/NEDS_2012_Labels_Core.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_labels[currline[0]] = currline[1]
            data_type.append(currline[0])
    return data_type

''' 
    The next function returns a list containing the data types for each column
    of the NEDS ED Supplement data file
'''
def get_data_type_ed_supplement():
    data_type = []
    with open('raw_data/NEDS_2012_Labels_ED_Supplement.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_type.append(currline[0])
    return data_type

def get_data_type_ip_supplement():
    data_type = []
    with open('raw_data/NEDS_2012_Labels_IP_Supplement.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_type.append(currline[0])
    return data_type

def percentile(sample_list, value):
    num_below = 0
    for sample in sorted(sample_list):
        if sample < value:
            num_below += 1
    return float(num_below)/float(len(sample_list))

def wald_stat(mean1,std1,mean2=0,std2=0):
    return (mean1-mean2)/math.sqrt(std1**2 +std2**2)

def wald_test(mean1,std1,mean2=0,std2=0):
    if (not std1 and not std2):
        return np.nan
    w = wald_stat(mean1,std1,mean2,std2)
    return scipy.special.ndtr(w)