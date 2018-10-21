
# coding: utf-8

# ### TODO
# 
# - The wordlist.txt is still mandatory now, to determine `ix_to_char`.

# In[1]:


import os 
import numpy as np
import h5py

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, SimpleRNN, GRU, TimeDistributed
from keras.callbacks import LambdaCallback


# In[2]:


from utils import text_to_words

# Generate a list of words (including newline)
corpus = "kmkcomp"
textfile = "wordlist/" + corpus + ".txt"
words = text_to_words(textfile)
#print(words[0:5])


# In[3]:
# Generate the set of unique characters (including newline)
# https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
chars = sorted(list(set([char for word in words for char in word])))

VOCAB_SIZE = len(chars)
N_WORDS = len(words)
MAX_WORD_LEN = 12  # maximum company name length


#print(N_WORDS, "words\n")
#print("vocabulary of", len(chars), "characters, including the \\n:")
#print(chars)
#print("\nFirst two sample words:")
#print(words[0:2])


# In[4]:


ix_to_char = {ix:char for ix, char in enumerate(chars)}
char_to_ix = {char:ix for ix, char in enumerate(chars)}


# In[5]:


X = np.zeros((N_WORDS, MAX_WORD_LEN, VOCAB_SIZE))
Y = np.zeros((N_WORDS, MAX_WORD_LEN, VOCAB_SIZE))

for word_i in range(N_WORDS):
    word = words[word_i]
    chars = list(word)
    word_len = len(word)
    
    for char_j in range(min(len(word), MAX_WORD_LEN)):
        char = chars[char_j]
        char_ix = char_to_ix[char]
        X[word_i, char_j, char_ix] = 1
        if char_j > 0:
            Y[word_i, char_j - 1, char_ix] = 1  # the 'next char' at time point char_j


# In[6]:


''' LAYER_NUM = 2
HIDDEN_DIM = 50

model = Sequential()
model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
for i in range(LAYER_NUM - 1):
    model.add(LSTM(HIDDEN_DIM, return_sequences=True))
model.add(TimeDistributed(Dense(VOCAB_SIZE)))
model.add(Activation('softmax'))
model.compile(loss="categorical_crossentropy", optimizer="rmsprop")


# In[7]:
model.summary() '''


# In[8]:
def temp_scale(probs, temperature = 1.0):
    # a low temperature (< 1 and approaching 0) results in the char sampling approaching the argmax.
    # a high temperature (> 1, approaching infinity) results in sampling from a uniform distribution)
    probs = np.exp(np.log(probs) / temperature)
    probs = probs / np.sum(probs)
    return probs
    
    
def generate_word(model, temperature = 1.0, min_word_length = 4):
    X = np.zeros((1, MAX_WORD_LEN, VOCAB_SIZE))
    
    # sample the first character
    initial_char_distribution = temp_scale(model.predict(X[:, 0:1, :]).flatten(), temperature)
    
    ix = 0
    while ix == 0:  # make sure the initial character is not a newline (i.e. index 0)
        ix = int(np.random.choice(VOCAB_SIZE, size = 1, p = initial_char_distribution))
    
    X[0, 0, ix] = 1
    generated_word = [ix_to_char[ix].upper()]  # start with first character, then later successively append chars
    
    # sample all remaining characters
    for i in range(1, MAX_WORD_LEN):
        next_char_distribution = temp_scale(model.predict(X[:, 0:i, :])[:, i-1, :].flatten(), temperature)

        
        ix_choice = np.random.choice(VOCAB_SIZE, size = 1, p = next_char_distribution)
        # ix_choice = np.argmax(next_char_distribution)  # <- corresponds to sampling with a very low temperature
        ctr = 0
        while ix_choice == 0 and i < min_word_length:
            ctr += 1
            # sample again if you picked the end-of-word token too early
            ix_choice = np.random.choice(VOCAB_SIZE, size = 1, p = next_char_distribution)
            if ctr > 1000:
                print("caught in a near-infinite loop. You might have picked too low a temperature and the sampler just keeps sampling \\n's")
                break
            
        
        next_ix = int(ix_choice)
        X[0, i, next_ix] = 1
        if next_ix == 0:
            break
        generated_word.append(ix_to_char[next_ix])
    
    return ('').join(generated_word)


''' # In[9]:
def on_epoch_end(epoch, logs):
    if epoch % 50 == 0:
        print("epoch " + str(epoch) + ": " + generate_word(model, temperature = 1.0, min_word_length = 4))


print_callback = LambdaCallback(on_epoch_end = on_epoch_end)


# In[10]:
NUM_EPOCHS = 500
BATCH_SIZE = 64  # or: N_WORDS

model.fit(X, Y, batch_size = BATCH_SIZE, verbose = 0, epochs = NUM_EPOCHS, callbacks = [print_callback])

# save the model, but only if the h5 file doesn't exist yet:
model_filename = "models/" + corpus + "_" + str(NUM_EPOCHS) + 'epochs.h5'
if not os.path.isfile(model_filename):
    model.save(model_filename) '''


# In[11]:

## Load one of these models if you have trained them before and want to skip re-training
from keras.models import load_model

# model = load_model("models/behemoth_500epochs.h5")
#model = load_model("models/pokemon_500epochs.h5")
#model = load_model("models/german_500epochs.h5")
# model = load_model("models/english_500epochs.h5")
#model = load_model("models/kmkpoke_500epochs.h5")
model = load_model("models/kmkcomp_500epochs.h5")


# In[13]:


# Print a few words with the final model:

for _ in range(20):
    print(generate_word(model, temperature = 1, min_word_length = 4))
