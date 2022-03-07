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

    Total = len(WordListSplit)
    FreqList = []
    for a in AlphaList:
        Count = WordListSplit.count(a)
        Freq = Count / Total
        FreqList.append(Freq)

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

    # Calculate entropy of each word
    EntropyDic = {}
    for w in WordList:
        Frequency = []
        for i in list(w):
            Frequency.append(FreqList[AlphaList.index(i)])
        EntropyDic[w] = entropy(Frequency, base=2)

        # print(EntropyDic[max(EntropyDic)])
    # Calculate entropy of each word
    EntropyDic = {}
    for w in WordList:
        Frequency = []
        for i in list(w):
            Frequency.append(FreqList[AlphaList.index(i)])
        EntropyDic[w] = entropy(Frequency, base=2)

    print(EntropyDic[max(EntropyDic)])
    print({k: v for k, v in sorted(EntropyDic.items(), key=lambda item: item[1])})
