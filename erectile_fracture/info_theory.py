from neds_utils import *
import numpy as np
import matplotlib.pyplot as pyplot
import csv
import math

data_type = get_data_type()
DX1_INDEX = int(data_type.index('DX1'))
DX15_INDEX = int(data_type.index('DX15'))
PT_WT_CORE = int(data_type.index('DISCWT'))
URETHRAL_INJURY_CODES = ('8670','8671')
PEYRONIES = "60785"
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

def bootstrap(func,data_mat,max_int,size,num_samples=1000):
	stats = np.empty(num_samples)
	for i in range(num_samples):
		curr_mat = resample_with_replacement(data_mat,max_int,size)
		stats[i] = func(curr_mat)
	return stats

def resample_with_replacement(data_mat,max_int,size):
	indices = np.random.randint(0,max_int,size=size)
	return data_mat[indices,:]

def prob_marginal(data_mat):
	px = float(np.sum(data_mat[:,0],axis=0))/float(data_mat.shape[0])
	py = float(np.sum(data_mat[:,1],axis=0))/float(data_mat.shape[0])
	return px,py

def prob_joint(data_mat):
	col1 = np.squeeze(data_mat[:,0])
	col2 = np.squeeze(data_mat[:,1])
	return np.sum(np.multiply(col1,col2))/float(data_mat.shape[0])

def binary_arrays(fname, code1, code2):
	px = dx_array(fname,code1)
	py = dx_array(fname,code2)
	px = px[:,np.newaxis]
	py = py[:,np.newaxis]
	pxpy = np.concatenate((px,py),axis=1)
	return pxpy

def dx_array(fname,code):
	results = hasforeach(fname,has_dx,code)
	return results

'''
Pass in a filename to look through, a function that returns either a 1 or a 0,
and a code that provides the true value. Returns an np.array of 1s and 0s
'''
def hasforeach(fname,func,code):
	outlist = np.asarray([])
	with open(fname) as inputfile:
		reader = csv.reader(inputfile)
		for line in reader:
			outlist = np.append(outlist,func(line,code))
	return outlist

def has_dx(line,code):
	if code in line[DX1_INDEX:DX15_INDEX]:
		return 1
	return 0

def main():
	fname = 'cleaned_data/core_male_cleaned.csv'
	code1 = URETHRAL_INJURY_CODES[0]
	code2 = PEYRONIES

	data_mat = binary_arrays(fname,code1,code2)
	true_stat = mi(data_mat)
	print(true_stat)
	bootstrap_stats = bootstrap_mi(data_mat)
	print(bootstrap_stats)
	print(percentile(bootstrap_stats,true_stat))

if __name__ == '__main__':
	main()