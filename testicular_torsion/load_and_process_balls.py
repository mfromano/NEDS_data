from __future__ import print_function
from __future__ import division

import os
import os.path
import sys
import csv
import numpy as np
import logging
import re
# import matplotlib.pyplot as plt
# from scipy import stats
# import scipy

# Okay, so only 268 patients have supplement files....does this match with num of inpatients?
TORSION_CODES = ['60820','60821','60822','60823','60824']
# 362 total patients with DX1 = penile fracture
TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS = 13797122    
# TOTAL_ALL_PATIENTS = 31,091,020  # total patients
penile_fracture_code = '95913'
urethral_injury_codes = ('8670','8671')
''' 8670,8671 -> urethral injury (closed, open)!!!!

    penile_fracture_code = '95913'
'''


'''
    The next function separates the patient file into male patients with corpus
    collosum fractures and male patients without these fractures. USE CAUTION:
    this classifies a patient as having a corpus collosum fracture is any of his
    DX values qualify. Also, oddly, it appears as though 9 non-male patients
    have collosal fractures.....
'''

def divide_ip_supplement():
    data_type = get_data_type()
    key_ed_index_core = int(data_type.index('KEY_ED'))
    key_ed_patients = []
    key_ed_controls = []

    with open('cleaned_data/core_torsion_patients_cleaned.csv') as core_file:
        reader = csv.reader(core_file)
        for line in reader:
            key_ed_patients.append(line[key_ed_index_core])

    # with open('cleaned_data/core_controls_cleaned.csv') as core_file:
    #     reader = csv.reader(core_file)
    #     for line in reader:
    #         key_ed_controls.append(line[key_ed_index_core])

    ip_data_type = get_data_type_ip_supplement() 
    key_ed_index = int(ip_data_type.index('KEY_ED'))
    with open('cleaned_data/ip_cleaned.csv','r') as core_file:
        read_file = csv.reader(core_file)
        with open('ip_torsion_patients_cleaned.csv','w') as patient_file:
            write_file = csv.writer(patient_file)
            # with open('ip_controls_cleaned.csv','w') as control_file:
            #     write_control = csv.writer(control_file)
            for line in read_file:
                if line[key_ed_index] in key_ed_patients:
                    write_file.writerow(line)
                # elif line[key_ed_index] in key_ed_controls:
                #     write_control.writerow(line)


def divide_ed_supplement():
    data_type = get_data_type()
    key_ed_index_core = int(data_type.index('KEY_ED'))
    ed_data_type = get_data_type_ed_supplement() 
    key_ed_index = int(ed_data_type.index('KEY_ED'))
    key_ed_patients = []
    key_ed_controls = []
    with open('cleaned_data/core_torsion_patients_cleaned.csv') as core_file:
        reader = csv.reader(core_file)
        for line in reader:
            key_ed_patients.append(line[key_ed_index_core])

    # with open('cleaned_data/core_controls_cleaned.csv') as core_file:
    #     reader = csv.reader(core_file)
    #     for line in reader:
    #         key_ed_controls.append(line[key_ed_index_core])

    with open('cleaned_data/ed_cleaned.csv','r') as core_file:
        read_file = csv.reader(core_file)
        with open('ed_torsion_patients_cleaned.csv','w') as patient_file:
            write_file = csv.writer(patient_file)
            # with open('ed_controls_cleaned.csv','w') as control_file:
            #     write_control = csv.writer(control_file)
            for line in read_file:
                if line[key_ed_index] in key_ed_patients:
                    write_file.writerow(line)
                # elif line[key_ed_index] in key_ed_controls:
                #     write_control.writerow(line)

def getlength(f):
    m = open(f)
    reader = csv.reader(m)
    count = 0
    for line in reader:
        count+=1
    return count

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


def main():
    divide_ed_supplement()
    divide_ip_supplement()


if __name__ == '__main__':
    # cd = os.getcwd()
    # os.chdir(os.path.pardir)
    main()
    # os.chdir(cd)
