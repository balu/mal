import unicodedata, string, pprint

# chillu letters
CHILLU_N    = 	unicodedata.lookup('MALAYALAM LETTER CHILLU N')
CHILLU_NN   = 	unicodedata.lookup('MALAYALAM LETTER CHILLU NN')
CHILLU_L    = 	unicodedata.lookup('MALAYALAM LETTER CHILLU L')
CHILLU_LL   = 	unicodedata.lookup('MALAYALAM LETTER CHILLU LL')
CHILLU_RR   = 	unicodedata.lookup('MALAYALAM LETTER CHILLU RR')

# vowel letters
LETTER_A = unicodedata.lookup('MALAYALAM LETTER A')
LETTER_AA = unicodedata.lookup('MALAYALAM LETTER AA')
LETTER_I = unicodedata.lookup('MALAYALAM LETTER I')
LETTER_II = unicodedata.lookup('MALAYALAM LETTER II')
LETTER_U = unicodedata.lookup('MALAYALAM LETTER U')
LETTER_UU = unicodedata.lookup('MALAYALAM LETTER UU')
LETTER_VOCALIC_R = unicodedata.lookup('MALAYALAM LETTER VOCALIC R')
LETTER_E = unicodedata.lookup('MALAYALAM LETTER E')
LETTER_EE = unicodedata.lookup('MALAYALAM LETTER EE')
LETTER_AI = unicodedata.lookup('MALAYALAM LETTER AI')
LETTER_O = unicodedata.lookup('MALAYALAM LETTER O')
LETTER_OO = unicodedata.lookup('MALAYALAM LETTER OO')
LETTER_AU = unicodedata.lookup('MALAYALAM LETTER AU')

# consonant letters
LETTER_KA = unicodedata.lookup('MALAYALAM LETTER KA')
LETTER_KHA = unicodedata.lookup('MALAYALAM LETTER KHA')
LETTER_GA = unicodedata.lookup('MALAYALAM LETTER GA')
LETTER_GHA = unicodedata.lookup('MALAYALAM LETTER GHA')
LETTER_NGA = unicodedata.lookup('MALAYALAM LETTER NGA')
LETTER_CHA = unicodedata.lookup('MALAYALAM LETTER CA')
LETTER_CHHA = unicodedata.lookup('MALAYALAM LETTER CHA')
LETTER_JA = unicodedata.lookup('MALAYALAM LETTER JA')
LETTER_JHA = unicodedata.lookup('MALAYALAM LETTER JHA')
LETTER_NJA = unicodedata.lookup('MALAYALAM LETTER NYA')
LETTER_TA = unicodedata.lookup('MALAYALAM LETTER TTA')
LETTER_TTA = unicodedata.lookup('MALAYALAM LETTER TTHA')
LETTER_DA = unicodedata.lookup('MALAYALAM LETTER DDA')
LETTER_DDA = unicodedata.lookup('MALAYALAM LETTER DDHA')
LETTER_NHA = unicodedata.lookup('MALAYALAM LETTER NNA')
LETTER_THA = unicodedata.lookup('MALAYALAM LETTER TA')
LETTER_TTHA = unicodedata.lookup('MALAYALAM LETTER THA')
LETTER_DHA = unicodedata.lookup('MALAYALAM LETTER DA')
LETTER_DDHA = unicodedata.lookup('MALAYALAM LETTER DHA')
LETTER_NA = unicodedata.lookup('MALAYALAM LETTER NA')
LETTER_PA = unicodedata.lookup('MALAYALAM LETTER PA')
LETTER_PHA = unicodedata.lookup('MALAYALAM LETTER PHA')
LETTER_BA = unicodedata.lookup('MALAYALAM LETTER BA')
LETTER_BHA = unicodedata.lookup('MALAYALAM LETTER BHA')
LETTER_MA = unicodedata.lookup('MALAYALAM LETTER MA')
LETTER_YA = unicodedata.lookup('MALAYALAM LETTER YA')
LETTER_RA = unicodedata.lookup('MALAYALAM LETTER RA')
LETTER_LA = unicodedata.lookup('MALAYALAM LETTER LA')
LETTER_VA = unicodedata.lookup('MALAYALAM LETTER VA')
LETTER_SHA = unicodedata.lookup('MALAYALAM LETTER SHA')
LETTER_SSA = unicodedata.lookup('MALAYALAM LETTER SSA')
LETTER_SA = unicodedata.lookup('MALAYALAM LETTER SA')
LETTER_HA = unicodedata.lookup('MALAYALAM LETTER HA')
LETTER_LLA = unicodedata.lookup('MALAYALAM LETTER LLA')
LETTER_ZHA = unicodedata.lookup('MALAYALAM LETTER LLLA')
LETTER_RRA = unicodedata.lookup('MALAYALAM LETTER RRA')

# vowel signs
VOWEL_SIGN_AA = unicodedata.lookup('MALAYALAM VOWEL SIGN AA')
VOWEL_SIGN_I = unicodedata.lookup('MALAYALAM VOWEL SIGN I')
VOWEL_SIGN_II = unicodedata.lookup('MALAYALAM VOWEL SIGN II')
VOWEL_SIGN_U = unicodedata.lookup('MALAYALAM VOWEL SIGN U')
VOWEL_SIGN_UU = unicodedata.lookup('MALAYALAM VOWEL SIGN UU')
VOWEL_SIGN_VOCALIC_R = unicodedata.lookup('MALAYALAM VOWEL SIGN VOCALIC R')
VOWEL_SIGN_E = unicodedata.lookup('MALAYALAM VOWEL SIGN E')
VOWEL_SIGN_EE = unicodedata.lookup('MALAYALAM VOWEL SIGN EE')
VOWEL_SIGN_O = unicodedata.lookup('MALAYALAM VOWEL SIGN O')
VOWEL_SIGN_OO = unicodedata.lookup('MALAYALAM VOWEL SIGN OO')
VOWEL_SIGN_AU = unicodedata.lookup('MALAYALAM AU LENGTH MARK')

# signs
SIGN_VIRAMA = unicodedata.lookup('MALAYALAM SIGN VIRAMA')
SIGN_ANUSVARA = unicodedata.lookup('MALAYALAM SIGN ANUSVARA')
SIGN_VISARGA = unicodedata.lookup('MALAYALAM SIGN VISARGA')
SIGN_AVAGRAHA = unicodedata.lookup('MALAYALAM SIGN AVAGRAHA')

# Define the patterns for substitution
vowels = [
(["a"], 	LETTER_A),
(["aa"], 	LETTER_AA),
(["i"], 	LETTER_I),
(["ii"], 	LETTER_II),
(["u"], 	LETTER_U),
(["uu"], 	LETTER_UU),
(["rh"], 	LETTER_VOCALIC_R),
(["e"], 	LETTER_E),
(["ee"], 	LETTER_EE),
(["ai"], 	LETTER_AI),
(["o"], 	LETTER_O),
(["oo"], 	LETTER_OO),
(["au"], 	LETTER_AU),
]

consonants = [
(["k"], 	LETTER_KA),
(["kh"], LETTER_KHA),
(["g"], 	LETTER_GA),
(["gh"], LETTER_GHA),
(["ng"], LETTER_NGA),
(["ch"], LETTER_CHA),
(["chh"], 	LETTER_CHHA),
(["j"], 	LETTER_JA),
(["jh"], LETTER_JHA),
(["nj"], LETTER_NJA),
(["t"], 	LETTER_TA),
(["tt"], LETTER_TTA),
(["d"], 	LETTER_DA),
(["dd"], LETTER_DDA),
(["nh"], LETTER_NHA),
(["th"], LETTER_THA),
(["tth"], 	LETTER_TTHA),
(["dh"], LETTER_DHA),
(["ddh"], 	LETTER_DDHA),
(["n"], 	LETTER_NA),
(["p"], 	LETTER_PA),
(["ph"], LETTER_PHA),
(["b"], 	LETTER_BA),
(["bh"], LETTER_BHA),
(["m"], 	LETTER_MA),
]

# Extra Consonants
for i in ("Y", "R", "RR", "L", "LL", "V", "SH", "SS", "S", "H"):
	consonants.append(([i.lower()], unicodedata.lookup('MALAYALAM LETTER ' + i + 'A')))
consonants.append((["zh"], unicodedata.lookup('MALAYALAM LETTER LLLA')))

# Add consonants followed by vowel sounds
consonant_vowel = []

for vowel_sign in ("AA", "I", "II", "U", "UU", "E", "EE", "AI", "O", "OO"):
	for c in consonants:
		consonant_vowel.append(([i + vowel_sign.lower() for i in c[0]], c[1] + unicodedata.lookup('MALAYALAM VOWEL SIGN ' + vowel_sign)))

for c in consonants:
	consonant_vowel.append(([i + "ow" for i in c[0]], c[1] + unicodedata.lookup('MALAYALAM AU LENGTH MARK')))
	consonant_vowel.append(([i + "a" for i in c[0]], c[1]))

for i, c in enumerate(consonants):
	consonants[i] = (c[0], c[1] + unicodedata.lookup('MALAYALAM SIGN VIRAMA'))

# List of all patterns
subst = vowels + consonants + consonant_vowel

# internally defined substitutions
mdict = {
"v": SIGN_AVAGRAHA,
"h": SIGN_VISARGA
}

if __name__ == "__main__":
	pprint.pprint(subst)
