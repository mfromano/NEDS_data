import csv

# 10415 = total cases in 2012 without chronic prostatitis
# 10418 = total cases in 2012 (including chronic prostatitis)

TORSION_CODES = ['60820','60821','60822','60823','60824']
PROSTATITIS_CODE = '6019'
CHRONIC_CODE = '6011'

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
    total_cases = [0, 0, 0, 0, 0]
    with open('raw_data/NEDS_2012_CORE.csv') as raw_file:
        reader = csv.reader(raw_file)
        for line in reader:
            for t in range(len(TORSION_CODES)):
                if TORSION_CODES[t] in line[DX1_index:DX15_index]:
                    total_cases[t] += 1

    print total_cases