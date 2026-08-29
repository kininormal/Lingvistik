#about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/         #about manage.py stats
from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from huggingface_hub import login
import datasets
from datasets import load_dataset
class Command(BaseCommand):
    help = 'Update data basis'

    def handle(self, *args, **kwargs):
      # You can specify the quality parameter here or get it from args/kwargs
      #create empty language_df
      language_df = pd.DataFrame()
      #add english text from corpus to language_df
      language_df  = update_english_data(language_df, 'english')
      #add danish text from corpus to language_df
      update_danish_data(language_df, 'danish') 
         
      self.stdout.write(self.style.SUCCESS('Successfully updated language data - just initial start.'))
def  update_english_data(df, lang):
   
   #Build basis for english language data
   
   #English sets version one
   source = 'gutenberg'
   name_of_work = 'austen-emma.txt'
   #fileids() contain name of works
   nltk.corpus.gutenberg.fileids()
  
   #Test working before building data and functions
   emma = nltk.corpus.gutenberg.words(name_of_work)

    # Create NLTK Text object
   emma_txt = nltk.Text(emma)
   
   #clean up  emma_txt for nlp use 1) lower case 2) remove any html tags 2) remove url 3) remove string.punctuation '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' 4) 3) remove abbreviations replace with full ASP and ASAP':'As Soon As Possible',
   # 'FAQ': 'Frequently Asked Questions', etc 4) Lemmatization (find eg occurrences of both head and heads when seach for body_name = 'head'
   #ALL CODDE MISSING 
  
  
   body_name = 'head'
   body_category = 'body part'
  
  
   # Find all concordances
   #concordances = emma_txt.concordance_list(body_name)
   concordances =  emma_txt .concordance_list(body_name)
   # Build rows for dataframe
   data = []

   for concordance in concordances:
         text = ' '.join(concordance.left) + ' ' \
               + concordance.query + ' ' \
               + ' '.join(concordance.right)
         data.append([
            text,
            body_name,
            body_category,
            lang,
            source,
            name_of_work
         ])

   # Create dataframe
   new_data = pd.DataFrame(
      data,
         columns=[
            'Text',
            'Body name',
            'Body category',
            'Language',
            'Source',
            'Name of work'
         ]
   )

   # Add new observations to existing dataframe
   df = pd.concat([df, new_data], ignore_index=True)
   # chech that i can get a file output, in text so cvs will not work as 
   df.to_excel('lingv.xlsx')
   print('Head of df with attributes:')
   print(df.head())

   print("English language data updated!")
   
   #return the df so I can append eg danish to the dataframe

   return df
def update_danish_data(df, lang):
   #Build basis for danish language data
   # Implement the logic to update Danish language data here
   #Danish sets
   sampleLst = []
   name = "danish-foundation-models/danish-gigaword"
   danish_set= load_dataset(name, split = "train")
   sample = danish_set[1] # see "Data Instances" below
   print('danish set index 1 keys', sample.keys())
   print('danish text index 1', sample["text"][:500])
   #next_sample  = danish_set[2]
   #print('danish set index 2 keys', next_sample.keys())
   #print('danish text index 2', next_sample["text"][:500])
   #Take first 10
   sampleLst = list(danish_set.take(100))  # 100 første elementer
   body_part ='head'
   for memberNr, sampleMember in enumerate(sampleLst):
      words = nltk.word_tokenize(sampleMember["text"], language=lang)
      text_obj = nltk.Text(words)
      print(f"--- Sample {memberNr} ---")
      text_obj.concordance(body_part)


   print("Danish language data updated! - no implementation yet  testing it seems to work danis not handled")



def nlp_handle_text(txt):
   #lower case
   text = txt.lower()
   #remove html
   text = remove_html_tags(text)

   return text

def remove_html_tags(text):
   import re
   pattern = re.compile('<.*?>')
   return pattern.sub(r'', text) #replace with empty string