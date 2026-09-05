def use_spacy_for_text_processing(text, name_of_work, source, designation, body_category, lang, nlp_lang):
   # ----------------------------------
   # Process text with spaCy
   # ----------------------------------
   nlp_lang.max_length = max(nlp_lang.max_length, len(text) + 1)
   doc = nlp_lang(text)
   
   # ----------------------------------
   # Build rows
   # ----------------------------------
   data = []
   
   # Loop through sentences
   for sent in doc.sents:
      # Loop through tokens in sentence
      for token in sent:
          # Find lemma matching the designation
         if token.lemma_.lower() == designation:
            data.append([
               sent.text,
               token.text,
               token.lemma_,
               designation,
               body_category,
               lang,
               source,
               name_of_work
            ])
   return data