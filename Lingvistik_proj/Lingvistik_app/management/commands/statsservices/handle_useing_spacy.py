from pydoc import doc

import spacy
from spacy import displacy
import re
from ....models import ParsedSentence
from .handle_svg import make_svg_responsive
from  .texthandling import remove_filetype, split_literary_text
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
   if  sentence_obj.name != 'Lemma sentence':
      sentence_obj.set_lemma_present(is_lemma_present)
      sentence_obj.set_lemmapositionlist(positionList)
   else: 
     sentence_obj.set_lemmapositionlist(positionList)       
   return sentence_obj

class Gramma:
   def __init__(self):
      self.gamma_cat = None
      self.word = None
      self.position = None
   def set_gramma_cat(self, gramma_cat):
      self.gamma_cat = gramma_cat
   def get_gramma_cat(self, gramma_cat):
      return self.gamma_cat
   def set_word(self, word):
      self.word = word
   def get_word(self):
      return  self.word
   def set_position(self, position):
      self.position = position
   def get_position(self, position):
      return self.position 
      
def gramma_in_sentence(sentence, nlp_lang):
   #allow very long sentences
   nlp_lang.max_length = max(nlp_lang.max_length, len(sentence) + 1)
   doc = nlp_lang(sentence)
   adjList = []
   verbList = []
   advList = []
   for sent in doc.sents:
      # ----------------------------------
      # Loop through tokens in sentence
      # ----------------------------------
      for token in sent:
         if token.pos_ == "ADJ":
            gramma_obj = Gramma()
            gramma_obj.set_word(token)
            gramma_obj.set_gramma_cat(token.pos_)
            gramma_obj.set_position(token.i)
            
            adjList.append(gramma_obj)
         if token.pos_ == "VERB":
            gramma_obj = Gramma()
            gramma_obj.set_word(token)
            gramma_obj.set_gramma_cat(token.pos_)
            gramma_obj.set_position(token.i)
                       
            verbList.append(gramma_obj)
         if token.pos_ == "ADV":
            gramma_obj = Gramma()
            gramma_obj.set_word(token)
            gramma_obj.set_gramma_cat(token.pos_)
            gramma_obj.set_position(token.i)
           
            advList.append(gramma_obj)
   return adjList, verbList, advList
            
   
                
   
















