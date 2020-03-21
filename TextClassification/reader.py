import csv

def getPath():
	return './TextClassification/data/'

#spam.csc
#v1,v2,,,
#ham,"Go until jurong point, crazy..

#clothing
#ID, ClothingID, Age, Title, ReviewText, Rating, RecommendedIND, PositiveFeedbackCount, DivisionName, DepartmentName, ClassName
#0, 767, 33, ,Absolutely wonderful - silky and sexy and comfortable, 4, 1, 0, Initmates, Intimate, Intimates

def readRawDataFor(source):
	if source=='spam':
		#spam.csv
		#v1,v2,,,
		#ham,"Go until jurong point, crazy..
		return readRawData(getPath()+'spam.csv', 1, 0)
	if source=='clothing':
		#clothing
		#ID, ClothingID, Age, Title, ReviewText, Rating, RecommendedIND, PositiveFeedbackCount, DivisionName, DepartmentName, ClassName
		#0, 767, 33, ,Absolutely wonderful - silky and sexy and comfortable, 4, 1, 0, Initmates, Intimate, Intimates
		return readRawData(getPath()+'clothing.csv', 4, 5)
	if source=='disaster':
		return readRawData(getPath()+'nlp-getting-started/train.csv', 3, 4)
	if source=='':
		return readRawData(getPath()+'nlp-getting-started/train.csv', 3, 4)

def readRawData(sourcePath, idxText, idxLabel):
	with open(sourcePath, 'r', encoding='latin-1') as csvfile:
		dataReader = csv.reader(csvfile, delimiter=',', quotechar='"')
		next(dataReader) #skip header
		return [(row[idxText], row[idxLabel]) for row in dataReader]

if __name__ == '__main__':
	print(len(readRawDataFor('spam')))
