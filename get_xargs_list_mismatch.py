import sys
import re
import glob

switcher = int(sys.argv[2])
chrom = str(sys.argv[1])
my_count = 0


if switcher == 1:
	with open("command_list_mismatch.txt", "a") as outfile:
		for filename in glob.glob('*.missplit.csv'):
			try:
				runner = "python get_majorminor.py --s " + str(filename) + " --o " + chrom + "." + str(my_count)
				outfile.write(runner + "\n")
				my_count += 1
			except:
				pass

elif switcher == 2:
	with open("command_list_mismatch_2.txt", "a") as outfile:
		for filename in glob.glob('*_majorminors.csv'):
			try:
				runner = "python compare_sync_to_parents.py --f " + str(filename) + " --o " + chrom + "." + str(my_count)
				outfile.write(runner + "\n")
				my_count += 1
			except:
				pass

elif switcher == 3:
	with open("command_list_mismatch_3.txt", "a") as outfile:
		for filename in glob.glob('*_mismatchtally.csv'):
			try:
				runner = "python add_subset_files_mismatch.py --f " + str(filename)
				outfile.write(runner + "\n")
			except:
				pass

else:
	sys.exit('sanity error check')

outfile.close()
