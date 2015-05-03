import csv
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
import json
import math
'''
   "610 " = "610 : SCROTUM & TUNICA I & D"
   "6111" = "6111: SCROTUM & TUNICA BIOPSY"
   "6119" = "6119: SCROT/TUNICA DX PROC NEC"
   "612 " = "612 : EXCISION OF HYDROCELE"
   "613 " = "613 : SCROTAL LES DESTRUCTION"
   "6141" = "6141: SUTURE SCROTAL LACERAT"
   "6142" = "6142: SCROTAL FISTULA REPAIR"
   "6149" = "6149: SCROTUM/TUNIC REPAIR NEC"
   "6191" = "6191: PERCUT TUNICA ASPIRATION"
   "6192" = "6192: EXCISION TUNICA LES NEC"
   "6199" = "6199: SCROTUM & TUNICA OP NEC"
   "620 " = "620 : INCISION OF TESTES"
   "6211" = "6211: CLOSED TESTICULAR BIOPSY"
   "6212" = "6212: OPEN TESTICULAR BIOPSY"
   "6219" = "6219: TESTES DX PROCEDURE NEC"
   "622 " = "622 : TESTICULAR LES DESTRUCT"
   "623 " = "623 : UNILATERAL ORCHIECTOMY"
   "6241" = "6241: REMOVE BOTH TESTES"
   "6242" = "6242: REMOVE SOLITARY TESTIS"
   "625 " = "625 : ORCHIOPEXY"
'''

# import matplotlib.pyplot as plt
# 10415 = total cases in 2012 without chronic prostatitis
# 10418 = total cases in 2012 (including chronic prostatitis)

ORCHIECTOMY_CODE = '623'
TORSION_CODES = ['60820','60821','60822','60823','60824']
TORSION_TOTALS = [1936, 4, 40, 310, 75]
PROSTATITIS_CODE = '6019'
CHRONIC_PROSTATITIS_CODE = '6011'


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

def fit_bino_glm(Y, X, intercept=1):
    X = np.array(X)
    Y = np.array(Y)
    if intercept:
        X = sm.tools.tools.add_constant(X)
    glm_binom = sm.GLM(Y,X,family=sm.families.Binomial())
    res = glm_binom.fit()
    print(res.summary())
    return res

def has_procedure_code(line, code):
    data_type = get_data_type_ip_supplement()
    PR_IP1_index = int(data_type.index('PR_IP1'))
    PR_IP9_index = int(data_type.index('PR_IP9'))
    if code in line[PR_IP1_index:PR_IP9_index]:
        return True
    else:
        return False

def age_response_vector(code):
    Y = []
    key_list = []
    core_data_type = get_data_type()
    ip_data_type = get_data_type_ip_supplement()
    ip_key_index = int(ip_data_type.index('KEY_ED'))
    # create response vector and get list of keys
    with open('cleaned_data/ip_torsion_patients_cleaned.csv') as ip_file:
        ip_reader = csv.reader(ip_file)
        for line in ip_reader:
            if has_procedure_code(line,code):
                Y.append(1)
            else:
                Y.append(0)
            key_list.append(line[ip_key_index])
    return Y, key_list

def ages_from_key_list(key_list, Y):
    core_data_type = get_data_type()
    age_list = []
    age_index = int(core_data_type.index('AGE'))
    core_key_index = int(core_data_type.index('KEY_ED'))
    for key in key_list:
        with open('cleaned_data/core_torsion_patients_cleaned.csv') as core_file:
            core_reader = csv.reader(core_file)
            for line in core_reader:
                if key == line[core_key_index]:
                    age_list.append(int(line[age_index]))
    with open('cleaned_data/core_torsion_patients_cleaned.csv') as core_file:
        core_reader = csv.reader(core_file)
        for line in core_reader:
            if line[core_key_index] not in key_list:
                Y.append(0)
                age_list.append(int(line[age_index]))
    return age_list, Y

def plot_odds(Y, age_list, numbins, proc_name):
    # find indices at which patient got procedure
    indices = [i for i, x in enumerate(Y) if x == 1]
    # get ages of patients who got the procedure
    patient_ages = list(age_list[i] for i in indices)
    # get the counts for ages of all patients
    age_hist, bins = np.histogram(age_list,bins=numbins)
    # get the counts for patients with the procedure
    patient_hist, bins = np.histogram(patient_ages,bins=bins)
    # now, plot odds

    # first, get the bin centers to plot the bar graph
    bin_centers = list((bins[i]+bins[i-1])/2 for i,x in enumerate(bins) if i > 0)
    # calculate the fraction of patients in each age group who received the procedure
    frac = list(float((patient_hist[i]))/float(x) for i,x in enumerate(age_hist))
    # odds of patients in each age group who got procedure
    odds = list((float(patient_hist[i])/float(x-patient_hist[i])) for i,x in enumerate(age_hist))
    plt.bar(bin_centers,odds,width=(100/len(bin_centers)/2))
    plt.title(proc_name)
    plt.xlabel('Age')
    plt.ylabel('Odds (number with procedure/number without procedure)')
    plt.show()

# MEAT of the file
def make_proc_vs_age(code, numbins, proc_title):
    '''
        1. Open both IP and Core patient files
        2. Add whether or not orchiectomy to Y vector (has proc code)
        3. Get key_ed
        4. Add to key_ed list
        5. Find key_ed in core patient file
        6. Add patient age to appropriate time bin in X
        7. calls fit_bino_glm
    '''
    Y, key_list = age_response_vector(code)
    print('Got response vector')
    # now get list of ages for each key
    age_list, Y = ages_from_key_list(key_list, Y)
    print('ot age list')
    # Fit to age
    res = fit_bino_glm(Y,age_list,intercept=1)

    plot_odds(Y,age_list, numbins, proc_title)


if __name__ == '__main__':
    make_proc_vs_age("623", 10, 'Orchiectomy')
    # make_proc_vs_age("625", 10, 'Orchiopexy')