#about stats.py: dir       #about manage.py stats
import csv

from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
import nltk
from schemdraw import config
import spacy
from pathlib import Path
import pandas as pd
from huggingface_hub import login
import datasets
from datasets import load_dataset, get_dataset_config_names, concatenate_datasets

from .statsservices.handle_useing_spacy import use_spacy_for_text_processing
from .statsservices.handle_corpus_building import handle_gutenberg_corpora_build
from .statsservices.texthandling import clean_text

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
      nlp_en = spacy.load("en_core_web_sm")
      nlp_da = spacy.load("da_core_news_sm")
      # You can specify the quality parameter here or get it from args/kwargs
      #create empty language_df
      language_df = pd.DataFrame()
      
          
      ################# Template for next version - not used yet - but could be used to create a more structured approach to the lexicon and translations
      #       from dataclasses import dataclass, field

      # @dataclass
      # class TermConcept:
      #     category: str
      #     translations: dict[str, str]  # fx {'en': 'head', 'da': 'hoved', 'de': 'kopf'}

      # # Samling af alle koncepter
      # lexicon = [
      #     TermConcept(category='body part', translations={'en': 'head', 'da': 'hoved', 'de': 'kopf'}),
      #     TermConcept(category='body part', translations={'en': 'foot', 'da': 'fod', 'de': 'fuß'}),
      #     TermConcept(category='sensory',   translations={'en': 'smell', 'da': 'lugt', 'de': 'geruch'}),
      #     TermConcept(category='organ',     translations={'en': 'heart', 'da': 'hjerte', 'de': 'herz'}),
      # ]

      # def get_terms_for_language(lexicon, lang='en'):
      #     """Uddrager ordbog til et specifikt sprog: {lokalt_ord: kategori}"""
      #     return {
      #         concept.translations[lang]: concept.category 
      #         for concept in lexicon 
      #         if lang in concept.translations
      #     }

      # # Generer automatisk listen til dansk NLP-kørsel
      # da_terms = get_terms_for_language(lexicon, 'da')
      # # Resultat: {'hoved': 'body part', 'fod': 'body part', 'lugt': 'sensory', 'hjerte': 'organ'}
      ##########
      
      list_of_names  = [ ['head', 'body part'], ['foot', 'body part' ], ['smell', 'sensory'], ['heart', 'organ'], ['eye', 'body part'], 
                        ['ear', 'body part'], ['nose', 'body part'], ['mouth', 'body part'], ['hand', 'body part'], ['arm', 'body part'], 
                        ['leg', 'body part'], ['brain', 'organ'], ['liver', 'organ'], ['kidney', 'organ'], ['gut', 'organ'],
                        ['stomach', 'organ'], ['lung', 'organ']]
      for part in list_of_names[:1]: #test with only two works for now -with two body names head and foot
         designation = part[0]
         body_category = part[1]
         #for every designation and body_category create a new language_df with english and danish data
         language_df = None
         #add english text from corpus to language_df
         language_df  = update_english_data(language_df, designation, body_category, 'English',  nlp_en)
         #add danish text from corpus to language_df
         # designation are in english - Tenplate for next version - not used yet - but could be used to create a more structured approach to the lexicon and translations
         #update_danish_data(language_df, designation, body_category, 'danish') focus on engisk soo far
         
         
      print('Language df after updates -  ONLY ENGLISH ONLY two works SO FAR:')
      rows, columns = language_df.shape
      print(f"Rows in main function:  {rows}")
      print("First rows in main function:")
      print( language_df.head())
      print("Last rows in main function:")
      print( language_df.tail())
         
      self.stdout.write(self.style.SUCCESS('Successfully updated language data - just initial start.'))
def  update_english_data(df, designation, body_category, language, nlp_lang): #LOOK at 'clean up' lang is here but then set later in work loop - should be set in function and not in loop - but for now it is set in loop
  
   BASE_DIR = Path(__file__).resolve().parents[4] #go to Lingvistik from Lingvistik_proj/Lingvistik_app/management/commands/stats.py, 4 levels to 
   map_name_for_sources = 'corpora/gutenberg/'
   MY_CORPUS_PATH = BASE_DIR / map_name_for_sources
   #Allow the path of MY_CORPUS_PATH for PlaintextCorpusReader
   nltk.data.path.append(str(MY_CORPUS_PATH)) #DO NOT USE allowed NLTK_PATH in allowed virtual environment map - Works from NLTK are then "lost" and not found by PlaintextCorpusReader - only works for nltk.corpus.gutenberg
   
   works, my_gutenberg = handle_gutenberg_corpora_build(MY_CORPUS_PATH, language)
   
  
   #loop though works and process each work   
   for work in works[:1]: #can be limited to n works with works[:n] does it wok outside NTLK 18 works and 12 works from my_gutenberg - total 30 works - can be limited to n works with works[:n] does it wok outside NTLK 18 works and 12 works from my_gutenberg - total 30 works
      # ----------------------------------
      # Build basis for English language data for current work
      # ----------------------------------
      df = handle_current_english_work(df,my_gutenberg, work, designation, body_category, nlp_lang)
      #fileid source and language  are knowen in work
    
      
   
   #export to excel
   rows, columns = df.shape
   print(f"Rows in function for english ALL handled works:  {rows}")
   print("English language data updated!")
   return df
def update_danish_data(df,  designation, body_category, lang):
   print("Starting to update Danish language data...")
   dataset_name = "danish-foundation-models/danish-gigaword"
   configs = get_dataset_config_names(dataset_name)

   # 2. Loop igennem og hent "train"-splittet for hver kilde
   all_data = {}
   for config in configs:
      # Vi springer 'default' over, hvis du vil hente de specifikke kilder rent
      if config == "default":
         continue
      all_data[config] = load_dataset(dataset_name, name=config, split="train")
      
   print(f"Fetched {len(all_data)} subsets from the Danish Gigaword dataset.")
   # Samler alle de hentede subsets til ét stort datasæt
   full_danish_gigaword = concatenate_datasets(list(all_data.values()))
   print(f"Total number of samples in full Danish Gigaword dataset: {len(full_danish_gigaword)}")
   
   #Build basis for danish language data
   # Implement the logic to update Danish language data here
   #Danish sets
   sampleLst = []
   danish_set = load_dataset(dataset_name, split = "train")
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
      text_obj.concordance(designation)


   print("Danish language data updated! - no implementation yet  testing it seems to work danis not handled")



def handle_current_english_work(df, my_gutenberg, work, designation, body_category, nlp_lang):
   source = work["source"]
   lang = work["language"]
   name_of_work = work["fileid"]
   # ----------------------------------
   # Clean text according to Gutenberg corpus
   # ----------------------------------
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
   # Process text with spaCy
   # ----------------------------------
   data = use_spacy_for_text_processing(text, name_of_work, source, designation, body_category, lang, nlp_lang)
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
      designation + '_lingvistik.xlsx',
      index=False
   )

   print('Head of df with attributes in function:')
   print(df.head())
   return df
