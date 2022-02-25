import pickle
from string import ascii_lowercase
from scipy.stats import entropy

def entropy_dic():
    # Find frequency of an alphabet
    AlphaList = ascii_lowercase
    with open('../Data/wordle-answers-alphabetical.txt', 'r') as f:
        WordList = f.readlines()
    with open('../Data/wordle-allowed-guesses.txt', 'r') as f:
        WordList += f.readlines()
    WordList = [i.strip('\n') for i in WordList]
    WordListSplit = ''.join(WordList)
    WordListSplit = list(WordListSplit)

<<<<<<< HEAD:Search/get_entropy.py
    Total = len(WordListSplit)
    FreqList = []
    for a in AlphaList:
        Count = WordListSplit.count(a)
        Freq = Count/Total
        FreqList.append(Freq)
=======
# Find frequency of an alphabet
from root import ROOT_DIR

AlphaList = ascii_lowercase
with open('../../Data/wordle-answers-alphabetical.txt', 'r') as f:
    WordList = f.readlines()
with open('../../Data/wordle-allowed-guesses.txt', 'r') as f:
    WordList += f.readlines()
WordList = [i.strip('\n') for i in WordList]
WordListSplit = ''.join(WordList)
WordListSplit = list(WordListSplit)
>>>>>>> 6a0554eb84c0c6ddce0991d89870493d48e1f4a9:Search/EntropySearch/get_entropy.py

    # Calculate entropy of each word
    EntropyDic = {}
    for w in WordList:
        Frequency = []
        for i in list(w):
            Frequency.append(FreqList[AlphaList.index(i)])
        EntropyDic[w] = entropy(Frequency, base=2)

<<<<<<< HEAD:Search/get_entropy.py
    # print(EntropyDic[max(EntropyDic)])
=======
# Calculate entropy of each word
EntropyDic = {}
for w in WordList:
    Frequency = []
    for i in list(w):
        Frequency.append(FreqList[AlphaList.index(i)])
    EntropyDic[w] = entropy(Frequency, base=2)

print(EntropyDic[max(EntropyDic)])

pickle.dump(EntropyDic, open('entropy.pkl', 'wb'))
>>>>>>> 6a0554eb84c0c6ddce0991d89870493d48e1f4a9:Search/EntropySearch/get_entropy.py
