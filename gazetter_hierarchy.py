#!/usr/bin/python3
import sys
import os
from pre_processing import PreProcessing


def n_slices(n, list_):
    for i in range(len(list_) + 1 - n):
        yield list_[i:i+n]

def is_sublist(list_, sub_list):
    for slice_ in n_slices(len(sub_list), list_):
        if slice_ == sub_list:
            return True
    return False

def place_in_tokenize(text,place_toke):
	return (len(place_toke) > 1 and is_sublist(text,place_toke)) or (len(place_toke) == 1 and place_toke[0] in text) 

def load_to_list_gazetteer_file(gazetteer_file):
	with open(gazetteer_file) as gazetteer_f:
		l = []
		for line in gazetteer_f:
			city,state,country = line.strip().split("\t")
			l.append((city,state,country))
		return l


def check_states(gazetteer_list,tweet_text_toke,user_location_toke,prepro):
	place_in_toke = False
	for city1,state1,country1 in gazetteer_list:
		city1_toke,state1_toke,country1_toke = prepro.preprocess(city1),prepro.preprocess(state1),prepro.preprocess(country1)
		if place_in_tokenize(tweet_text_toke,city1_toke):
			for city2,state2,country2 in gazetteer_list:
				city2_toke,state2_toke,country2_toke = prepro.preprocess(city2),prepro.preprocess(state2),prepro.preprocess(country2)
				# print(city1_toke,city2_toke)
				if place_in_tokenize(user_location_toke,city2_toke):
					place_in_toke = True
					country1_detected, country2_detected = " ".join(country1_toke)," ".join(country2_toke)
					state1_detected, state2_detected = " ".join(state1_toke)," ".join(state2_toke)
					city1_detected, city2_detected = " ".join(city1_toke)," ".join(city2_toke)
					if state1_toke == state2_toke:
						return ((True,country1_detected),(True,state1_detected,state2_detected),(False,city1_detected,city2_detected))
	if place_in_toke:
		return ((True,country1_detected),(False,state1_detected,state2_detected),(False,city1_detected,city2_detected))
	return ((False,""),(False,"",""),(False,"",""))


def write_for_tweet_or_location_signal(line_tweets_file,extract_from,gazetteer_list,final_file,prepro,lang_tweets): 
	t = "{0}\t{1}\t{2}\n"
	l  = line_tweets_file.strip().split("\t")

	if lang_tweets != None and lang_tweets != l[10]:
		return None
	if extract_from == "tweet":
		text_toke = prepro.preprocess(l[11])
	elif extract_from == "location":
		text_toke = prepro.preprocess(l[46])
	elif extract_from == "gps":
		text_toke = prepro.preprocess(l[31])
	print("Text toke: ",text_toke)
	with open(final_file,"a") as final_f:
		location_set = set()
		flag_country = False
		for city,state,country in gazetteer_list:
			city_toke,state_toke,country_toke = prepro.preprocess(city),prepro.preprocess(state),prepro.preprocess(country)
			#search city in text tokenize
			if place_in_tokenize(text_toke,city_toke):
				if ('city'," ".join(city_toke)) not in location_set:
					final_f.write(t.format(line_tweets_file.strip(),'city'," ".join(city_toke)))
					location_set.add(('city'," ".join(city_toke)))
				if ('state'," ".join(state_toke)) not in location_set:
					final_f.write(t.format(line_tweets_file.strip(),'state'," ".join(state_toke)))
					location_set.add(('state'," ".join(state_toke)))
				if not flag_country:
					final_f.write(t.format(line_tweets_file.strip(),'country'," ".join(country_toke)))
					flag_country = True

		if not flag_country and country in text_toke: #i.e: chile explicitly appear in text but not any city
					final_f.write(t.format(line_tweets_file.strip(),'country'," ".join(country_toke)))

def write_for_gps_signal(line_tweets_file,gazetteer_list,final_file,prepro): 
	t = "{0}\t{1}\t{2}\n"
	l  = line_tweets_file.strip().split("\t")
	text_toke = prepro.preprocess(l[31])
	print("Text toke: ",text_toke)
	with open(final_file,"a") as final_f:
		final_f.write(t.format(line_tweets_file.strip(),'city'," ".join(text_toke)))
		location_set = set()
		flag_country = False
		flag_state = False
		for city,state,country in gazetteer_list:
			city_toke,state_toke,country_toke = prepro.preprocess(city),prepro.preprocess(state),prepro.preprocess(country)
			#search city in text tokenize
			if place_in_tokenize(text_toke,city_toke):
				final_f.write(t.format(line_tweets_file.strip(),'state'," ".join(state_toke)))
				flag_state = True
				if not flag_country:
					final_f.write(t.format(line_tweets_file.strip(),'country'," ".join(country_toke)))
					flag_country = True
				break
		if not flag_state:
			final_f.write(t.format(line_tweets_file.strip(),'state',"Null"))
		if not flag_country: #i.e: chile explicitly appear in text but not any city
			final_f.write(t.format(line_tweets_file.strip(),'country'," ".join(country_toke)))


def write_for_mixed_signal(line_tweets_file,gazetteer_list,final_file,prepro,lang_tweets):
	t = "{0}\t{1}\t{2}\n"
	l = line_tweets_file.strip().split("\t")
	if lang_tweets != None and lang_tweets != l[10]:
		return None
	tweet_text_toke = prepro.preprocess(l[11])
	user_location_toke = prepro.preprocess(l[46])
	print("Tweet toke: ",tweet_text_toke)
	print("User toke: ",user_location_toke)
	print("**********")
	with open(final_file,"a") as final_f:
		flag_country = False
		flag_city = False
		for city,state,country in gazetteer_list:
			place_toke,state_toke,country_toke = prepro.preprocess(city),prepro.preprocess(state),prepro.preprocess(country)
			if place_in_tokenize(tweet_text_toke,place_toke) and place_in_tokenize(user_location_toke,place_toke):
				final_f.write(t.format(line_tweets_file.strip(),'city'," ".join(place_toke)))
				final_f.write(t.format(line_tweets_file.strip(),'state'," ".join(state_toke)))
				final_f.write(t.format(line_tweets_file.strip(),'country'," ".join(country_toke)))
				flag_country = True
				flag_city = True
				break
		country_check, state_check, city_check = check_states(gazetteer_list,tweet_text_toke,user_location_toke,prepro)
		if state_check[0] and not flag_city:
			# print (check_states(gazetteer_file,tweet_text_toke,user_location_toke,prepro))
			final_f.write(t.format(line_tweets_file.strip(),'state',state_check[1]))
			final_f.write(t.format(line_tweets_file.strip(),'country',country_check[1]))
			flag_country = True
		elif not flag_country and country_check[0]:
			final_f.write(t.format(line_tweets_file.strip(),'country',country_check[1]))

def apply_gazetteer(extract_from,tweets_file,gazetteer_file,final_file, lang_tweets = None):
	with open(tweets_file) as tweets_f:
		gazetteer_list = load_to_list_gazetteer_file(gazetteer_file)
		prepro = PreProcessing()
		i = 0
		t = "{0}\t{1}\t{2}\n"
		for line in tweets_f:
			if i > 0:
				if extract_from == "mixed":
					write_for_mixed_signal(line,gazetteer_list,final_file,prepro,lang_tweets)
				elif extract_from == "gps":
					write_for_gps_signal(line,gazetteer_list,final_file,prepro)
				else:
					write_for_tweet_or_location_signal(line,extract_from,gazetteer_list,final_file,prepro,lang_tweets)
			else:
				with open(final_file,"w") as final_f:
					final_f.write(t.format(line.strip(),'hierarchy','location_detected'))
			i+=1
			# if i == 300:
			# 	return 0


if __name__ == "__main__":
	extract_from = sys.argv[1]
	tweets_file = sys.argv[2]
	gazetteer_file = sys.argv[3]
	final_file = sys.argv[4]
	print("Number of argv:", len(sys.argv))
	if len(sys.argv) == 5:
		apply_gazetteer(extract_from,tweets_file,gazetteer_file,final_file)
	elif len(sys.argv) == 6:
		lang_tweets = sys.argv[5]
		apply_gazetteer(extract_from,tweets_file,gazetteer_file,final_file,lang_tweets)
