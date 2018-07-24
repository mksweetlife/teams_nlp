from gensim.models import FastText, KeyedVectors
import random
import re

#1. import a pretrained model
model = KeyedVectors.load_word2vec_format('wiki-news-300d-1M.vec')
#print(model)
sim1 = model.most_similar('grapefruit', topn = 25)
sim2 = '\n'.join([s[0] for s in sim1])
#print(sim2)

f = open("sim2.txt", 'w')
f.write(sim2)
f.close()