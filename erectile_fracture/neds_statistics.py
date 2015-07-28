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

TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS = 13797122   
PENILE_FRACTURE_CODE = '95913'
URETHRAL_INJURY_CODES = ('8670','8671')
RETROGRADE_CYSTOURETHROGRAM = '8776'
ULTRASOUND_URINARY = '8875'

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
                # num_patients +=1
                wt = pt_weight(row,data_type)
                num_patients += wt
                total_age+=float(row[age_index])*wt
            else:
                # missing_patients += 1
                missing_patients += pt_weight(row,data_type)
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
            wt = pt_weight(row,data_type)
            try:
                if int(row[transfer_index]) == code:
                    # total_patients += 1
                    total_patients += wt
            except:
                missing_patients += wt
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
            wt = pt_weight(row,data_type)
            if row[edevent_index] is not None and row[edevent_index] > 0 and row[edevent_index] is not '':
                if int(row[edevent_index]) == code:
                    # total_patients += 1
                    total_patients += wt
            else:
                # missing_patients += 1
                missing_patients += wt
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
            wt = pt_weight(row,data_type)
            try:
                if int(row[payer1_index]) == code:
                    # total_patients += 1
                    total_patients += wt
            except:
                if row[payer1_index] is None:
                    # missing_patients += 1
                    missing_patients += wt
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
            wt = pt_weight(row,data_type)
            try:
                if int(row[payer2_index]) == code:
                    # total_patients += 1
                    print(wt)
                    total_patients += wt
            except:
                if row[payer2_index] is None:
                    # missing_patients += 1
                    missing_patients += wt
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
        if stat_func == total_ed_event:
            file_name = 'control_surrogates/control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES))
        elif stat_func == total_with_median_income:
            file_name = 'control_surrogates/core_surrogate_{0}_{1}.csv'.format(str(i),'ZIPINC_QRTL')
        elif stat_func == total_in_quarter:
            file_name = 'control_surrogates/core_surrogate_{0}_{1}.csv'.format(str(i),'DQTR')
        elif stat_func == average_age:
            file_name = 'control_surrogates/core_surrogate_{0}_{1}.csv'.format(str(i),'AGE')
           
        else:
            print('invalid stat_func.')
            sys.exit(1)
        if code is not None:
            random_stat.append(stat_func(file_name,code))
        else:
            random_stat.append(stat_func(file_name))

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
    Median household income quartiles for patient's ZIP Code.
    For 2012, the median income quartiles are defined as:
    1) $1 - $38,999; (2) $39,000 - $47,999; (3) $48,000 - $62,999;
    and (4) $63,000 or more.
'''
def total_with_median_income(filename,code, no_missing=0):

    data_type = get_data_type()
    ZIPINC_QRTL_index = int(data_type.index('ZIPINC_QRTL'))
    num_with_zip_inc = total_with(filename,code,ZIPINC_QRTL_index,None,no_missing,data_type)
    return num_with_zip_inc

''' 
'''
def total_in_quarter(filename,code, no_missing=0):

    data_type = get_data_type()
    DQTR_index = int(data_type.index('DQTR'))
    num_in_dqtr = total_with(filename,code,DQTR_index,None,no_missing,data_type)
    return num_in_dqtr

''' 
    ICD-9-CM procedures performed in ED
'''
def total_with_procedure_ed(filename,code, no_missing=0):
    data_type = get_data_type_ed_supplement()
    PR_ED1_index = int(data_type.index('PR_ED1'))
    PR_ED9_index = int(data_type.index('PR_ED9'))
    num_with_procedure = total_with(filename,code,PR_ED1_index,PR_ED9_index, no_missing,data_type)
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
    num_with_procedure = total_with(filename,code,PR_IP1_index,PR_IP9_index, no_missing,data_type)
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
            wt = pt_weight(line,data_type)
            try:
                if float(line[TOTCHG_ED_index]) >= 0:
                    total_charges += float(line[TOTCHG_ED_index])*wt
                    # num_patients += 1
                    num_patients += wt
            except:
                # missing_patients +=1
                missing_patients += wt
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
            wt = pt_weight_ip(line,data_type)
            try:
                if float(line[TOTCHG_IP_index]) >= 0:
                    total_charges += float(line[TOTCHG_IP_index])*wt
                    # num_patients += 1
                    num_patients += wt
            except:
                # num_patients += 1
                missing_patients += wt
    if missing_patients > 0:
        print('Missing patients: {0}'.format(str(missing_patients),))
        print('Counted patients: {0}'.format(str(num_patients),))
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
            wt = pt_weight_ip(line,data_type)
            try:
                los_total += float(line[LOS_IP_index])*wt
                num_patients += wt
            except:
                missing_patients +=wt
    if missing_patients > 0:
        print('Missing patients: {0}'.format(str(missing_patients),))
        print('Counted patients: {0}'.format(str(num_patients),))
    return float(los_total)/float(num_patients)

def test_erectile_fracture_code():
    data_type = get_data_type()
    filename = 'cleaned_data/core_patients_cleaned.csv'
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    return total_with(filename,PENILE_FRACTURE_CODE,DX1_index,DX15_index,0,data_type)

def odds_ratio_urethral_injury():
    data_type = get_data_type()
    patients_filename = 'cleaned_data/core_patients_cleaned.csv'
    core_filename = 'cleaned_data/core_controls_cleaned.csv'
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))

    DE = 0
    DNE = 0
    HE = 0
    HNE = 0

    missing_patients = 0
    missing_controls = 0


    with open(patients_filename,'r') as patients:
        reader = csv.reader(patients)
        for line in reader:
            wt = pt_weight(line,data_type)
            if URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                # DE += 1
                DE += wt
            else:
                # HE += 1
                HE += wt
    with open(core_filename, 'r') as controls:
        reader = csv.reader(controls)
        for line in reader:
            wt = pt_weight(line,data_type)
            if URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                # DNE += 1
                DNE += wt
            else:
                # HNE += 1
                HNE += wt
    print('Number of urethral injuries in EF patients: ')
    print(float(DE))
    print('Total number of other patients: ')
    print(float(DE+HE))
    print('Number of urethral injuries in rest: ')
    print(float(DNE))
    print('Total number of other patients: ')
    print(float(DNE+HNE))
    NE = DE+HE
    NNE = DNE+HNE
    return (float(DE)/float(HE))/(float(DNE)/float(HNE))

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
            return 0.0
    else:
        return 0.0

def core_by_key(key):
    data_type = get_data_type()
    key_index_core = int(data_type.index('KEY_ED'))
    with open('cleaned_data/core_patients_cleaned.csv') as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            if line[key_index_core] == key:
                return line
    return []

def pt_weight_ip(line,data_type):
    key_index = int(data_type.index('KEY_ED'))
    pt = core_by_key(line[key_index])
    if not pt:
        return 0.0
    return pt_weight(line,get_data_type())

def total_patients():
    data_type = get_data_type()
    tp = 0
    with open('cleaned_data/core_patients_cleaned.csv') as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            tp += pt_weight(line,data_type)
    return tp


def main():

    # print('Average age')
    # stat = get_bootstrap_statistic(average_age)
    # print('Statistic: {0}'.format(stat,))
    # print(stat > (1-0.025/float(6)))
    # print('Total patients: {0}'.format(total_patients()))
    # print('Total ED events')
    # choices = [1, 2, 3, 9, 98, 99]
    # labels = ['treated and released','admitted','transferred','died','destination unknown','discharged alive']
    # for choice in choices:
    #     print('\t{0}: {1}'.format(labels[choices.index(choice)],str(total_ed_event('cleaned_data/core_patients_cleaned.csv',choice))))
    #     stat = get_bootstrap_statistic(total_ed_event,choice)
    #     print('\tStatistic: {0}'.format(stat,))
    #     print(stat > (1-0.025/float(6)))
    #     print(stat < (0.025/float(6)))


    # print('TOTAL WITH MEDIAN INCOME')
    # choices = [1, 2, 3, 4]
    # labels = []
    # for choice in choices:
    #     stat = get_bootstrap_statistic(total_with_median_income,choice)
    #     print('Statistic: {0}'.format(stat,))
    #     print(stat > (1-0.025/float(6)))
    #     print(stat < (0.025/float(6)))

    # print('total in quarter')
    # choices = [1, 2, 3, 4]
    # for choice in choices:
    #     stat = get_bootstrap_statistic(total_in_quarter,choice)
    #     print('Statistic: {0}'.format(stat,))
    #     print(stat > (1-0.025/float(6)))
    #     print(stat < (0.025/float(6)))
    
    # print(test_erectile_fracture_code())


    # print('Average age of control group: {0}'.format(str(average_age('cleaned_data/core_controls_cleaned.csv')),))
    # print('Average age of patient group: {0}'.format(str(average_age('cleaned_data/core_patients_cleaned.csv')),))
    # print('Total number  of urethral fractures:')
    # print(total_with_urethral_injury('cleaned_data/core_patients_cleaned.csv'))

    # print('Total cost of stay in ED:')
    # print(average_charges_ed('cleaned_data/core_patients_cleaned.csv'))

    print('Odds ratio for urethral injury:')
    print(odds_ratio_urethral_injury())

    print('Average length of stay:')
    print(average_los('cleaned_data/ip_patients_cleaned.csv'))

    print('Total cost of stay in IP:')
    print(average_charges_ip('cleaned_data/ip_patients_cleaned.csv'))




    

if __name__ == '__main__':
    main()
