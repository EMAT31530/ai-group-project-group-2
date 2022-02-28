import pickle

from Data.data import get_all_words

word_list = get_all_words()


def count_vowels(word: str):
    return sum(letter in 'aeiou' for letter in word)


vowel_frequencies = {word: count_vowels(set(word)) for word in word_list}
vowel_frequencies = dict(sorted(vowel_frequencies.items(),
                  key=lambda item: item[1], reverse=True))

pickle.dump(vowel_frequencies, open('vowel_frequencies.pkl', 'wb'))
print(vowel_frequencies)
