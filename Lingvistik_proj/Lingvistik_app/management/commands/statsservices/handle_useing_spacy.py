from pydoc import doc

import spacy
from spacy import displacy
import re
from ....models import ParsedSentence, Lemma
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
   print(f"More than one lemma in sentence to analyse ")
   
   lemmainfoobjs = handle_lemma_sentence(lemma_record)
   print(f"For lemma sentence with id  {lemma_record.findingID} there are {len(lemmainfoobjs)} lemma info objects")
   words_of_analytical_interest_infoobjs = handle_words_for_lemma_sentence(lemma_record)
   # print(f"For lemma sentence with id  {lemma_record.findingID} there are {len(words_of_analytical_interest_infoobjs)} words of analytical intrest")
   # for  words_of_analytical_interst in  words_of_analytical_interest_infoobjs:
   #    print(f"word: { words_of_analytical_interst.word } with gramma {words_of_analytical_interst.gramma_class} is of interst")
   
   #get words of analyticaly interest with gramma, position the word, the word it is adj, adver -.. to the position   from the "raw" lemma sentence using the access in lemma_record
   sentenceinfoobjs = handle_lemma_sentence_content(lemma_record, words_of_analytical_interest_infoobjs, nlp_lang)
   print(f"For the sentence with id {lemma_record.findingID} there are {len(sentenceinfoobjs)} sentence object to check for relationship")
   gramma_relationship(lemma_record , sentenceinfoobjs)

         
         
         
         
#################### Toulmin argument model alike ###########################################################
#def process_triplet is main function 


# Extract "meaning modifier" markers (intensifier, downtoner, negation, hedge,
# reinforcer, concession) relative to a target lemma, across a
# previous / lemma / following sentence triplet.

# Design notes (see chat for the full explanation):
# - Sentences are parsed SEPARATELY, not concatenated + re-split, so your
#   existing sentence boundaries are trusted rather than re-derived by spaCy.
# - A running token offset gives every token a position in one shared
#   integer space, so distances are comparable across sentence boundaries.
# - Category is carried by the Matcher's match_id, so word -> category
#   lookup never needs a manual dict scan.
# - One MarkerHit row per marker occurrence (one-to-many vs. your source id).
# """

from spacy.matcher import Matcher
from dataclasses import dataclass
from typing import Optional, List, Dict

nlp_lang = spacy.load("en_core_web_sm")

MARKERS = {
    "intensifier": {
        "very", "really", "extremely", "highly", "deeply", "utterly",
        "completely", "totally", "absolutely",
    },
    "downtoner": {
        "rather", "fairly", "quite", "somewhat", "slightly", "barely",
        "hardly", "almost",
    },
    "negation": {
        "not", "never", "neither", "nor", "no",
    },
    "hedge": {
        "perhaps", "probably", "possibly", "apparently", "seemingly", "maybe",
    },
    "reinforcer": {
        "certainly", "clearly", "indeed", "undoubtedly", "surely", "definitely",
    },
    "concession": {
        "but", "however", "although", "though", "yet", "nevertheless",
        "nonetheless", "still",
    },
}


def build_matcher(nlp_lang) -> Matcher:
    """One Matcher pattern per marker word, keyed by category via match_id.
    Also doubles as a duplicate-assignment check across categories."""
    seen = {}
    matcher = Matcher(nlp_lang.vocab)
    for category, words in MARKERS.items():
        for w in words:
            if w in seen and seen[w] != category:
                raise ValueError(
                    f"'{w}' assigned to both '{seen[w]}' and '{category}'"
                )
            seen[w] = category
        patterns = [[{"LOWER": w}] for w in words]
        matcher.add(category, patterns)
    return matcher


MATCHER = build_matcher(nlp_lang)


@dataclass
class MarkerHit:
    source_id: str                      # FK back to your existing lemma-sentence id
    sentence_position: str              # 'previous' | 'lemma' | 'following'
    marker_text: str                    # surface form, e.g. "Nevertheless"
    marker_lemma: str                   # spaCy lemma of the marker token
    marker_category: str                # e.g. 'concession'
    lemma_present_in_sentence: bool     # target lemma occurs in THIS sentence
    marker_token_idx: int               # position in the shared 3-sentence space
    lemma_token_idx: Optional[int]      # anchor token's position, if any
    distance: Optional[int]             # signed: marker_idx - lemma_idx


def process_triplet(
    source_id: str,
    prev_text: Optional[str],
    lemma_text: Optional[str],
    foll_text: Optional[str],
    target_lemma: str,
) -> List[MarkerHit]:
    """
    prev_text / lemma_text / foll_text: raw sentence strings, already
    segmented by your existing pipeline (can be None/"" if missing, e.g.
    lemma sentence is the first sentence of the work -> no 'previous').
    target_lemma: the lemma you're tracking, e.g. 'foot'.
    """
    parts = [("previous", prev_text), ("lemma", lemma_text), ("following", foll_text)]

    docs, offsets = {}, {}
    running_offset = 0
    for name, text in parts:
        if text:
            d = nlp_lang(text)
            docs[name] = d
            offsets[name] = running_offset
            running_offset += len(d)

    # Anchor: first occurrence of target_lemma in the lemma sentence.
    # (If it occurs more than once, this picks the first -- document that
    # choice if it matters for your analysis, and lemma_token_idx below
    # lets you always trace back which occurrence was used.)
    lemma_global_idx = None
    if "lemma" in docs:
        for tok in docs["lemma"]:
            if tok.lemma_.lower() == target_lemma.lower():
                lemma_global_idx = offsets["lemma"] + tok.i
                break

    hits: List[MarkerHit] = []
    for name, doc in docs.items():
        lemma_present_here = any(
            t.lemma_.lower() == target_lemma.lower() for t in doc
        )
        for match_id, start, _end in MATCHER(doc):
            token = doc[start]
            category = nlp_lang.vocab.strings[match_id]
            global_idx = offsets[name] + token.i
            distance = (
                global_idx - lemma_global_idx
                if lemma_global_idx is not None
                else None
            )
            hits.append(MarkerHit(
                source_id=source_id,
                sentence_position=name,
                marker_text=token.text,
                marker_lemma=token.lemma_,
                marker_category=category,
                lemma_present_in_sentence=lemma_present_here,
                marker_token_idx=global_idx,
                lemma_token_idx=lemma_global_idx,
                distance=distance,
            ))
    return hits


if __name__ == "__main__":
    example = process_triplet(
        source_id="melville-moby-dick_s0042_l01",
        prev_text="He walked slowly toward the shore.",
        lemma_text="His foot was certainly not steady on the wet rocks.",
        foll_text="Nevertheless, he pressed on.",
        target_lemma="foot",
    )
    for hit in example:
        print(hit)


def handle_lemma_sentence(lemma_record):
   id_of_text =    lemma_record.findingID
   sentence = lemma_record.lemma_sentence
   lemma =  lemma_record.lemma
   lemma_content_records = lemma_record.analysis_focus.all()
   
   lemmainfo: List[LemmaInLemmaSentence] = []
   for lemma in  lemma_content_records:
      lemmainfo.append(LemmaInLemmaSentence(
                      lemma_pk = lemma.pk,
                      lemma = lemma.lemma,
                      lemma_position =lemma.lemma_position,
                  ))
   return lemmainfo


def handle_words_for_lemma_sentence(lemma_record):
   words_lemma_sentence = lemma_record.words_analysis_focus.all() # only words of analytical interest are here via build_view_models deciding gramma of analytical  interest
   words_lemma_sentence = sorted( words_lemma_sentence, key=lambda r: r.position) #order words by position
   wordinfo: List[WordForAnalysis] = []
   for word in words_lemma_sentence:
      wordinfo.append(WordForAnalysis(
                     word = word.word,
                     word_position = word.position, 
                     gramma_class = word.wordclass,))
      
   return wordinfo

def handle_lemma_sentence_content(lemma_record, info_of_words_objs, nlp_lang):
   lemma_sentence_info: List[LemmaInLemmaSentence] = []
   text = lemma_record.lemma_sentence
   print(f"Whole sentence to analyse in handle_lemma_sentence_content: {text} ")
   #register used wordclasses  -> make a class to access used grammas #get  allowed_pos form words. Words are determined by relevant gramma set in build_view_models
   allowed_pos = {}
   for info_of_word in info_of_words_objs:
      if info_of_word.gramma_class not in  allowed_pos:
       allowed_pos = info_of_word.gramma_class
      
   
   
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1) # able to handle extreme long sentence
   doc = nlp_lang(text)       
   for token in doc: #doc is lemma sentence to analyse
      # Only consider whole words in lemma sentence, allow eg COVID-19 to be word
      if token.is_punct or token.is_space:  
         continue
      # #Only consider words of analytically interes
      if token.pos_ not in  allowed_pos:  
         continue 
       
      # print(f"CHECK WHOLE WORDS Token word to check  {token.text} with pos {token.i} and gramma {token.pos_}"  )
      lemma_sentence_info.append(LemmaSentenceWords(
                                                    word = token.text,
                                                    word_position =  token.i,
                                                    gramma_class =  token.pos_,
                                                    gramma_related_to_word =  token.head,
                                                    gramma_related_to_word_at_pos = token.head.i,
      ))

   return lemma_sentence_info
      
def gramma_relationship(lemma_rec, lst_of_lemmasentenceWords_objs):
   
   #missing lemma-position
    #missing lemma-pk
   #direct relation 
   for lemmasentenceWord in lst_of_lemmasentenceWords_objs:
      if  lemmasentenceWord.gramma_related_to_word == lemma_rec.lemma:
         lemmasentenceWord.is_direct_relatede = True
      else:
         lemmasentenceWord.is_direct_relatede = False
   #nearest to 
   for lemmasentenceWord in lst_of_lemmasentenceWords_objs: 
      word_pos_in_sentence = lemmasentenceWord.word_position   
      dist = 1000000        
      gramma_class_in_sentence = lemmasentenceWord.gramma_class  
      for lemma in lemma_rec.analysis_focus.all(): # all lemmas for lemma sentence
         if abs(lemma.lemma_position - word_pos_in_sentence) < dist:
            dist = abs(lemma.lemma_position - word_pos_in_sentence)
      print(f"The min dist between {lemmasentenceWord.word } grammaclass {gramma_class_in_sentence} and a lemma is {dist} ")
   
   
@dataclass
class LemmaInLemmaSentence :
   lemma: str 
   lemma_position: int             
   lemma_pk: str  

@dataclass
class WordForAnalysis:
   word: str 
   word_position: int             
   gramma_class: str   #  gramma of analytical  interest in record   


@dataclass
class LemmaSentenceWords:
   word: str 
   word_position: int             
   gramma_class: str  
   gramma_related_to_word: str 
   gramma_related_to_word_at_pos: int
   is_direct_relatede: bool = False
   is_nearest: bool = False
  

         