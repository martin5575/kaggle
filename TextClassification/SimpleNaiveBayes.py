from math import floor
import nltk

from preprocess import cleanRawData, getAllText, split
from reader import readRawDataFor
from metrics import analyze
from tokenizer import createFeatureSet, getTokens

def createClassifier(trainSet):
	classifier = nltk.NaiveBayesClassifier.train(trainSet)		
	return classifier

def predictAll(classifier, test_set):
	return [classifier.classify(item) for (item, label) in test_set]

def evaluateModel(classifier, testSet, label):
	predictions = predictAll(classifier, testSet)
	gold = [lbl for (item, lbl) in testSet]
	(tp, tn, fp, fn) = getConfusionMatrix( gold, predictions) 
	return calcQualityMeasures(tp, tn, fp, fn)
	
def getFeatures(freqDist, mostFrequentWords, rareWords):
	features = [w[0] for w in freqDist.most_common()][mostFrequentWords:-rareWords]

	return features

def toFeatureSet(features, trainData, testData):
	trainSet = createFeatureSet(trainData, features)
	testSet = createFeatureSet(testData, features)
	return trainSet, testSet

if __name__ == '__main__':

	# spam, clothing, disaster
	rawDataName = 'disaster' 
	testSetPercentage = 0.1
	#mostFrequentWords = 10
	#rareWords = 8000
	mostFrequentWords = 0
	rareWords = 2000
	id='[{}:-{}]'.format(mostFrequentWords, rareWords)
	
	#main
	rawData = readRawDataFor(rawDataName)
	rawData = cleanRawData(rawData)
	n = len(rawData)
	print('rawData size: ' + str(n))
	
	(trainData, testData) = split(rawData, testSetPercentage)
	
	#spamText = getAllText(rawData, 'spam')
	#hamText = getAllText(rawData, 'ham')
	
	allText = getAllText(trainData)
	#tokens = nltk.word_tokenize(allText)
	tokens = getTokens(allText)
	print('tokens: '+ str(len(tokens)))
	freqDist = nltk.FreqDist(tokens)
	print(freqDist.most_common()[:50])
	freqDist.plot(20, cumulative=False)
	
	features = getFeatures(freqDist, mostFrequentWords, rareWords)
	print('{}: features: {}'.format(id, len(features)))
	
	trainSet, testSet = toFeatureSet(features, trainData, testData)
	classifier = createClassifier(trainSet)
	
	print('labels', classifier.labels())
	print(classifier.most_informative_features())
	
	accuracy = nltk.classify.accuracy(classifier, testSet)
	print('Model accuracy: ' + str(accuracy))
	
	#probs = classifier.prob_classify(test_set)
	#print(probs)
	
	predictions = predictAll(classifier, testSet)
	gold = [label for (item, label) in testSet]
	analyze(gold, predictions, classifier.labels())
		
	#print(classifier.prob_classify(trainSet[0]))
	
	def optimize(freqDist):
		for top in [0, 5, 10, 20, 50, 100, 200, 400]:
			for tail in [7000, 7500, 8000, 8500, 9000]:
				id='[{}:-{}]'.format(top, tail)
				features = getFeatures(freqDist, top, tail)
				print('{}: features: {}'.format(id, len(features)))
				trainSet, testSet = toFeatureSet(features, trainData, testData)
				classifier = createClassifier(trainSet)
				predictions = predictAll(classifier, testSet)
				id='[{}:-{}]'.format(top, tail)
				analyze(gold, predictions, classifier.labels(), id, True)
				
				
	#optimize(freqDist)
