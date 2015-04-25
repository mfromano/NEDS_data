from __future__ import print_function
from __future__ import division

import os
import os.path
import sys
import csv
import numpy as np
import logging
import re

TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS = 13797122   
PENILE_FRACTURE_CODE = '95913'
URETHRAL_INJURY_CODES = ('8670','8671')

''' TOD0: is number of patients in each quarter significantly different? what about wealth?

'''
'''
    Number of entries in files:
    in ed_patients_cleaned: 268
    in ed_controls_cleaned: 26617273
    in ip_patients_cleaned: 122 (=number of patients admitted to same hospital)
    in ip_controls_cleaned: 4473357
'''
'''
    General getter method for a particular stat
'''
def total_with(filename, code, index_begin, index_end=None, truncate=0):

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
                            total_with_stat += 1
                        elif int(line[index_begin]) < 0:
                            print('Getting rid of Nones fucked up')
                            sys.exit(1)
                    except:
                        if line[index_begin] is None or line[index_begin] == '':
                            total_missing += 1
            else:
                for line in reader:
                    try:
                        if str(code) in line[index_begin:index_end]:
                            total_with_stat += 1
                    except:
                            total_missing += 1
    if total_missing > 0:
        print('Total number of Nones: {0}'.format(str(total_missing),))
    return total_with_stat, total_missing

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
            if row[age_index] is not None and row[age_index] is not '':
                num_patients +=1
                total_age+=int(row[age_index])
            else:
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
            if row[edevent_index] is not None and row[edevent_index] > 0 and row[edevent_index] is not '':
                if int(row[edevent_index]) == code:
                    total_patients += 1
            else:
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
    print("Total number of missing patients: {0}".format(missing_patients,))
    return total_patients, len(choices)

''' 
    The next series of functions require input of a filename to load and some code
    They return the respective test statistic. Code significance is commented above each. 
'''
def get_bootstrap_statistic(stat_func, code=None):
    if code is not None:
        test_stat = stat_func('cleaned_data/core_patients_cleaned.csv', code)
    else:
        test_stat = stat_func('cleaned_data/core_patients_cleaned.csv')
    print("Test statistic: {0}".format(str(test_stat),))
    random_stat = []

    for i in range(1000):
        if stat_func == average_age:
            file_name = 'control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES))
        else:
            print('invalid stat_func.')
            sys.exit(1)
        try:
            if code is not None:
                random_stat.append(stat_func(file_name,code, 0))
            else:
                random_stat.append(stat_func(file_name, 0))
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
    # print(random_stat)
    # numbins = 50
    # h = np.histogram(random_stat,bins=numbins)
    # lineheight = max(h[0])*1.25
    # plt.hist(random_stat,bins=numbins)
    # plt.plot([test_stat, test_stat], [0, lineheight])
    # x1, x2, y1, y2 = plt.axis()
    # plt.axis((x1,x2,0, lineheight))
    # plt.title('Distribution of bootstrapped stat')
    # plt.xlabel('Value')
    # plt.ylabel('Count')

    # plt.show()

    return percentile(random_stat,test_stat)

'''
    Next function gets total with concomitant urethral injuries
'''
def total_with_urethral_injury(filename):
    data_type = get_data_type()
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    num_with_ui = [0,0]

    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            if URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                num_with_ui[0] += 1
            elif URETHRAL_INJURY_CODES[1] in line[DX1_index:DX15_index]:
                num_with_ui[1] += 1
    return num_with_ui

''' 
    Median household income quartiles for patient's ZIP Code.
    For 2012, the median income quartiles are defined as:
    1) $1 - $38,999; (2) $39,000 - $47,999; (3) $48,000 - $62,999;
    and (4) $63,000 or more.
'''
def total_with_median_income(filename,code, no_missing=0):

    data_type = get_data_type()
    ZIPINC_QRTL_index = int(data_type.index('ZIPINC_QRTL'))
    num_with_zip_inc = total_with(filename,code,ZIPINC_QRTL_index,None,no_missing)
    return num_with_zip_inc

''' 
'''
def total_in_quarter(filename,code, no_missing=0):

    data_type = get_data_type()
    DQTR_index = int(data_type.index('DQTR'))
    num_in_dqtr = total_with(filename,code,DQTR_index,None,no_missing)
    return num_in_dqtr

''' 
    ICD-9-CM procedures performed in ED
'''
def total_with_procedure_ed(filename,code, no_missing=0):

    data_type = get_data_type_ed_supplement()
    PR_ED1_index = int(data_type.index('PR_ED1'))
    PR_ED9_index = int(data_type.index('PR_ED9'))
    num_with_procedure = total_with(filaname,code,PR_ED1_index,PR_ED9_index, no_missing)
    return num_with_procedure

''' 
    ICD-9-CM procedures coded on ED admissions.
    Procedure may have been performed in the ED
    or during the hospital stay.
'''
def total_with_procedure_all(filename,code, no_missing=0):
    data_type = get_data_type_ip_supplement()
    PR_IP1_index = int(data_type.index('PR_IP1'))
    PR_IP9_index = int(data_type.index('PR_IP9'))
    num_with_procedure = total_with(filaname,code,PR_IP1_index,PR_IP9_index, no_missing)
    return num_with_procedure


def average_charges_ed(filename):
    data_type = get_data_type()
    TOTCHG_ED_index = int(data_type.index('TOTCHG_ED'))
    total_charges = 0
    num_patients = 0
    missing_patients = 0
    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            try:
                if float(line[TOTCHG_ED_index]) >= 0:
                    total_charges += float(line[TOTCHG_ED_index])
                    num_patients += 1
            except:
                missing_patients +=1
    if missing_patients > 0:
        print('Missing patients: {0}'.format(str(missing_patients),))
    return float(total_charges)/float(num_patients)

def average_charges_ip(filename):
    data_type = get_data_type_ip_supplement()
    TOTCHG_IP_index = int(data_type.index('TOTCHG_IP'))
    total_charges = 0
    num_patients = 0
    missing_patients = 0
    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            try:
                if float(line[TOTCHG_IP_index]) >= 0:
                    total_charges += float(line[TOTCHG_IP_index])
                    num_patients += 1
            except:
                missing_patients +=1
    if missing_patients > 0:
        print('Missing patients: {0}'.format(str(missing_patients),))
    return float(total_charges)/float(num_patients)

def average_los(filename):
    data_type = get_data_type_ip_supplement()
    LOS_IP_index = int(data_type.index('LOS_IP'))
    los_total = 0
    num_patients = 0
    missing_patients = 0
    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            try:
                los_total += float(line[LOS_IP_index])
                num_patients += 1
            except:
                missing_patients +=1
    if missing_patients > 0:
        print('Missing patients: {0}'.format(str(missing_patients),))
    return float(los_total)/float(num_patients)

def test_erectile_fracture_code():
    data_type = get_data_type()
    filename = 'cleaned_data/core_patients_cleaned.csv'
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    return total_with(filename,PENILE_FRACTURE_CODE,DX1_index,DX15_index)

def main():
    choices = [1, 2, 3, 9, 98, 99]
    for choice in choices:
        print('Total ed event: {0}'.format(str(total_ed_event('cleaned_data/core_patients_cleaned.csv',choice)),))

    print(test_erectile_fracture_code())
    # print('Average age of control group: {0}'.format(str(average_age('cleaned_data/core_controls_cleaned.csv')),))
    print('Average age of patient group: {0}'.format(str(average_age('cleaned_data/core_patients_cleaned.csv')),))
    print('Total number  of urethral fractures:')
    print(total_with_urethral_injury('cleaned_data/core_patients_cleaned.csv'))

    print('Average length of stay:')
    print(average_los('cleaned_data/ip_patients_cleaned.csv'))

    print('Total cost of stay in IP:')
    print(average_charges_ip('cleaned_data/ip_patients_cleaned.csv'))
    # print('Total cost of stay in ED:')
    # print(average_charges_ed('cleaned_data/ed_patients_cleaned.csv'))

    print('Total in each quarter:')
    print(total_in_quarter('cleaned_data/core_patients_cleaned.csv',1))
    print(total_in_quarter('cleaned_data/core_patients_cleaned.csv',2))
    print(total_in_quarter('cleaned_data/core_patients_cleaned.csv',3))
    print(total_in_quarter('cleaned_data/core_patients_cleaned.csv',4))

    print('Total with median incomes:')
    print(total_with_median_income('cleaned_data/core_patients_cleaned.csv',1))
    print(total_with_median_income('cleaned_data/core_patients_cleaned.csv',2))
    print(total_with_median_income('cleaned_data/core_patients_cleaned.csv',3))
    print(total_with_median_income('cleaned_data/core_patients_cleaned.csv',4))

    print('Bootstrap statistic for average age:')
    print(get_bootstrap_statistic(average_age))

if __name__ == '__main__':
    main()