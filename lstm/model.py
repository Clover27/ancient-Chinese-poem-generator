import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

seq_len = 6 #sequence length
n_mmu = 512 # number of memory units
dropout = 0.2 # dropout rate
epoch = 50 # number of training epoch
batch = 128 # batch size
n_len = 4 # default poem length

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
	X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
	# normalize
	X = X / float(n_vocab)
	# one hot encode the output variable
	Y = np_utils.to_categorical(dataY)
	return X,Y

def train(X,Y):
	# define model
	model = Sequential()
	model.add(LSTM(n_mmu, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
	model.add(Dropout(dropout))
	model.add(LSTM(n_mmu))
	model.add(Dropout(dropout))
	model.add(Dense(y.shape[1], activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	# define the checkpoint
	filepath="./model/checkpoint/weights-improvement-{epoch:02d}-{loss:.4f}-1.hdf5"
	checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
	callbacks_list = [checkpoint]
	# training
	model.fit(X, Y, epochs=epoch, batch_size=batch, callbacks=callbacks_list)

def first_sentence(first = ""):
	'''
	' first: first character of the first sentence
	' return:
	'	first sentence 	
	'''
	if seq_len == 6:
		return '苟利国家生'
	if seq_len == 8:
		return '苟利国家生死已'

def predict(prediction):
	'''
	' prediction: output from model, vector of size 'n_vocab'
	' return the chosen character
	'''
	return numpy.argmax(prediction)

def generate(filename, char_to_index,index_to_char,prime = "" ,first_sentence = ""):
	# load the network weights
	# filename = "weights-improvement-47-1.2219-bigger.hdf5"
	model.load_weights(filename)
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	# get first sentence
	fs = ""
	if prime == "":
		fs = first_sentence("")
	else :
		fs = first_sentence(prime[0])
	poem = [fs]
	fs = fs + '$'
	pattern = [char_to_index[c] for c in fs]
	# generate characters
	if prime == "":
		n_s = n_len - 1
	else:
		n_s = len(prime) - 1

	for i in range(0,n_s,1):
		s = ""
		for j in range(0,seq_len -1,1):
			x = numpy.reshape(pattern, (1, len(pattern), 1))
			x = x / float(n_vocab)
			prediction = model.predict(x, verbose=0)
			index = predict(prediction)
			result = index_to_char[index]
			s = s+result
			pattern.append(index)
			pattern = pattern[1:len(pattern)]
		poem.append(s)
		pattern.append(char_to_index['$'])
		pattern = pattern[1:len(pattern)]
	return poem

def generate2(filename, char_to_index,index_to_char,prime = "" ,first_sentence = ""):
	# load the network weights
	# filename = "weights-improvement-47-1.2219-bigger.hdf5"
	model.load_weights(filename)
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	# get first sentence
	fs = ""
	if prime == "":
		fs = first_sentence("")
	else :
		fs = first_sentence(prime[0])
	poem = [fs]
	pattern = [char_to_index[c] for c in fs]
	# generate characters
	if prime == "":
		n_s = n_len - 1
	else:
		n_s = len(prime) - 1

	for i in range(0,n_s,1):
		s = ""
		for j in range(0,seq_len -1,1):
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

