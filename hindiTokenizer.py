import re
def tokenize(fin):
	hindi = re.compile("[U00000000-U000FFFFF\u0000-\u0899\u0964-\u0971\u0980-\U000FFFFF u002D]")
	fin = fin.replace('.',' ')
	fin = fin.replace(',',' ')
	text = hindi.sub(' ',fin).strip()
	words = set()
	for word in text.split():
	    words.add(word)
	return set(sorted(words))