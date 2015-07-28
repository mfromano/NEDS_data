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
KEY_INDEX = int(data_type.index('KEY_ED'))
KEY_INDEX_IP = int(data_type_ip.index('KEY_ED'))
age_index = int(data_type.index('AGE'))
DQTR_index = int(data_type.index('DQTR'))
DX1_INDEX = int(data_type.index('DX1'))
DX15_INDEX = int(data_type.index('DX15'))
PT_WT_CORE = int(data_type.index('DISCWT'))
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
    '''
    uf = open('cleaned_data/core_patients_cleaned_uf.csv','r')
    no_uf = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
    print(avg_age(uf,1))
    print(avg_age(no_uf,1))

    for i in [1, 2, 3, 4]:
        uf = open('cleaned_data/core_patients_cleaned_uf.csv','r')
        no_uf = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
        print(proportion_with_income(uf,i,1))
        print(proportion_with_income(no_uf,i,1))
    '''
    '''
    # f = open('cleaned_data/ip_patients_cleaned_uf.csv','r')
    # print(get_average_los(f,1))
    # f = open('cleaned_data/ip_patients_cleaned_no_uf.csv','r')
    # print(get_average_los(f,1))

    Results:
    (1.3852565636026553, 0.33257123228775143, 1.3739200592005396)
    (1.3104457078589253, 0.12300279919850013, 1.3102100680086051)

    '''
    '''
    uf = open('cleaned_data/ip_patients_cleaned_uf.csv','r')
    print(get_average_charges_ip(uf,1))
    no_uf = open('cleaned_data/ip_patients_cleaned_no_uf.csv','r')
    print(get_average_charges_ip(no_uf,1))

    results:
    (25957.623945936248, 3770.8267806642266, 26018.075265601037)
    (24053.334909953413, 1730.6620820702638, 24105.3718470364)

    '''
    for quarter in [1, 2, 3, 4]:
        f = open('cleaned_data/core_patients_cleaned_uf.csv','r')
        print('Quarter {0} for urethral fractures: {1}'.format(str(quarter),str(get_total_in_quarter(f,quarter,1)),))
        f = open('cleaned_data/core_patients_cleaned_no_uf.csv','r')
        print('Quarter {0} for non-urethral fractures: {1}'.format(str(quarter),str(get_total_in_quarter(f,quarter,1)),))

    '''
    Quarter 1 for urethral fractures: (0.22903066731519597, 0.06810571802475085, 0.23140388894479119)
    Quarter 1 for non-urethral fractures: (0.22640423214421407, 0.024015952558090827, 0.22586610095899673)
    Quarter 2 for urethral fractures: (0.2553422604123565, 0.073562934347024031, 0.2551065482705987)
    Quarter 2 for non-urethral fractures: (0.2922457089672853, 0.025422477292863066, 0.29174102091696275)
    Quarter 3 for urethral fractures: (0.27067430682929383, 0.070802866457861352, 0.27108968049809024)
    Quarter 3 for non-urethral fractures: (0.28983899372191385, 0.025423987474402852, 0.29018609342546359)
    Quarter 4 for urethral fractures: (0.24495276544315392, 0.072831618626388095, 0.24322737425873014)
    Quarter 4 for non-urethral fractures: (0.19151106516658642, 0.022132580084108282, 0.19273848546435088)

    '''
    

if __name__ == "__main__":
    main()