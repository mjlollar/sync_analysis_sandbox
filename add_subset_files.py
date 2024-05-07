#Add up are_u_contaminated_sing_all.py results
#MJL 05/08/24

import argparse
import numpy as np
import pandas as pd
import sys
import os.path
import csv

parser = argparse.ArgumentParser(description="Compare to sync files")
parser.add_argument('--f', help='File', required=True, type=str)
parser.add_argument('--i', help='individual', required=True, type=str)
parser.add_argument('--c', help='chrom', required=True, type=str)
args = parser.parse_args()

### Load file and assign column names
df = pd.read_csv(args.f, sep='\t', header=None) # parent 1
df.columns = ['sync','chr','singleton','third','fourth','major_tie','majmin_prop','depth','counter','counter_prop']

total1 = df['singleton'].astype(int).sum()
total2 = df['third'].astype(int).sum()
total3 = df['fourth'].astype(int).sum()
total4 = df['majortie'].astype(int).sum()
total5 = df['majmin_prop'].astype(int).sum() / df['counter_prop'].astype(int).sum()
total6 = df['depth'].astype(int).sum() / df['counter'].astype(int).sum()

outname = "Masteresults_areucontaminatedsingleall.csv" #Match initited file
exist_check = os.path.isfile(outname)
with open (outname, 'a') as outfile:
	topline = ['sync','chr','singleton','third','fourth','major_tie','majmin_prop','depth']
	writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n',fieldnames=topline)
	if not exist_check:
		writer.writeheader()
	writer.writerow({'sync':str(args.i),'chr':str(args.c),'singleton':str(total1),'third':str(total2),'fourth':str(total3),'major_tie':str(total4), 'majmin_prop':str(total5), 'depth':str(total6)})
