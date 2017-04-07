# ancien-Chinese-poetry-generator
This is a group project for CSCI 544, Applied Natural Language Processing.

Members:
- Shengyu Chen
- Shuai Zhou
- Yizhao He
- Zichen Yang

# Parameters
The first version is a sequence to word language model based on LSTM programmed in Python with Keras.
The model is a two-LSTM stacked together
- memory units number: 256 & 512
- dropout: 0.2
- batch size: 64
- epoch: 20 - 100
- sequence length: 6 or 8

# Usage

### Train
```bash
python ./lstm/train.py [-m save_path] [-d data_path]
```

### Generate
```bash
python ./lstm/generate.py [-p prime] [-s sentence] [-v vocabulary_path] [-w model_weights_path] [-m model_struct_path]
```

