#!/usr/bin/python
# -*- coding: utf8 > -*-
from keras.models import model_from_json
import keras.backend as K
import sys
import numpy as np
import random

def to_word(predict, vocabs):
    t = np.cumsum(predict)
    s = np.sum(predict)
    sample = int(np.searchsorted(t, np.random.rand(1) * s))
    if sample > len(vocabs):
        sample = len(vocabs) - 1
    return sample 



maxlen = 40

path = './data.txt'
print 'opening txt'

text = open(path).read().lower().decode('utf-8')
print 'corpus length:', len(text)

chars = set(text)
chars_len=len(chars)
print 'total chars:', len(chars)
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))


mf=open('model.json')
model = model_from_json(mf.read())
mf.close()
model.load_weights('model_weights.h5')

def init_with_start(start):
    sentence = [' '] * maxlen
    start_len=len(start)
    for i in range(maxlen):
        if((i+9)%12==0):
            sentence[i]=u"。"
        elif((i+9)%6==0):
            sentence[i]=u"，"
        #else:
            #sentence[i]=start[random.randint(0,start_len-1)]
            #sentence[i]=indices_char[random.randint(0,chars_len-1)]
    print 'a',''.join(sentence).encode('utf8')
    for i in range(start_len):
        sentence.append(start[i])
    sentence=sentence[len(start):]
    print 'b',''.join(sentence).encode('utf8')
    return sentence
def predict_with_start(sentence,start):
    generated = start
    while not len(generated.split(u"。"))==5:
        X = np.zeros((1, maxlen, len(chars)))
        for i in range(maxlen):
            if(char_indices.has_key(sentence[i])):
                X[0, i, char_indices[sentence[i]]] = 1.0
        preds = model.predict(X)[0]
        next_index = to_word(preds, indices_char)
        next_char = indices_char[next_index]
        if(not next_char =='\n'):
            generated += next_char
        sentence = sentence[1:]
        sentence.append(next_char)
    return generated
def init_with_head(head):
    sentence = [' '] * maxlen
    for i in range(maxlen):
        if((i+9)%12==0):
            sentence[i]=u"。"
        elif((i+9)%6==0):
            sentence[i]=u"，"
        #else:
            #sentence[i]=start[random.randint(0,start_len-1)]
            #sentence[i]=indices_char[random.randint(0,chars_len-1)]
    print 'a',''.join(sentence).encode('utf8')
    sentence.append(head[0])
    sentence=sentence[1:]
    print 'b',''.join(sentence).encode('utf8')
    return sentence
def predict_with_head(sentence,head):
    generated = head[0]
    head_index=1
    while not len(generated.split(u"。"))==5:
        X = np.zeros((1, maxlen, len(chars)))
        for i in range(maxlen):
            if(char_indices.has_key(sentence[i])):
                X[0, i, char_indices[sentence[i]]] = 1.0
        preds = model.predict(X)[0]
        next_index = to_word(preds, indices_char)
        next_char = indices_char[next_index]
        if((next_char == u'。' or next_char ==u'，')and len(head)>head_index):
            generated += next_char
            generated += head[head_index]
            sentence = sentence[2:]
            sentence.append(next_char)
            sentence.append(head[head_index])
            head_index = head_index + 1
        else:
            if(not next_char == '\n'):
                generated += next_char
            sentence = sentence[1:]
            sentence.append(next_char)
    return generated

input_data = sys.argv[1].decode('utf-8')
input_type = int(sys.argv[2])
if(input_type==0):
    sentence=init_with_start(input_data)
    generated = predict_with_start(sentence,input_data)
    print generated.encode('utf8')
else:
    sentence=init_with_head(input_data)
    generated=predict_with_head(sentence,input_data)
    print generated.encode('utf8')
