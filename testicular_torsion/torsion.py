import csv
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
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


def average_age(filename):
    data_type = get_data_type()
    age_index = int(data_type.index('AGE'))
    total_age = 0
    num_patients = 0
    missing_patients = 0
    age_list = []
    with open(filename,'r') as currfile:
        reader = csv.reader(currfile)
        for row in reader:
            if row[age_index] is not None and row[age_index] is not '':
                num_patients +=1
                total_age+=int(row[age_index])
                age_list.append(int(row[age_index]))
            else:
                missing_patients += 1
    if missing_patients > 0:
        print("Total number of missing patients: {0}".format(missing_patients,))

    return (float(total_age)/float(num_patients)), age_list

def load_and_format():
    # Next line gets the type of data for each entry in the core file
    data_type = get_data_type()

    # The next few lines get the indices for the specific entries
    injury_index = int(data_type.index('INJURY'))
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    isfemale_index = int(data_type.index('FEMALE'))

    # open the Core Control file. We will write to this all of the patient
    # records that do not contain a torsion DX*
    with open('core_torsion_control_cleaned.csv','w') as control_file:
        control_writer = csv.writer(control_file,delimiter=',')
        # open the Core Patient file. We will write to this all of the patient
        # records that do contain a broken penis DX
        with open('core_torsion_patients_cleaned.csv','w') as patient_file:
            filewriter = csv.writer(patient_file,delimiter=',')
            with open('cleaned_data/core_cleaned.csv','r') as data_file:
                csv_reader = csv.reader(data_file)
                # num_patients stores the number of patients with a broken penis
                num_patients = 0
                # total_patients stores total male patients
                total_patients = 0
                # 
                for line in csv_reader:
                    if line[isfemale_index] == '0':
                        if any(t in line[DX1_index:DX15_index] for t in TORSION_CODES):
                            num_patients += 1
                            filewriter.writerow(line)
                            total_patients += 1
                        else:
                            control_writer.writerow(line)
                            total_patients += 1
    print(num_patients)
    print(total_patients)

def get_total():
    data_type = get_data_type()
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    total_cases = [0, 0, 0, 0, 0]
    with open('raw_data/NEDS_2012_CORE.csv') as raw_file:
        reader = csv.reader(raw_file)
        for line in reader:
            for t in range(len(TORSION_CODES)):
                if TORSION_CODES[t] in line[DX1_index:DX15_index]:
                    total_cases[t] += 1

    print(total_cases)


if __name__ == "__main__":
    load_and_format()
    