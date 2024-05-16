#Comparing sync file to two parental files
#MJL 05/08/24

import argparse
import numpy as np
import pandas as pd
import sys

parser = argparse.ArgumentParser(description="Compare to sync files")
parser.add_argument('--f', help='File Input', required=True, type=str)
parser.add_argument('--o', help='Output File prefix (default=output)[ends with _mismatchtally.csv]', required=False, default='output', type=str)
args = parser.parse_args()

df = pd.read_csv(args.f, sep=',', header=0)

counter_match = 0
counter_mp1 = 0
counter_mp2 = 0
counter_mf2 = 0
def tallythis(row):
	global counter_match
	global counter_mp1
	global counter_mp2
	global counter_mf2

	M1 = str(row['M1']) #f2
	m1 = str(row['m1'])

	M2 = str(row['M2']) #par1
	m2 = str(row['m2'])

	M3 = str(row['M3']) #par2
	m3 = str(row['m3'])

	set_1 = [M1, m1]
	set_2 = [M2, m2, M3, m3]
	try:
		set_1.remove('N')
	except ValueError:
		pass
	try:
		set_2.remove('N')
	except ValueError:
		pass

	if M2 == M3: #if same majors in both parents (for calcs)
		major_same = 1
	else:
		major_same = 0

	if set(set_1).isdisjoint(set_2): #if there is no allele overlap
		mismatch = 1
		p1M = 0
		p2M = 0
		p1m = 0
		p2m = 0
		mismatch_sub = 0
	elif not set(set_1).isdisjoint(set_2): #if there is any allele overlap
		counter_match += 1
		mismatch = 0

		if (M1 == M2) or (m1 == M2): #If match to parent 1 major
			p1M = 1
		else:
			p1M = 0

		if (M1 == M3) or (m1 == M3): #If match to parent 2 major
			p2M = 1
		else:
			p2M = 0

		if m2 != "N": #If minor p1 exists
			counter_mp1 += 1
			if (M1 == m2) or (m1 == m2): #If match to p1 minor
				p1m = 1
			else:
				p1m = 0
		else:
			p1m = 0

		if m3 != "N": #If minor p2 exists
			counter_mp2 += 1
			if (M1 == m3) or (m1 == m3): #If match to p2 minor
				p2m = 1
			else:
				p2m = 0
		else:
			p2m = 0

		if m1 != "N": #If minor F2 exists
			counter_mf2 += 1
			if (set(set_2).isdisjoint([M1])) or (set(set_2).isdisjoint([m1])): #If one allele does not overlap
				mismatch_sub = 1
			else:
				mismatch_sub = 0
		else:
			mismatch_sub = 0
	else:
		sys.exit('Error: Main Function Loop')
	return mismatch, mismatch_sub, p1M, p2M, p1m, p2m, major_same
####EOF tallythis()

#try:
df[['mismatch', 'mismatch_sub', 'p1M', 'p2M', 'p1m', 'p2m','major_same']] = df.apply(lambda row: tallythis(row), axis='columns', result_type='expand')
#except ValueError:
#	sys.exit('Error: Function 1 Apply')

df.drop(df.columns[[2,3,4,5,6,7]], axis=1, inplace=True) #drop unneeded columns
df['counter_match']= str(counter_match)
df['counter_mp1']= str(counter_mp1)
df['counter_mp2']= str(counter_mp2)
df['counter_mf2']= str(counter_mf2)

#Print to out
outname = args.o + "_mismatchtally.csv"
df.to_csv(outname, sep=',', header=True, index=False)





