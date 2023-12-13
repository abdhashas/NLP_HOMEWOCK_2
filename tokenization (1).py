from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.disambig.mle import MLEDisambiguator
import re


punctuationPattern = r"([*|,\-#!<&>_+{:/$\\=()?؟.،'}%\";\[\]])"
# # Initialize disambiguators
mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='atbtok')


def tokenize(text):
	tokens = msa_bw_tokenizer.tokenize([token for sent in re.split(punctuationPattern, text.strip()) for token in sent.split()])
	for i, token in enumerate(tokens):
	  if token.startswith(('ب', 'ف', 'ل')):
	    subtokens = token.split('+_')
	    if len(subtokens) > 1:
	      tokens[i] = subtokens[0]
	      tokens.insert(i+1, subtokens[1])
	  elif token == 'من_+ما':
	    tokens[i] = 'مما'
	  else:
	    tokens[i] = re.sub(r'\+_|_\+', '', token)
	return tokens
