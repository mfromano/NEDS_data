from __future__ import print_function
from __future__ import division

import os
import os.path
import sys
import csv
import numpy as np
import logging
import re


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
                if row[age_index] is not None:
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
                if row[transfer_index] is None:
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
                if row[EDevent] is None:
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
                if row[payer1_index] is None:
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
                if row[payer2_index] is None:
                    missing_patients += 1
    if missing_patients > 0:
        print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients, len(choices)

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

    return percentile(random_stat,test_stat

