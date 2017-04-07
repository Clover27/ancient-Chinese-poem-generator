# Ancien-Chinese-Poetry-Generator
This generator generates Chinese poem automatically when given the first sentence or the initial characters.
Two LSTMs are stacked together and trained as a generative model.

This is a group project for CSCI 544, Applied Natural Language Processing.

Members:
- Shengyu Chen
- Shuai Zhou
- Yizhao He
- Zichen Yang

# Usage

### Train
```bash
python ./lstm/train.py [-m save_path] [-d data_path]
```

### Generate
```bash
python ./lstm/generate.py [-p prime] [-s sentence] [-v vocabulary_path] [-w model_weights_path] [-m model_struct_path]
```

# Parameters
The first version is a sequence to word language model based on LSTM programmed in Python with Keras.

- memory units number: 256 & 512
- dropout: 0.2
- batch size: 64
- epoch: 20 - 100
- sequence length: 6 or 8

# Data Source
All poetry data comes from [JackyGao's work](https://github.com/jackeyGao/chinese-poetry), which is a great contribution for this model. Peotries are labed with special rhymes which are the rules Chinese poems need to follow. 