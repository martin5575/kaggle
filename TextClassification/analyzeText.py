from reader import readRawDataFor
from preprocess import split, getAllText, countStrings, cleanRawData
from tokenizer import getTokens
import random
from nltk.corpus import wordnet as wn

def hasSynset(word):
	wordSynsets = wn.synsets(word)
	#print(wordSynsets)
	return len(wordSynsets) > 0
	

# spam, clothing, disaster
rawData = readRawDataFor('clothing')
cleanedData = cleanRawData(rawData)
random.shuffle(cleanedData)
trainData, testData = split(cleanedData, 0.1)
allText = getAllText(trainData)
tokens = getTokens(allText, False)
wordCount = countStrings(tokens)
threshold=50
moreThanThreshold = [(w, wordCount[w]) for w in wordCount if wordCount[w]>threshold]

nonDictionaryWords = [w for (w, c) in moreThanThreshold if not hasSynset(w)]

for w in nonDictionaryWords:
	print(w, wordCount[w])
