from neds_utils import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
from numpy import genfromtxt
import re
from collections import defaultdict

'''
Example: my_data = genfromtxt('my_file.csv', delimiter=',')

'''

CORE_MALE_FILE_LENGTH = 13797512
data_type = get_data_type()
DX1_INDEX = int(data_type.index('DX1'))
DX15_INDEX = int(data_type.index('DX15'))
PT_WT_CORE = int(data_type.index('DISCWT'))
CHRON1_INDEX = int(data_type.index('CHRON1'))
CHRON15_INDEX = int(data_type.index('CHRON15'))
URETHRAL_INJURY_CODES = ('8670','8671')
PEYRONIES = "60785"
TOBACCO_USE_DISORDER = "3051"
DXLIST = []
'''
"6068 " = "6068 : MALE INFERTILITY NEC"
"6069 " = "6069 : MALE INFERTILITY NOS"
"6070 " = "6070 : LEUKOPLAKIA OF PENIS"
"6071 " = "6071 : BALANOPOSTHITIS"
"6072 " = "6072 : INFLAM DIS- PENIS NEC"
"6073 " = "6073 : PRIAPISM"
"60781" = "60781: BALANITIS XEROTICA OBLIT"
"60782" = "60782: VASCULAR DISORDER- PENIS"
"60783" = "60783: EDEMA OF PENIS"
"60784" = "60784: IMPOTENCE- ORGANIC ORIGN"
"60785" = "60785: PEYRONIES DISEASE (Begin 2003)"
"60789" = "60789: DISORDER OF PENIS NEC"
"6079 " = "6079 : DISORDER OF PENIS NOS"

"4400 " = "4400 : AORTIC ATHEROSCLEROSIS"
"4401 " = "4401 : RENAL ARTERY ATHEROSCLER"
"4402 " = "4402 : ATHEROSCLEROS-EXTREMITY (Begin 1980 End 1992)"
"44020" = "44020: ATHEROSCLEROS-EXTREM NOS (Begin 1992)"
"44021" = "44021: ATHEROSCL-EXTREM CLAUDIC (Begin 1992)"
"44022" = "44022: ATHEROSCL-EXTREM REST PAIN (Begin 1992)"
"44023" = "44023: ATHEROSCL-EXTREMITY+ULCERATION (Begin 1993)"
"44024" = "44024: ATHEROSCL-EXTREMITY+GANGRENE (Begin 1993)"
"44029" = "44029: OTH ATHEROSCLEROSIS-EXTREMITY (Begin 1993)"
"44030" = "44030: ATHEROSCLER OF GRAFT NOS (Begin 1994)"
"44031" = "44031: ATHEROSCLER OF AUTOL VEIN GRAFT (Begin 1994)"
"44032" = "44032: ATHEROSCLER OF NONAUTOL GRAFT (Begin 1994)"
"4404 " = "4404 : CHR TOT OCCL ART EXTREM (Begin 2007)"
"4408 " = "4408 : ATHEROSCLEROSIS NEC"
"4409 " = "4409 : ATHEROSCLEROSIS NOS"

"4430 " = "4430 : RAYNAUD-s SYNDROME"
"4431 " = "4431 : THROMBOANGIIT OBLITERANS"
"44321" = "44321: DISSECTION OF CAROTID ARTERY (Begin 2002)"
"44322" = "44322: DISSECTION OF ILIAC ARTERY (Begin 2002)"
"44323" = "44323: DISSECTION OF RENAL ARTERY (Begin 2002)"
"44324" = "44324: DISSECTION OF VARTEBRAL ARTERY (Begin 2002)"
"44329" = "44329: DISSECTION OF OTHER ARTERY (Begin 2002)"
"44381" = "44381: ANGIOPATHY IN OTHER DIS"
"44382" = "44382: ERYTHROMELALGIA (Begin 2005)"
"44389" = "44389: PERIPH VASCULAR DIS NEC"
"4439 " = "4439 : PERIPH VASCULAR DIS NOS"
"4140 " = "4140 : CORONARY ATHEROSCLEROSIS (End 1994)"
"41400" = "41400: CORONARY ATHERO NOS (Begin 1994)"
"41401" = "41401: CORONARY ATHERO NATIVE VESSEL (Begin 1994)"
"41402" = "41402: CORONARY ATHERO AUTOLOG VEIN (Begin 1994)"
"41403" = "41403: CORONARY ATHERO NONAUTOL BYPASS (Begin 1994)"
"41404" = "41404: ATHERO ART BYPAS GFT (Begin 1996)"
"41405" = "41405: ATHERO BYPAS GFT NOS (Begin 1996)"
"41406" = "41406: CORONARY ATHERO CRNRY ARTERY OF TRANS (Begin 2002)"
"41407" = "41407: CORONARY ATHEROSCLEROSIS- OF BYPASS GRAFT (AR (Begin 2003)"
"41410" = "41410: ANEURYSM- HEART (WALL)"
"41411" = "41411: CORONARY VESSEL ANEURYSM"
"41412" = "41412: DISSECTION OF CORONARY ARTERY (Begin 2002)"
"41419" = "41419: ANEURYSM OF HEART NEC"
"4142 " = "4142 : CHR TOT OCCLUS COR ARTRY (Begin 2007)"
"4143 " = "4143 : COR ATH D/T LPD RCH PLAQ (Begin 2008)"
"4144 " = "4144 : Cor ath d/t calc cor lsn (Begin 2011)"
"4148 " = "4148 : CHR ISCHEMIC HRT DIS NEC"
"4149 " = "4149 : CHR ISCHEMIC HRT DIS NOS"

'''

def mi(data_mat):
	px, py = prob_marginal(data_mat)
	pxy = prob_joint(data_mat)

	if px == 0 or py == 0 or pxy == 0:
		# print(px)
		# print(py)
		# print(pxy)
		return 0
	else:
		try:
			I = float(pxy)*math.log(float(pxy)/(float(px)*float(py)),2)
		except:
			print('px: {0}'.format(px,))
			print('py: {0}'.format(py,))
			I = 0
	return I

def bootstrap_mi(data_mat):
	return bootstrap(mi, data_mat,data_mat.shape[0]-1,data_mat.shape[0])

def surrogate_mi(data_mat):
	return surrogate(mi, data_mat,data_mat.shape[0]-1,data_mat.shape[0],500)

def surrogate(func,data_mat,max_int,size,num_samples=500):
	stats = np.empty(num_samples)
	for i in range(num_samples):
		curr_mat = generate_surrogate(data_mat)
		stats[i] = func(curr_mat)
		# print('done with iteration {0}'.format(str(i),))
	return stats

def bootstrap(func,data_mat,max_int,size,num_samples=500):
	stats = np.empty(num_samples)
	for i in range(num_samples):
		curr_mat = resample_with_replacement(data_mat,max_int,size)
		stats[i] = func(curr_mat)
		# print('done with iteration {0}'.format(str(i),))
	return stats

def generate_surrogate(data_mat):
	max_int = data_mat.shape[0]-1
	size = max_int+1
	indices = np.random.randint(0,max_int,size=size)
	data_mat[:,0] = data_mat[indices,0]
	return data_mat

def resample_with_replacement(data_mat,max_int,size,surrogate=False):
	indices = np.random.randint(0,max_int,size=size)
	return data_mat[indices,:]

def prob_marginal(data_mat):
	numer = np.sum(np.squeeze(data_mat[:,0]))
	denom = np.sum(np.squeeze(data_mat[:,2]))
	px = numer / denom
	numer = np.sum(np.squeeze(data_mat[:,1]))
	py = numer / denom
	return px,py

def prob_joint(data_mat):
	col1 = np.squeeze(data_mat[:,0])
	col2 = np.squeeze(data_mat[:,1])
	col3 = np.squeeze(data_mat[:,2])
	return np.sum(np.multiply(np.multiply(col1,col2),col3))/float(np.sum(col3))

def binary_arrays(fname, code1, code2, chronic=False):
	px = dx_array(fname,code1, chronic)
	print('Done with px')
	py = dx_array(fname,code2, chronic)
	print('Done with py')
	wt = wt_array(fname)
	print('Done with wt')
	px = px[:,np.newaxis]
	py = py[:,np.newaxis]
	wt = wt[:,np.newaxis]
	pxpywt = np.concatenate((px,py,wt),axis=1)
	# np.savetxt('cleaned_data/pxpywt.txt',pxpywt,fmt='%f')
	return pxpywt

def dx_array(fname,code, chronic):
	if chronic:
		return hasforeach(fname,has_chronic_dx,code)
	return hasforeach(fname,has_dx,code)

def wt_array(fname):
	return hasforeach(fname,get_wt,None)

'''
Pass in a filename to look through, a function that returns either a 1 or a 0,
and a code that provides the true value. Returns an np.array of 1s and 0s
'''
def hasforeach(fname,func,code):
	outlist = np.empty(CORE_MALE_FILE_LENGTH)
	f = open(fname,"r")
	table = f.read()
	table = table.split("\n")
	print('Table split! Beginning file generation...')
	position = 0
	for line in table:
		if len(line) > 1:
			currline = line.split(",")
			outlist[position] = func(currline,code)
			position += 1
	return outlist

def get_wt(line,code):
	wt = float(line[PT_WT_CORE])
	if not wt:
		return 0.0
	return wt

def has_chronic_dx(line, code):
	for dx in line[CHRON1_INDEX:DX15_INDEX]:
		if re.match(code,dx):
			return int(1)
	return int(0)

def has_dx(line,code):
	
	# if code in line[DX1_INDEX:DX15_INDEX]:
	for dx in line[DX1_INDEX:DX15_INDEX]:
		if re.match(code,dx):
			return int(1)
		'''
		if re.match(code,dx) for dx in line[DX1_INDEX:DX15_INDEX]:
				if dx is not '':
					DXLIST.append(dx)
		'''
	return int(0)

def leaders(xs, top=10):
    counts = defaultdict(int)
    for x in xs:
        counts[x] += 1
    return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

def filelength(fname):
	f = open(fname,"r")
	table = f.read()
	table = table.split("\n")
	count = 0
	for line in table:
		if len(line) > 1:
			count += 1
	return count

def main():
	fname = 'cleaned_data/core_male_cleaned.csv'
	# print(filelength(fname))
	# fname = 'cleaned_data/core_patients_cleaned.csv'
	# code1 = URETHRAL_INJURY_CODES[0]
	PENILE_FRACTURE_CODE = '95913'
	code1 = '60785'
	code2 = '95913'
	# try:
	# 	data_mat = np.loadtxt('cleaned_data/pxpywt.txt')
	# 	print('Done loading file! Starting analysis.')
	# except:
	print('cannot load data, going to try generating...')
	data_mat = binary_arrays(fname,code1,code2)
	true_stat = mi(data_mat)
	print(true_stat)
	# print(leaders(DXLIST))
	print('beginning surrogate_stats')
	surrogate_stats = surrogate_mi(data_mat)
	print('beginning bootstrap_stats')
	bootstrap_stats = bootstrap_mi(data_mat)
	# plt.hist(bootstrap_stats,50)
	# plt.show()
	print(wald_test(true_stat, np.nanstd(bootstrap_stats), np.nanmean(surrogate_stats), np.nanstd(surrogate_stats)))

if __name__ == '__main__':
	main()