#about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/         #about manage.py stats
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
         
         
      print('Language df after updates - more languages full update ONLY ENGLISH SO FAR:')
      rows, columns = language_df.shape
      print(f"Rows in main function:  {rows}")
      print("First rows")
      print( language_df.head())
      print("Last rows")
      print( language_df.tail())
         
      self.stdout.write(self.style.SUCCESS('Successfully updated language data - just initial start.'))
def  update_english_data(df, body_name, body_category, lang, nlp_lang):
   #BASE_DIR = Path(__file__).resolve().parent
   
   # nltk known (allowd) paths
   for path in nltk.data.path:
      p = Path(path)
      print('allowed knowen paht PlaintextCorpusReader promlem ') 
      print(p, "→", p.exists())
      print('nlkt paths')
      print(nltk.data.path)
   
   BASE_DIR = Path(__file__).resolve().parents[3]
   source = 'gutenberg'
   GUTENBERG_PATH = BASE_DIR /'data'/'gutenberg'
   my_gutenberg = PlaintextCorpusReader(
      str(GUTENBERG_PATH),
      r".*\.txt"
   )
   print("MY works from gutenberg")
   print(my_gutenberg.fileids())
   #work in gutenberg in fileids
   file_ids = nltk.corpus.gutenberg.fileids()
   print('number of works in gutenberg', len(file_ids))

   for fileindex in range(0, 2):
      name_of_work = file_ids[fileindex]
      print(f"Valgt værk: {name_of_work}")
      # ----------------------------------
      # Build basis for English language data
      # ----------------------------------

      df = handle_current_vork(df,source, name_of_work, body_name, body_category, lang, nlp_lang)
   
   rows, columns = df.shape
   print(f"Rows in function for english:  {rows}")
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



def handle_current_vork(df, source, name_of_work, body_name, body_category, lang, nlp_lang):
    # ----------------------------------
      # Load raw text from NLTK Gutenberg
      # ----------------------------------
   
      raw_text = nltk.corpus.gutenberg.raw(name_of_work)
   
      # ----------------------------------
      # Process text with spaCy
      # ----------------------------------
   
      doc = nlp_lang(raw_text)
   
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
   