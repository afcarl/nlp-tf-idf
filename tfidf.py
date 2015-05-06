# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re
import operator
from math import log

def create_synonyms_dictionary(synonyms_file):
  synonyms = {}
  with open(synonyms_file) as f:
    for line in f:
      words = unicode(line, "utf-8").split(', ')
      for word in words[1:]:
        synonyms[word] = words[0]
  return synonyms

def count_tf(corpus_file, synonyms):
  with open(corpus_file) as f:
    data = unicode(f.read(), "utf-8")
  data = re.findall(ur"(#[\d]+)([^#]*)#[\d]+", data, re.DOTALL)
  notes = {}
  BOWs = {}
  for item in data:
    notes[item[0]] = item[1]
    value = [word.lower() for word in re.findall(ur"[a-zA-ZżółćęśąźńŻÓŁĆĘŚĄŹŃ]+", item[1])]
    value = [synonyms[word] if word in synonyms else word for word in value]
    word_dict = {}
    for word in value:
      if word not in word_dict:
        word_dict[word] = 1.
      else:
        word_dict[word] += 1.
    value_length = len(value)
    BOWs[item[0]] = {word:word_dict[word] / value_length for word in word_dict}
  return notes, BOWs

def count_idf(BOWs):
  idf = {}
  for key in BOWs:
    document = BOWs[key]
    for word in document:
      if word not in idf:
        idf[word] = 1.
      else:
        idf[word] += 1.
  return idf

def count_tfidf(BOWs, idf):
  number_of_documents = len(BOWs)
  for key in BOWs:
    document = BOWs[key]
    for word in document:
      document[word] *= log( number_of_documents / idf[word] )
  return BOWs

def get_key_words(tfidf, keyword, limit=5):
  return sorted(tfidf[keyword].items(), key=operator.itemgetter(1), reverse=True)[:limit]

def count_tfidf_matrix(tfidf, idf):
  keys = idf.keys()
  tfidf_matrix = {}
  for document in tfidf:
    doc = tfidf[document]
    tfidf_matrix[document] = [doc[i] if i in doc else 0. for i in keys]
  return tfidf_matrix, keys

if __name__ == '__main__':
  if len(sys.argv) >= 3:
    corpus_file = sys.argv[1]
    synonyms_file = sys.argv[2]

    synonyms = create_synonyms_dictionary(synonyms_file)
    notes, BOWs = count_tf(corpus_file, synonyms)
    idf = count_idf(BOWs)
    tfidf = count_tfidf(BOWs, idf)
    tfidf_matrix, _ = count_tfidf_matrix(tfidf, idf)
    print tfidf_matrix

  else:
    print("python tfidf.py [corpus] [synonyms]")
