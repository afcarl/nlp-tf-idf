# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from tfidf import *

if __name__ == '__main__':
  if len(sys.argv) >= 4:
    corpus_file = sys.argv[1]
    synonyms_file = sys.argv[2]
    keyword = unicode(sys.argv[3], "utf-8")

    synonyms = create_synonyms_dictionary(synonyms_file)
    notes, BOWs = count_tf(corpus_file, synonyms)
    idf = count_idf(BOWs)
    tfidf = count_tfidf(BOWs, idf)
    key_words = get_key_words(tfidf, keyword)

    for items in key_words:
      print(items[0] + " : " + str(items[1]))

  else:
    print("python keywords.py [corpus] [synonyms] [keyword]")
