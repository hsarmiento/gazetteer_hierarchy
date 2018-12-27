#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

with open(sys.argv[1]) as input_file:
	l = []
	for line in input_file:
		_,_,location,_,_ = line.strip().split("\t")
		location = location.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
		print location
		l.append(location)
	with open(sys.argv[2],'w') as output_file:
		output_file.write(','.join(l))


