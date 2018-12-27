#!/usr/bin/python3
import sys

if __name__ == "__main__":
	extract_from = sys.argv[1]
	save_to = sys.argv[2]
	locations = []
	with open(extract_from) as extract_file, open(save_to,"w") as save_file:
		for line in extract_file:
			# print(line)
			l = line.strip().split("\t")
			locations+=l
		locations = set(locations)
		save_file.write(','.join(locations))
