'''
this module contains code for conditioning on erectile fracture: what makes patients more
likely to get 
'''

from neds_utils import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
from numpy import genfromtxt

'''


Initialize global variables


'''


data_type = get_data_type()
data_type_ip = get_data_type_ip_supplement()
data_type_ed = get_data_type_ed_supplement()
PAYER1_INDEX = int(data_type.index('PAY1'))
KEY_INDEX = int(data_type.index('KEY_ED'))
KEY_INDEX_IP = int(data_type_ip.index('KEY_ED'))
KEY_INDEX_ED = int(data_type_ed.index('KEY_ED'))
DISP_INDEX = int(data_type.index('DISP_ED'))
age_index = int(data_type.index('AGE'))
DQTR_index = int(data_type.index('DQTR'))
DX1_INDEX = int(data_type.index('DX1'))
DX15_INDEX = int(data_type.index('DX15'))
PT_WT_CORE = int(data_type.index('DISCWT'))
TOTCHG_ED_index = int(data_type.index('TOTCHG_ED'))
TOTCHG_IP_index = int(data_type_ip.index('TOTCHG_IP'))
ZIPINC_QRTL_index = int(data_type.index('ZIPINC_QRTL'))
URETHRAL_INJURY_CODES = ('8670','8671')
PEYRONIES = "60785"
LOS_IP_index = int(data_type_ip.index('LOS_IP'))

def loaddata(filehandle):
    data = filehandle.read()
    data = data.split("\n")
    for i,line in enumerate(data):
        data[i] = np.asarray(line.split(","))
    return np.asarray(data)

def avg_age(filehandle,plot=False):
    data = loaddata(filehandle)
    ages = np.asarray([])
    weight_sum = 0
    for line in data:
        try:
            ages = np.append(ages,int(line[age_index])*pt_weight(line))
            weight_sum += pt_weight(line)
        except:
            ages = np.append(ages,np.nan)
    mean_age = np.nansum(ages/weight_sum)
    '''
    Fix next line
    '''
    std_age = (np.nanstd(ages/weight_sum));
    return mean_age,std_age

def proportion_income(data,code):
    total = 0
    patient_count = 0
    for line in data:
        if len(line) > 1:
            patient_count += pt_weight(line)
            if line[ZIPINC_QRTL_index] and int(line[ZIPINC_QRTL_index]) == code:
                total += pt_weight(line)
    return total/patient_count

def proportion_with_income(filehandle,code,std=False):
    data = loaddata(filehandle)
    total = proportion_income(data,code)
    if std:
        stats = bootstrap(proportion_income,data,max_int=(len(data)-1),size=len(data),code=code)
    return total, np.nanstd(stats), np.nanmean(stats)

def average_los(data,code=None):
    los_total = 0
    num_patients = 0
    missing_patients = 0
    for line in data:
        if len(line) > 1:
            wt = pt_weight_ip(line,data_type_ip)
            ip_line = ip_by_key(line[KEY_INDEX_IP])
            try:
                los_total += float(ip_line[LOS_IP_index])*wt
                num_patients += wt
            except:
                missing_patients +=wt
    if missing_patients > 0:
        print('Missing patients: {0}'.format(str(missing_patients),))
        print('Counted patients: {0}'.format(str(num_patients),))

    return float(los_total)/float(num_patients)

def get_average_los(ipfilehandle,std=False):
    data_type = data_type_ip
    los_total = 0
    num_patients = 0
    missing_patients = 0
    data = loaddata(ipfilehandle)
    stats = np.nan
    if std:
        stats = bootstrap(average_los,data,len(data)-1,len(data),1000,None)
    return average_los(data), np.nanstd(stats), np.nanmean(stats)

def average_charges_ip(data,code=None):
    total_charges = 0
    num_patients = 0
    missing_patients = 0
    for line in data:
        if len(line) > 1:
            wt = pt_weight_ip(line)
            ip_line = ip_by_key(line[KEY_INDEX_IP])
            try:
                if float(ip_line[TOTCHG_IP_index]) >= 0:
                    total_charges += float(ip_line[TOTCHG_IP_index])*wt
                    num_patients += wt
            except:
                # num_patients += 1
                missing_patients += wt
    # if missing_patients > 0:
        # print('Missing patients: {0}'.format(str(missing_patients),))
        # print('Counted patients: {0}'.format(str(num_patients),))
    return float(total_charges)/float(num_patients)

def get_average_charges_ip(filehandle,std=False):
    data = loaddata(filehandle)
    stats = np.nan
    if std:
        stats = bootstrap(average_charges_ip,data,len(data)-1,len(data),1000,None)
    return average_charges_ip(data), np.nanstd(stats), np.nanmean(stats)

def total_in_quarter(data,code):
    total = 0
    total_pts = 0
    missing_patients = 0
    for line in data:
        if len(line) > 1:
            wt = pt_weight(line)
            try:
                if int(line[DQTR_index]) == code:
                    total += wt
                total_pts += wt
            except:
                missing_patients += wt
    # if missing_patients > 0:
    #     print('Missing patients: {0}'.format(str(missing_patients),))
    return float(total)/float(total_pts)

def get_total_in_quarter(filehandle,code,std=False):
    data = loaddata(filehandle)
    stats = np.nan
    if std:
        stats = bootstrap(total_in_quarter,data,len(data)-1, len(data), 1000, code)
    return total_in_quarter(data,code), np.nanstd(stats), np.nanmean(stats)

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

def total_disp(data,code):
    total = 0
    total_pts = 0
    missing_patients = 0
    for line in data:
        if len(line) > 1:
            wt = pt_weight(line)
            try:
                if int(line[DISP_INDEX]) == code:
                    total += wt
                total_pts += wt
            except:
                missing_patients += wt
    # if missing_patients > 0:
    #     print('Missing patients: {0}'.format(str(missing_patients),))
    return float(total)/float(total_pts)

def get_total_disp(filehandle,code,std=False):
    data = loaddata(filehandle)
    stats = np.nan
    if std:
        stats = bootstrap(total_disp,data,len(data)-1,len(data), 1000, code)
    return total_disp(data,code), np.nanstd(stats), np.nanmean(stats)

def average_charges_ed(data):
    total_charges = 0
    num_patients = 0
    missing_patients = 0
    for line in data:
        wt = pt_weight(line)
        try:
            if float(line[TOTCHG_ED_index]) >= 0:
                total_charges += float(line[TOTCHG_ED_index])*wt
                num_patients += wt
        except:
            # missing_patients +=1
            missing_patients += wt
    # if missing_patients > 0:
    #     print('Missing patients: {0}'.format(str(missing_patients),))
    return float(total_charges)/float(num_patients)

def get_average_charges_ed(filehandle,std=False):
    data = loaddata(filehandle)
    stats = np.nan
    if std:
        stats = bootstrap(average_charges_ed,data,len(data)-1,len(data), 1000, None)
    return average_charges_ed(data), np.nanstd(stats), np.nanmean(stats)

def total_payer1(data,code):
    total = 0
    total_pts = 0
    missing_patients = 0
    for line in data:
        if len(line) > 1:
            wt = pt_weight(line)
            try:
                if int(line[PAYER1_INDEX]) == code:
                    total += wt
                total_pts += wt
            except:
                missing_patients += wt
    # if missing_patients > 0:
    #     print('Missing patients: {0}'.format(str(missing_patients),))
    return float(total)/float(total_pts)

def get_total_payer1(filehandle,code,std=False):
    data = loaddata(filehandle)
    stats = np.nan
    if std:
        stats = bootstrap(total_payer1,data,len(data)-1,len(data), 1000, code)
    return total_payer1(data,code), np.nanstd(stats), np.nanmean(stats)


'''


The next section includes the bootstrapping utilities


'''
def bootstrap(func,data_mat,max_int,size,num_samples=1000,code=None):
    stats = np.empty(num_samples)
    for i in range(num_samples):
        curr_mat = resample_with_replacement(data_mat,max_int,size)
        if code is not None:
            stats[i] = func(curr_mat,code)
        else:
            stats[i] = func(curr_mat)
    return stats

def resample_with_replacement(data_mat,max_int,size):
    indices = np.random.randint(0,max_int,size=size)
    return data_mat[indices]

'''

Next section includes getter methods

'''


def pt_weight(line,data_type=data_type):
    key_index_core = int(data_type.index('DISCWT'))
    if key_index_core is not '':
        try:
               return float(line[key_index_core])
        except:
            return 0.0
    else:
        return 0.0

def ip_by_key(key):
    key_index_ip = int(data_type_ip.index('KEY_ED'))
    with open('cleaned_data/ip_patients_cleaned.csv') as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            if line[key_index_ip] == key:
                return line
    return []

def core_by_key(key,data_type=data_type):
    key_index_core = int(data_type.index('KEY_ED'))
    with open('cleaned_data/core_patients_cleaned.csv') as inputfile:
        reader = csv.reader(inputfile)
        for line in reader:
            if line[key_index_core] == key:
                return line
    return []

def pt_weight_ip(line,data_type=data_type_ip):
    key_index = int(data_type.index('KEY_ED'))
    pt = core_by_key(line[key_index])
    if not pt:
        return 0.0
    return pt_weight(line,get_data_type())


'''
def split_by_urethral_fracture(filehandle):
    data_type = get_data_type()
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    data = loaddata(filehandle)
    with open('cleaned_data/core_patients_cleaned_uf.csv','w') as uf_file:
        uf_writer = csv.writer(uf_file)
        with open('cleaned_data/core_patients_cleaned_no_uf.csv','w') as nouf_file:
            nouf_writer = csv.writer(nouf_file)

            for line in data:
                if URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                    uf_writer.writerow(line)
                elif URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                    uf_writer.writerow(line)
                else:
                    nouf_writer.writerow(line)
'''
'''
def split_by_urethral_fracture_ip(filehandle):
    data_type = get_data_type()
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    data = loaddata(filehandle)
    with open('cleaned_data/ip_patients_cleaned_uf.csv','w') as uf_file:
        uf_writer = csv.writer(uf_file)
        with open('cleaned_data/ip_patients_cleaned_no_uf.csv','w') as nouf_file:
            nouf_writer = csv.writer(nouf_file)

            for currline in data:
                if len(currline) > 1:
                    line = core_by_key(currline[KEY_INDEX_IP])
                    if URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                        uf_writer.writerow(currline)
                    elif URETHRAL_INJURY_CODES[0] in line[DX1_index:DX15_index]:
                        uf_writer.writerow(currline)
                    else:
                        nouf_writer.writerow(currline)
'''
def main():
    
    uf = open('cleaned_data/core_patients_cleaned_uf.csv','r')
    no_uf = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
    mean1,std1 = avg_age(uf,1)
    mean2,std2 = avg_age(no_uf,1)
    print('Mean age for uf patients: {0} +/- {1}'.format(str(mean1),str(std1),))
    print('Mean age for no-uf patients: {0} +/- {1}'.format(str(mean2),str(std2),))
    print('Age p-value (uf - no_uf): {0}\n'.format(str(wald_test(mean1,std1,mean2,std2))))
    print("\n")

    for i in [1, 2, 3, 4]:
        uf = open('cleaned_data/core_patients_cleaned_uf.csv','r')
        no_uf = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
        mean1,std1,other = proportion_with_income(uf,i,1)
        mean2,std2,other = proportion_with_income(no_uf,i,1)
        print('Proportion uf patients with income {0}: {1} +/- {2}'.format(str(i),str(mean1),str(std1),))
        print('Proportion no-uf patients with income {0}: {1} +/- {2}'.format(str(i),str(mean2),str(std2),))
        print('Income {0} p-value (uf - no_uf): {1}\n'.format(str(i), str(wald_test(mean1,std1,mean2,std2))))

    print("\n")
    uf = open('cleaned_data/ip_patients_cleaned_uf.csv','r')
    no_uf = open('cleaned_data/ip_patients_cleaned_no_uf.csv','r')
    mean1,std1,other = get_average_los(uf,1)
    mean2,std2,other = get_average_los(no_uf,1)
    print('Mean length of stay for uf patients: {0} +/- {1}'.format(str(mean1),str(std1),))
    print('Mean length of stay for no-uf patients: {0} +/- {1}'.format(str(mean2),str(std2),))
    print('Length of stay p-value (uf - no_uf): {0}\n'.format(str(wald_test(mean1,std1,mean2,std2))))
    print("\n")

    uf = open('cleaned_data/ip_patients_cleaned_uf.csv','r')
    no_uf = open('cleaned_data/ip_patients_cleaned_no_uf.csv','r')
    mean1,std1,other = get_average_charges_ip(uf,1)
    mean2,std2,other = get_average_charges_ip(no_uf,1)
    print('Mean IP charges for uf patients: {0} +/- {1}'.format(str(mean1),str(std1),))
    print('Mean IP charges for no-uf patients: {0} +/- {1}'.format(str(mean2),str(std2),))
    print('IP charges p-value (uf - no_uf): {0}\n'.format(str(wald_test(mean1,std1,mean2,std2))))
    print("\n")


    for quarter in [1, 2, 3, 4]:
        uf = open('cleaned_data/core_patients_cleaned_uf.csv','r')
        no_uf = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
        mean1,std1,other = get_total_in_quarter(uf,quarter,1)
        mean2,std2,other = get_total_in_quarter(no_uf,quarter,1)
        print('Proportion uf patients in quarter {0}: {1} +/- {2}'.format(str(quarter),str(mean1),str(std1),))
        print('Proportion no-uf patients in quarter {0}: {1} +/- {2}'.format(str(quarter),str(mean2),str(std2),))
        print('Income {0} p-value (uf - no_uf): {1}\n'.format(str(i), str(wald_test(mean1,std1,mean2,std2))))

    
    disp_codes = [1, 2, 5, 6, 7, 9, 20, 21, 98, 99]
    for code in disp_codes:
        f = open('cleaned_data/core_patients_cleaned_uf.csv','r')
        mean1,std1,other1 = get_total_disp(f,code,1)
        f = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
        mean2,std2,other2 = get_total_disp(f,code,1)
        print('Proportion uf patients with dispo {0}: {1} +/- {2}'.format(str(code),str(mean1),str(std1),))
        print('Proportion no-uf patients with dispo {0}: {1} +/- {2}'.format(str(code),str(mean2),str(std2),))
        print('Disp {0} for p-value: {1}\n'.format(str(code),str(wald_test(mean1,std1,mean2,std2))))

    '''
    Disp 1 for p-value: 0.00884769895944
    Disp 2 for p-value: 0.00671030440287
    Disp 5 for p-value: 0.0230632291823
    Disp 6 for p-value: 0.151082757681
    Disp 7 for p-value: 0.00241310069598
    Disp 9 for p-value: 0.999851356752
    Disp 20 for p-value: nan
    Disp 21 for p-value: nan
    Disp 98 for p-value: 0.161672911723
    Disp 99 for p-value: nan
    '''
    print("\n\n")
    f = open('cleaned_data/core_patients_cleaned_uf.csv','r')
    mean1,std1,other1 = get_average_charges_ed(f,1)
    f = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
    mean2,std2,other2 = get_average_charges_ed(f,1)
    print('Mean ED charges for uf patients: {0} +/- {1}'.format(str(mean1),str(std1),))
    print('Mean ED charges for no-uf patients: {0} +/- {1}'.format(str(mean2),str(std2),))
    print('Average charges ED p-value: {0}\n'.format(str(wald_test(mean1,std1,mean2,std2))))
    print("\n")

    uf = open('cleaned_data/ip_patients_cleaned_uf.csv','r')
    mean1,std1,other1 = get_average_charges_ip(uf,1)
    no_uf = open('cleaned_data/ip_patients_cleaned_no_uf.csv','r')
    mean2,std2,other2 = get_average_charges_ip(no_uf,1)
    print('Mean IP charges for uf patients: {0} +/- {1}'.format(str(mean1),str(std1),))
    print('Mean IP charges for no-uf patients: {0} +/- {1}'.format(str(mean2),str(std2),))
    print('Average charges IP p-value: {0}\n'.format(str(wald_test(mean1,std1,mean2,std2))))
    
    '''
        Expected primary payer, uniform: (1) Medicare, (2)
        Medicaid, (3) private including HMO, (4) self-pay, (5) no
        charge, (6) other
    '''
    print("\n")
    for code in [1, 2, 3, 4, 5, 6]:
        uf = open('cleaned_data/core_patients_cleaned_uf.csv','r')
        mean1,std1,other1 = get_total_payer1(uf,code,std=True)
        no_uf = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
        mean2,std2,other2 = get_total_payer1(no_uf,code,std=True)
        print('Proportion uf patients with payer1 {0}: {1} +/- {2}'.format(str(code),str(mean1),str(std1),))
        print('Proportion no-uf patients with payer1 {0}: {1} +/- {2}'.format(str(code),str(mean2),str(std2),))
      
        print('Proportion of patients with payer1 {0} p-value: {1}'.format(str(code),str(wald_test(mean1,std1,mean2,std2))))
   

if __name__ == "__main__":
    main()