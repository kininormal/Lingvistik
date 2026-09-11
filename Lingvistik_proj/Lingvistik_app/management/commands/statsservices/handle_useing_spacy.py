from pydoc import doc

import spacy
from spacy import displacy
import re
from ....models import ParsedSentence

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
   sentenceNr = 0
   lemma_occurrences = 0
   # ----------------------------------
   # Build rows
   # ----------------------------------
   chars_in_pattern = ".txt"
   pattern = f"[{chars_in_pattern}]"
      
    
   
   data = []
   
   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
         sentenceNr = sentenceNr + 1
         # Find lemma matching the designation
         if token.lemma_.lower() == designation:
            #lemma found in  work
            WORKID =  re.sub(pattern, "", name_of_work) 
            #number of times lemma found
            lemma_occurrences = lemma_occurrences + 1
         
            WORKID_SENTNR_LEMMANR = f"{WORKID}_S_{sentenceNr}_L_{lemma_occurrences}"
            
            
           
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
            #Handle registraion in model 
            model_doc = nlp_lang(three_sentences)
            svg_html = displacy.render(model_doc, style="dep", page=False)

            obj = ParsedSentence.objects.create(findingID=WORKID_SENTNR_LEMMANR,  treesentences=three_sentences, svg_html=svg_html)
            
            
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


















