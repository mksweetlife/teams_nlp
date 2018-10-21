# serve.py 설명 
# keras-name-generate.py에서 트레이닝이 완료된 모델 불러오기 


import keras_name_generator
def get_random_name():
    r = generate_word(model, temperature = 1.1, min_word_length = 4)
    return r 