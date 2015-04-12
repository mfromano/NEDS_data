import os
import csv
import numpy as np
import scipy

# 362 total patients with DX1 = penile fracture
TOTAL_FRACTURES = 399
TOTAL_PATIENTS =  31091020  # total patients

def load_and_format():
    data_labels = {}
    data_type = []
    with open('NEDS_2012_Labels_Core.txt','r') as read_file:
        for f in read_file:
            currline = f.split('\"')[:2]
            currline[0] = currline[0].strip()
            data_labels[currline[0]] = currline[1]
            data_type.append(currline[0])

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
                total_men = 0
                for line in csv_reader:
                    if penile_fracture_code in line[np.arange(DX1_index,DX15_index)]:
                        if line[isfemale_index] == 0
                            num_patients += 1
                            filewriter.writerow(line)
                            total_patients += 1
                    else if line[isfemale_index] == 0:
                        control_writer.writerow(line)
                        total_patients += 1
    return data_type

def bootstrap(col_number,num_samples, statistic):

    patient_column = get_patient_column()
    patient_stat = statistic(patient_column)

    control_statistic = [];

    for i in range(len(num_samples)):
        control_indices = np.random.randint(0,TOTAL_PATIENTS-TOTAL_FRACTURES-1,size=TOTAL_FRACTURES)
        control_column = get_control_column(control_indices)
        control_statistic.append(statistic(control_column))

    def get_control_column(indices):
        column = []
        with open('NEDS_2012_CORE_Control.csv','r') as control_file:
            control_reader = csv.reader(control_file)
            line_number = 0
            for line in control_reader:
                if line_number in indices:
                    column.append(line[col_number])
                line_number += 1
        return column

    def get_patient_column():
        column = []
        with open('NEDS_2012_CORE_Patients.csv','r') as patient_file:
            patient_reader = csv.reader(patient_file)
            for line in patient_reader:
                column.append(line[col_number])
        return column

    return column

def main():
    data_type = load_and_format()
    bootstrap(sdkjf,1000)

if __name__ == '__main__':
    main()