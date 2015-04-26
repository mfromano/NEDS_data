import csv
import numpy

def getlength(f):
    m = open(f)
    reader = csv.reader(m)
    count = 0
    for line in reader:
        count+=1
    return count


for i in np.arange(0,1000):
    curr_file = 'control_surrogates/core_surrogate_{0}_DQTR.csv'.format(str(i),)
    length = getlength(curr_file)
    if length is not 381:
        print curr_file