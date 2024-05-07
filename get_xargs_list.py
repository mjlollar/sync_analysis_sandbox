import sys
import re
import glob

chrom = str(sys.argv[1])

with open("command_list.txt", "a") as outfile:
	for filename in glob.glob('*.split.sync'):
		try:
			runner = "python are_u_contaminated_single_all.py --s " + str(filename) + " --rc 1 --o " + chrom
			outfile.write(runner + "\n")
		except:
			pass
outfile.close()
