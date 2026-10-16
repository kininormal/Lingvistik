
from django.core.management.base import BaseCommand
import spacy
from pathlib import Path
import pandas as pd

from ... models import  ParsedSentence,  LemmaSentence, PreviousSentence, FollowingSentence, Lemma

from .statsservices.handle_useing_spacy import record_lemmas

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
   
      
      BASE_DIR = Path(__file__).resolve().parents[4] 
      nlp_en = spacy.load("en_core_web_sm")
      #Get ParsedSentence record content to meke records able to make desired views
      sentence_context_objects = ParsedSentence.objects.all()
      print("Number of Sentence to build models for views: ", len(sentence_context_objects ) )
      #TEST FASE - START BY empty records for views and templates
      LemmaSentence.objects.all().delete()
      #check
      records = LemmaSentence.objects.all()
      print("TEST FASE Number of lemma sentence records from works are  initilized to: ", len(records) )
    
         #create records relating  lemma sentence, previous and following 
      createSentenceRecords(sentence_context_objects )
    
      lemma_sentence_records = LemmaSentence.objects.all()
      print(f"There was created :{len(lemma_sentence_records)} lemma records")
      
      
   
      for lemma_sentence in  lemma_sentence_records:
         createLemmaRecords(lemma_sentence, nlp_en) 
      #    #createWordRecords(lemma_sentence)
      
      records = LemmaSentence.objects.all()
      
      
      for record in records:
         lemma_sentence_id = record.findingID
         lemma_sentence = record.lemma_sentence
         
         prev_obj = getattr(record, 'previous_sentence', None)
         fol_obj = getattr(record, 'following_sentence', None)
         
         
         #print(f"lemma sentence with ID: {lemma_sentence_id }\n Has content :{lemma_sentence} \nPrevious sentence { prev_obj.previous_sentence}\n And following  sentence { fol_obj.following_sentence}")
                  
         
         lemma_lemmas = record.analysis_focus.all()
         previous_lemmas = prev_obj.previous.all()
         following_lemmas  = fol_obj.following.all()
         
         print(f"There is {len(lemma_lemmas)} lemmas in lemma sent PREV had {len(previous_lemmas)}  follow had {len(following_lemmas)}")
        
            
      # print(f"There is {len(lemma_lemmas)} lemmas in lemma sent and {len(previous_lemmas)} lemmas in previous and {len(following_lemmas)} in follow")
         
      
      # print("For views in test face the Number of Sentence records from works are: ", len(records) )
     
      
      self.stdout.write(self.style.SUCCESS('Successfully EMPTY IN TEST FASE run of building models for views and templates .'))

def createSentenceRecords(sentenceCtxObjects):

   for sentence_object in  sentenceCtxObjects:
      # handle objects in ParsedSentence to be recorded in LemmaSentenceContext
      lemma_sentence_id= sentence_object.findingID
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
      following_sentence = sentence_object.follow_sentence 
      if following_sentence != None:
         following_sentence = following_sentence
      else:
         following_sentence = '' #lemma in last sentence so no following sentence
         
      # Then record  as LemmaSentence, with related PreviousSentence. FollowingSentence
      lemma_sentence_record = LemmaSentence.objects.create(findingID = lemma_sentence_id,
                                                            lemma = sentence_object.lemma ,
                                                         lemma_sentence  = lemma_sentence,)
      previous_sentence_record = PreviousSentence.objects.create(previous_sentence   = previous_sentence,
                                                               lemma_sentence_for_previous = lemma_sentence_record,)
      following_sentence_record = FollowingSentence.objects.create(following_sentence   = following_sentence,
                                                                     lemma_sentence_for_following  = lemma_sentence_record,)
      


def createLemmaRecords(lemma_sentence_obj, nlp_lang):

   prev_obj = getattr(lemma_sentence_obj, 'previous_sentence', None)
   fol_obj = getattr(lemma_sentence_obj, 'following_sentence', None)
   
   
   text =  lemma_sentence_obj.lemma_sentence
   lemma =  lemma_sentence_obj.lemma
   # ----------------------------------
   # Process text with spaCy
   # ----------------------------------
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)
   #ensure that designation is lower case
   designation =  lemma.lower()
   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
         # Find lemma matching the designation
         if token.lemma_.lower() == designation:
            position = token.i
            
            lemmaa_record = Lemma.objects.create(lemma = designation, 
                                             lemma_position = position,
                                             lemmasentence=lemma_sentence_obj,
                                          )
      #lemmas in prev_obj
      text = prev_obj.previous_sentence
      nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
      doc = nlp_lang(text)
      for sent in doc.sents:
         # Loop through tokens in sentence
         for token in sent:
            # Find lemma matching the designation
            if token.lemma_.lower() == designation:
               position = token.i
               
               lemmaa_record = Lemma.objects.create(lemma = designation, 
                                                lemma_position = position,
                                                previoussentence= prev_obj,
                                             )
      #lemmas in following _obj
      text = fol_obj.following_sentence
      nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
      doc = nlp_lang(text)
      for sent in doc.sents:
         # Loop through tokens in sentence
         for token in sent:
            # Find lemma matching the designation
            if token.lemma_.lower() == designation:
               position = token.i
               
               lemmaa_record = Lemma.objects.create(lemma = designation, 
                                                lemma_position = position,
                                                followingsentence= fol_obj,
                                             )

   #          prev_obj.previous_sentence
   #          fol_obj.following_sentence
   #          print(f"To concider previous { prev_obj.previous_sentence} and following {fol_obj.following_sentence}")

def createWordRecords(lemma_sentence):
   print(f"lemma sentence with id:{lemma_sentence.findingID} has {lemma_sentence.words_in_lemma_sentence} words")
   previous_sentence_record = lemma_sentence.previoussentence 
   print(f"The previous  sentence is :{previous_sentence_record.previous_sentence} and has {previous_sentence_record.words_in_previous_sentence} words")
   following_sentence_record = lemma_sentence.followingsentence 
   print(f"The Following sentence is :{following_sentence_record.following_sentence} and has {following_sentence_record.words_in_following_sentence} words")

               
# # # #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats