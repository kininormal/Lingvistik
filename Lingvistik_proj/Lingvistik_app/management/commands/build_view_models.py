
from django.core.management.base import BaseCommand
import spacy
from pathlib import Path
import pandas as pd

from ... models import  ParsedSentence, LemmaSentence, PreviousSentence, FollowingSentence

from .statsservices.meaning import apply_values_to_sentences

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
      nlp_en = spacy.load("en_core_web_sm")
      
      BASE_DIR = Path(__file__).resolve().parents[4] 
      #All sentences 
      sentence_objects = ParsedSentence.objects.all()
      print("Number of Sentence to build models for views: ", len(sentence_objects) )
      #TEST FASE - START BY empty records for views and templates
      LemmaSentence.objects.all().delete()
      #check
      records = LemmaSentence.objects.all()
      print("TEST FASE Number of lemma sentence records from works are  initilized to: ", len(records) )
      
      #ParsedSentence record to analytical context records
         #create records relating  lemma sentence, previous and following 
      createRecordsOfLemmaSentenceContext(sentence_objects) 
      #get all record lemma sentences as "anchor"
      lemma_sentence_records =  LemmaSentence.objects.all()
      print(f"A record with {len(lemma_sentence_records)} lemma sentences was created")
      for lemma_sentence in  lemma_sentence_records:
         print(f"lemma sentence with id:{lemma_sentence.findingID} has {lemma_sentence.words_in_lemma_sentence} words")
         previous_sentence_record = lemma_sentence.previoussentence 
         print(f"The previous  sentence is :{previous_sentence_record.previous_sentence} and has {previous_sentence_record.words_in_previous_sentence} words")
         following_sentence_record = lemma_sentence.followingsentence 
         print(f"The Following sentence is :{following_sentence_record.following_sentence} and has {following_sentence_record.words_in_following_sentence} words")
      
      
      
      print("For views in test face the Number of Sentence records from works are: ", len(records) )
     
      
      self.stdout.write(self.style.SUCCESS('Successfully EMPTY IN TEST FASE run of building models for views and templates .'))


def createRecordsOfLemmaSentenceContext(sentence_records):
   for sentence_object in sentence_records:
      lemma_sentence_id = sentence_object.findingID
      lemma_sentence = sentence_object.sentence
      if  lemma_sentence != None:
         lemma_sentence = lemma_sentence
      else: 
         lemma_sentence = 'SOMETHING IS ROTTEN MUST BE LEMMA'
      previous_sentence =  sentence_object.prev_sentence
      if  previous_sentence != None:
         previous_sentence = previous_sentence
      else:
         previous_sentence = ''  #lemma in first sentence so no previous sentence
      following__sentence = sentence_object.follow_sentence  
      if following__sentence != None:
         following__sentence = following__sentence
      else:
         following__sentence = '' #lemma in last sentence so no following sentence
         
      lemma_sentence_record = LemmaSentence.objects.create(findingID = lemma_sentence_id,
                                                         lemma_sentence  = lemma_sentence,)
      previous_sentence_record = PreviousSentence.objects.create(previous_sentence   = previous_sentence,
                                                               sentence_for_previous_id = lemma_sentence_record,)
      following_sentence_record = FollowingSentence.objects.create(following_sentence   = following__sentence,
                                                                  sentence_for_following_id = lemma_sentence_record,)
      return 


               
# # # #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats