
from .handle_useing_spacy import apply_object_values, gramma_in_sentence


class LemmaSentence:
   def __init__(self, lemma, lemmasentence, sentenceid):
        self.name = 'Lemma sentence'
        self.lemma = lemma
        self.sentence = lemmasentence
        self.sentenceID = sentenceid
        self.is_lemma_present = True
        self.lemmapositionList = []
        self.words_in_sentence = None
   def get_lemma(self):
      return self.lemma
   def set_words_in_sentence(self, words_in_sentence):
     self.words_in_sentence = words_in_sentence
   def get_words_in_sentence(self):
      return  self.words_in_sentence
   def get_sentence(self):
      return self.sentence 
   def get_sentenceID(self):
      return self.sentenceid
   def set_lemmapositionlist(self, lemmapositionlist):
      self.lemmapositionList = lemmapositionlist
   def get_lemmapositionlist(self):
      return self.lemmapositionList
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
      self.lemmapositionList = []
      self.words_in_sentence = None
   def set_lemma_present(self, is_lemma_present):
      self.is_lemma_present = is_lemma_present
   def has_lemma(self):
      #if return value is None: Has not been set
      return self.is_lemma_present
   def set_words_in_sentence(self, words_in_sentence):
      self.words_in_sentence = words_in_sentence
   def get_words_in_sentence(self):
      return  self.words_in_sentence
   def set_lemmapositionlist(self, lemmapositionlist):
      self.lemmapositionList = lemmapositionlist
   def get_lemmapositionlist(self):
      return self.lemmapositionList
   def get_sentence(self):
      return self.sentence
   def get_parent_sentence(self):
      return self.lemma_sentence_ref.get_sentence()
   def get_sentenceID(self):
      return self.lemma_sentence_ref.get_sentenceID()
   def get_lemma(self): #get_parent_lemma????
      return self.lemma_sentence_ref.get_lemma()
     
class FollowingSentence:
   def __init__(self, followingsentence, lemma_sentence_obj):
      self.name = 'Following sentence'
      self.sentence = followingsentence
      self.lemma_sentence_ref = lemma_sentence_obj  # Reference til LemmaSentence-objektet
      self.is_lemma_present = None
      self.lemmapositionList = []
      self.words_in_sentence = None
   def set_lemma_present(self, is_lemma_present):
      self.is_lemma_present = is_lemma_present
   def has_lemma(self):
      #if return value is None: Has not been set
      return self.is_lemma_present
   def set_words_in_sentence(self, words_in_sentence):
      self.words_in_sentence = words_in_sentence
   def get_words_in_sentence(self):
      return  self.words_in_sentence
   def set_lemmapositionlist(self, lemmapositionlist):
      self.lemmapositionList = lemmapositionlist
   def get_lemmapositionlist(self):
      return self.lemmapositionList
   def get_sentence(self):
      return self.sentence
   def get_parent_sentence(self):
      return self.lemma_sentence_ref.get_sentence()
   def get_sentenceID(self):
      return self.lemma_sentence_ref.get_sentenceID()
   def get_lemma(self): #get_parent_lemma????
         return self.lemma_sentence_ref.get_lemma()

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




def apply_values_to_sentences(database_objects, nlp_lang):
   num_objects_in_database = len(database_objects)
   print(f"Database ParsedSentence ought to contain ALL the sentences  (ALL works) n in dataframe : {num_objects_in_database}")
   
   for database_object in database_objects:
      lemma_obj = LemmaSentence(database_object.lemma, database_object.sentence, database_object.findingID)
      prev_obj = PreviousSentence(database_object.prev_sentence, lemma_obj)
      follow_obj = FollowingSentence(database_object.follow_sentence,lemma_obj)
      
      # apply position of lemma in sentance
      # apply if lemma is present in prev and follow
      lemma_obj = apply_object_values(lemma_obj, nlp_lang)
      prev_obj =  apply_object_values(prev_obj, nlp_lang)
      follow_obj =  apply_object_values(follow_obj, nlp_lang)
       
      adjektives, verbs, adverbs = gramma_in_sentence(lemma_obj.get_sentence() , nlp_lang)
      print("Lemma contains list with nomber of adj  objets", len(adjektives))
      print("Lemma contains list with nomber of verbs  objets", len(verbs))
      print("Lemma contains list with nomber of adverbs  objets", len(adverbs))
      
    
      
      #1)
      #a check if prev_obj and follow_obj contains lemma set is lemma present accodinly
      #b regiser words  word class adjektives and adverbies in lemma_obj, prev_obj, and follow_obj (signed distance to lemma in lemma_obj)
      #c register to model
      
      #2) check meaning modifires -> See Claude AI
      #a check if prev_obj and follow_obj contains lemma set is lemma present accodinly
      #b regiser  meaning modififiewrs class of modifier   and their distance to lemma with sign 
      #c register to model