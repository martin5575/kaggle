from nltk.corpus import wordnet as wn

def findSimilarFeatures(root, tokens, threshold=0.8):
	rootSynsets = wn.synsets(root)
	#print(rootSynsets)
	result = []
	for token in tokens:
		tokenSynsets = wn.synsets(token)
		#print(tokenSynsets)
		for rootSynset in rootSynsets:
			for tokenSynset in tokenSynsets:
				similarity = rootSynset.wup_similarity(tokenSynset)
				#print (similarity, rootSynset.name(), tokenSynset.name())
				if similarity != None and similarity >= threshold and not token in result:
					result.append(token)
					break
	return result
	
if __name__ == '__main__':
	root = 'disaster'
	tokens = ['bomb', 'tornado', 'hurricane', 'thunder', 'accident', 'man', 'baby', 'hospital', 'flood', 'tornado', 'battle']
	features = findFeatures(root, tokens, 0.6)
	print(root)
	print('tokens', tokens)
	print ('features', features)
	root = 'calamity'
	features = findFeatures(root, tokens, 0.6)
	print(root)
	print('tokens', tokens)
	print ('features', features)
	root = 'war'
	features = findFeatures(root, tokens, 0.6)
	print(root)
	print('tokens', tokens)
	print ('features', features)
