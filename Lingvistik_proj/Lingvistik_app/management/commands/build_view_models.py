
from django.core.management.base import BaseCommand
import nltk
import re
from schemdraw import config
import spacy
from pathlib import Path
import pandas as pd
from huggingface_hub import login
from datasets import load_dataset, get_dataset_config_names, concatenate_datasets
from ... models import ParsedSentence
from .statsservices.handle_useing_spacy import use_spacy_for_text_processing
from .statsservices.handle_corpus_building import handle_gutenberg_corpora_build
from .statsservices.texthandling import clean_text, remove_filetype
from .statsservices.meaning import apply_values_to_sentences

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      #------TEST FASE START BY empy records thats visualizes sentenses
      objects_in_database = ParsedSentence.objects.all()
      
      print(f"Current number of Objects in ParsedSentence database to use for views and templates: {len(objects_in_database)}")
  

         
      self.stdout.write(self.style.SUCCESS('Successfully run of building models for views and templates .'))







# # #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats