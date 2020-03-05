import math 
from reader import readRawDataFor
from metrics import analyze, printErrors
from preprocess import split, getAllText, countStrings, cleanRawData
from tokenizer import getTokens
		

def train(trainSet):
	totalDocsCount = len(trainSet)
	
	allClasses = [cls for (text, cls) in trainSet]
	classesCount = countStrings(allClasses)
	classes = [cls for cls in classesCount]
	print(classesCount)
	
	allText = getAllText(trainSet)
	allWords = getTokens(allText)
	allWordsCount = countStrings(allWords)
	vocabulary = [word for word in allWordsCount]
	uniqueWordCount = len(vocabulary)
	totalWordCount = len(allWords)
	print('all words: ' + str(totalWordCount))
	print('unique words: ' + str(uniqueWordCount))
	
	textPerClass = {}
	wordsCountPerClass = {}
	wordsPerClass = {}
	for cls in classes:
		textPerClass[cls] = getAllText(trainSet, cls)
		tokens = getTokens(textPerClass[cls])
		wordsCountPerClass[cls] = len(tokens)
		wordsPerClass[cls] = countStrings(tokens)
		
	logPrior = {}
	for cls in classes:
		logPrior[cls] = math.log(classesCount[cls]/totalDocsCount)
		
	logLikelihood = {}
	for word in vocabulary:
		classesPerWord = {}
		for c in classes:
			wordsOfClass = wordsPerClass[c]
			if word in wordsOfClass:
				wc = wordsOfClass[word]
			else:
				wc = 0
				
			classesPerWord[c] = math.log((wc + 1) / (wordsCountPerClass[c] + uniqueWordCount))
		logLikelihood[word] = classesPerWord
		
	return vocabulary, classes, logPrior, logLikelihood

def predict(text, vocabulary, classes, logPrior, logLikelihood):
	tokens = [token for token in getTokens(text) if token in vocabulary]
	scores = {}
	for c in classes:
		scores[c] = logPrior[c]
		for token in tokens:
			scores[c] += logLikelihood[token][c]
	#print(scores)
	
	probs = {}
	probsSum = 0.0
	max = -float('inf')
	argmax = None
	for c in classes:
		score = scores[c]
		probs[c] = math.exp(math.exp(score))
		probsSum += probs[c]
		if score > max:
			max = score
			argmax = c
		
	prob = probs[argmax] / probsSum
	return argmax, prob
	
def printDetails(predictionsWithScore, gold):
	n = len(gold)
	for i in range(n):
		p, s = predictionsWithScore[i]
		print(gold[i], p, s)	


if __name__ == '__main__':
	#settings
	
	# spam, clothing, disaster
	rawDataName = 'disaster' 
	testSetPercentage = 0.01
	
	#main
	rawData = readRawDataFor(rawDataName)
	rawData = cleanRawData(rawData)
	trainSet, testSet = split(rawData, testSetPercentage)
	
	vocabulary, classes, logPrior, logLikelihood = train(trainSet)
		
	gold = [c for (text, c) in testSet]
	predictionsWithScore = [predict(text, vocabulary, classes, logPrior, logLikelihood) for (text, c) in testSet]
	#printDetails(predictionsWithScore, gold)
	predictions = [c for (c,s) in predictionsWithScore]
	analyze(gold, predictions, classes)
	printErrors(testSet, predictions, '0')
	printErrors(testSet, predictions, '1')
	

