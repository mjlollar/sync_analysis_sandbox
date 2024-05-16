#Comparing sync file to two parental files
#MJL 05/08/24

import argparse
import numpy as np
import pandas as pd
import sys

parser = argparse.ArgumentParser(description="Compare to sync files")
parser.add_argument('--s', help='Split Sync File Input', required=True, type=str)
parser.add_argument('--ms', help='Minimum minor read count (default=1)', required=False, default=1, type=int)
parser.add_argument('--mp', help='Minimum minor read count (default=2)', required=False, default=2, type=int)
parser.add_argument('--mt', help='Minor count minimum frequency (default=0.25[25%])', required=False, default=0.25, type=float)
parser.add_argument('--o', help='Output File prefix (default=declared)[ends with _majorminors.csv]', required=False, default='declared', type=str)
args = parser.parse_args()

df = pd.read_csv(args.s, sep=',', header=None)
df.columns = ['chr1','pos','A1','T1','C1','G1','A2','T2','C2','G2','A3','T3','C3','G3']
allele_dict = {'0':'A','1':'T','2':'C','3':'G'}
chrom_dict = {'3':'2L','4':'X','5':'3L','7':'2R', '8':'3R'}

def get_majorminor(row, set_num):
	if set_num == 1:
		A_count = int(row['A1'])
		T_count = int(row['T1'])
		C_count = int(row['C1'])
		G_count = int(row['G1'])
	elif set_num == 2:
		A_count = int(row['A2'])
		T_count = int(row['T2'])
		C_count = int(row['C2'])
		G_count = int(row['G2'])
	elif set_num == 3: #little old code artifact
		A_count = int(row['A3'])
		T_count = int(row['T3'])
		C_count = int(row['C3'])
		G_count = int(row['G3'])
	else:
		sys.exit('Error: Code 01')

	counts = np.array([A_count, T_count, C_count, G_count])
	count_index = np.argsort(counts)
	major_allele = allele_dict.get(str(count_index[3]))
	major_count = int(counts[int(count_index[3])])
	minor_count = int(counts[int(count_index[2])])
	third_count = int(counts[int(count_index[1])])

	if set_num == 1: #For input F2
		if third_count >= 1: #If third allele is present
			if (minor_count == 1) or (minor_count == third_count):
				if major_count == 1:
					major_count = "N" #Rename major to missing if all counts =1
				else:
					pass
				minor_allele = "N"
			elif minor_count > third_count: #threshold test if second count is higher than third count
				if (minor_count >= args.ms) and (float(minor_count) >= (float(major_count) * args.mt)):
					minor_allele = allele_dict.get(str(count_index[2]))
				else:
					minor_allele = "N"
			else:
				sys.exit('Error: Code 02')
		elif third_count == 0: #if no third allele
			if minor_count >= args.ms: #If minor count is above read threshold
				minor_allele = allele_dict.get(str(count_index[2]))
			else:
				minor_allele = "N"
		else:
			sys.exit('Error: Code 03')
			
	elif (set_num == 2) or (set_num == 3): #For parental input
		if third_count == 0: #If no third read
			if (minor_count >= args.mp) and (float(minor_count) >= (float(major_count) * args.mt)):
				minor_allele = allele_dict.get(str(count_index[2]))
			else:
				minor_allele = "N"
		elif (third_count > 0) and (third_count == minor_count):
			minor_allele = "N"#If second and third read 
		elif (third_count > 0) and (third_count <= minor_count):
			if (minor_count >= args.mp) and (float(minor_count) >= (float(major_count) * args.mt)):
				minor_allele = allele_dict.get(str(count_index[2]))
			else:
				minor_allele = "N"
		else:
			sys.exit('Error: Code 04')
	else:
		sys.exit('Error: Code 05')
	return major_allele, minor_allele
#### EOF get_majorminor()

try:
	df[["M1", "m1"]] = df.apply(lambda row: get_majorminor(row, 1), axis='columns', result_type='expand')
except ValueError:
	sys.exit('Error: Code 06')

try:
	df[["M2", "m2"]] = df.apply(lambda row: get_majorminor(row, 2), axis='columns', result_type='expand')
except ValueError:
	sys.exit('Error: Code 07')

try:
	df[["M3", "m3"]] = df.apply(lambda row: get_majorminor(row, 3), axis='columns', result_type='expand')
except ValueError:
	sys.exit('Error: Code 08')

df.drop(df.loc[df['M1']=="N"].index, inplace=True) #Drop rows with no major call in F2
df.drop(df.columns[[2,3,4,5,6,7,8,9,10,11,12,13]], axis=1, inplace=True) #drop unused columns

### Write to output
outname = args.o + "_majorminors.csv"
df.to_csv(outname, sep=',', header=True, index=False)
