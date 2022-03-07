from typing import List


def read_words():
    f = open("words.txt", 'r')
    english_words = []
    for line in f:
        word = line.strip()
        english_words.append(word)
    five_letter_words = [word for word in english_words if len(word) == 5]
    
    return five_letter_words
