import nltk
from nltk.corpus import gutenberg
from nltk.corpus.reader import PlaintextCorpusReader

def handle_gutenberg_corpora_build(MY_CORPUS_PATH, language):
   gutenberg = nltk.corpus.gutenberg   
      
   my_gutenberg = PlaintextCorpusReader(
      str((MY_CORPUS_PATH)),
      r".*\.txt",
      encoding="utf-8"
   )
      
      #Metadata for initial works nltk_works
   works = [
      {
           "corpus": gutenberg,
           "fileid": fileid,
           "source": "NLTK Gutenberg",
           "language":  language,
      }
      for fileid in gutenberg.fileids()
   ]
    
      #add works from my_gutenberg
   works += [
      {
         "corpus": my_gutenberg,
         "fileid": fileid,
         "source": "Project Gutenberg",
         "language": language,
      }
         for fileid in my_gutenberg.fileids()
      ]
   return works, my_gutenberg