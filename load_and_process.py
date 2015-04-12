import os
import os.path
import csv
import numpy as np
# import scipy

# 362 total patients with DX1 = penile fracture
TOTAL_FRACTURES = 390  # so, 9 women had penile fractures???? Or messed up entries???
TOTAL_MALE_PATIENTS =  13797122    
# TOTAL_ALL_PATIENTS = 31091020  # total patients

def load_and_format(start, finish):
    # if os.path.isfile('NEDS_2012_CORE_Control.csv') and os.path.isfile('NEDS_2012_CORE_Patients.csv'):
    #     return
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
    print num_patients
    print total_patients
    return data_type
    samples = np.array(start,finish)
def make_surrogate_data(indices):
    def get_and_save_control_rows(indices,i):
            with open('control_surrogate_{0}_numfracs_{1}.csv'.format(str(i),str(TOTAL_FRACTURES)),'w') as outputfile:
                outputwriter = csv.writer(outputfile)
                with open('NEDS_2012_CORE_Control.csv','r') as control_file:
                    control_reader = csv.reader(control_file)
                    line_number = 0
                    for line in control_reader:
                        if line_number in indices:
                            outputwriter.writerow(line)
                        elif line_number > max(indices):
                            return
                        line_number += 1

    for i in samples:
        control_indices = np.random.randint(0,TOTAL_MALE_PATIENTS-TOTAL_FRACTURES-1,size=TOTAL_FRACTURES)
        get_and_save_control_rows(control_indices,i)
        print "done with surrogate number {0}".format(str(i))

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

def main():
    # load_and_format()
    make_surrogate_data(56,999)

if __name__ == '__main__':
    main()