from gensim.models import FastText, KeyedVectors
import random
import re
import nltk

model = None

def similar(self):
    
    global model
    if model is None:
        model = KeyedVectors.load_word2vec_format('wiki-brooklyn.bin', binary=True, unicode_errors='ignore')
#    sim2 = []
#    sim1 = model.most_similar(self, topn = 25)
#    sim3 = [sim2.append(word) for word, score in sim1]

############## KEYWORD EXTRACTION ##################
    token = nltk.word_tokenize(self)
    pos = nltk.pos_tag(token)

    keyword_list = []
    mostRelated = []

    for s in pos:
        if s[1] in ['NNP', 'JJ', 'NN']:
            keyword_list.append(s[0])

############## SIMILAR WORDS ##################
    for i in keyword_list:
        if i in model.vocab:
            mostRelated_with_score = model.most_similar(positive=i, topn=10)
            for word, score in mostRelated_with_score:
                word2 = re.sub('[-=.#/?:$}]', '', word)
                mostRelated.append(word2)
    return mostRelated

############## MARKOV_CHAIN ##################

import random
from collections import defaultdict
from sys import argv

WORD_SEP = ' '

class MarkovName:
  def __init__(self):
      """ input file should have one name per line"""
      input 
      markov_file = similar(input)
      # markov chain is a dictionary from {(letter) to list-of-letters-seen-after}
      # {c: 'aaoehhhhh   '}
      self.chain = defaultdict(list)
      names = (line for line in markov_file if not line[0] == '#')
      for name in names:
          proper_name = name.lower().strip()
          pairs = zip(proper_name, proper_name[1:])
          for first, second in pairs: 
              self.chain[first].append(second)
          self.chain[proper_name[-1]].append(WORD_SEP)
          self.chain[WORD_SEP].append(proper_name[0])

  def generate_name(self):
      name = []
      current = WORD_SEP
      while not (current == WORD_SEP and name):
       current = random.choice(self.chain[current])
       name.append(current)
      return ''.join(name).strip().capitalize()

chain = MarkovName()
name = chain.generate_name()
print(name)