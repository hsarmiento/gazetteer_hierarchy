#!/usr/bin/python
# -*- coding: utf-8 -*-
#argv1: tweets file
#argv2: location file
#argv3: output common file

import sys

with open(sys.argv[1]) as tweets_file, open(sys.argv[2]) as location_file, open(sys.argv[3],"w") as output_file:
	locations = location_file.readline().split(",")
	d_tweet = {}
	d_user = {}
	d_common = {}
	i = 0
	total_lines = 0
	common_locations = 0
	not_common_locations = 0
	for line in tweets_file:
		l = line.strip().split("\t")
		if i > 0:
			total_lines += 1
			text_tweet = l[11].replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
			text_tweet = text_tweet.lower()
			user_location = l[46].replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
			user_location = user_location.lower()
			common = False
			for location in locations:
				location = location.lower()
				if location in text_tweet:
					if location not in d_tweet:
						d_tweet[location] = 0
					d_tweet[location] += 1
				if location in user_location:
					if location not in d_user:
						d_user[location] = 0
					d_user[location] += 1
				if location in text_tweet and location in user_location:
					common = True
					common_locations += 1
					output_file.write('\t'.join(l)+'\t'+'1'+'\t'+location+'\n')
					if location not in d_common:
						d_common[location] = 0
					d_common[location] += 1
			if not common:
				output_file.write('\t'.join(l)+'\t'+'0'+'\t'+'NA'+'\n')
		else:
			output_file.write('\t'.join(l)+'\t'+"is_common"+'\t'+"common_location"+'\n')
				# if (location in text_tweet and location not in user_location) or (location not in text_tweet and location in user_location):
				# 	not_common_locations += 1 
			# print text_tweet
			# break
		i+= 1

print "total tweets: ", total_lines
print "common locations: ", common_locations
print "no common locations:", total_lines - common_locations
# print "no common locations:", not_common_locations