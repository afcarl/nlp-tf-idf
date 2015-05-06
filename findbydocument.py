# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from tfidf import *
from heapq import nlargest
from math import sqrt

def cosine_distance(document_a, document_b):
  distance = 0.
  for word in document_a:
    if word in document_b:
      distance += document_a[word] * document_b[word]
  distance /= sqrt(sum([x*x for x in document_a.values()]))
  distance /= sqrt(sum([x*x for x in document_b.values()]))
  return distance

def findbydocument(tfidf, document_id, limit=5):
  my_document = tfidf[document_id]

  max_list = []
  for document_key in tfidf:
    document = tfidf[document_key]
    max_list.append((document_key, cosine_distance(my_document, document)))
  return nlargest(limit, max_list, key=lambda e:e[1])

if __name__ == '__main__':
  if len(sys.argv) >= 4:
    corpus_file = sys.argv[1]
    synonyms_file = sys.argv[2]
    word = unicode(sys.argv[3], "utf-8")
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10

    synonyms = create_synonyms_dictionary(synonyms_file)
    notes, BOWs = count_tf(corpus_file, synonyms)
    idf = count_idf(BOWs)
    tfidf = count_tfidf(BOWs, idf)

    documents = findbydocument(tfidf, word, limit)
    for document in documents:
      print(document[0] + " : " + str(document[1]))

  else:
    print("python findbydocument.py [corpus] [synonyms] [document_id] [limit]")
