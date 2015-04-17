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

# 362 total patients with DX1 = penile fracture
TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS =  13797122    
# TOTAL_ALL_PATIENTS = 31,091,020  # total patients

def clean_core_data():
    with open('NEDS_2012_CORE.csv') as raw_file:
        reader = csv.reader(raw_file)
        with open('core_cleaned.csv','w') as cleaned_file:
            writer = csv.writer(cleaned_file)
            for line in reader:
                print(line)
                writer.writerow(cleaned_core(line))
    print('Done with core!')

def clean_ed_data():
    with open('NEDS_2012_ED.csv') as raw_file:
        reader = csv.reader(raw_file)
        with open('ed_cleaned.csv','w') as cleaned_file:
            writer = csv.writer(cleaned_file)
            for line in reader:
                print(line)
                writer.writerow(cleaned_ed_supplement(line))
    print('Done with ED!')

def clean_ip_data():
    with open('NEDS_2012_IP.csv') as raw_file:
        reader = csv.reader(raw_file)
        with open('ip_cleaned.csv','w') as cleaned_file:
            writer = csv.writer(cleaned_file)
            for line in reader:
                print(line)
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
            data_entry[i] = None
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
    for i in range(len(data_entry)):
        ed_index = data_type.index(label_list[i])
        if data_entry[ed_index] in null_vals[i]:
            data_entry[i] = None
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
    for i in range(len(data_entry)):
        ed_index = data_type.index(label_list[i])
        if data_entry[ed_index] in null_vals[i]:
            data_entry[i] = None
    return data_entry
'''
    Next method is getter method. Returns the keys for each of the entries in the ED supplement
'''
# def get_ed_keys():
#     filename = 'NEDS_2012_ED.csv'
#     data_type_supplement = get_data_type_ed_supplement()
#     key_index = int(data_type_supplement('KEY_ED'))
#     key_list = []
#     with open(filename,'r') as datafile:
#         reader = csv.reader(datafile)
#         for line in reader:
#             # BE CAREFUL WITH NEXT LINE: which columns do people need in order to be included????
#             if :
#                 key_list.append(line[key_index])
#     return key_list

# '''
#     Next method creates a file that contains only those names that contain associated
#     supplementary files
# '''
# def get_core_with_supplement():
#     ed_keys = get_ed_keys()



'''
The next function separates the patient file into male patients with corpus
collosum fractures and male patients without these fractures. USE CAUTION:
this classifies a patient as having a corpus collosum fracture is any of his
DX values qualify. Also, oddly, it appears as though 9 non-male patients
have collosal fractures.....

'''

def load_and_format():
    # Next line gets the type of data for each entry in the core file
    data_type = get_data_type()

    # The next few lines get the indices for the specific entries
    injury_index = int(data_type.index('INJURY'))
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    isfemale_index = int(data_type.index('FEMALE'))
    penile_fracture_code = '95913'

    # open the Core Control file. We will write to this all of the patient
    # records that do not contain a broken penis DX*
    with open('NEDS_2012_CORE_Control.csv','w') as control_file:
        control_writer = csv.writer(control_file,delimiter=',')
        # open the Core Patient file. We will write to this all of the patient
        # records that do contain a broken penis DX
        with open('NEDS_2012_CORE_Patients.csv','w') as patient_file:
            filewriter = csv.writer(patient_file,delimiter=',')
            with open('NEDS_2012_CORE.csv','r') as data_file:
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

''' The next function generates surrogate data.
    TODO: make sure no missing vals
'''

''' This takes as input the name of a core data file and generates a list of
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

def make_surrogate_data(start,finish):
    samples = np.arange(start,finish)
    for i in samples:
        make_surrogate_replacement(i)
        print("done with surrogate number {0}".format(str(i)))

def convert_core_to_supplement(start,finish):
    samples = np.arange(start,finish)
    for i in samples:
        filename = 'control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES)) 
        get_ed_supplement_from_core(filename)

'''
If a surrogate file is messed up, use this one.
'''
def make_surrogate_replacement(num):
    def get_and_save_control_rows(indices,i):
        with open('control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES)),'w') as outputfile:
            outputwriter = csv.writer(outputfile)
            with open('NEDS_2012_CORE_Control.csv','r') as control_file:
                control_reader = csv.reader(control_file)
                line_number = 0
                for line in control_reader:
                    if line_number in indices:
                        outputwriter.writerow(line)
                    line_number += 1
    control_indices = np.random.randint(0,TOTAL_MALE_PATIENTS-TOTAL_FRACTURES-1,size=TOTAL_FRACTURES)
    get_and_save_control_rows(control_indices,num)
    return 'control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(num),str(TOTAL_FRACTURES))

''' The next function returns a list containing the data types for each column
    of the NEDS Core data file
'''
def get_data_type():
    data_labels = {}
    data_type = []
    with open('NEDS_2012_Labels_Core.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_labels[currline[0]] = currline[1]
            data_type.append(currline[0])
    return data_type

''' The next function returns a list containing the data types for each column
    of the NEDS ED Supplement data file
'''
def get_data_type_ed_supplement():
    data_type = []
    with open('NEDS_2012_Labels_ED_Supplement.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_type.append(currline[0])
    return data_type

def get_data_type_ip_supplement():
    data_type = []
    with open('NEDS_2012_Labels_IP_Supplement.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_type.append(currline[0])
    return data_type

''' The next series of functions require input of a filename to load and some code
    They return the respective test statistic. Code significance is commented above each. 
'''
def get_bootstrap_statistic(stat_func, code=None):
    if code is not None:
        test_stat = stat_func('NEDS_2012_CORE_Patients.csv', code)
    else:
        test_stat = stat_func('NEDS_2012_CORE_Patients.csv')
    print("Test statistic: {0}".format(str(test_stat),))
    random_stat = []

    for i in range(1000):
        try:
            file_name = 'control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES))
            if code is not None:
                random_stat.append(stat_func(file_name,code))
            else:
                random_stat.append(stat_func(file_name))
        except:
            # print('Couldnt load file!')
            # try:
            #     print('Trying to generate a replacement file for iteration i= {0}'.format(str(i),) )
            #     file_name = make_surrogate_replacement(i)
            #     random_stat.append(stat_func(file_name,code))
            # except:
            #     print('Couldn\'t generate replacement')
            return None
        # print('Done with {0}'.format(str(i),))
    numbins = 50
    h = np.histogram(random_stat,bins=numbins)
    lineheight = max(h[0])*1.25
    plt.hist(random_stat,bins=numbins)
    plt.plot([test_stat, test_stat], [0, lineheight])
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1,x2,0, lineheight))
    plt.title('Distribution of bootstrapped stat')
    plt.xlabel('Value')
    plt.ylabel('Count')

    plt.show()

    return percentile(random_stat,test_stat)

'''
Takes a list of statistics from random samples with replacement and a test
statistic. Returns the percentile of the test statistic
'''
def percentile(sample_list, value):
    num_below = 0
    for sample in sorted(sample_list):
        if sample < value:
            num_below += 1
    return float(num_below)/float(len(sample_list))

'''
Hopefully self explanatory...gets the average age from a file
'''
def average_age(filename):
    data_type = get_data_type()
    age_index = int(data_type.index('AGE'))
    total_age = 0
    num_patients = 0
    missing_patients = 0

    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            try:
                if row[age_index] is not '' and int(row[age_index]) > 0:
                    num_patients +=1
                    total_age+=int(row[age_index])
            except:
                missing_patients += 1
    if missing_patients > 0:
        print("Total number of missing patients: {0}".format(missing_patients,))
    return float(total_age)/float(num_patients)


'''
Disposition from ED: (1) routine, (2) transfer to shortterm
hospital, (5) other transfers, including skilled
nursing facility, intermediate care, and another type of
facility, (6) home health care, (7) against medical
advice, (9) admitted as an inpatient to this hospital, (20)
died in ED, (21) Discharged/transferred to court/law
enforcement , (98) not admitted, destination unknown,
(99) discharged alive, destination unknown (but not
admitted)
'''
def total_disposition(filename, code):
    if code not in [1, 2, 5, 6, 7, 9, 20, 21, 98, 99]:
        return None
    data_type = get_data_type()
    transfer_index = int(data_type.index('DISP_ED'))
    total_patients = 0
    missing_patients = 0

    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            # print(row[transfer_index])
            try:
                if int(row[transfer_index]) == code:
                    total_patients += 1
            except:
                if row[transfer_index] == '':
                    missing_patients += 1
    print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients

'''
Type of ED event: (1) ED visit in which the patient is
treated and released, (2) ED visit in which the patient is
admitted to this same hospital, (3) ED visit in which the
patient is transferred to another short-term hospital, (9)
ED visit in which the patient died in the ED, (98) ED
visits in which patient was not admitted, destination
unknown, (99) ED visit in which patient was discharged
alive, destination unknown (but not admitted)
'''
def total_ed_event(filename, code):
    choices = [1, 2, 3, 9, 98, 99]
    if code not in choices:
        return None
    data_type = get_data_type()
    edevent_index = int(data_type.index('EDEVENT'))
    total_patients = 0
    missing_patients = 0

    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            try:
                if int(row[edevent_index]) == code:
                    total_patients += 1
            except:
                if row[EDevent] == '' or int(row[EDevent]) < 0:
                    missing_patients += 1
    if missing_patients > 0:
        print("Total number of missing patients: {0}".format(str(missing_patients),))

    return total_patients

'''
Expected primary payer, uniform: (1) Medicare, (2)
Medicaid, (3) private including HMO, (4) self-pay, (5) no
charge, (6) other
'''
def total_payer1(filename,code):
    choices = [1, 2, 3, 4, 5, 6]
    if code not in choices:
        return None
    data_type = get_data_type()
    payer1_index = int(data_type.index('PAY1'))
    total_patients = 0
    missing_patients = 0
    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            try:
                if int(row[payer1_index]) == code:
                    total_patients += 1
            except:
                if row[payer1_index] == '' or int(row[payer1_index]) < 0:
                    missing_patients += 1
    if missing_patients > 0:
        print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients, len(choices)

'''
Expected secondary payer, uniform: (1) Medicare, (2)
Medicaid, (3) private including HMO, (4) self-pay, (5) no
charge, (6) other
'''
def total_payer2(filename,code):
    choices = [1, 2, 3, 4, 5, 6]
    if code not in choices:
        return None
    data_type = get_data_type()
    payer2_index = int(data_type.index('PAY2'))
    total_patients = 0
    missing_patients = 0
    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            try:
                if int(row[payer2_index]) == code:
                    total_patients += 1
            except:
                if row[payer2_index] == '':
                    missing_patients += 1
    if missing_patients > 0:
        print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients, len(choices)

def main():

    # start, finish = int(sys.argv[1]), int(sys.argv[2])
    # make_surrogate_data(start,finish)
    # convert_core_to_supplement(start, finish)
    # stat = get_bootstrap_statistic(total_ed_event,1)
    # get_ed_supplement_from_core('NEDS_2012_CORE_Patients.csv')
    # choices for ed = [1, 2, 3, 9, 98, 99]
    clean_core_data()
    clean_ed_data()
    # clean_ip_data()
    # stat = get_bootstrap_statistic(average_age)
    # print(stat < 0.025)
    # print((1-stat) < (0.025))


if __name__ == '__main__':
    # cd = os.getcwd()
    # os.chdir(os.path.pardir)
    main()
    # os.chdir(cd)
