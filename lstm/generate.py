#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
# sys.stderr = open('/dev/null', 'w')

import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from config import *
from model import *
import os
import argparse
import json


def main():
	parser = argparse.ArgumentParser(description='Ancient Chinese poetry generator.')
	parser.add_argument('-p','--prime',type = str,help = "Initial Chinese characters for each sentence.",default = "")
	parser.add_argument('-s','--sentence',type = str,help = "First sentence for the poem.",default = "")
	parser.add_argument('-v','--voc',type = str,help = "Vocabulary file path.",default = "../model/weights/sample-vocabulary2.json")
	parser.add_argument('-w','--weights',type = str,help = "Model weights to be loaded.",default = "../model/weights/weights-improvement-29-5.1411-1.hdf5")
	parser.add_argument('-m','--model',type = str,help = "LSTM Model to be loaded.",default = "../model/weights/model.h5")

	args = parser.parse_args()

	# check
	if args.prime != '' and args.sentence != '' and args.sentence[0] != args.prime[0]:
		print("ERROR: First character should be same!")
		return
	# if len(args.sentence) != seq_len - 1:
	# 	print("ERROR: Sentence length should be {}".format(seq_len - 1))
	# 	return
	# global seq_len
	# if len(args.sentence) != seq_len - 1:
	# 	seq_len = len(args.sentence) + 1

	voc_t = open(args.voc,'r',encoding = 'utf-8')
	[voc,voc_count,pz] = json.loads(voc_t.read())
	voc_t.close()

	char_to_int = dict((c, i) for i, c in enumerate(voc))
	int_to_char = dict((i, c) for i, c in enumerate(voc))

	fs = ''
	if args.sentence == '':
		fs = first_sentence(args.prime)
	else:
		fs = args.sentence

	p = generate(args.weights,args.model,char_to_int,int_to_char,pz,args.prime,args.sentence)

	for s in p:
		print("\t" + s)


if __name__ == "__main__":
	main()