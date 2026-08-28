#about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/python manage.py stats
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
      #add english to language_df
      language_df  = update_english_data(language_df, 'english')
      #add danish 
      update_danish_data(language_df, 'danish') 
         
      self.stdout.write(self.style.SUCCESS('Successfully updated language data - just initial start.'))
def  update_english_data(df, lang):
   
   #Build basis for english language data
   
   #English sets version one
   source = 'gutenberg'
   name_of_work = 'austen-emma.txt'
   nltk.corpus.gutenberg.fileids()
   #Test working before building data and functions
   emma = nltk.corpus.gutenberg.words(name_of_work)
   print(len(emma))
   print(type(emma))

   body_part = 'head'

    # Create NLTK Text object
   emma_txt = nltk.Text(emma)

   # Find all concordances
   concordances = emma_txt.concordance_list(body_part)

   # Build rows for dataframe
   data = []

   for concordance in concordances:
         text = ' '.join(concordance.left) + ' ' \
               + concordance.query + ' ' \
               + ' '.join(concordance.right)
         data.append([
            text,
            body_part,
            lang,
            source,
            name_of_work
         ])

   # Create dataframe
   new_data = pd.DataFrame(
      data,
         columns=[
            'Text',
            'Body part',
            'Language',
            'Source',
            'Name_of_work'
         ]
   )

   # Add new observations to existing dataframe
   df = pd.concat([df, new_data], ignore_index=True)

   print('Head of df with attributes:')
   print(df.head())

   print("English language data updated!")

   return df
def update_danish_data(df, lang):
   #Build basis for danish language data
   # Implement the logic to update Danish language data here
   #Danish sets
   sampleLst = []
   name = "danish-foundation-models/danish-gigaword"
   danish_set= load_dataset(name, split = "train")
   sample = danish_set[1] # see "Data Instances" below
   print(sample.keys())
   print(sample["text"][:300])
   
   #Take first 10
   sampleLst = list(danish_set.take(10))  # 10 første elementer
   body_part ='head'
   for memberNr, sampleMember in enumerate(sampleLst):
      words = nltk.word_tokenize(sampleMember["text"], language=lang)
      text_obj = nltk.Text(words)
      print(f"--- Sample {memberNr} ---")
      text_obj.concordance(body_part)


   print("Danish language data updated! - no implementation yet  testing it seems to work danis not handled")
