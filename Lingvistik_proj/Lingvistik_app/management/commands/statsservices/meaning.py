
def handle_words_modifying_meaning(database_objects):
   num_objects_in_database = len(database_objects)
   print(f"Database ParsedSentence ought to contain ALL the sentences  (ALL works) n in dataframe : {num_objects_in_database}")
   
   for database_object in database_objects:
      lemma_sentence_id = database_object.findingID
      prev_sentence = database_object.prev_sentence
      lemma_sentence = database_object.sentence
      follow_sentence = database_object.follow_sentence