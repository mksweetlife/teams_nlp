#2. generate names using markov chain
import random
from collections import defaultdict
from sys import argv

WORD_SEP = ' '

class MarkovName:
  def __init__(self):
      """ input file should have one name per line"""
      markov_file = open('sim2.txt', 'r')
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
#print(name)

def count_length(name):
      n_length = []
      if len(name) > 1 and len(name) < 10: 
              n_length.append(name)
      return n_length
print(count_length(name))
