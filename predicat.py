#!/usr/bin/python
# -*- coding: utf8 > -*-
from keras.models import model_from_json
import keras.backend as K
import sys

print "开头为:" + sys.argv[1]
print len(sys.argv[1])
maxlen = 40

mf=open('model.json')
model = model_from_json(mf.read())
mf.close()
model.load_weights('model_weights.h5')
