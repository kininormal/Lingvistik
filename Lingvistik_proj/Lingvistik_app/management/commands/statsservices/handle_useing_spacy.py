from pydoc import doc

import spacy
#import spacytextblob # not sufficient
from spacytextblob.spacytextblob import SpacyTextBlob
#import transformers
#from transformers import pipeline  # not sufficient


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
   
   # Perform sentiment analysis using spaCyTextBlob
   nlp_lang.add_pipe("spacytextblob")
 
   # ----------------------------------
   # Build rows
   # ----------------------------------
   data = []
   
   # Loop through sentences
   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
         #Hel sætning
         full_sentence = sent.text
         #
         # tre sætniniger 
         #
         # Find starten af forrige sætning (eller starten af doc)
         start_token = sent[0].sent.start
         prev_sent_start = sent[0].doc[start_token].sent.start
         # Hvis vi er ved første sætning, henter vi fra indeks 0
         start_idx = sent[0].doc[sent.start - 1].sent.start if sent.start > 0 else 0
         # Find slutningen af næste sætning (eller slutningen af doc)
         end_idx = sent[-1].doc[sent.end].sent.end if sent.end < len(doc) else len(doc)
         # Skær doc til
         three_sentences = doc[start_idx:end_idx].text
            
   
         #forbred mulighed for antal ord 250 "for meget"  hvis det kan undgås
         # 2a) 250 words before and after
         # start_word = max(0, token.i - 250)
         # end_word = min(len(doc), token.i + 250 + 1)
         # words_window = doc[start_word:end_word].text
         # 2b) 250 tegn før og efter
         #
         #250 tegn for og efter
         #
         start_char = max(0, token.idx - 250)
         end_char = min(len(doc.text), token.idx + len(token.text) + 250)
         chars_window = doc.text[start_char:end_char]
         
         #standard libs not able to judge sentiment proberly Dismissed 
         #register  around lemma i  full_sentence
         # before_ADJ
         # before_VERB
         # before_ADP
         # before_obj
         # after_ADJ
         # after_VERB
         # after_ADP
         # after_obj
             
         
         data.append([
            sent.text,
            #three_sentences  #comming version  evaluate whether previous and/or following sentence should be taken into account for in next version for sentiment
            token.text,
            token.lemma_,
            designation,#renamed some are eg senes 
            body_category,
            lang,
            source,
             name_of_work
         ])
   return data

# def polarity_and_subjectivity_analysis_with_spacy(text, nlp_lang):
#    #requires nlp_lang.add_pipe("spacytextblob") before useing
#    nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1) #able to handle longer texts
#    doc = nlp_lang(text)
#    polarity = doc._.blob.polarity
#    subjectivity = doc._.blob.subjectivity

#    polarity = round(polarity, 4)
#    subjectivity = round(subjectivity, 4)
  
#    print(f"TEST In Function Sentiment analysis results: Polarity={polarity}, Subjectivity={subjectivity}")
#    return polarity, subjectivity

# def subjectivity_analysis_with_huggingface(text, classifier):

#     result = classifier(text)[0]

#     label = result["label"]
#     score = round(result["score"], 4)

#     return label, score