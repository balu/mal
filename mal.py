import unicodedata
from optparse import OptionParser

from subst import *
import copy, re

class Parser:

	WHITESPACE 	= 0
	SWORD		= 1
	GWORD		= 2
	MWORD		= 3
	ECHAR		= 4
	LWORD		= 5
	OTHER_CHAR	= 6

	tokens = [
		 [re.compile("\\\s+"), 		WHITESPACE],
		 [re.compile("[a-zA-Z]+"), 	SWORD],
		 [re.compile("\\([a-zA-Z]+\)"),	GWORD],
		 [re.compile("\\{.+\}"), 	MWORD],
		 [re.compile("\\\\."), 		ECHAR],
		 [re.compile("\\[.*\\]"),	LWORD]
	]

		

	def __init__(self):
		self.subst = copy.deepcopy(subst)
		self.mdict = copy.deepcopy(mdict)

	def _match(self, word):
		matches = []
		for s in self.subst:
			m = filter(lambda x: word.startswith(x), s[0])
			if m:
				matches.append((s, m[0]))
		return matches

	def _is_chillu_form(self, uni):
		return uni[0] == LETTER_NA or uni[0] == LETTER_RA or \
			uni[0] == LETTER_NHA or uni[0] == LETTER_LA or uni[0] == LETTER_LLA

	def _chillu_form(self, uni):
		chillus = { \
				LETTER_NA : CHILLU_N,\
				LETTER_NHA : CHILLU_NN,\
				LETTER_LA : CHILLU_L,\
				LETTER_LLA : CHILLU_LL,\
				LETTER_RA : CHILLU_RR}
		if chillus[uni]: return chillus[uni]
		return u''
			
			

	# Post processing for handling certain special forms in malayalam
	# Handle anusvaram, vocalic R, /nta/
	# If /m/ is not followed by pa or ma, turn it into anusvara, unless /m/ occurs at the beginning.
	# If a CONSONANT, VIRAMA, VOCALIC R sequence occurs, turn into sign for VOCALIC R
	# Chillu letters
	def _post_process(self, uni):
		global options
		new_uni = u''
		i = 0
		while i <= len(uni) - 2:
			if i == len(uni) - 2 and self._is_chillu_form(uni[i]) and uni[i+1] == SIGN_VIRAMA:
				new_uni = new_uni + self._chillu_form(uni[i])
				i = i + 2
			elif uni[i+1] == SIGN_VIRAMA and i+2 < len(uni) and uni[i+2] == LETTER_VOCALIC_R:
				new_uni = new_uni + uni[i] + VOWEL_SIGN_VOCALIC_R
				i = i + 3
			elif i > 0 and uni[i] == LETTER_MA and uni[i+1] == SIGN_VIRAMA and \
			(i+2 >= len(uni) or uni[i+2] != LETTER_PA and uni[i+2] != LETTER_MA):
				new_uni = new_uni + SIGN_ANUSVARA
				i = i + 2
			elif i+2 < len(uni) and uni[i] == LETTER_NA and uni[i+1] == SIGN_VIRAMA and uni[i+2] == LETTER_TA:
				if options.oldnta: new_uni = new_uni + LETTER_NA + SIGN_VIRAMA + LETTER_RRA
				else: new_uni = new_uni + CHILLU_N + SIGN_VIRAMA + LETTER_RRA
				i = i + 3
			else:
				new_uni = new_uni + uni[i]
				i = i + 1
		new_uni = new_uni + uni[i:]
		return new_uni


	# convert a word containing only letters into unicode codepoints for malayalam.
	def __convert(self, word):
		word = word.lower()
		uni = u''
		while word:
			m = self._match(word)
			if m:
				m = reduce(lambda x, y: len(x[1]) >= len(y[1]) and x or y, m) # Pick the longest match
				uni = uni + m[0][1]
				word = word[len(m[1]):]
			else:
				uni = uni + word[0] # No matches found skip one character
				word = word[1:]
		return self._post_process(uni)

	def _process_group(self, m):
		gbody = m[1:-1]
		return self.__convert(gbody)

	def _process_macro(self, m):
		mbody = m[1:-1]
		if mbody in self.mdict.keys():
			return self.mdict[m[1:-1]]
		return m

	def _process_literal(self, m):
		return m[1:-1]

	def _get_token(self, text):
		for pat, t in Parser.tokens:
			m = re.match(pat, text)
			if m:
				return (t, m.group())
		return (Parser.OTHER_CHAR, text[0])
		

	def convert(self, text):
		"""Use for lines to be converted (Not to be used for import lines)"""
		out = u''
		while text != "":
			(ty, te) = self._get_token(text)
			if ty == Parser.WHITESPACE:
				out = out + te
			elif ty == Parser.SWORD:
				out = out + self.__convert(te)
			elif ty == Parser.GWORD:
				out = out + self._process_group(te)
			elif ty == Parser.MWORD:
				out = out + self._process_macro(te)
			elif ty == Parser.ECHAR:
				out = out + te[1]
			elif ty == Parser.LWORD:
				out = out + self._process_literal(te)
			else:
				out = out + te[0]
			text = text[len(te):]
		return out

	def source(self, line):
		"""Use for a line of text"""
		if line.startswith("import"):
			fname = line.split()[1] + '.py'
			execfile(fname)
			return u''
		else:
			return self.convert(line)

	def stream(self, istream, ostream):
		"""Use to copy from one stream to another"""
		line = istream.readline()
		while line != "":
			ostream.write(self.source(line))
			line = istream.readline()

	def text(self, text):
		"""Use for a chunk of text"""
		out = u''
		lines = text.splitlines()
		for line in lines:
			u = u + self.source(line) + '\n'
		return u

if __name__ == "__main__":
	import sys, codecs
	global options
	parser = OptionParser()
	parser.add_option("--old-nta", action="store_true", dest="oldnta", default=False, 
		help="Use old style code for the ligature /nta/. (Required to work with older fonts not supporting Unicode 5.1")
	(options,args) = parser.parse_args()

	p = Parser()

	with open("/dev/stdin", "r") as infile:
		with codecs.open("/dev/stdout", "w", "utf_8") as outfile:
			p.stream(infile, outfile)

