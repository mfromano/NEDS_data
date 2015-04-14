import sys
import csv

m = open(str(sys.argv[1]))
reader = csv.reader(m)

count = 0
for line in reader:
    count+=1
print(count)