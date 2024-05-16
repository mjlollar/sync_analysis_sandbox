#Add up compare_sync_to_parents.py results
#Hard coded to follow filename design of input (05/08/24)
#MJL 05/08/24

import argparse
import numpy as np
import pandas as pd
import sys
import os.path
import csv

parser = argparse.ArgumentParser(description="Talley Ho!")
parser.add_argument('--f', help='File', required=True, type=str)
args = parser.parse_args()

### Load file and assign column names
df = pd.read_csv(args.f, sep=',', header=0)

counter_match = int(df.at[0, 'counter_match'])
counter_mp1 = int(df.at[0, 'counter_mp1'])
counter_mp2 = int(df.at[0, 'counter_mp2'])
counter_mf2 = int(df.at[0, 'counter_mf2'])
considered = int(df.shape[0] - 1)

try: #mistmatch rate
	total1 = df['mismatch'].astype(int).sum()
except ValueError:
	total1 = pd.NA

try: #mistmatch_sub rate
	total2 = df['mismatch_sub'].astype(int).sum()
except ValueError:
	total2 = pd.NA

try: #P1 match
	total3 = df['p1M'].astype(int).sum()
except ValueError:
	total3 = pd.NA

try: #P2 match
	total4 = df['p2M'].astype(int).sum()
except ValueError:
	total4 = pd.NA

try: #Pm1match
	total5 = df['p1m'].astype(int).sum()
except ValueError:
	total5 = pd.NA

try: #Pm2match
	total6 = df['p2m'].astype(int).sum()
except ValueError:
	total6 = pd.NA

out_ind = str(args.f.split("_")[0].split(".")[1])
out_chrom = str(args.f.split("_")[0].split(".")[0])
outname = out_chrom + "_aggregate.csv" #Match initited file
exist_check = os.path.isfile(outname)
with open (outname, 'a') as outfile:
	#topline = ['ind', 'chr', 'mismatch', 'mismatch_sub', 'p1M', 'p2M', 'p1m', 'p2m', 'cm', 'cmp1', 'cmp2', 'cmf2', 'total']
	#writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n',fieldnames=topline)
	#if not exist_check:
		#writer.writeheader()
	#writer.writerow({'ind':str(out_ind), 'chr':str(out_chrom), 'mismatch':str(total1), 'mismatch_sub':str(total2), 'p1M':str(total3), 'p2M':str(total4), 'p1m':str(total5), 'p2m':str(total6), 'cm':str(counter_match), 'cmp1':str(counter_mp1), 'cmp2':str(counter_mp2), 'cmf2':str(counter_mf2), 'total':str(considered)})
	#writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n')
	writer = csv.writer(outfile, delimiter=',', lineterminator='\n')
	writer.writerow([str(out_ind), str(out_chrom), str(total1), str(total2), str(total3), str(total4), str(total5), str(total6), str(counter_match), str(counter_mp1), str(counter_mp2), str(counter_mf2), str(considered)])
