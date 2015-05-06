# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from tfidf import *
from heapq import nlargest

def findbyword(tfidf, word, limit=5):
  max_list = []
  for document_key in tfidf:
    document = tfidf[document_key]
    for word_key in document:
      # print "word_key", type(word_key)
      # print "word", type(word)
      if word_key == word:
        max_list.append((document_key, document[word_key]))
  return nlargest(limit, max_list, key=lambda e:e[1])

if __name__ == '__main__':
  if len(sys.argv) >= 4:
    corpus_file = sys.argv[1]
    synonyms_file = sys.argv[2]
    word = unicode(sys.argv[3], "utf-8")

    synonyms = create_synonyms_dictionary(synonyms_file)
    notes, BOWs = count_tf(corpus_file, synonyms)
    idf = count_idf(BOWs)
    tfidf = count_tfidf(BOWs, idf)

    documents = findbyword(tfidf, word)
    for document in documents:
      print(document[0] + " : " + str(document[1]))

  else:
    print("python findbywords.py [corpus] [synonyms] [keyword]")
