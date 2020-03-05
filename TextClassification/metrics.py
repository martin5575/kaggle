from nltk import ConfusionMatrix
from nltk.metrics.scores import accuracy #, precision, recall, f_measure

def getConfusionMatrix(forClass, gold,  predictions):
	tp=0; tn=0; fp=0; fn=0
	n = len(gold)
	for i in range(n):
		c = gold[i]
		predict = predictions[i]
		isPositive = c==forClass
		isCorrect = c==predict
		if (isPositive):
			if (isCorrect):
				tp += 1
			else:
				fp += 1
		else:
			if (isCorrect):
				tn += 1
			else:
				fn += 1
	return (tp, tn, fp, fn)

def calcQualityMeasures(tp, tn, fp, fn):
	accuracy = (tp + tn) / (tp + tn + fp + fn)
	
	if tp == 0 and fn == 0:
		precision = float('nan')
	else:
		precision = tp / (tp + fn)
		
	if tp == 0 and fp == 0:
		recall = float('nan')
	else:
		recall = tp / (tp + fp)

	if (precision==0 and recall==0):
		f1 = float('nan')
	else:
		f1 = 2 * precision * recall / (precision + recall)
		
	return (accuracy, precision, recall, f1)	
	
def printDetails(predictionsWithScore, gold):
	n = len(gold)
	for i in range(n):
		p, s = predictionsWithScore[i]
		print(gold[i], p, s)	

def calcAllMetrics(cls, gold, predictions):
	(tp, tn, fp, fn) = getConfusionMatrix(cls, gold, predictions)
	(ac, pr, rc, f1) = calcQualityMeasures(tp, tn, fp, fn)
	return (ac, f1, pr, rc, tp, tn, fp, fn)

def analyze(gold, predictions, classes, id=None, compact=False):
	#print('accuracy: {:09.6f}', accuracy(gold, predictions))
	for c in classes:
		ac, f1, pr, rc, tp, tn, fp, fn = calcAllMetrics(c, gold, predictions)
		if compact:
			print('{}: f1:{:05.3f}, ac:{:05.3f}, pr:{:05.3f}, rc:{:05.3f}'.format(id, f1, ac, pr, rc))
		else:
			print('Class: {}, tp: {}, tn: {}, fp: {}, fn: {}'.format(c, tp, tn, fp, fn))
			print('f1: {:05.3f}, accuracy: {:05.3f}, precision: {:05.3f}, recall: {:05.3f}'.format(f1, ac, pr, rc))
	
		if len(classes) < 3:
			break
		
	if not compact:
		cm=ConfusionMatrix(gold, predictions)
		print(cm)
	
def printErrors(testSet, predictions, toClass=None):
	for i in range(len(testSet)):
		item = testSet[i]
		label = item[1]
		predict = predictions[i]
		
		if label != predict and (toClass == None or toClass == predict):
			print('predict', predict)
			print('but', item)

if __name__ == '__main__':
	gold = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	predictions = [1, 0, 0, 0, 0, 1, 1, 1, 1, 0]
	classes = [0, 1]
	analyze(gold, predictions, classes)

