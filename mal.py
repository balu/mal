import unicodedata
from subst import *


def match(word, subst):
	"""Match the prefix of the word with subst. Return all matched substitutions"""
	matches = []
	for s in subst:
		m = filter(lambda x: word.startswith(x), s[0])
		if m:
			matches.append((s, m[0]))
	return matches


# Post processing for handling certain special forms in malayalam
# Handle anusvaram, vocalic R, /nta/
# If /m/ is not followed by pa or ma, turn it into anusvara
# If a CONSONANT, VIRAMA, VOCALIC R sequence occurs, turn into sign for VOCALIC R
def _post_process(uni):
	new_uni = u''
	i = 0
	while i <= len(uni) - 2:
		if uni[i+1] == SIGN_VIRAMA and i+2 < len(uni) and uni[i+2] == LETTER_VOCALIC_R:
			new_uni = new_uni + uni[i] + VOWEL_SIGN_VOCALIC_R
			i = i + 3
		elif uni[i] == LETTER_MA and uni[i+1] == SIGN_VIRAMA and \
		(i+2 >= len(uni) or uni[i+2] != LETTER_PA and uni[i+2] != LETTER_MA):
			new_uni = new_uni + SIGN_ANUSVARA
			i = i + 2
		elif i+2 < len(uni) and uni[i] == LETTER_NA and uni[i+1] == SIGN_VIRAMA and uni[i+2] == LETTER_TA:
			# TODO: As per Unicode 5.1, the correct sequence is CHILLU_NA + SIGN+VIRAMA + LETTER_RRA
			# However no font supports this sequence (as of Jul 2012)
			new_uni = new_uni + LETTER_NA + SIGN_VIRAMA + LETTER_RRA
			i = i + 3
		else:
			new_uni = new_uni + uni[i]
			i = i + 1
	new_uni = new_uni + uni[i:]
	return new_uni


# convert a word containing only letters into unicode codepoints for malayalam.
def __convert(word):
	uni = u''
	word = word.lower().strip()
	while word:
		m = match(word, subst)
		if m:
			m = reduce(lambda x, y: len(x[1]) >= len(y[1]) and x or y, m) # Pick the longest match
			uni = uni + m[0][1]
			word = word[len(m[1]):]
		else:
			return u'' # Failed to convert the word.
	return _post_process(uni)

def _group_until_match(word, char, match_char):
	w = char
	c = 0
	i = 1
	while i < len(word) and (c > 0 or word[i] != match_char):
		if word[i] == char: c = c + 1
		elif word[i] == match_char: c = c - 1
		w, i = w + word[i], i + 1
	if c > 0 or i >= len(word):
		word = w = ""
	else:
		w = w + word[i]
		word = word[i+1:]
	return (w, word)

def _split_to_groups(word):
	w = ""
	if word == "": return []

	if word[0] == '(':
		(w, word) = _group_until_match(word, '(', ')')
	elif word[0] == '{':
		(w, word) = _group_until_match(word, '{', '}')
	elif word[0] == '\\':
		w = word[0:2]
		word = word[2:]
	elif word.isalpha():
		return [word]
	elif not word[0].isalpha():
		w, word = word[0], word[1:]
	else:
		i = 0
		while i < len(word) and word[i].isalpha():
			w, i = w + word[i], i+1
		word = word[i:]
	# Invariant: w - the first member of the group, word - the rest of the word after removing group w
	return [w] + _split_to_groups(word)

def _process_macro(m):
	mbody = m[1:-1]
	if mbody in mdict.keys():
		return mdict[m[1:-1]]
	return u''

def _process_group(g):
	gbody = g[1:-1]
	return _convert(gbody)
		
# Convert a word (possibly containing substs) into unicode malayalam.
def _convert(word):
	uni = u''
	word = word.lower().strip()
	wg = _split_to_groups(word)
	for w in wg:
		if w[0] == '(':
			u = _process_group(w)
		elif w[0] == '{':
			u = _process_macro(w)
		elif w[0] == '\\':
			u = w[1]
		elif w.isalpha():
			u = __convert(w)
		else:
			u = w
		uni = uni + u
	return uni


def convert(stream):
	lines = u''
	line = stream.readline()
	while line != "":
		i = 0
		while i < len(line):
			while i < len(line) and line[i].isspace(): i, lines = i+1,lines + line[i]
			
			# Gather the next word (A string of non-whitespace characters)
			w = ""
			while i < len(line) and not line[i].isspace(): i, w = i+1, w + line[i]
		
			u = _convert(w)
			lines = lines + u
		line = stream.readline()
	return lines


if __name__ == "__main__":
	import sys, codecs
	f = codecs.open("/dev/stdout", "w", "utf_8")
	f.write(convert(sys.stdin))
