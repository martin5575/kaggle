import numpy as np
import math
from metrics import calcAllMetrics

def performCrossValidation(rawData, trainFunc, predictFunc, id='Model', n=10):
	avg_f1, avg_ac, avg_pr, avg_rc = crossValidate(rawData, trainFunc, predictFunc, n)
	print('Cross validation ({} folds) for {}'.format(n, id))				
	print('AVG: F1: {}, AC: {}, PR: {}, RC: {}'.format(avg_f1, avg_ac, avg_pr, avg_rc))		
	
def crossValidate(rawData, trainFunc, predictFunc, k=10):
	folds = createFolds(rawData, k)
	labels = getLabels(rawData)
	accuracy = []
	f1 = []
	precission = []
	recall = []
	for i in range(k):
		trainData, testData = selectData(folds, i)
		model = trainFunc(trainData)
		gold = [c for (text, c) in testData]
		predictions = predictFunc(model, testData)
		ac_, f1_, pr_, rc_, tp, tn, fp, fn = calcAllMetrics(labels[0], gold, predictions)
		print('fold {}: {} (f1), {} (ac)'.format(i, f1_, ac_))
		f1.append(f1_)
		accuracy.append(ac_)
		precission.append(pr_)
		recall.append(rc_)
	avg_f1 = np.mean(np.array(f1))
	avg_ac = np.mean(np.array(accuracy))
	avg_pr = np.mean(np.array(precission))
	avg_rc = np.mean(np.array(recall))
	return avg_f1, avg_ac, avg_pr, avg_rc
	
def createFolds(rawData, k):
	n = math.floor( len(rawData) / k )
	folds = []
	for i in range(k-1):
		start = i * n
		end = start + n
		folds.append(rawData[start:end])
	folds.append(rawData[(k-1)*n:])
	return folds
				
def selectData(folds, trainIndex):
	testData = folds[trainIndex]
	trainData = []
	for i in range(len(folds)):
		if not trainIndex==i:
			tuples = folds[i]
			for (t, l) in tuples:
				trainData.append((t, l))
	return trainData, testData

def getLabels(rawData):
	labels = {}
	for (text, lbl) in rawData:
		if not lbl in labels:
			labels[lbl] = 1
	return [l for l in labels]
	
if __name__ == '__main__':

	def trainTest(rawData):
		return None
		
	def predictTest(model, testData):
		predictions = []
		for i in range(len(testData)):
			predictions.append(0)
		return predictions;
				
	rawData = [('abc', 0), ('bbc', 1), ('aeg', 0), ('zdf', 1), ('asc', 0), ('org', 1), ('ard', 0)]

	performCrossValidation(rawData, trainTest, predictTest, 'TEST', 3)
