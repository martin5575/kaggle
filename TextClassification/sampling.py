import random

def undersample(trainSet):
	byClass = {}
	for (text, c) in trainSet:
		if not c in byClass:
			byClass[c] = []
		byClass[c].append((text, c))
	
	min = float('inf')
	for c in byClass:
		length = len(byClass[c])
		if length < min:
			min = length
			
	print('elements in smallest class: ' + str(min))
	for c in byClass:
		random.shuffle(byClass[c])
	
	result=[]	
	for c in byClass:
		result += byClass[c][:min]
		
	print('undersampled to: '+str(len(result)))
	return result
		
def oversample(trainSet, tokens):
	byClass = {}
	for (text, c) in trainSet:
		if not c in byClass:
			byClass[c] = []
		byClass[c].append((text, c))
	
	max = 0
	for c in byClass:
		length = len(byClass[c])
		if length > max:
			max = length
			
	print('elements in largest class: ' + str(max))
	for c in byClass:
		listForClass = byClass[c]
		k = max - len(listForClass)
		for i in range(k):
			idx = random.randint(0, len(listForClass)-1)
			newItem = copy.copy(listForClass[idx])
			toChange = newItem[0]
			changeCount = random.randint(1, 5)
			if changeCount<0:
				delIndex = random.randint(0, len(toChange))
				del toChange[delIndex]
			else:
				for j in range(changeCount):
					tokenIdx = random.randint(0, len(tokens)-1)
					token = tokens[tokenIdx]
					toChange[token] = 1		
			listForClass.append(newItem)
	
	result=[]	
	for c in byClass:
		result += byClass[c]
		
	print('oversampled to: '+str(len(result)))
	return result	
