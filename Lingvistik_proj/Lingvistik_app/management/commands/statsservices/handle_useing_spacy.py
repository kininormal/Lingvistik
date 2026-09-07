from pydoc import doc

import spacy
import spacytextblob 
from spacytextblob.spacytextblob import SpacyTextBlob
import transformers
from transformers import pipeline


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
  
   subjectivity_classifier = pipeline(
    "text-classification",
    model="GroNLP/mdebertav3-subjectivity-english"
   )
   test_text = "That is what you have in your head, I know and what you would certainly say if my father were not by."

   print("TextBlob:")
   polarity, subjectivity = \
   polarity_and_subjectivity_analysis_with_spacy(test_text, nlp_lang)

   print("Hugging Face:")
   label, score = \
   subjectivity_analysis_with_huggingface(test_text, subjectivity_classifier)
    
   # ----------------------------------
   # Build rows
   # ----------------------------------
   data = []
   
   # Loop through sentences
   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
         # Find starten af forrige sætning (eller starten af doc)
            start_token = sent[0].sent.start
            prev_sent_start = sent[0].doc[start_token].sent.start
            # Hvis vi er ved første sætning, henter vi fra indeks 0
            start_idx = sent[0].doc[sent.start - 1].sent.start if sent.start > 0 else 0
            
            # Find slutningen af næste sætning (eller slutningen af doc)
            end_idx = sent[-1].doc[sent.end].sent.end if sent.end < len(doc) else len(doc)
            
            # Skær doc til
            three_sentences = doc[start_idx:end_idx].text
            
           
            #full sentence where lemma is
            #250 words before and after lemma 250 chars if words not possible
            test_txt = f"Found text with token loop: {sent.text}"
            full_sentence = sent.text
  
           
            # 2a) 250 words before and after
            # start_word = max(0, token.i - 250)
            # end_word = min(len(doc), token.i + 250 + 1)
            # words_window = doc[start_word:end_word].text
            # 2b) 250 tegn før og efter
            start_char = max(0, token.idx - 250)
            end_char = min(len(doc.text), token.idx + len(token.text) + 250)
            chars_window = doc.text[start_char:end_char]
            
            # Eksempel på output
            print(f"Sætning: {full_sentence}\n")
            print("Test tre sætninger:")
            print(three_sentences)

            print(f"250 tegn vindue: {chars_window}\n")
            
            
            #Can i avoid  #Problem with 'spacytextblob' already exists in pipeline. by using a different nlp_lang for the polarity_and_subjectivity_analysis_with_spacy function?
            sentences_polarity, sentences_subjectivity = polarity_and_subjectivity_analysis_with_spacy(full_sentence, nlp_lang)
            #Just print for test not apply yet And is test_txt 500 char enough
            print("sentences value")
            print(f"Polarity={sentences_polarity:.4f}, Subjectivity={sentences_subjectivity:.4f}")
            
            chars_polarity, chars_subjectivity =  polarity_and_subjectivity_analysis_with_spacy(chars_window, nlp_lang)
            print("chars value")
            print(f"Polarity={chars_polarity:.4f}, Subjectivity={chars_subjectivity:.4f}")
            three_sentences_polarity, three_sentences_subjectivity =  polarity_and_subjectivity_analysis_with_spacy(three_sentences, nlp_lang)
            print("tree sentences value")
            print(f"Polarity={three_sentences_polarity:.4f}, Subjectivity={three_sentences_subjectivity:.4f}")
            
            
            
            print(test_txt)
            data.append([
               sent.text,
               token.text,
               token.lemma_,
               sentences_polarity,
               sentences_subjectivity,
               chars_polarity,
               chars_subjectivity,
               three_sentences_polarity,
               three_sentences_subjectivity,
               designation,
               body_category,
               lang,
               source,
               name_of_work
            ])
   return data

def polarity_and_subjectivity_analysis_with_spacy(text, nlp_lang):
   #requires nlp_lang.add_pipe("spacytextblob") before useing
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1) #able to handle longer texts
   doc = nlp_lang(text)
   polarity = doc._.blob.polarity
   subjectivity = doc._.blob.subjectivity

   polarity = round(polarity, 4)
   subjectivity = round(subjectivity, 4)
  
   print(f"TEST In Function Sentiment analysis results: Polarity={polarity}, Subjectivity={subjectivity}")
   return polarity, subjectivity

def subjectivity_analysis_with_huggingface(text, classifier):

    result = classifier(text)[0]

    label = result["label"]
    score = round(result["score"], 4)

    return label, score