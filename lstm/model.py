#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.models import load_model
import random
from config import *


def get_training_data(raw_dict, char_to_index):
	'''
	'Generate data for training LSTM from raw data
	'
	'raw_dict: 		original data. struct: {'title':"",'strains':'zzppz$ppzzp$...','paragraphs':"12345$67890$..."}
	'char_to_index: 	dictonary map char to index
	'
	'return:
	'	X [input chars sequence]
	'	Y [char label]
	'''
	
	data_X = []
	data_Y = []
	for poem in raw_dict:
		n_chars = len(poem['paragraphs'])
		for i in range(0,n_chars - seq_len,1):
			s_out = poem['paragraphs'][i+seq_len]
			# never output '$'
			if(s_out == '$'):
				continue
			s_in = poem['paragraphs'][i:i+seq_len]
			data_X.append([char_to_index[c] for c in s_in])
			data_Y.append(char_to_index[s_out])
	return data_X,data_Y


def get_training_data2(raw_dict, char_to_index):
	'''
	'Generate data for training LSTM from raw data without considering $
	'
	'raw_dict: 		original data. struct: {'title':"",'strains':'zzppz$ppzzp$...','paragraphs':"12345$67890$..."}
	'char_to_index: 	dictonary map char to index
	'
	'return:
	'	X [input chars sequence]
	'	Y [char label]
	'''
	
	data_X = []
	data_Y = []
	for poem in raw_dict:
		context = poem['paragraphs']
		context.replace('$','')
		n_chars = len(context)
		for i in range(0,n_chars - seq_len - 1,1):
			s_out = context[i+seq_len - 1]
			s_in = context[i:i+seq_len - 1]
			data_X.append([char_to_index[c] for c in s_in])
			data_Y.append(char_to_index[s_out])
	return data_X,data_Y

def one_hot_encode(data_X,data_Y,n_vocab):
	# n_vocab: 		size of vocabulary
	n_patterns = len(data_X)
	# reshape X to be [samples, time steps, features]
	X = numpy.reshape(data_X, (n_patterns, seq_len, 1))
	# normalize
	X = X / float(n_vocab)
	# one hot encode the output variable
	Y = np_utils.to_categorical(data_Y)
	return X,Y

def train(X,Y,file,load_path):
	# define model
	model = Sequential()
	model.add(LSTM(n_mmu, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
	model.add(Dropout(dropout))
	model.add(LSTM(n_mmu, return_sequences=True))
	model.add(Dropout(dropout))
	if n_layer == 3:
		model.add(LSTM(n_mmu))
		model.add(Dropout(dropout))
	model.add(Dense(Y.shape[1], activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam')

	model.save(file + "/model-{}-{}.h5".format(n_mmu,dropout))
	# define the checkpoint
	filepath=file + "/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
	checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
	callbacks_list = [checkpoint]
	# loading
	if load_path != "":
		model.load_weights(load_path)
	# training
	model.fit(X, Y, epochs=epoch, batch_size=batch, callbacks=callbacks_list,validation_split = 0.1)

def first_sentence(first = ""):
	'''
	' first: first character of the first sentence
	' return:
	'	first sentence 	
	'''
	if seq_len == 6:
		return u"春气满林香"
	else:
		return u"苟利国家生死以"

def predict(prediction,pz,tonedic,index_to_char,pre):
	'''
	' prediction: output from model, vector of size 'n_vocab'
	' return the chosen character
	'''
	if pz == '' or pz == '-':
		return numpy.argmax(prediction)
	[prediction] = prediction
	
	s = sorted(range(len(prediction)),key = lambda k:prediction[k],reverse = True)

	for i in s:
		c = index_to_char[i]
		if pre != i and c in tonedic and tonedic[c] == pz:
			return i

def gettone(p):
	'''
	' p: first sequence pattern
	' return the whole pattern
	'''
	if p == 'ppzzp' or p == 'pppzp':
		return ['ppzzp','-zzpp','-zppz','pp-zp']
	if p == 'pppzz' or p == 'zppzz':
		return ['pppzz','-zzpp','-zppz','pp-zp']
	if p == 'zzzpp' or p == 'pzzpp':
		return ['zzzpp','pp-zp','-ppzz','-zzpp']
	if p == 'zzppz' or p == 'pzppz':
		return ['zzppz','pp-zp','-ppzz','-zzpp']
	return None


def generate(filename, model_path,char_to_index,index_to_char,tonedic,prime = "" ,sentence = ""):
	# load the network weights
	# filename = "weights-improvement-47-1.2219-bigger.hdf5"
	model = load_model(model_path)

	# model.add(LSTM(n_mmu, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
	# model.add(Dropout(dropout))
	# model.add(LSTM(n_mmu))
	# model.add(Dropout(dropout))
	# model.add(Dense(Y.shape[1], activation='softmax'))

	model.load_weights(filename)
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	# get first sentence
	fs = ""
	if sentence != "":
		fs = sentence
	else:
		if prime == "":
			fs = first_sentence()
		else :
			fs = first_sentence(prime[0])
	poem = [fs]
	fs = fs + '$'

	n_vocab = len(char_to_index)
	random.seed()
	pattern = []
	for c in fs:
		if c in char_to_index:
			pattern.append(char_to_index[c])
		else:
			pattern.append(random.randint(0,n_vocab-1))
	prime2 = ""
	for c,x in enumerate(prime):
		if x not in char_to_index:
			prime2 += index_to_char[random.randint(0,n_vocab-1)]
		else:
			prime2 += x
	# pattern = [char_to_index[c] for c in fs]
	# generate characters
	
	# get tone pattern
	tone = ""
	tonepattern = []
	if sentence != "":
		for c in sentence:
			if c != '$':
				tone += tonedic[c]
		tonepattern = gettone(tone)


	pre = 0
	sen_len = len(pattern)

	pattern = pattern[len(pattern) - seq_len:]
	if prime == "":
		n_s = n_len - 1
	else:
		n_s = len(prime) - 1

	for i in range(0,n_s,1):
		s = ""
		if prime != "":
			s = s + prime[1 + i]
			pre = char_to_index[prime2[0]]
			pattern.append(char_to_index[prime2[0]])
			pattern = pattern[1:len(pattern)]
		for j in range(len(s),sen_len -1,1):
			x = numpy.reshape(pattern, (1, len(pattern), 1))
			x = x / float(n_vocab)
			prediction = model.predict(x, verbose=0)
			pz = ''
			if tonepattern is not None:
				pz = tonepattern[i+1][j]
			index = predict(prediction,pz,tonedic,index_to_char,pre)
			pre = index
			result = index_to_char[index]
			s = s+result
			pattern.append(index)
			pattern = pattern[1:len(pattern)]
		poem.append(s)
		pattern.append(char_to_index['$'])
		pattern = pattern[1:len(pattern)]
	return poem

def generate2(filename,model_path, char_to_index,index_to_char,prime = "" ,sentence = ""):
	# load the network weights
	# filename = "weights-improvement-47-1.2219-bigger.hdf5"
	model = load_model(model_path)
	model.load_weights(filename)
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	# get first sentence
	fs = ""
	if sentence != "":
		fs = sentence
	else:
		if prime == "":
			fs = first_sentence()
		else :
			fs = first_sentence(prime[0])
	poem = [fs]
	pattern = [char_to_index[c] for c in fs]
	# generate characters
	n_vocab = len(char_to_index)
	if prime == "":
		n_s = n_len - 1
	else:
		n_s = len(prime) - 1

	for i in range(0,n_s,1):
		s = ""
		if prime != "":
			s = "" + prime[1 + i]
			pattern.append(char_to_index[s[0]])
			pattern = pattern[1:len(pattern)]
		for j in range(len(s),seq_len -1,1):
			x = numpy.reshape(pattern, (1, len(pattern), 1))
			x = x / float(n_vocab)
			prediction = model.predict(x, verbose=0)
			index = predict(prediction)
			result = index_to_char[index]
			s = s+result
			pattern.append(index)
			pattern = pattern[1:len(pattern)]
		poem.append(s)
	return poem

