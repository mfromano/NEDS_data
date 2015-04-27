import csv

PROSTATITIS_CODE = '6019 '

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

if __name__ == "__main__":
    data_type = get_data_type()
    DX1_index = int(data_type.index('DX1'))
    DX15_index = int(data_type.index('DX15'))
    total_cases = 0
    with open('raw_data/NEDS_2012_CORE.csv') as raw_file:
        reader = csv.reader(raw_file)
        for line in reader:
            if PROSTATITIS_CODE in line[DX1_index:DX15_index]:
                total_cases += 1
    print total_cases