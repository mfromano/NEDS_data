from __future__ import print_function
from __future__ import division
from neds_utils import *
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

# 362 total patients with DX1 = penile fracture
TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS = 13797122
# TOTAL_ALL_PATIENTS = 31,091,020  # total patients
penile_fracture_code = '95913'
urethral_injury_codes = ('8670','8671')
''' 8670,8671 -> urethral injury (closed, open)!!!!

    penile_fracture_code = '95913'
'''

def clean_core_data():
    with open('raw_data/NEDS_2012_CORE.csv') as raw_file:
        reader = csv.reader(raw_file)
        with open('core_cleaned.csv','w') as cleaned_file:
            writer = csv.writer(cleaned_file)
            for line in reader:
                writer.writerow(cleaned_core(line))
    print('Done with core!')

def clean_ed_data():
    with open('raw_data/NEDS_2012_ED.csv') as raw_file:
        reader = csv.reader(raw_file)
        with open('ed_cleaned.csv','w') as cleaned_file:
            writer = csv.writer(cleaned_file)
            for line in reader:
                writer.writerow(cleaned_ed_supplement(line))
    print('Done with ED!')

def clean_ip_data():
    with open('raw_data/NEDS_2012_IP.csv') as raw_file:
        reader = csv.reader(raw_file)
        with open('ip_cleaned.csv','w') as cleaned_file:
            writer = csv.writer(cleaned_file)
            for line in reader:
                writer.writerow(cleaned_ip_supplement(line))
    print('Done with IP!')

def cleaned_core(data_entry):
    data_type = get_data_type()
    # The next few lines will get the null values to replace
    null_vals = []
    label_list = []
    with open('Core_missing_vals.txt') as inputfile:
        for line in inputfile:
            m = re.search('(?<=\().*(?=\=SYSMIS\))',line)
            label = re.search('(?<=\s)\S*(?!=\s)',line)
            label_list.append(label.group(0))
            null_vals.append(m.group(0).split(' '))

    # Go through list of entries and replace missing values with nones
    # Go through all of the indices in the list of missing value data types
    for i in range(len(label_list)):

        # get the corresponding index in the Core file for this data type
        core_index = data_type.index(label_list[i])
        # if the value in this index equals the 
        if data_entry[core_index] in null_vals[i]:
            data_entry[core_index] = None
    return data_entry

def cleaned_ed_supplement(data_entry):
    # The next few lines will get the null values to replace
    data_type = get_data_type_ed_supplement()
    null_vals = []
    label_list = []
    with open('ED_supplement_missing_vals.txt') as inputfile:
        for line in inputfile:
            m = re.search('(?<=\().*(?=\=SYSMIS\))',line)
            label = re.search('(?<=\s)\S*(?!=\s)',line)
            label_list.append(label.group(0))
            null_vals.append(m.group(0).split(' '))

    # Go through list of entries and replace missing values with nones
    for i in range(len(label_list)):
        ed_index = data_type.index(label_list[i])
        if data_entry[ed_index] in null_vals[i]:
            data_entry[ed_index] = None
    return data_entry

def cleaned_ip_supplement(data_entry):
    # The next few lines will get the null values to replace
    data_type = get_data_type_ip_supplement()
    print(data_type)
    null_vals = []
    label_list = []
    with open('IP_supplement_missing_vals.txt') as inputfile:
        for line in inputfile:
            m = re.search('(?<=\().*(?=\=SYSMIS\))',line)
            label = re.search('(?<=\s)\S*(?!=\s)',line)
            label_list.append(label.group(0))
            null_vals.append(m.group(0).split(' '))

    # Go through list of entries and replace missing values with nones
    for i in range(len(label_list)):
        ed_index = data_type.index(label_list[i])
        if data_entry[ed_index] in null_vals[i]:
            data_entry[ed_index] = None
    return data_entry

'''
    The next function separates the patient file into male patients with corpus
    collosum fractures and male patients without these fractures. USE CAUTION:
    this classifies a patient as having a corpus collosum fracture is any of his
    DX values qualify. Also, oddly, it appears as though 9 non-male patients
    have collosal fractures.....
'''

def make_core_cleaned_male():
    data_type = get_data_type()
    isfemale_index = int(data_type.index('FEMALE'))
    with open('core_male_cleaned.csv','w') as control_file:
        control_writer = csv.writer(control_file,delimiter=',')
        with open('cleaned_data/core_cleaned.csv','r') as data_file:
                csv_reader = csv.reader(data_file)
                # total_patients stores total male patients
                total_patients = 0
                # 
                for line in csv_reader:
                    if line[isfemale_index] == '0':
                        control_writer.writerow(line)
                        total_patients += 1
    print(total_patients)
    return data_type

def load_and_format():
    # Next line gets the type of data for each entry in the core file
    data_type = get_data_type()

    # The next few lines get the indices for the specific entries
    injury_index = int(data_type.index('INJURY'))
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    isfemale_index = int(data_type.index('FEMALE'))

    # open the Core Control file. We will write to this all of the patient
    # records that do not contain a broken penis DX*
    with open('core_control_cleaned.csv','w') as control_file:
        control_writer = csv.writer(control_file,delimiter=',')
        # open the Core Patient file. We will write to this all of the patient
        # records that do contain a broken penis DX
        with open('core_patients_cleaned.csv','w') as patient_file:
            filewriter = csv.writer(patient_file,delimiter=',')
            with open('cleaned_data/core_cleaned.csv','r') as data_file:
                csv_reader = csv.reader(data_file)
                # num_patients stores the number of patients with a broken penis
                num_patients = 0
                # total_patients stores total male patients
                total_patients = 0
                # 
                for line in csv_reader:
                    if penile_fracture_code in line[DX1_index:DX15_index]:
                        if line[isfemale_index] == '0':
                            num_patients += 1
                            filewriter.writerow(line)
                            total_patients += 1
                        else:
                            print('non-male patient!')
                    elif line[isfemale_index] == '0':
                        control_writer.writerow(line)
                        total_patients += 1
    print(num_patients)
    print(total_patients)
    return data_type

''' 
    The next function generates surrogate data.
    TODO: make sure no missing vals
'''

''' 
    This takes as input the name of a core data file and generates a list of
    supplement entries that correspond to the entries in the core data file
'''
def get_ed_supplement_from_core(filename):
    
    data_type = get_data_type()
    data_type_supplement = get_data_type_ed_supplement()

    key_index = int(data_type.index('KEY_ED'))
    key_list = []
    with open(filename) as currentfile:
        reader = csv.reader(currentfile)
        for entry in reader:
            if int(entry[key_index]) > 0:
                key_list.append(entry[key_index])
            else:
                print('Missing key value for file: {0}'.format(filename,))
                return None
    key_index_supplement = int(data_type_supplement.index('KEY_ED'))
    total_patients = TOTAL_FRACTURES
    # entry_list = [None]*total_patients
    entry_list = []
    with open('NEDS_2012_ED.csv','r') as data_file:
        reader = csv.reader(data_file)
        for entry in reader:
            if entry[key_index_supplement] in key_list:
                entry_list.append(entry)
    print(len(entry_list))
    outputfile = filename[:(len(filename)-4)]+'_ed_supplement.csv'
    
    with open(outputfile,'w') as output:
        writer = csv.writer(output)
        for item in entry_list:
            writer.writerow(item)
    return outputfile

def divide_ip_supplement():
    data_type = get_data_type()
    key_ed_index_core = int(data_type.index('KEY_ED'))
    key_ed_patients = []
    key_ed_controls = []

    with open('cleaned_data/core_patients_cleaned.csv') as core_file:
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
        with open('ip_patients_cleaned.csv','w') as patient_file:
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
    with open('cleaned_data/core_patients_cleaned.csv') as core_file:
        reader = csv.reader(core_file)
        for line in reader:
            key_ed_patients.append(line[key_ed_index_core])

    # with open('cleaned_data/core_controls_cleaned.csv') as core_file:
    #     reader = csv.reader(core_file)
    #     for line in reader:
    #         key_ed_controls.append(line[key_ed_index_core])

    with open('cleaned_data/ed_cleaned.csv','r') as core_file:
        read_file = csv.reader(core_file)
        with open('ed_patients_cleaned.csv','w') as patient_file:
            write_file = csv.writer(patient_file)
            # with open('ed_controls_cleaned.csv','w') as control_file:
            #     write_control = csv.writer(control_file)
            for line in read_file:
                if line[key_ed_index] in key_ed_patients:
                    write_file.writerow(line)
                # elif line[key_ed_index] in key_ed_controls:
                #     write_control.writerow(line)

def make_surrogate_data(start,finish, data_size, data_type):
    samples = np.arange(start,finish)
    data_file = 'cleaned_data/core_controls_cleaned_{0}.csv'.format(data_type,)
    max_size = getlength(data_file)
    for i in samples:
        make_surrogate_replacement(i, data_size, data_type,max_size)
        print("done with surrogate number {0} for {1}".format(str(i),data_type))

def convert_core_to_supplement(start,finish):
    samples = np.arange(start,finish)
    for i in samples:
        filename = 'control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES)) 
        get_ed_supplement_from_core(filename)

def getlength(f):
    m = open(f)
    reader = csv.reader(m)
    count = 0
    for line in reader:
        count+=1
    return count
'''
    If a surrogate file is messed up, use this one.
'''
def make_surrogate_replacement(num, data_size, datum,max_size):

    data_file = 'cleaned_data/core_controls_cleaned_{0}.csv'.format(datum,)

    with open(data_file,'r') as control_file:
        control_reader = csv.reader(control_file)
        control_indices = np.random.randint(0, max_size,size=data_size)
        with open('control_surrogates/core_surrogate_{0}_{1}.csv'.format(str(num),datum),'w') as outputfile:
            outputwriter = csv.writer(outputfile)
            line_number = 0
            for line in control_reader:
                while line_number in control_indices:
                    outputwriter.writerow(line)   
                    control_indices=np.delete(control_indices,np.where(control_indices==line_number)[0][0])
                line_number += 1
    return 'control_surrogates/core_surrogate_{0}_{1}.csv'.format(str(num),datum)


def main():
    # clean_core_data()
    # clean_ed_data()
    # clean_ip_data()
    # load_and_format()
    # divide_ed_supplement()
    # divide_ip_supplement()
    # start, finish = int(sys.argv[1]), int(sys.argv[2])
    # make_surrogate_data(start,finish)
    # convert_core_to_supplement(start, finish)
    # stat = get_bootstrap_statistic(total_ed_event,1)
    # get_ed_supplement_from_core('NEDS_2012_CORE_Patients.csv')
    # choices for ed = [1, 2, 3, 9, 98, 99]

    # stat = get_bootstrap_statistic(average_age)
    # print(stat < 0.025)
    # print((1-stat) < (0.025))
    make_core_cleaned_male()


if __name__ == '__main__':
    # cd = os.getcwd()
    # os.chdir(os.path.pardir)
    main()
    # os.chdir(cd)
