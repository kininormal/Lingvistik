
class LemmaSentence:
   def __init__(self, lemmasentence, sentenceid):
        self.name = 'Lemma sentence'
        self.sentence = lemmasentence
        self.sentenceID = sentenceid
        self.is_lemma_present = True

   def get_sentence(self):
      return self.sentence 
   def get_sentenceID(self):
      return self.sentenceid
    
   def has_lemma(self):
      return self.is_lemma_present
      
   def info(self):
      print("Contains:", self.name)

class PreviousSentence: 
   def __init__(self, previoussentence, lemma_sentence_obj):
      self.name = 'Previous sentence'
      self.sentence = previoussentence
      self.lemma_sentence_ref = lemma_sentence_obj  # Reference til LemmaSentence-objektet
      self.is_lemma_present = None
   def set_lemma_present(self, is_lemma_present):
     self.is_lemma_present = is_lemma_present
   def has_lemma(self):
      #if return value is None: Has not been set
      return self.is_lemma_present
   def get_parent_sentence(self):
      return self.lemma_sentence_ref.get_sentence()
   def get_sentenceID(self):
      return self.lemma_sentence_ref.get_sentenceID()
     
class FollowingSentence:
   def __init__(self, followingsentence, lemma_sentence_obj):
      self.name = 'Following sentence'
      self.sentence = followingsentence
      self.lemma_sentence_ref = lemma_sentence_obj  # Reference til LemmaSentence-objektet
      self.is_lemma_present = None
      
   def set_lemma_present(self, is_lemma_present):
      self.is_lemma_present = is_lemma_present
   def has_lemma(self):
      #if return value is None: Has not been set
      return self.is_lemma_present

   def get_parent_sentence(self):
      return self.lemma_sentence_ref.get_sentence()
   def get_sentenceID(self):
      return self.lemma_sentence_ref.get_sentenceID()

#Version 2 noter 
# class BaseSentence:
#     """En fælles basisklasse til at håndtere delt logik for sætninger."""
#     def __init__(self, name, sentence, lemma_sentence_obj):
#         self.name = name
#         self.sentence = sentence
#         self.lemma_sentence_ref = lemma_sentence_obj  # Reference til LemmaSentence-objektet
#         self.is_lemma_present = None

#     def set_lemma_present(self, is_lemma_present):
#         self.is_lemma_present = is_lemma_present

#     def has_lemma(self):
#         # Hvis returværdien er None: Er ikke blevet sat endnu
#         return self.is_lemma_present

#     def get_parent_sentence(self):
#         return self.lemma_sentence_ref.get_sentence()

#     def get_sentenceID(self):
#         return self.lemma_sentence_ref.get_sentenceID()


# class PreviousSentence(BaseSentence):
#     def __init__(self, previoussentence, lemma_sentence_obj):
#         # super() kalder __init__ i basisklassen og sender de korrekte værdier med
#         super().__init__('Previous sentence', previoussentence, lemma_sentence_obj)


# class FollowingSentence(BaseSentence):
#     def __init__(self, followingsentence, lemma_sentence_obj):
#         # super() kalder __init__ i basisklassen og sender de korrekte værdier med
#         super().__init__('Following sentence', followingsentence, lemma_sentence_obj)







def handle_words_modifying_meaning(database_objects):
   num_objects_in_database = len(database_objects)
   print(f"Database ParsedSentence ought to contain ALL the sentences  (ALL works) n in dataframe : {num_objects_in_database}")
   
   for database_object in database_objects:
      lemma_obj = LemmaSentence(database_object.sentence, database_object.findingID)
      prev_obj = PreviousSentence(database_object.prev_sentence, lemma_obj)
      follow_obj = FollowingSentence(database_object.follow_sentence,lemma_obj)
      #1)
      #a check if prev_obj and follow_obj contains lemma set is lemma present accodinly
      #b regiser words  word class adjektives and adverbies in lemma_obj, prev_obj, and follow_obj (signed distance to lemma in lemma_obj)
      #c register to model
      
      #2) check meaning modifires -> See Claude AI
      #a check if prev_obj and follow_obj contains lemma set is lemma present accodinly
      #b regiser  meaning modififiewrs class of modifier   and their distance to lemma with sign 
      #c register to model