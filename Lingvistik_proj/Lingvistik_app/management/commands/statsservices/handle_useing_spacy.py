from pydoc import doc

import spacy
from spacy import displacy
import re
from ....models import ParsedSentence, Lemma
from .handle_svg import make_svg_responsive
from  .texthandling import remove_filetype, split_literary_text

class GrammaRelations:
   def __init__(self, gramma_class, is_related):
      self.name = 'Gramma Relations'
      self.word = ''
      self.word_pos = 0
      self.gramma = gramma_class
      self.relation = is_related
      self.lemma = ''
      self.lemma_position = 0
      self.lemma_pk = 0
   def set_word(self, word):
      self.word =  word
   def get_word(self):
      return self.word 
   def set_word_pos(self, word_pos):
      self.word_pos =  word_pos
   def get_word_pos(self):
      return self.word_pos 
   def set_gramma(self, grammaclass):
      self.gramma =  grammaclass
   def get_gramma(self):
      return self.gramma
   def set_relation(self, is_related):
       self.relation =  is_related
   def get_relation(self):
      return  self.relation
   def set_lemma(self,lemma):
      self.lemma = lemma
   def get_lemmas(self):
      return self.lemma
   def set_lemma_pos(self,lemma_pos):
      self.lemma_position = lemma_pos
   def get_lemma_pos(self):
      return self.lemma_position
   def set_lemma_pk(self,lemma_key):
         self.lemma_pk = lemma_key
   def get_lemma_pk(self):
      return self.lemma_pk
      
def get_sentence_context(doc, target_sent):
    
    sentences = list(doc.sents)
    
    index = sentences.index(target_sent)
    
    context = []
    
    if index > 0:
        context.append(sentences[index - 1].text)
        
    context.append(sentences[index].text)
    
    if index < len(sentences) - 1:
        context.append(sentences[index + 1].text)
    
    return " ".join(context)



def use_spacy_for_text_processing(text, name_of_work, source, designation, body_category, lang, nlp_lang):
   # ----------------------------------
   # Process text with spaCy
   # ----------------------------------
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)

   #-----------------------------------
   # New work sentencesNr 0 i work
   #          lemma occurred 0 times
   #-----------------------------------
   WORKID =  remove_filetype(name_of_work, '.txt') 
   sentenceNr = 0
   lemma_occurrences = 0
   #ensure that designation is lower case
   designation = designation.lower()
   # ----------------------------------
   # Build rows
   # ----------------------------------

   data = []
   
   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
         sentenceNr = sentenceNr + 1
         # Find lemma matching the designation
         if token.lemma_.lower() == designation:
            #lemma found in  work number of times lemma found
            lemma_occurrences = lemma_occurrences + 1
         
            WORKID_SENTNR_LEMMANR = f"{WORKID}_S#{sentenceNr}_L#{lemma_occurrences}"
            
            #Full sentence
            full_sentence = sent.text
            #
            # tree sentences (simple implementation for a start no function yet)
            #
            # # Find starten af forrige sætning (eller starten af doc)
            start_token = sent[0].sent.start
            prev_sent_start = sent[0].doc[start_token].sent.start
            # Hvis vi er ved første sætning, henter vi fra indeks 0
            start_idx = sent[0].doc[sent.start - 1].sent.start if sent.start > 0 else 0
            # Find slutningen af næste sætning (eller slutningen af doc)
            end_idx = sent[-1].doc[sent.end].sent.end if sent.end < len(doc) else len(doc)
            # Tree sentences
            three_sentences = doc[start_idx:end_idx].text
            #split three_sentences in  prev_sentence (we have lemma sentence in full_sentence) and follow__sentence

            prev_sentence, follow__sentence = split_literary_text(three_sentences)

            #Handle registraion in model 
            three_sentences_model_doc = nlp_lang(three_sentences)
            prev_sentence_model_doc = nlp_lang(prev_sentence)
            sentences_model_doc = nlp_lang(full_sentence)
            follow_sentences_model_doc = nlp_lang(follow__sentence)
            options = {
               "compact": True,      # tighter arcs, smaller overall diagram
               "distance": 90,        # default is ~175; lower = tokens closer together
               "font": "Arial",
               "bg": "#ffffff",
            }
            #save raw svg in model/database
            three_sentences_svg_html = displacy.render(three_sentences_model_doc, style="dep", options=options, page=False)
            prev_sentence_svg_html = displacy.render(prev_sentence_model_doc, style="dep", options=options, page=False) 
            sentences_svg_html = displacy.render(sentences_model_doc, style="dep", options=options, page=False) 
            follow_sentence_svg_html = displacy.render(follow_sentences_model_doc, style="dep", options=options, page=False)
            #save raw svg in database
            obj = ParsedSentence.objects.create(findingID = WORKID_SENTNR_LEMMANR,
                                                lemma = designation,
                                                sentence = full_sentence, 
                                                sentence_svg_html= sentences_svg_html,
                                                prev_sentence = prev_sentence,
                                                prev_sentence_svg_html = prev_sentence_svg_html, 
                                                follow_sentence = follow__sentence,
                                                follow_sentence_svg_html = follow_sentence_svg_html,
                                                treesentences = three_sentences, 
                                                treesentences_svg_html = three_sentences_svg_html)
            
            
            # ----------------------------------
            # Loop through tokens in sentence
            # ----------------------------------
            for token in sent:
               # ----------------------------------
               # Context BEFORE the token
               # ----------------------------------
               before_tokens = [
                  t for t in sent
                  if t.i < token.i
               ]
               # ----------------------------------
               # Context AFTER the token
               # ----------------------------------
               after_tokens = [
                  t for t in sent
                  if t.i > token.i
               ]
               
               # ----------------------------------
               # BEFORE
               # ----------------------------------
               before_NOUNS = [
                  t.text for t in before_tokens
                  if t.pos_ == "NOUN"
               ]

               before_ADJ = [
                  t.text for t in before_tokens
                  if t.pos_ == "ADJ"
               ]

               before_VERB = [
                  t.text for t in before_tokens
                  if t.pos_ == "VERB"
               ]
            
               #ADV often Qualifier,  Rebuttal or direct indicater of oppersit menain daish ikke
               before_ADV = [
                  t.text for t in before_tokens
                  if t.pos_ == "ADV"
               ]

               before_ADP = [
                  t.text for t in before_tokens
                  if t.pos_ == "ADP"
               ]

               before_obj = [
                  t.text for t in before_tokens
                  if t.dep_ == "obj"
               ]
               # ----------------------------------
               # AFTER
               # ----------------------------------
               after_NOUNS = [
                  t.text for t in after_tokens
                  if t.pos_ == "NOUN"
               ]

               after_ADJ = [
                  t.text for t in after_tokens
                  if t.pos_ == "ADJ"
               ]

               after_VERB = [
                  t.text for t in after_tokens
                  if t.pos_ == "VERB"
               ]
               #ADV often Qualifier,  Rebuttal or direct indicater of oppersit menain daish ikke
               after_ADV = [
                  t.text for t in after_tokens
                  if t.pos_ == "ADV"
               ]
               after_ADP = [
                  t.text for t in after_tokens
                  if t.pos_ == "ADP"
               ]

               after_obj = [
                  t.text for t in after_tokens
                  if t.dep_ == "obj"
               ]

             
               
            
            data.append([
               WORKID_SENTNR_LEMMANR,
               sent.text,
               three_sentences,  #evaluate whether previous and/or following sentence should be taken into account for in next version for sentiment
               token.text,
               token.lemma_,
               designation,#renamed some are eg senes or pictures/metafores of autonome body "reactions"
               body_category,
               lang,
               source,
               name_of_work,
               # BEFORE
               ", ".join(before_NOUNS),
               ", ".join(before_ADJ),
               ", ".join(before_VERB),
               ", ".join(before_ADV),
               ", ".join(before_ADP),
               ", ".join(before_obj),
                # AFTER
               ", ".join(after_NOUNS),
               ", ".join(after_ADJ),
               ", ".join(after_VERB),
               ", ".join(after_ADV),
               ", ".join(after_ADP),
               ", ".join(after_obj),
            ])
   return data


def apply_object_values(sentence_obj,  nlp_lang):
   
   
   text = sentence_obj.get_sentence()
   lemma = sentence_obj.get_lemma()
   is_lemma_present = False
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   #ensure lower case of lemma
   lemma = lemma.lower()
   doc = nlp_lang(text)
   is_lemma_present = False
   positionList = []
   
   for sent in doc.sents:
      words_in_sentence = len(sent)
      for token in sent:
         # Find lemma matching the designation
         if token.lemma_.lower() == lemma:
            position = token.i
            positionList.append(position)
            is_lemma_present = True
   
   
   sentence_obj.set_words_in_sentence(words_in_sentence)
   sentence_obj.set_lemmapositionlist(positionList)
   if  sentence_obj.name != 'Lemma sentence':
      sentence_obj.set_lemma_present(is_lemma_present)
        
   return sentence_obj


      




def record_lemmas(lemma_sentence_record_obj, nlp_lang):
   print("Entering record lemma")
   text =  lemma_sentence_record_obj.lemma_sentence
   lemma =  lemma_sentence_record_obj. lemma
   
   print(f"in record lemmas the lemma is: { lemma} and sentance is {text}")
   # ----------------------------------
   # Process text with spaCy
   # ----------------------------------
   text =  lemma_sentence_record_obj.lemma_sentence
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)
   designation = lemma_sentence_record_obj.lemma
   #ensure that designation is lower case
   designation = designation.lower()

   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
         # Find lemma matching the designation
         if token.lemma_.lower() == designation:
            print("Try to record lemma")
            position = token.i
            
            lemmaobj = Lemma.objects.create(lemma = designation, 
                                             lemma_position = position,
                                              lemmasentence=lemma_sentence_record_obj,
                                             )

def find_wordclass_lemma_relations(lemma_record, nlp_lang):
   id_of_text =    lemma_record.findingID
   text = lemma_record.lemma_sentence
   lemma_records  = lemma_record.analysis_focus.all() # know that length is > 1 here most often 2
   
   words_for_lemmas =  lemma_record.words_analysis_focus.all()
   #sort according to position
   words_for_lemmas = sorted(words_for_lemmas, key=lambda r: r.position)
   
   
   #dict to find lemma wiht lowest dist to hhe head that word are realted to
   lemma_dict = {}
   #make dict of lemmas in sentence  and their position
   for lemma in lemma_records:
      print(f"Lemma position {lemma.lemma_position}")
      lemma_dict = lemma_dict|{lemma.pk : lemma.lemma_position}
   
   
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1) # able to handle extreme long sentence
   ### NB BUILD the followin  AS A SHARE WITH build_view_models
   #preperation for taking more gramma into account
   #allowed_pos = {"ADJ", "NOUN", "VERB", "ADV", "PRON", "DET", "ADP", "CONJ", "NUM", "PART", "INTJ"}
   #current gramma for analysis
   allowed_pos = {"ADJ", "VERB", "ADV", "PRON"} # of   analytical interest ### NB BUILD THIS AS A SHARE WITH build_view_models
   print("MORE THAN ONE LEMMA NOT HANDELD FOR WORDS  YET - spacy and sentence to figure out LEMMA that word are related to")
   print(f"ID of text to analyse: {id_of_text}")
   print(f"Text to analyse: {text}")
   #start by not using   allowed_posdoes it work as expected
   # find words 
   doc = nlp_lang(text)
               
   for token in doc: #doc is lemma_sentence
     
      if token.is_punct or token.is_space:  # Only consider words in lemma_sentence allow eg covid-19 to be a sentence
         continue
      print(f"Token word to check  {token.text} with pos {token.i}"  )
   
      if token.pos_ not in  allowed_pos:   # #Only consider words of analytically interes
         continue 
      
      print(f"Token with gramma {token.pos_} IS OF analytical interest Make analytical context") 
      grammaObjList = []
      #stat by having control over gramma class (does it work as expected)
      for gramma_class in allowed_pos:
         grammaobj = GrammaRelations(token.pos_, False)
         print(f"THE GRAMMA CLASS TO consider IS {gramma_class}")
         if token.pos_ == gramma_class:
            
            
            
           
            
           
            
            # find position of wer of  analytical interest, find the word it relates to and the position of the word it relates to  
            token_position = token.i
            related_word = token.head
            related_word_position = related_word.i
            #Does any lemma has the position that word it relates to -> the word is direct related to the lemma 
            ###########################################
             #REGISTER BOTH DIRECT AND NOT DIRECT relatioms 
             #look up for DIRECT AND NOT DIRECT relatioms
             #For NOT DIRECT AND NOT DIRECT relatioms  connet by --- or ... line 
                        
            ############################################
                        
            for lemma_key, lemma_pos in lemma_dict.items():
               print(f"Sentence: Lemma with key {lemma_key}, and position {lemma_pos}")
               if lemma_pos == related_word_position:
                  #pgramma of word is set GrammaRelations(token.pos_, False)
                  grammaobj.set_lemma_pos(lemma_pos)   #set by register more than needed  in GrammaRelations
                  grammaobj.set_lemma_pk(lemma_record.pk)    #set by register more than needed  in GrammaRelations
                  grammaobj.set_lemma(lemma_record.lemma)    #set by register more than needed  in GrammaRelations
                  grammaobj.set_word(token.text)    #set by register more than needed in GrammaRelations
                  grammaobj.set_word_pos(token.i)
                  grammaobj.set_relation(True) #set by register more than needed in GrammaRelations
                  print(f"There is a direct relation between word {token.text:<12} and lemma with key {lemma_key}")
                  grammaObjList.append(grammaobj) # make a list of words  directly related  to lemma the gramm kan ber acceced by 
               
            print(f"There are a current list of {len(grammaObjList)} gramma objects directly related  to lemma")
            print(f"FOR WORD OF analytical interest") 
            print(f"token position { token_position  } related position {related_word_position}")
            print(f"{token.text:<12} -> {related_word.text:<12} (Direct Modifier)")
         
      print(f"There are a total list of {len(grammaObjList)} gramma objects dirictly relatedt to lemma")
      
         
         

























      # if token.pos_ == "ADJ":
      #    # Direct modifier (amod) -> Related to its immediate head
      #    if token.dep_ == "amod":
      #       related_word = token.head
      #       token_position = token.i
      #       related_word_position = related_word.i
      #       print(f"token position { token_position  } related position {related_word_position}")
      #       print(f"{token.text:<12} -> {related_word.text:<12} (Direct Modifier)")
            
         #     if token.pos_ == "VERB":
               
         #         # Direct modifier (amod) -> Related to its immediate head
         #         if token.dep_ == "amod":
         #             related_word = token.head
         #             print(f"{token.text:<12} -> {related_word.text:<12} (Direct Modifier)")
                     
                    
         #     if token.pos_ == "ADV":
                  
         #         # Direct modifier (amod) -> Related to its immediate head
         #         if token.dep_ == "amod":
         #             related_word = token.head
         #             print(f"{token.text:<12} -> {related_word.text:<12} (Direct Modifier)")
            
         #     if token.pos_ == "PRON":
                  
         #         # Direct modifier (amod) -> Related to its immediate head
         #         if token.dep_ == "amod":
         #             related_word = token.head
         #             print(f"{token.text:<12} -> {related_word.text:<12} (Direct Modifier)")

         
         
         