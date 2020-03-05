from nltk.corpus import stopwords
from nltk.stem.porter import *

#def __init__():
	

def getTokens(text, applyStemmer=True):
	#print(text)
	rawTokens = [word for word in text.split()]
	
	if applyStemmer:
		stemmer = PorterStemmer()
		stemmedTokens = [stemmer.stem(t) for t in rawTokens]
	else:
		stemmedTokens = rawTokens
		
	tokens = removeStopWords(stemmedTokens)
	#print(tokens)
	return tokens

def removeStopWords(tokens, lang='english'):
	stoplist = stopwords.words(lang)
	cleanTokens = [word for word in tokens if word not in stoplist]
	return cleanTokens
	
def textToFeatureSet(text, features):
	result = {}
	for token in getTokens(text):
		if token in features:
			result[token] = 1
	return result

def createFeatureSet(rawData, features):
	return [(textToFeatureSet(text, features), label) for (text, label) in rawData]
	
if __name__=='__main__':
	print('test')
	tokens = getTokens('he washed his hairs')
	print(tokens)
