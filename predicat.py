#!/usr/bin/python
# -*- coding: utf8 > -*-
from keras.models import model_from_json
import keras.backend as K
import sys

def to_word(predict, vocabs):
    t = np.cumsum(predict)
    s = np.sum(predict)
    sample = int(np.searchsorted(t, np.random.rand(1) * s))
    if sample > len(vocabs):
        sample = len(vocabs) - 1
    return sample 


print "开头为:" + sys.argv[1]
start = sys.argv[1].decode('utf-8')

maxlen = 40

path = './data.txt'
print 'opening txt'

text = open(path).read().lower().decode('utf-8')
print 'corpus length:', len(text)

chars = set(text)
print 'total chars:', len(chars)
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))


mf=open('model.json')
model = model_from_json(mf.read())
mf.close()
model.load_weights('model_weights.h5')

sentence = [' '] * maxlen

