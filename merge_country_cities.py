#!/usr/bin/python
import sys

with open(sys.argv[1]) as geofile, open(sys.argv[2]) as wikifile, open(sys.argv[3],"w") as mergefile:
	cities = set()
	for line in geofile:
		cities.add(line.strip().lower())
	for line in wikifile:
		cities.add(line.strip().lower())
	l = list(cities)
	l.sort()
	mergefile.write(','.join(l))



