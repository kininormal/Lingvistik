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
   
   map_name_for_sources = 'corpora/gutenberg/'
   #Allowe the path for PlaintextCorpusReader
   MY_CORPUS_PATH = BASE_DIR / map_name_for_sources
   nltk.data.path.append(str(MY_CORPUS_PATH)) #DO NOT USE allowed NLTK_PATH in virtual environment - Works from NLTK are then "lost" and not found by PlaintextCorpusReader - only works for nltk.corpus.gutenberg
   
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
  
   #loop though works and process each work   
   for work in works[:2]: #testing with first 2 works
      corpus = work["corpus"]
      fileid = work["fileid"]

      text = corpus.raw(fileid)

      source = work["source"]
      language = work["language"]
      
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


def handle_current_english_work(df, my_gutenberg, source, name_of_work, body_name, body_category, lang, nlp_lang):
  
   # Check source Then handle  Clean text according to Gutenberg corpus (NLKT often adds \r to \n, and my_gutenberg may have different formatting)  
   if source == "NLTK Gutenberg":   
           
      raw_text = nltk.corpus.gutenberg.raw(name_of_work)          
      text = clean_text(raw_text)
   elif source == "Project Gutenberg":          
       
      raw_text =  my_gutenberg.raw(name_of_work)          
      text = clean_text(raw_text)
   else:          
      print(f"PROBLEM: Unknown source: {source}. Skipping work: {name_of_work}")        
      return df  # Skip processing for unknown sources
   
   # ----------------------------------
   # Clean text according to Gutenberg corpus
   # ----------------------------------
   
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
   text = text.replace("_", " ") # eg jame ausin uses _ insted of blank to indicate words said with litte pause between them in some works
   text = text.replace("--", "  ") # eg jame ausin uses --  to indicate renovation pause
   # Alle former for linjeskift erstattes med mellemrum
   text = text.replace("\n", " ")

    # Flere whitespace-tegn reduceres til ét mellemrum
   text = re.sub(r"\s+", " ", text)
  
   return text.strip()