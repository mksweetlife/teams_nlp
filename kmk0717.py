from gensim.models import FastText
import random
import numpy as np

from typing import List

Vector = List[float]

class Word:
    def __init__(self, text: str, vector: Vector) -> None:
        self.text = text
        self.vector = vector

# 1. 데이터 로드: 위키 simple english 파일 
fasttext_model = FastText.load_fasttext_format('wiki.simple.bin')
print(fasttext_model.most_similar('love'))

def vector_len(v: Vector) -> float:
    return math.sqrt(sum([x*x for x in v]))

def dot_product(v1: Vector, v2: Vector) -> float:
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """
    Returns the cosine of the angle between the two vectors.
    Results range from -1 (very different) to 1 (very similar).
    """
    return dot_product(v1, v2) / (vector_len(v1) * vector_len(v2))
