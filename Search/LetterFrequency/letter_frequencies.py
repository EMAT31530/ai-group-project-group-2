import pickle
import string

from Data.data import get_all_words

alphabet = string.ascii_lowercase
word_list = get_all_words()


letter_frequencies = {letter: 0 for letter in alphabet}

for word in word_list:
    for letter in word:
        letter_frequencies[letter] += word.count(letter)

letter_frequencies = dict(sorted(letter_frequencies.items(),
                  key=lambda item: item[1], reverse=True))

pickle.dump(letter_frequencies, open('letter_frequencies.pkl', 'wb'))
print(letter_frequencies)
