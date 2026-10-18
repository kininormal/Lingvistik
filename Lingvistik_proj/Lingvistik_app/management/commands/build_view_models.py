
from django.core.management.base import BaseCommand
import spacy
from pathlib import Path
import pandas as pd

from ... models import  ParsedSentence,  LemmaSentence, PreviousSentence, FollowingSentence, Lemma, Word

from .statsservices.handle_useing_spacy import record_lemmas

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
     
   
      
      BASE_DIR = Path(__file__).resolve().parents[4] 
      
      # Load English spaCy model
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
         createWordRecords(lemma_sentence, nlp_en)
      
      records = LemmaSentence.objects.all()
      
   
         
      print(f"There are {len(records)} lemma records after createLemmaRecords and reateWordRecords")
      
      
      total_lemmas = Lemma.objects.all()
      print(f"There are a total of  {len( total_lemmas)}  Lemma records after createLemmaRecords and createWordRecords")
        
        
      total_words_for_analysis = Word.objects.all()
      print(f"There are a total of  {len(total_words_for_analysis)}  Word records after createWordRecords and createLemmaRecord")
      
      # lemma_sentence_objs = LemmaSentence.objects.all()
               
                  

      
      
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
   #check tat the code wors before reducing
   #lemma sentence
   text =  lemma_sentence_obj.lemma_sentence
   lemma =  lemma_sentence_obj.lemma
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
                                             lemmasentencelemmas =lemma_sentence_obj,
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
                                                previoussentencelemmas = prev_obj,
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
                                                followingsentencelemmas = fol_obj,
                                             )

   

def createWordRecords(lemma_sentence_obj, nlp_lang):
   #check tat the code wors before reducing
   allowed_pos = {"ADJ", "NOUN", "VERB", "ADV", "PRON", "DET", "ADP", "CONJ", "NUM", "PART", "INTJ"}
   prev_obj = getattr(lemma_sentence_obj, 'previous_sentence', None)
   fol_obj = getattr(lemma_sentence_obj, 'following_sentence', None)
   #words in lemma sentence
   text =  lemma_sentence_obj.lemma_sentence
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)

  
   for sent in doc.sents:
    for token in sent:
       # Spring over, hvis det er decideret tegnsætning eller mellemrum
        if token.is_punct or token.is_space:
            continue
            
        wordclass = token.pos_ if token.pos_ in allowed_pos else "X"
        
        Word.objects.create(
            word=token.text,
            position=token.i,
            wordclass=wordclass,
            lemmasentencewords = lemma_sentence_obj, # relate to lemma sentence
        )
   
   #words previous sentence
   text = prev_obj.previous_sentence
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)

   for sent in doc.sents:
      for token in sent:
         #Spring over, hvis det er decideret tegnsætning eller mellemrum
         if token.is_punct or token.is_space:
            continue
  
         wordclass = token.pos_ if token.pos_ in allowed_pos else "X"
         
         Word.objects.create(
            word = token.text,  # Brug token.text (eller token.text_with_ws) til databasefelter
            position = token.i,
            wordclass = wordclass,
            previoussentencewords = prev_obj, # relate to previous sentence
         )    
   #words following sentence
   text = fol_obj.following_sentence
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)

   for sent in doc.sents:
      for token in sent:
         # Spring over, hvis det er decideret tegnsætning eller mellemrum
         if token.is_punct or token.is_space:
            continue
         # Tjek om ordklassen er tilladt, ellers sæt til 'X'
         wordclass = token.pos_ if token.pos_ in allowed_pos else "X"
         
         Word.objects.create(
            word=token.text,  # Brug token.text (eller token.text_with_ws) til databasefelter
            position=token.i,
            wordclass=wordclass,
            followingsentencewords = fol_obj, # relate to following sentence
         )    
   
   

               
# # # #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats