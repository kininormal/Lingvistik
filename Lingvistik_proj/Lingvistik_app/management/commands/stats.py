from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
import nltk
from huggingface_hub import logipythonn
#import datasets
from datasets import load_dataset
class Command(BaseCommand):
    help = 'Update data basis'

    def handle(self, *args, **kwargs):
      # You can specify the quality parameter here or get it from args/kwargs
       
      update_english_data()
      #update_danish_data() #comming update_danish_data()
         
      self.stdout.write(self.style.SUCCESS('Successfully updated diamond and iris plots in the database.'))
def  update_english_data():
   
   #English sets version one
   nltk.corpus.gutenberg.fileids()
   #Test working before building data and functions
   emma = nltk.corpus.gutenberg.words('austen-emma.txt')
   print(len(emma))
   print(type(emma))


   emma_txt = nltk.Text(emma)
   emma_txt.concordance('head') 
   
   print("English language data updated!- no implementation yet testing it seems to work") 
def update_danish_data():
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

   for memberNr, sampleMember in enumerate(sampleLst):
      words = nltk.word_tokenize(sampleMember["text"], language="danish")
      text_obj = nltk.Text(words)
      print(f"--- Sample {memberNr} ---")
      text_obj.concordance("hoved")


   print("Danish language data updated! - no implementation yet  testing it seems to work")
