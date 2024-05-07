#More ancestry information for F2, single sync addition
#expected output, one text file with a single chrom,match,mismatch row
#MJL 04/25/24

import argparse
import numpy as np
import pandas as pd
import sys
import os.path
import csv

parser = argparse.ArgumentParser(description="Compare to sync files")
parser.add_argument('--s', help='Sync File Prefix', required=True, type=str)
parser.add_argument('--rc', help='Minimum read count in Parental sync files (default=12)', required=False, default=12, type=int)
parser.add_argument('--mc', help='Minimum minor read count (default=1)', required=False, default=1, type=int)
parser.add_argument('--mt', help='Parental minor count minimum read count frequency to major (default=0)', required=False, default=0.0, type=float)
parser.add_argument('--o', help='Output File prefix (default=mismatch_check_results.csv)', required=False, default="all_results", type=str)
args = parser.parse_args()

### Load sync file and assign column names
df = pd.read_csv(args.s, sep='\t', header=None) # parent 1
df.columns = ['chr', 'pos', 'refA', 'countA']
df[['A1', 'T1', 'C1', 'G1', 'countN1', 'countDel1']] = df['countA'].str.split(':', expand=True)

###Drop read columns with less than the minimum read count
df = df[(df['A1'].astype(int) + df['T1'].astype(int) + df['C1'].astype(int) + df['G1'].astype(int)).ge(args.rc)]

allele_dict = {'0':'A','1':'T','2':'C','3':'G'}
counter = 0
counter_prop = 0

### Get Major/Minor
def major_minor(row, set_num):
	global counter
	global counter_prop
	counter += 1
	
	if set_num == 1:
		A_count = int(row['A1'])
		T_count = int(row['T1'])
		C_count = int(row['C1'])
		G_count = int(row['G1'])
	else:
		sys.exit("You just got wrecked")
	
	counts = np.array([A_count, T_count, C_count, G_count])
	count_index = np.argsort(counts)
	major_allele = allele_dict.get(str(count_index[3])) #Major count (Base with greatest read count)
	
	if counts[count_index[2]] == 0:
		minor_allele = pd.NA
		major_tie = 0
		major_minor_prop = 0
	else:
		minor_allele = allele_dict.get(str(count_index[2]))
		major_minor_prop = int(counts[count_index[2]]) / int(counts[count_index[3]])
		counter_prop += 1
		if int(counts[count_index[2]]) == int(counts[count_index[3]]):
			major_tie = 1
		else:
			major_tie = 0
	
	if counts[count_index[1]] == 0:
		third_allele = pd.NA
	else:
		third_allele = allele_dict.get(str(count_index[1]))
		#if int(counts[count_index[1]]) == int(counts[count_index[2]]):
			#print("Minor allele tie in at site: " + str(row['pos']))
	
	if counts[count_index[0]] == 0:
		fourth_allele = pd.NA
	else:
		fourth_allele = allele_dict.get(str(count_index[0]))

	if counts[count_index[3]] == 1: #Major is single read
		singleton = 1
	else:
		singleton = 0

	#if (counts[int(count_index[2])] > args.mc) and (counts[int(count_index[2])] < (float(counts[int(count_index[3])])* args.mt)):
		#minorfail = 1
	#else:
		#minorfail = 0

	if counts[count_index[1]] >= 1:
		third = 1
	else:
		third = 0

	#if counts[count_index[1]] == 1:
		#thirdcount = 1
	#else:
		 #thirdcount = 0
		 
	if counts[count_index[0]] >= 1:
		fourcount = 1
	else:
		fourcount = 0

	depth = int(A_count) + int(T_count) + int(G_count) + int(C_count)

	return singleton, third, fourcount, major_tie, major_minor_prop, depth

### Run major_minor function to get sync1 and then sync2 counts
#try:
df[["singleton", "third", "fourth", "majortie", "prop", "d"]] = df.apply(lambda row: major_minor(row,1), axis='columns', result_type='expand')
#except ValueError: #catch instances where empty dataframe
#	sys.exit("Empty Dataframe (Error catch 1) Exiting....")

total1 = df['singleton'].astype(int).sum()
total2 = df['third'].astype(int).sum()
total3 = df['fourth'].astype(int).sum()
total4 = df['majortie'].astype(int).sum()
total5 = df['prop'].astype(int).sum()
total6 = df['d'].astype(int).sum()
#total5 = (df['d'].astype(int).sum()/(df.shape[0]-1))

chrom_dict = {'3':'2L','4':'X','5':'3L','7':'2R', '8':'3R'}
out_ind = args.s.split('.')[1]
chrom_index = args.s.split('.')[0]
out_chrom = chrom_dict.get(str(chrom_index))

#print("Total sites considered: " + str(counter))

outname = str(args.o) + "_singlesync_results.csv" #Match initited file
exist_check = os.path.isfile(outname)
with open (outname, 'a') as outfile:
	topline = ['sync','chr','singleton','third','fourth','major_tie','majmin_prop','depth','counter','counter_prop']
	writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n',fieldnames=topline)
	if not exist_check:
		writer.writeheader()
	writer.writerow({'sync':str(out_ind),'chr':str(out_chrom),'singleton':str(total1),'third':str(total2),'fourth':str(total3),'major_tie':str(total4), 'majmin_prop':str(total5), 'depth':str(total6), 'counter':str(counter),'counter_prop':str(counter_prop)})


#optional print final df that lists M and MM columns by site (sanity check purposes)
#df.to_csv('test.csv', sep=',', index=False, header=True)
