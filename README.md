# Ancient-Chinese-Poem-Generator
This generator generates Chinese poem automatically when given the first sentence or the initial characters. Basically, it's a rule based sequence to character model.
2 or 3 LSTMs are stacked together and trained as a generative model. To make poem more human-written alike, tone pattern rule is also added.

This is a group project for CSCI 544, Applied Natural Language Processing.

Members:
- Shengyu Chen
- Shuai Zhou
- Yizhao He
- Zichen Yang

# Live Demo

We provide a User Interface to demo our Poem Generator: [http://poem.knotesapp.com/](http://poem.knotesapp.com/)

For fast testing, type in the first sentence: `春至花海棠` , leave intial characters empty and press `Generate` button

![UI](./docs/demo.png)

# Requirements

- python 3
- numpy, scipy
- yaml
- HDF5 and h5py
- TensorFlow
- Keras

# Usage

### Train
```sh
python ./lstm/train.py [-m SAVE_PATH] [-d DATA_PATH] [-v]
```

### Generate
```sh
python ./lstm/generate.py [-p PRIME] [-s SENTENCE] [-v VOCAB_PATH] [-w MODEL_WEIGHTS_PATH] [-m MODEL_STRUCT_PATH]
```

# Sample

	春至花海棠，
	衰家夜有人，
	一去见家悲，
	今气又去禅。

# Parameters
The first version is a sequence to word language model based on LSTM programmed in Python with Keras.

All poems used in training are 5-character simplified Chinese poems written in Tang dynasty. 
- data size: 16,000+ poems
- memory units number: 256 to 700
- dropout: 0.2
- batch size: 64 to 256
- epoch: 100+
- sequence length: 6 or 8
- number of LSTM layers: 2 to 3

# Data Source
All poetry data comes from [JackyGao's work](https://github.com/jackeyGao/chinese-poetry), which is a great contribution for this model. Peotries are labed with tone patterns which are the rules Chinese poems need to follow. 

# License
MIT