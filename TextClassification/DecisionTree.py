from math import floor, log
import csv
import nltk
import re
from nltk.corpus import stopwords 
import nltk.classify
import random
import operator
import copy

from reader import readRawDataFor
from preprocess import cleanRawData, getAllText, split
from tokenizer import getTokens, textToFeatureSet, createFeatureSet
from metrics import analyze, printErrors
from sampling import oversample, undersample
import StanfordNaiveBayes as snb
from featureSelector import findSimilarFeatures
				
def createClassifier(trainSet):
	classifier = nltk.classify.DecisionTreeClassifier.train(trainSet)
	return classifier

def predictAll(classifier, test_set):
	return [classifier.classify(item) for (item, label) in test_set]

def evaluateModel(classifier, testSet, label):
	predictions = predictAll(classifier, testSet)
	gold = [lbl for (item, lbl) in testSet]
	return analyze(gold, predictions, classes)
	
def createModel(trainSet, tokens):
	resampledSet = undersample(trainSet)
	#resampledSet = oversample(trainSet, tokens)
	classifier = createClassifier(resampledSet)
	return classifier
	
def selectFeatures(trainSet, top=10, bottom=10, addSimilarFeature=True, similarFeaturesThreshold=0.9):
	vocabulary, classes, logPrior, logLikelihood = snb.train(trainSet)
	
	features = []
	for c in classes:
		print('fearures for: ' + c)
		wordLikelihood = dict([(word, logLikelihood[word][c]) for word in vocabulary])
		#print(wordLikelihood)
		#print(type(wordLikelihood))
		wordsSorted = [(word, prob) for word, prob in sorted(wordLikelihood.items(), key=lambda item: item[1])]
		
		print(wordsSorted[:top])
		for (k, v) in wordsSorted[:top]:
			if not k in features:
				features.append(k)
		
		print(wordsSorted[-bottom:])
		for (k, v) in wordsSorted[-bottom:]:
			if not k in features:
				features.append(k)
				
		if addSimilarFeature:	
			for topWord, score in wordsSorted[:top]:
				similarWords = findSimilarFeatures(topWord, vocabulary, similarFeaturesThreshold)
				print(topWord, similarWords)
				features += similarWords
		
		print(features)
	return features

def getFillWords(tokens, mostFrequentWords, plot=False):
	freqDist = nltk.FreqDist(tokens)
	fillWords = [w for (w, cnt) in freqDist.most_common()[:mostFrequentWords]]

	#print(freqDist.most_common()[:mostFrequentWords])
	if plot:
		freqDist.plot(mostFrequentWords, cumulative=False)
	return fillWords
			
testSetPercentage = 0.3
#rareWords = 8350
fillWordCount = 0
takeTop = 0
takeBottom = 120

# spam, clothing, disaster
rawData = readRawDataFor('disaster')
rawData = cleanRawData(rawData)
random.shuffle(rawData)
n = len(rawData)
print('rawData size: ' + str(n))

(trainData, testData) = split(rawData, testSetPercentage)
print('trainData size: {}'.format(len(trainData)))

allText = getAllText(trainData)
tokens = getTokens(allText)
print('tokens: '+ str(len(tokens)))

fillWords = getFillWords(tokens, fillWordCount)
print('fillWords', fillWords)

features = selectFeatures(trainData, takeTop, takeBottom, addSimilarFeature=True, similarFeaturesThreshold=0.9)
print('features: '+str(len(features)))
print(features)

trainSet = createFeatureSet(trainData, features)
testSet = createFeatureSet(testData, features)

classifier = createModel(trainSet, tokens)

print(classifier.labels())
#print(classifier.decisions[1].pseudocode())

accuracy = nltk.classify.accuracy(classifier, testSet)
print('Model accuracy: ' + str(accuracy))

#probs = classifier.prob_classify(test_set)
#print(probs)

predictions = predictAll(classifier, testSet)
gold = [label for (item, label) in testSet]
classes = classifier.labels()

analyze(gold, predictions, classes)
#printErrors(testSet, predictions, '1')


def optimize(freqDist):
	for top in [0, 5, 10, 20, 50, 100, 200, 400]:
		for tail in [7000, 7500, 8000, 8500, 9000]:
			classifier, testSet, trainSet = createModel(freqDist, top, tail)
			(precision, recall, f1) = evaluateModel(classifier, testSet)
			print('[{}:-{}] pr: {:05.3f}, rc: {:05.3f}, f1: {:05.3f}'.format(top, tail, precision, recall, f1))
			
#optimize(freqDist)
