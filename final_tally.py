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
parser.add_argument('--o', help='output prefix', required=True, type=str)
parser.add_argument('--p1', help='output prefix, parent 1', required=True, type=str)
parser.add_argument('--p2', help='output prefix, parent 2', required=True, type=str)
args = parser.parse_args()
np.seterr(invalid='ignore')
### Load file and assign column names
df = pd.read_csv(args.f, sep=',', header=0)

try: #mistmatch rate
	total1 = (df['mismatch'].astype(int).sum() / df['total'].astype(int).sum()) * float(100)
except ValueError:
	total1 = "err"

try: #mistmatch_sub rate
	total2 = (df['mismatch_sub'].astype(int).sum() / df['cmf2'].astype(int).sum()) * float(100)
except ValueError:
	total2 = "err"

try: #P1 match
	total3 = (df['p1M'].astype(int).sum() / df['cm'].astype(int).sum()) * float(100)
except ValueError:
	total3 = "err"

try: #P2 match
	total4 = (df['p2M'].astype(int).sum() / df['cm'].astype(int).sum()) * float(100)
except ValueError:
	total4 = "err"

try: #Pm1match
	total5 = (df['p1m'].astype(int).sum() / df['cmp1'].astype(int).sum()) * float(100)
except ValueError:
	total5 = "err"

try: #Pm2match
	total6 = (df['p2m'].astype(int).sum() / df['cmp2'].astype(int).sum()) * float(100)
except ValueError:
	total6 = "err"

try: #Total number of sites considered
	considered = str(df['total'].astype(int).sum())
except ValueError:
	considered = "err"

try: #Total number of F2 het sites considered
	considered_het = str(df['cmf2'].astype(int).sum())
except ValueError:
	considered_het = "err"

out_chrom = str(df.at[0, 'chr'])
outname = "MISMATCH_FINALTALLYS_MASTERFILE.csv" #Match initited file
exist_check = os.path.isfile(outname)
with open (outname, 'a') as outfile:
	topline = ['ind', 'par1', 'par2', 'chr', 'mismatch', 'mismatch_sub', 'p1M', 'p2M', 'p1m', 'p2m', 'total_het', 'total']
	writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n',fieldnames=topline)
	if not exist_check:
		writer.writeheader()
	writer.writerow({'ind':str(args.o), 'par1':str(args.p1), 'par2':str(args.p2), 'chr':str(out_chrom), 'mismatch':str(total1), 'mismatch_sub':str(total2), 'p1M':str(total3), 'p2M':str(total4), 'p1m':str(total5), 'p2m':str(total6), 'total_het':str(considered_het), 'total':str(considered)})
