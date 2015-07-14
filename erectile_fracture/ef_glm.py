from __future__ import print_function
from __future__ import division

import os
import os.path
import sys
import csv
import numpy as np
import logging
import re
import matplotlib.pyplot as plt

TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS = 13797122   
PENILE_FRACTURE_CODE = '95913'
URETHRAL_INJURY_CODES = ('8670','8671')
RETROGRADE_CYSTOURETHROGRAM = '8776'
ULTRASOUND_URINARY = '8875'

'''
    Number of entries in files:
    in ed_patients_cleaned: 268
    in ed_controls_cleaned: 26617273
    in ip_patients_cleaned: 122 (=number of patients admitted to same hospital)
    in ip_controls_cleaned: 4473357
'''
def total_with(filename, code, index_begin, index_end=None, truncate=0,data_type=None):

    total_with_stat = 0
    total_missing = 0
    with open(filename) as inputfile:
            reader = csv.reader(inputfile)
            for i in range(truncate):
                reader.next()
            if index_end is None:
                for line in reader:
                    try:
                        if code == int(line[index_begin]):
                            # total_with_stat += 1
                            total_with_stat += pt_weight(line,data_type)
                        elif int(line[index_begin]) < 0:
                            print('Getting rid of Nones fucked up')
                            sys.exit(1)
                    except:
                        if line[index_begin] is None or line[index_begin] == '':
                            # total_missing += 1
                            total_missing += pt_weight(line,data_type)
            else:
                for line in reader:
                    try:
                        if str(code) in line[index_begin:index_end]:
                            # total_with_stat += 1
                            total_with_stat += pt_weight(line,data_type)
                    except:
                            # total_missing += 1
                            total_missing += pt_weight(line,data_type)
    if total_missing > 0:
        print('Total number of Nones: {0}'.format(str(total_missing),))
    return total_with_stat, total_missing

def total_with_urethral_injury(filename):
    data_type = get_data_type()
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    num_with_ui = [0,0]

    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            wt = pt_weight(line,data_type)
            if URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                # num_with_ui[0] += 1
                num_with_ui[0] += wt
            elif URETHRAL_INJURY_CODES[1] in line[DX1_index:DX15_index]:
                # num_with_ui[1] += 1
                num_with_ui[1] += wt
    return num_with_ui

def total_with_treatment(filename, treatment_code):
    data_type = get_data_type_ip_supplement()
    PR_IP1_index = int(data_type.index('PR_IP1'))
    PR_IP15_index = int(data_type.index('PR_IP15'))
    total = 0
    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            wt = pt_weight(line,data_type)
            if treatment_code in line[PR_IP1_index:PR_IP15_index]:
                # total += 1
                total += wt
    return total

def pt_weight(line,data_type):
    key_index_core = int(data_type.index('DISCWT'))
    if key_index_core is not '':
        try:
   	        return float(line[key_index_core])
        except:
            print('Missing line: {0}'.format(line,))
            print(key_index_core)
            return 0.0
    else:
        return 0.0

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
'''