from __future__ import print_function
from __future__ import division

import os
import os.path
import sys
import csv
import numpy as np
import logging
from scipy import stats
# import scipy

# 362 total patients with DX1 = penile fracture
TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS =  13797122    
# TOTAL_ALL_PATIENTS = 31091020  # total patients

'''
The next function separates the patient file into male patients with corpus
collosum fractures and male patients without these fractures. USE CAUTION:
this classifies a patient as having a corpus collosum fracture is any of his
DX values qualify. Also, oddly, it appears as though 9 non-male patients
have collosal fractures.....

'''

def load_and_format():
    if os.path.isfile('NEDS_2012_CORE_Control.csv') and os.path.isfile('NEDS_2012_CORE_Patients.csv'):
        return
    data_type = get_data_type()

    injury_index = int(data_type.index('INJURY'))
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    isfemale_index = int(data_type.index('FEMALE'))
    penile_fracture_code = '95913'

    with open('NEDS_2012_CORE_Control.csv','w') as control_file:
        control_writer = csv.writer(control_file,delimiter=',')
        with open('NEDS_2012_CORE_Patients.csv','w') as patient_file:
            filewriter = csv.writer(patient_file,delimiter=',')
            with open('NEDS_2012_CORE.csv','r') as data_file:
                csv_reader = csv.reader(data_file)
                num_patients = 0
                total_patients = 0
                for line in csv_reader:
                    if penile_fracture_code in line[DX1_index:DX15_index]:
                        if line[isfemale_index] == '0':
                            num_patients += 1
                            filewriter.writerow(line)

                            total_patients += 1
                    elif line[isfemale_index] == '0':
                        control_writer.writerow(line)
                        total_patients += 1
    print(num_patients)
    print(total_patients)
    return data_type

''' The next function generates surrogate data.
    TODO: make sure no missing vals
'''
def make_surrogate_data(start,finish):
    samples = np.arange(start,finish)
    def get_and_save_control_rows(indices,i):
            with open('control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES)),'w') as outputfile:
                outputwriter = csv.writer(outputfile)
                with open('NEDS_2012_CORE_Control.csv','r') as control_file:
                    control_reader = csv.reader(control_file)
                    line_number = 0
                    for line in control_reader:
                        if line_number in indices:
                            outputwriter.writerow(line)

                        line_number += 1

    for i in samples:
        control_indices = np.random.randint(0,TOTAL_MALE_PATIENTS-TOTAL_FRACTURES-1,size=TOTAL_FRACTURES)
        get_and_save_control_rows(control_indices,i)
        print("done with surrogate number {0}".format(str(i)))


'''
If a surrogate file is messed up, use this one. THIS IS UNTESTED. TODO: test
'''
def make_surrogate_replacement(num):
    def get_and_save_control_rows(indices,i):
        with open('control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES)),'w') as outputfile:
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
    return 'control_surrogate_{0}_numfracs_{1}.csv'.format(str(num),str(TOTAL_FRACTURES))

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


''' The next series of functions require input of a filename to load and some code
    They return the respective test statistic. Code significance is commented above each. 
'''
def get_bootstrap_statistic(stat_func, code):
    test_stat = stat_func('NEDS_2012_CORE_Patients.csv', code)
    random_stat = []

    for i in range(1000):
        try:
            file_name = 'control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES))
            random_stat.append(stat_func(file_name,code))
        except:
            try:
                print('Trying to generate a replacement file for iteration i= {0}'.format(str(i),) )
                file_name = make_surrogate_replacement(i)
                random_stat.append(stat_func(file_name,code))
            except:
                return None

    return percentile(random_stat,test_stat)

'''
Takes a list of statistics from random samples with replacement and a test
statistic. Returns the percentile of the test statistic
'''
def percentile(list, value):
    num_below = 0
    for item in list.sort():
        if item < value:
            num_below += 1
    return float(num_below)/float(len(list))

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
                if row[age_index] is not '':
                    num_patients +=1
                    total_age+=int(row[age_index])
            except:
                missing_patients += 1
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
    if code not in [1, 2, 3, 9, 98, 99]:
        return None
    data_type = get_data_type()
    edevent_index = int(data_type.index('EDevent'))
    total_patients = 0
    missing_patients = 0

    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            try:
                if int(row[edevent_index]) == code:
                    total_patients += 1
            except:
                if row[EDevent] == '':
                    missing_patients += 1
    print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients

'''
Expected primary payer, uniform: (1) Medicare, (2)
Medicaid, (3) private including HMO, (4) self-pay, (5) no
charge, (6) other
'''
def total_payer1(filename,code):
    if code not in [1, 2, 3, 4, 5, 6]:
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
                if row[payer1_index] == '':
                    missing_patients += 1
    print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients

'''
Expected secondary payer, uniform: (1) Medicare, (2)
Medicaid, (3) private including HMO, (4) self-pay, (5) no
charge, (6) other
'''
def total_payer2(filename,code):
    if code not in [1, 2, 3, 4, 5, 6]:
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
    print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients


def main():
    load_and_format()
    # make_surrogate_data(0,1000)
    get_bootstrap_statistic(total_payer1,1)


if __name__ == '__main__':
    main()