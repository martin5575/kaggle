import math 
import re

def split(rawData, testPercentage):
	n = len(rawData)
	p = math.floor(n*testPercentage)
	return rawData[:-p], rawData[-p:]

def getAllText(rawData, label=None):
	#selector = lambda x: label==None or x[1]==label
	#filter(rawData, selector)
	selectedTextRows = [(row[0]) for row in rawData if (label==None or row[1]==label)]
	text = " ".join(selectedTextRows)
	return text
	
def countStrings(list):
	result = {}
	for item in list:
		if item in result:
			result[item] += 1
		else:
			result[item] = 1
	return result
	

	
def cleanRawData(rawData):
	return [(cleanText(row[0]), row[1]) for row in rawData]
	
def cleanText(rawText, toLower=True, removeSlang=True, removeNumbers=True, removeSpecialNotations=True, removeUrls=True):
	cleanedText = rawText
	
	if toLower:
		cleanedText = cleanedText.lower()
		
	if removeUrls:
		cleanedText = replaceUrls(cleanedText)
	
	if removeSlang:
		cleanedText = replaceSlang(cleanedText)
		
	if removeSpecialNotations:
		cleanedText = replaceSpecialNotations(cleanedText)
	
	if removeNumbers:
		cleanedText = re.sub(r'[^a-z ]', '', cleanedText)
		
	#print(cleanText)
	return cleanedText

def replaceSlang(rawText):
	cleanText = re.sub(r'i\'m', 'i am', rawText)
	cleanText = re.sub(r'i\'ve', 'i have', cleanText)
	cleanText = re.sub(r'i\'ll', 'i will', cleanText)
	cleanText = re.sub(r' n ', ' and ', cleanText)
	cleanText = re.sub(r' u ', ' you ', cleanText)
	cleanText = re.sub(r' u\?', ' you\?', cleanText)
	cleanText = re.sub(r' u\.', ' you\.', cleanText)
	cleanText = re.sub(r' u\!', ' you\!', cleanText)
	cleanText = re.sub(r'^u ', 'you ', cleanText)
	cleanText = re.sub(r' c ', ' see ', cleanText)
	cleanText = re.sub(r' r ', ' are ', cleanText)
	cleanText = re.sub(r' ur ', ' you are ', cleanText)
	cleanText = re.sub(r' ur\?', ' you are\?', cleanText)
	cleanText = re.sub(r'^ur ', 'you are', cleanText)
	cleanText = re.sub(r' wk ', ' week ', cleanText)
	cleanText = re.sub(r' wkly ', ' weekly ', cleanText)
	cleanText = re.sub(r' don\'t ', ' do not ', cleanText)
	cleanText = re.sub(r' did\'t ', ' do not ', cleanText)
	cleanText = re.sub(r' you\'re ', ' you are ', cleanText)
	cleanText = re.sub(r' that\'s ', ' that is ', cleanText)
	cleanText = re.sub(r' lol ', ' laugh out loud ', cleanText)
	cleanText = re.sub(r' im ', ' i am ', cleanText)
	cleanText = re.sub(r' gonna ', ' going to ', cleanText)
	cleanText = re.sub(r' hey ', ' hello ', cleanText)
	cleanText = re.sub(r' wat ', ' what ', cleanText)
	cleanText = re.sub(r' pls ', ' please ', cleanText)
	return cleanText
	
	
def replaceSpecialNotations(text):
	cleanText = re.sub(r'1st', 'first', text)
	cleanText = re.sub(r'2nd', 'second', cleanText)
	cleanText = re.sub(r'n''t', ' not', cleanText)
	cleanText = re.sub(r'&lt;', '<', cleanText)
	cleanText = re.sub(r'&gt;', '>', cleanText)
	return cleanText
	
def replaceUrls(text):
	cleanText = re.sub(r'http[^ ]+', '', text)
	return cleanText
