from pydoc import doc

import spacy



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


# def use_spacy_for_text_processing(text, name_of_work, source, designation, body_category, lang, nlp_lang):
#    # ----------------------------------
#    # Process text with spaCy
#    # ----------------------------------
#    nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
#    doc = nlp_lang(text)

#    # ----------------------------------
#    # Build rows
#    # ----------------------------------
#    data = []
   
#    # Loop through sentences
#    for sent in doc.sents:
     
#       # Loop through tokens in sentence
#       for token in sent:
         
#          #Hel sætning
#          full_sentence = sent.text
#          #
#          # tree sentences (simple implementation for a start no function yet)
#          #
#          # # Find starten af forrige sætning (eller starten af doc)
#          start_token = sent[0].sent.start
#          prev_sent_start = sent[0].doc[start_token].sent.start
#          # Hvis vi er ved første sætning, henter vi fra indeks 0
#          start_idx = sent[0].doc[sent.start - 1].sent.start if sent.start > 0 else 0
#          # Find slutningen af næste sætning (eller slutningen af doc)
#          end_idx = sent[-1].doc[sent.end].sent.end if sent.end < len(doc) else len(doc)
#          # Skær doc til
#          three_sentences = doc[start_idx:end_idx].text
               
#          #Prepare option for 250 words before and after
#          # 2a) 250 words before and after
#          # start_word = max(0, token.i - 250)
#          # end_word = min(len(doc), token.i + 250 + 1)
#          # words_window = doc[start_word:end_word].text
#          # 2b) 250 tegn før og efter
#          #
#          #Prepare option for 250 chars befor and after
#          #
#          # start_char = max(0, token.idx - 250)
#          # end_char = min(len(doc.text), token.idx + len(token.text) + 250)
#          # chars_window = doc.text[start_char:end_char]
            
#          #standard libs not able to judge sentiment proberly Dismissed 
#          #register  around lemma i  full_sentence
#          #ADD NOUNS TO LIST (do some languages refere to bodyparts of animals, pictures/metaphors of animals autonome reaction, pictures/metaphors of plans/trees for human  autonome reaction   
#          # Danish "Ryster som et espeløv" as pictures/metaphor of autonme body reatiov    )
#          # before_ADJ
#          # before_VERB
#          # before_ADP
#          # before_obj
#          # after_ADJ
#          # after_VERB
#          # after_ADP
#          # after_obj
               
            
#       data.append([
#          sent.text,
#          three_sentences,  #evaluate whether previous and/or following sentence should be taken into account for in next version for sentiment
#          token.text,
#          token.lemma_,
#          designation,#renamed some are eg senes or pictures/metafores of autonome body "reactions"
#          body_category,
#          lang,
#          source,
#          name_of_work
#       ])

#    return data
def use_spacy_for_text_processing(
    text,
    name_of_work,
    source,
    designation,
    body_category,
    lang,
    nlp_lang
):

    # ----------------------------------
    # Process text with spaCy
    # ----------------------------------
    nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
    doc = nlp_lang(text)

    # ----------------------------------
    # Build rows
    # ----------------------------------
    data = []

    # ----------------------------------
    # Loop through sentences
    # ----------------------------------
    for sent in doc.sents:

        full_sentence = sent.text

        # ----------------------------------
        # Tree sentences:
        # previous + current + following
        # ----------------------------------
        start_idx = (
            sent[0].doc[sent.start - 1].sent.start
            if sent.start > 0
            else 0
        )

        end_idx = (
            sent[-1].doc[sent.end].sent.end
            if sent.end < len(doc)
            else len(doc)
        )

        three_sentences = doc[start_idx:end_idx].text

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

            # ----------------------------------
            # Store one row for this token
            # ----------------------------------

            data.append([
                full_sentence,
                three_sentences,
                token.text,
                token.lemma_,
                designation,
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
               ", ".join(after_obj)
            ])

    return data




