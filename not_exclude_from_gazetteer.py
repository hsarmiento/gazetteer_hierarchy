#!/usr/bin/python3
import sys
import os

def not_exclude_set(not_exclude_file):
	with open(not_exclude_file) as exfile:
		for line in exfile:
			l = line.strip().split(",")
			return set(l)


def not_exclude_generator(extract_from,not_exclude_file,final_file):
	with open(extract_from) as f, open(final_file,"w") as ff:
		not_exclude = not_exclude_set(not_exclude_file)
		# print("extract from",extract_from)
		i = 0
		for line in f:
			if i > 0:
				# l = line.strip().split(",")
				l = line.strip().split("\t")
				# print(l[4].replace('"',''))
				# print(l[3])
				# if l[3].replace('"','') in not_exclude:
				print (l[-1])
				if l[-1] in not_exclude:
					ff.write(line)
			else:
				ff.write(line)
				i+=1

if __name__ == "__main__":
	extract_from = sys.argv[1]
	not_exclude_file = sys.argv[2]
	final_file = sys.argv[3]
	not_exclude_generator(extract_from,not_exclude_file,final_file)
