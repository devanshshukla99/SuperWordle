import numpy as np
from core.wordle import Wordle

def generate_entropy_data(filename: str):
    w = Wordle()
    words = np.load(filename)
    w.available_words = words
    words_entropy = w._entropy_of_guesses(words)
    return words_entropy


