#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import RegexpTokenizer
import preprocessor as p
import string
import unicodedata

class PreProcessing:

	def cleaning(self,text):
		p.set_options(p.OPT.EMOJI,p.OPT.SMILEY,p.OPT.URL,p.OPT.MENTION,p.OPT.RESERVED) #clean element in tweet
		return p.clean(text)

	def remove_accents(self,text):
		return ''.join(x for x in unicodedata.normalize('NFKD', text) if x in string.ascii_letters).lower()

	def preprocess(self,sentence):
		sentence = self.cleaning(sentence)
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(sentence)
		tokens = [token if token.isdigit() else self.remove_accents(token) for token in tokens ]
		return tokens
