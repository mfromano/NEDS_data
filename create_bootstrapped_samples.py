from load_and_process import *
import csv

def make_parsed_core(data_name):
    data_type = get_data_type()
    data_index = int(data_type.index(data_name))

    with open('cleaned_data/core_control_cleaned.csv','r') as control_file:
        csv_reader = csv.reader(control_file)
        with open('core_control_cleaned_{0}.csv'.format(data_name,), 'w') as new_file:
            csv_writer = csv.writer(new_file)
            for line in csv_reader:
                if line[data_index] is not None and line[data_index] is not '':
                    csv_writer.writerow(line)

if __name__ == '__main__':
    make_parsed_core('PAY1')
    make_parsed_core('ZIPINC_QRTL')
    make_parsed_core('DQTR')
