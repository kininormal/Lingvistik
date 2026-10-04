
from django.core.management.base import BaseCommand
import spacy
from pathlib import Path
import pandas as pd

from ... models import ParsedSentence, SentenceInAnalyticalContext

from .statsservices.meaning import apply_values_to_sentences

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
      nlp_en = spacy.load("en_core_web_sm")
      
      BASE_DIR = Path(__file__).resolve().parents[4] 
 
      objects_in_database = ParsedSentence.objects.all()
      print("Number of Sentence to build models for views: ", len(objects_in_database) )
      
      #TEST FASE - START BY empy records thats visualizes sentenses
      # Sentence.objects.all().delete()
      # #check
      # records = Sentence.objects.all()
      # print("TEST FASE Number of Sentence records from works are  initilized to: ", len(records) )
 
      list_of_lemma_context_gramma_objects = apply_values_to_sentences(objects_in_database, nlp_en)
      print(f"Returned number of gramma context gramma objects {len(list_of_lemma_context_gramma_objects)}")
      
      
      for lemma_context in  list_of_lemma_context_gramma_objects:
         #Lemma sentence in LemmaGrammaContext
         lemma_sentence_content = lemma_context.get_lemma_sentence_gramma_objects()
         lemma_sentence_ID = lemma_sentence_content.get_sentenceID()  
         print(f"sentence ID is: {lemma_sentence_ID}")
         lemma_sentence = lemma_sentence_content.get_sentence()
         print(f"sentence is: {lemma_sentence}")
         words_in_sentence = lemma_sentence_content.get_words_in_sentence()
         print(f"Words in lemma sentence: {words_in_sentence}")
         #Start simple Does migrate still complain about missing Sentence model?  - yes, but it is not used in the code, so it is not a problem, but it is better to remove it from the code, and use the new model SentenceInAnalyticalContext instead
         #Start by creating a new SentenceInAnalyticalContext object for the lemma sentence
         obj = SentenceInAnalyticalContext.objects.create(findingID = lemma_sentence_ID,
                                                         sentence = lemma_sentence)
         
         
   
      
      
       
      
       
         # modelobj =  Sentence.objects.create(findingID = lemma_sentence_ID,
         #                                           sentence_type = 'lemmasentence',
         #                                           contains_lemma = 'True', 
         #                                          sentence = lemma_sentence,
         #                                          wordsinsentence = words_in_sentence)
        
        
        
         
         
         #getadjektive info (some "redudance" in coding TESTING)
         #access list of  adjektive s 
         # lemma_sentence_adj_info_obj = lemma_sentence.get_adjektive_obj_lst()
         # #access adjektive info
         # for adjektivinfo  in  lemma_sentence_adj_info_obj:
            # found_word = adjektivinfo.get_word()
            # word_class = adjektivinfo.get_gramma_cat()
            # position = adjektivinfo.get_position()

            
            #obj = Sentence.objects.create(findingID = lemma_sentence_ID,
            #                                       word = found_word, 
             #                                      wordclass = word_class,
              #                                     wordposition = position)
            
            
            
            
         
            
         
         # lemma_sentence_berbs_info_obj = lemma_sentence.set_verb_obj_lst()
            
         # lemma_sentence_adberbs_info_obj = lemma_sentence.set_adverb_obj_lst()
            
         
        
         
         
         
         
         # for adjektive in  lemma_sentence_adj_info_obj:
         #    wordclass =adjektive.get_gramma_cat()
         #    adj =  WordClass.objects.create(navn=wordclass)
         #    wordpositions =adjektive.
            
         #    pos1 = Position.objects.create(navn="Forfelt")
         #    pos2 = Position.objects.create(navn="Subjektspredikativ")
         
         
         
         # lemma_sentence_verb_info_obj = lemma_sentence.get_verb_obj_lst()
         # lemma_sentence_adverb_info_obj = lemma_sentence.get_adverb_obj_lst()
         
     
         # previous_sentence_gramma  =  lemma_context.get_previous_sentence_objects()

         # following_sentence_gramma  = lemma_context.get_following_sentence_objects()
         # print(f"There are:  {len( following_sentence_gramma_list)} raw gramma info for following sentence")
  
      
      # print(f"Current number of Objects in ParsedSentence database to use for views and templates: {len(objects_in_database)}")
  
    
         
      self.stdout.write(self.style.SUCCESS('Successfully run of building models for views and templates .'))







# # #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats