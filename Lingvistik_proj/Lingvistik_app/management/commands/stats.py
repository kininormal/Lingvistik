#about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/         #about manage.py stats
import csv

from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
import nltk
import spacy
from pathlib import Path
import pandas as pd
from huggingface_hub import login
import datasets
from datasets import load_dataset
from nltk.corpus import gutenberg
from nltk.corpus.reader import PlaintextCorpusReader
import re

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
      nlp_en = spacy.load("en_core_web_sm")
      nlp_da = spacy.load("da_core_news_sm")
      # You can specify the quality parameter here or get it from args/kwargs
      #create empty language_df
      language_df = pd.DataFrame()
      #list_of_names  = [ ['head', 'body part'], ['foot', 'body part' ], ['heart', 'organ']] #tested works
      list_of_names  = [ ['head', 'body part']]
      for part in list_of_names:
         body_name = part[0]
         body_category = part[1]
      
         print(f"Searce tex for:  {body_name} with category {body_category}")
         #add english text from corpus to language_df
         language_df  = update_english_data(language_df, body_name, body_category, 'english',  nlp_en)
         #add danish text from corpus to language_df
         #update_danish_data(language_df, body_name, body_category, 'danish') 
         
         
      print('Language df after updates -  ONLY ENGLISH ONLY two words  SO FAR:')
      rows, columns = language_df.shape
      print(f"Rows in main function:  {rows}")
      print("First rows in main function:")
      print( language_df.head())
      print("Last rows in main function:")
      print( language_df.tail())
         
      self.stdout.write(self.style.SUCCESS('Successfully updated language data - just initial start.'))
def  update_english_data(df, body_name, body_category, lang, nlp_lang):
  
   BASE_DIR = Path(__file__).resolve().parents[4] #go to project root to access allowed Lingvistik_env/nltk_data/corpora/gutenberg for PlaintextCorpusReader
   print(BASE_DIR)
   source = 'gutenberg'
   NLTK_PATH_PART= 'Lingvistik_env/nltk_data/corpora/'
   NLTK_PATH_PART =  NLTK_PATH_PART + source
   GUTENBERG_PATH = BASE_DIR / NLTK_PATH_PART #allowed path for PlaintextCorpusReader
   
   file_ids = nltk.corpus.gutenberg.fileids()
   print('number of works in gutenberg', len(file_ids))
   nltk_works = [
     (gutenberg, fileid)
     for fileid in gutenberg.fileids()
   ]
   

   my_gutenberg = PlaintextCorpusReader(
      str(GUTENBERG_PATH),
      r".*\.txt",
      encoding="utf-8"
   )
   
   #WORKING TESTS - to identify problems with the text files in the my_gutenberg corpus
   # #Test 2 two identify charater problems in the text - it seems to be a problem with the encoding of the text file. The text file is encoded in UTF-8, but it contains some characters that are not valid UTF-8 characters. This can happen if the text file was created on a different platform or with a different encoding. To fix this, you can try to read the file with a different encoding, such as 'latin-1' or 'cp1252', which are more permissive and can handle a wider range of characters. You can also try to clean the text by removing or replacing invalid characters before processing it.
   # file_path = GUTENBERG_PATH / "Mansfield Park.txt"

   # # Test 2.1 – almindelig Python
   # with open(file_path, "r", encoding="utf-8") as file:
   #        text_python = file.read()

   # print("PYTHON:")
   # print(text_python[2500:5000])
   
   # cleaned_text_python = clean_text(text_python)
   # print("PYTHON cleaned:")
   # print(cleaned_text_python[2500:5000])


   # # Test 2.2 – NLTK CorpusReader
   # text_nltk = my_gutenberg.raw("Mansfield Park.txt")

   # cleaned_text_nltk = clean_text(text_nltk)

   # print("\nNLTK:")
   # print(cleaned_text_nltk[2500:5000])
   # print("PYTHON with repr - gives hitten:")
   # print(repr(cleaned_text_python[2500:5000]))
   # print("\nNLTK with repr - gives hitten:")
   # print(repr(cleaned_text_nltk[2500:5000]))
   
   # my_works = [
   #  (my_gutenberg, fileid)
   #  for fileid in my_gutenberg.fileids()
   # ]
   
   #Metadata for initial works nltk_works
   works = [
     {
        "corpus": gutenberg,
        "fileid": fileid,
        "source": "NLTK Gutenberg",
        "language": "English",
    }
    for fileid in gutenberg.fileids()
   ]
   
   #add works from my_gutenberg
   works += [
    {
        "corpus": my_gutenberg,
        "fileid": fileid,
        "source": "Project Gutenberg",
        "language": "English",
    }
    for fileid in my_gutenberg.fileids()
]
   #print("MY works from gutenberg")
   #print(my_gutenberg.fileids())
   #work in gutenberg in fileids
   #all_works = nltk_works + my_works
   #for corpus, fileid in all_works:
    #  print(fileid)
   #loop though works and process each work   
   for work in works[:1]: #testing with first 1 works
      corpus = work["corpus"]
      fileid = work["fileid"]

      text = corpus.raw(fileid)

      source = work["source"]
      language = work["language"]
      #check if loop through works is correct before processing
      print(f"Processing work: {fileid} from source: {source} in language: {language}")
      print(f"Valgt værk: {fileid}")
      # ----------------------------------
      # Build basis for English language data for current work
      # ----------------------------------
      df = handle_current_english_work(df,my_gutenberg, source, fileid, body_name, body_category, lang, nlp_lang)
   
   #export to excel
   rows, columns = df.shape
   print(f"Rows in function for english ALL handled works:  {rows}")
   print("English language data updated!")
   return df
def update_danish_data(df,  body_name, body_category, lang):
   #Build basis for danish language data
   # Implement the logic to update Danish language data here
   #Danish sets
   sampleLst = []
   name = "danish-foundation-models/danish-gigaword"
   danish_set = load_dataset(name, split = "train")
   sample = danish_set[1] # see "Data Instances" below
   print('danish set index 1 keys', sample.keys())
   print('danish text index 1', sample["text"][:500])
   #next_sample  = danish_set[2]
   #print('danish set index 2 keys', next_sample.keys())
   #print('danish text index 2', next_sample["text"][:500])
   #Take first 10
   sampleLst = list(danish_set.take(100))  # 100 første elementer
   for memberNr, sampleMember in enumerate(sampleLst):
      words = nltk.word_tokenize(sampleMember["text"], language=lang)
      text_obj = nltk.Text(words)
      print(f"--- Sample {memberNr} ---")
      text_obj.concordance(body_name)


   print("Danish language data updated! - no implementation yet  testing it seems to work danis not handled")


#only works for my_gutenberg corpus - not for nltk gutenberg corpus
def handle_current_english_work(df, my_gutenberg, source, name_of_work, body_name, body_category, lang, nlp_lang):
    # ----------------------------------
      # Load raw text from NLTK Gutenberg
      # ----------------------------------
   
      raw_text =  my_gutenberg.raw(name_of_work)
      text = clean_text(raw_text)
      #Test if text is cleaned correctly
      print(f"Text from {name_of_work} after cleaning IN HANDLER:")
      print(text[2500:5000])
      
      
     

   
      
      
      # ----------------------------------
      # Process text with spaCy
      # ----------------------------------
   
      doc = nlp_lang(text)
   
      # ----------------------------------
      # Build rows
      # ----------------------------------
      data = []
   
      # Loop through sentences
      for sent in doc.sents:
         # Loop through tokens in sentence
         for token in sent:
            # Find lemma "head"
            if token.lemma_.lower() == body_name:
               data.append([
                  sent.text,
                  token.text,
                  token.lemma_,
                  body_name,
                  body_category,
                  lang,
                  source,
                  name_of_work
               ])
      
      # ----------------------------------
      # Create dataframe
      # ----------------------------------
      new_data = pd.DataFrame(
         data,
            columns=[
               'Text',
               'Found word',
               'Lemma',
               'Body name',
               'Body category',
               'Language',
               'Source',
               'Name of work'
            ]
      )
      
      # ----------------------------------
      # Append to existing dataframe
      # ----------------------------------
      df = pd.concat(
         [df, new_data],
         ignore_index=True
      )
   
      # ----------------------------------
      # Export
      # ----------------------------------
      df.to_excel(
         'lingvistik.xlsx',
         index=False
      )
   
      print('Head of df with attributes in function:')
      print(df.head())
      return df
def normalize_text(text):
    """Gør forskellige linjeskift ens."""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text
def clean_text(text):
   """Rydder linjeskift og retter almindelige UTF-8/Windows-1252
    encoding-fejl fra Gutenberg-tekst."""

   # Ret fejlfortolket UTF-8, hvis teksten er blevet læst som cp1252
   # try:
   #    text = text.encode("cp1252").decode("utf-8")
   # except (UnicodeEncodeError, UnicodeDecodeError):
   #    pass
   text = normalize_text(text)
    # Alle former for linjeskift erstattes med mellemrum
   text = text.replace("\n", " ")

    # Flere whitespace-tegn reduceres til ét mellemrum
   text = re.sub(r"\s+", " ", text)
  
   return text.strip()