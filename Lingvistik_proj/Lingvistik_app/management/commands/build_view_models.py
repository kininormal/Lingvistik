
from django.core.management.base import BaseCommand
import spacy
from pathlib import Path
import pandas as pd

from ... models import LemmaObjectForAnalysis, ParsedSentence, SentenceInAnalyticalContext, WordObjectForAnalysis

from .statsservices.meaning import apply_values_to_sentences

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
      nlp_en = spacy.load("en_core_web_sm")
      
      BASE_DIR = Path(__file__).resolve().parents[4] 
 
      objects_in_database = ParsedSentence.objects.all()
      print("Number of Sentence to build models for views: ", len(objects_in_database) )
      
      #TEST FASE - START BY empty records for views and templates
      SentenceInAnalyticalContext.objects.all().delete()
      #check
      records = SentenceInAnalyticalContext.objects.all()
      print("TEST FASE Number of Sentence records from works are  initilized to: ", len(records) )
      
      list_of_lemma_context_gramma_objects = apply_values_to_sentences(objects_in_database, nlp_en)
      print(f"Returned number of gramma context gramma objects {len(list_of_lemma_context_gramma_objects)}")
      
      #Register objects to records Start by idiot approch, and then refactor to a more elegant approach, but for now it is better
      lemma_sentence_handling(list_of_lemma_context_gramma_objects)
      previous_sentence_handling(list_of_lemma_context_gramma_objects)
      following_sentence_handling(list_of_lemma_context_gramma_objects)
      #All records are now registered in the database, and can be used to build views and templates for displaying the sentences in the context of the analysis.      
             
      #Coming up USE records to build views and templates for displaying the sentences in the context of the analysis.  The SentenceInAnalyticalContext model can be used to store any type of sentence in the context of the analysis, and can be used to build views and templates for displaying the sentences in the context of the analysis.      
             
             
             
      #Check lemma record before implementing the following code (for previous and following sentences), because it is not necessary to register the lemma in the database, because it is already registered as a lemma sentence in the database, and it is not necessary to register the lemma in the database, because it is already registered as a lemma sentence in the database
      records = SentenceInAnalyticalContext.objects.all()
      print("Number of Sentence records from works are  in the database after building models for views and templates: ", len(records) )
      
      for record in records:
         print(f"Sentence record ID: {record.findingID}, sentence: {record.sentence}, contains_lemma: {record.contains_lemma}, sentence_type: {record.sentence_type}, words_in_sentence: {record.words_in_sentence}")
         words = record.words.all()
         for word in words:
            print(f"Word record ID: {word.id}, word: {word.word}, wordclass: {word.wordclass}, position: {word.position}, sentence ID: {word.sentence.findingID}")
         lemmas = record.lemmas.all()
         for lemma in lemmas:
            print(f"Lemma record ID: {lemma.id}, lemma: {lemma.lemma}, lemma_position: {lemma.lemma_position}, sentence ID: {lemma.sentence.findingID}")
      
      
      ################################################################
      #TEST FASE 
      SentenceInAnalyticalContext.objects.all().delete()
                  #check
      records = SentenceInAnalyticalContext.objects.all()
      print("TEST FASE At leave Number of Sentence records from works are initilized to: ", len(records) )
      
      self.stdout.write(self.style.SUCCESS('Successfully EMPTY IN TEST FASE run of building models for views and templates .'))



def lemma_sentence_handling(list_of_lemma_context_gramma_objects):
   for lemma_context in  list_of_lemma_context_gramma_objects:
         #Lemma sentence in LemmaGrammaContext
         lemma_sentence_content = lemma_context.get_lemma_sentence_gramma_objects()
         lemma_sentence_ID = lemma_sentence_content.get_sentenceID()  
         #print(f"sentence ID is: {lemma_sentence_ID}")
         sentence_with_lemma = lemma_sentence_content.get_sentence()
         #print(f"sentence is: {sentence_with_lemma}")
         words_in_sentence = lemma_sentence_content.get_words_in_sentence()
         # print(f"Words in lemma sentence: {words_in_sentence}")
         #Start simple Does migrate still complain about missing Sentence model?  - yes, but it is not used in the code, so it is not a problem, but it is better to remove it from the code, and use the new model SentenceInAnalyticalContext instead
         #Start by creating a new SentenceInAnalyticalContext object for the lemma sentence
         sentence_record_obj = SentenceInAnalyticalContext.objects.create(findingID = lemma_sentence_ID,
                                                         contains_lemma = 'True',
                                                         sentence_type = 'lemma_sentence',
                                                         sentence = sentence_with_lemma,
                                                         words_in_sentence = words_in_sentence)
         
         #words for analysis are in lemma_context but in tree lists adjektiveObjList, verbObjList and adverbObjList, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
         #get adjektive info (some "redudance" in coding TESTING)
         lemma_adjektive_info_lst = lemma_sentence_content.get_adjektive_obj_lst()
         #get adjektive  objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
         for adjektivinfo  in  lemma_adjektive_info_lst:
            found_word = adjektivinfo.get_word()
            #hard coded as ADJ, because it is an adjektive, and not a noun, verb or adverb, so it is not necessary to get the word class from the adjektivinfo object
            word_class = adjektivinfo.get_gramma_cat() #Value is None so something is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the adjektivinfo object, so it is better to hard code it as ADJ
            position = adjektivinfo.get_position()
            # print(f"Adjektive info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
            #register adjektive word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
            word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                      wordclass ='ADJ', #hard coded as ADJ, because it is an adjektive, and not a noun, verb or adverb, so it is not necessary to get the word class from the adjektivinfo object
                                                      position = position,
                                                      sentence = sentence_record_obj)
            
   
         #get verb info (some "redudance" in coding TESTING)
         lemma_verb_info_lst = lemma_sentence_content.get_verb_obj_lst()
         #get verb objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
         for verbinfo in lemma_verb_info_lst:
            found_word = verbinfo.get_word()
            #hard coded as VERB, because it is a verb, and not a noun, adjektive or adverb, so it is not necessary to get the word class from the verbinfo object
            word_class = verbinfo.get_gramma_cat() #Value is None so something  is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the verbinfo object, so it is better to hard code it as VERB
            position = verbinfo.get_position()
            # print(f"Verb info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
            #register verb word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
            word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                               wordclass ='VERB',#hard coded as VERB, because it is a verb, and not a noun, adjektive or adverb, so it is not necessary to get the word class from the verbinfo object
                                                               position = position,
                                                               sentence = sentence_record_obj)

         #get adverb info (some "redudance" in coding TESTING)
         lemma_adverb_info_lst = lemma_sentence_content.get_adverb_obj_lst()
         #get adverb objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
         for adverbinfo in lemma_adverb_info_lst:
            found_word = adverbinfo.get_word()
            #hard coded as ADVERB, because it is an adverb, and not a noun, verb or adjektive, so it is not necessary to get the word class from the adverbinfo object
            word_class = adverbinfo.get_gramma_cat() #Value is None so something  is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the adverbinfo object, so it is better to hard code it as ADVERB
            position = adverbinfo.get_position()
            # print(f"Adverb info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
            #register adverb word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
            word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                                  wordclass = 'ADVERB',#hard coded as ADVERB, because it is an adverb, and not a noun, verb or adjektive, so it is not necessary to get the word class from the adverbinfo object
                                                                  position = position,
                                                                  sentence = sentence_record_obj)
         # check if sentence has lemma (must be true here) 
         contains_lemma_status =  lemma_sentence_content.has_lemma()
         if contains_lemma_status == True:
            #print(f"Sentence with ID: {lemma_sentence_ID} has a lemma, so it is registered as a lemma sentence in the database")
            lemma = lemma_sentence_content.get_lemma()
            #lemma can ocurre in the sentence more than once, so it is necessary to get the position of the lemma in the sentence, and register it in the database as a LemmaObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
            lemma_positions = lemma_sentence_content.get_lemmapositionlist()
            for lemma_position in lemma_positions: 
              lemma_record_obj = LemmaObjectForAnalysis.objects.create(lemma = lemma,
                                                                        lemma_position = lemma_position,
                                                                        sentence = sentence_record_obj)
         else:
            # print(f"Sentence with ID: {lemma_sentence_ID} does not have a lemma, so it is not registered as a lemma sentence in the database")
            pass
     

def previous_sentence_handling(list_of_lemma_context_gramma_objects):
   for previous_context in  list_of_lemma_context_gramma_objects:
      #Previous sentence in LemmaGrammaContext
      previous_sentence_content = previous_context.get_previous_sentence_gramma_objects()
      previous_sentence_ID = previous_sentence_content.get_sentenceID()  
      #print(f"Previous sentence ID is: {previous_sentence_ID}")
      previous_sentence = previous_sentence_content.get_sentence()
      #print(f"Previous sentence is: {previous_sentence}")
      words_in_previous_sentence = previous_sentence_content.get_words_in_sentence()
      # print(f"Words in previous sentence: {words_in_previous_sentence}")
      contains_lemma_status = previous_sentence_content.has_lemma()
      #Start simple Does migrate still complain about missing Sentence model?  - yes, but it is not used in the code, so it is not a problem, but it is better to remove it from the code, and use the new model SentenceInAnalyticalContext instead
      #Start by creating a new SentenceInAnalyticalContext object for the previous sentence
      sentence_record_obj = SentenceInAnalyticalContext.objects.create(findingID = previous_sentence_ID,
                                                      contains_lemma = contains_lemma_status,
                                                      sentence_type = 'previous_sentence',
                                                      sentence = previous_sentence,
                                                      words_in_sentence = words_in_previous_sentence)
      #get adjektive info (some "redudance" in coding TESTING) 
      previous_adjektive_info_lst = previous_sentence_content.get_adjektive_obj_lst()
      for adjektivinfo  in  previous_adjektive_info_lst:
                  found_word = adjektivinfo.get_word()
                  #hard coded as ADJ, because it is an adjektive, and not a noun, verb or adverb, so it is not necessary to get the word class from the adjektivinfo object
                  word_class = adjektivinfo.get_gramma_cat() #Value is None so something is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the adjektivinfo object, so it is better to hard code it as ADJ
                  position = adjektivinfo.get_position()
                  # print(f"Adjektive info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
                  #register adjektive word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
                  word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                            wordclass ='ADJ', #hard coded as ADJ, because it is an adjektive, and not a noun, verb or adverb, so it is not necessary to get the word class from the adjektivinfo object
                                                            position = position,
                                                            sentence = sentence_record_obj)
    
  
   #get verb info (some "redudance" in coding TESTING)
   previous_adjektive_info_lst_verb_info_lst = previous_sentence_content.get_verb_obj_lst()
   #get verb objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
   for verbinfo in previous_adjektive_info_lst_verb_info_lst:
      found_word = verbinfo.get_word()
      #hard coded as VERB, because it is a verb, and not a noun, adjektive or adverb, so it is not necessary to get the word class from the verbinfo object
      word_class = verbinfo.get_gramma_cat() #Value is None so something  is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the verbinfo object, so it is better to hard code it as VERB
      position = verbinfo.get_position()
      # print(f"Verb info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
      #register verb word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
      word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                         wordclass ='VERB',#hard coded as VERB, because it is a verb, and not a noun, adjektive or adverb, so it is not necessary to get the word class from the verbinfo object
                                                         position = position,
                                                         sentence = sentence_record_obj)

      #get adverb info (some "redudance" in coding TESTING)
      previous_adjektive_info_lst_adverb_info_lst = previous_sentence_content.get_adverb_obj_lst()
      #get adverb objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
      for adverbinfo in previous_adjektive_info_lst_adverb_info_lst:
         found_word = adverbinfo.get_word()
         #hard coded as ADVERB, because it is an adverb, and not a noun, verb or adjektive, so it is not necessary to get the word class from the adverbinfo object
         word_class = adverbinfo.get_gramma_cat() #Value is None so something  is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the adverbinfo object, so it is better to hard code it as ADVERB
         position = adverbinfo.get_position()
         # print(f"Adverb info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
         #register adverb word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
         word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                               wordclass = 'ADVERB',#hard coded as ADVERB, because it is an adverb, and not a noun, verb or adjektive, so it is not necessary to get the word class from the adverbinfo object
                                                               position = position,
                                                               sentence = sentence_record_obj)
      #only different from lemma sentence handling here 
      # check if sentence has lemma (can be true or false here) 
      contains_lemma_status =  previous_sentence_content.has_lemma()
      if contains_lemma_status == True:
         #print(f"Sentence with ID: {previous_sentence_ID} has a lemma, so it is registered as a previous sentence in the database")
         lemma = previous_sentence_content.get_lemma()
         #lemma can ocurre in the sentence more than once, so it is necessary to get the position of the lemma in the sentence, and register it in the database as a LemmaObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
         lemma_positions = previous_sentence_content.get_lemmapositionlist()
         for lemma_position in lemma_positions: 
            lemma_record_obj = LemmaObjectForAnalysis.objects.create(lemma = lemma,
                                                                      lemma_position = lemma_position,
                                                                      sentence = sentence_record_obj)
            
        
       
         
         
         
         
def following_sentence_handling(list_of_lemma_context_gramma_objects):
   for following_context in  list_of_lemma_context_gramma_objects:
      #Previous sentence in LemmaGrammaContext
      following_sentence_content = following_context.get_previous_sentence_gramma_objects()
      previous_sentence_ID = following_sentence_content.get_sentenceID()  
      #print(f"Previous sentence ID is: {previous_sentence_ID}")
      previous_sentence = following_sentence_content.get_sentence()
      #print(f"Previous sentence is: {previous_sentence}")
      words_in_previous_sentence = following_sentence_content.get_words_in_sentence()
      # print(f"Words in previous sentence: {words_in_previous_sentence}")
      contains_lemma_status = following_sentence_content.has_lemma()
      #Start simple Does migrate still complain about missing Sentence model?  - yes, but it is not used in the code, so it is not a problem, but it is better to remove it from the code, and use the new model SentenceInAnalyticalContext instead
      #Start by creating a new SentenceInAnalyticalContext object for the previous sentence
      sentence_record_obj = SentenceInAnalyticalContext.objects.create(findingID = previous_sentence_ID,
                                                      contains_lemma = contains_lemma_status,
                                                      sentence_type = 'previous_sentence',
                                                      sentence = previous_sentence,
                                                      words_in_sentence = words_in_previous_sentence)
      #get adjektive info (some "redudance" in coding TESTING) 
      previous_adjektive_info_lst = following_sentence_content.get_adjektive_obj_lst()
      for adjektivinfo  in  previous_adjektive_info_lst:
                  found_word = adjektivinfo.get_word()
                  #hard coded as ADJ, because it is an adjektive, and not a noun, verb or adverb, so it is not necessary to get the word class from the adjektivinfo object
                  word_class = adjektivinfo.get_gramma_cat() #Value is None so something is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the adjektivinfo object, so it is better to hard code it as ADJ
                  position = adjektivinfo.get_position()
                  # print(f"Adjektive info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
                  #register adjektive word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
                  word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                            wordclass ='ADJ', #hard coded as ADJ, because it is an adjektive, and not a noun, verb or adverb, so it is not necessary to get the word class from the adjektivinfo object
                                                            position = position,
                                                            sentence = sentence_record_obj)
       
     
      #get verb info (some "redudance" in coding TESTING)
      following_adjektive_info_lst_verb_info_lst = following_sentence_content.get_verb_obj_lst()
      #get verb objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
      for verbinfo in following_adjektive_info_lst_verb_info_lst:
         found_word = verbinfo.get_word()
         #hard coded as VERB, because it is a verb, and not a noun, adjektive or adverb, so it is not necessary to get the word class from the verbinfo object
         word_class = verbinfo.get_gramma_cat() #Value is None so something  is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the verbinfo object, so it is better to hard code it as VERB
         position = verbinfo.get_position()
         # print(f"Verb info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
         #register verb word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
         word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                            wordclass ='VERB',#hard coded as VERB, because it is a verb, and not a noun, adjektive or adverb, so it is not necessary to get the word class from the verbinfo object
                                                            position = position,
                                                            sentence = sentence_record_obj)
   
         #get adverb info (some "redudance" in coding TESTING)
         following_adjektive_info_lst_adverb_info_lst = following_sentence_content.get_adverb_obj_lst()
         #get adverb objects from lemma_context, but not in the SentenceInAnalyticalContext model, so they are not stored in the database, but they can be accessed through the lemma_context object
         for adverbinfo in following_adjektive_info_lst_adverb_info_lst:
            found_word = adverbinfo.get_word()
            #hard coded as ADVERB, because it is an adverb, and not a noun, verb or adjektive, so it is not necessary to get the word class from the adverbinfo object
            word_class = adverbinfo.get_gramma_cat() #Value is None so something  is rotten here, because the word class is not always correct, and it is not always possible to get the word class from the adverbinfo object, so it is better to hard code it as ADVERB
            position = adverbinfo.get_position()
            # print(f"Adverb info:  {found_word}, OBS word class is there  abbreviations problems {word_class}, {position}")
            #register adverb word in the database as a WordObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
            word_record_obj = WordObjectForAnalysis.objects.create(word = found_word,
                                                                  wordclass = 'ADVERB',#hard coded as ADVERB, because it is an adverb, and not a noun, verb or adjektive, so it is not necessary to get the word class from the adverbinfo object
                                                                  position = position,
                                                                  sentence = sentence_record_obj)
         #only different from lemma sentence handling here 
         # check if sentence has lemma (can be true or false here) 
         contains_lemma_status =  following_sentence_content.has_lemma()
         if contains_lemma_status == True:
            #print(f"Sentence with ID: {previous_sentence_ID} has a lemma, so it is registered as a previous sentence in the database")
            lemma = following_sentence_content.get_lemma()
            #lemma can ocurre in the sentence more than once, so it is necessary to get the position of the lemma in the sentence, and register it in the database as a LemmaObjectForAnalysis object, and link it to the SentenceInAnalyticalContext object
            lemma_positions = following_sentence_content.get_lemmapositionlist()
            for lemma_position in lemma_positions: 
               lemma_record_obj = LemmaObjectForAnalysis.objects.create(lemma = lemma,
                                                                         lemma_position = lemma_position,
                                                                         sentence = sentence_record_obj)
               
# # #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats