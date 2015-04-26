from load_and_process import *
import csv

def make_parsed_core(data_name):
    data_type = get_data_type()
    data_index = int(data_type.index(data_name))

    with open('cleaned_data/core_controls_cleaned.csv','r') as control_file:
        csv_reader = csv.reader(control_file)
        with open('core_controls_cleaned_{0}.csv'.format(data_name,), 'w') as new_file:
            csv_writer = csv.writer(new_file)
            for line in csv_reader:
                if line[data_index] is not None and line[data_index] is not '':
                    csv_writer.writerow(line)



if __name__ == '__main__':
    # make_parsed_core('PAY1')
    # make_parsed_core('ZIPINC_QRTL')
    # make_parsed_core('DQTR')
    # make_parsed_core('AGE')
    # make_surrogate_data(0,1000, 389, 'ZIPINC_QRTL')
    # print('Done with zipinc_qrtl')
    make_surrogate_data(42,44, 381, 'DQTR')
    print('Done with dqtr')