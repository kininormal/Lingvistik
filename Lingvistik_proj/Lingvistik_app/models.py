from django.db import models
   
# Create your models here.
class ParsedSentence(models.Model):
   class Meta:
      ordering = ['findingID']
   
   findingID = models.TextField()
   lemma = models.TextField()
   sentence =  models.TextField()
   sentence_svg_html = models.TextField() 
   prev_sentence = models.TextField() 
   prev_sentence_svg_html = models.TextField()
   follow_sentence = models.TextField()
   follow_sentence_svg_html  = models.TextField() 
   treesentences = models.TextField()
   treesentences_svg_html = models.TextField()  # just store the raw SVG string
   
#Build on this Succeded removing that migrate "is missing/or are unabel to find" the Sentence model, and using the new model SentenceInAnalyticalContext instead, which is simpler and more flexible, and can be used for any type of sentence, not just lemma sentences.  The SentenceInAnalyticalContext model can be used to store any sentence in the context of the analysis, including previous and following sentences, and other sentences that are not directly related to the lemma sentence.  The findingID field can be used to link the sentences together, and the sentence field can be used to store the raw text of the sentence.  The SentenceInAnalyticalContext model can be used to store any type of sentence in the context of the analysis, and can be used to build views and templates for displaying the sentences in the context of the analysis.
class SentenceInAnalyticalContext(models.Model):
   class Meta:
      ordering = ['findingID']
   
   findingID = models.TextField()
   sentence =  models.TextField()

 
   
   
# class Sentence(models.Model): #leme sentenced and the previous and following sentences are stored in this model, and the words are in Words
#    class Meta:
#       ordering = ['findingID']
#    findingID = models.TextField()   
#    SENTENCE_TYPE = [
#       ('previous', 'Previous'),
#       ('lemmasentence', 'Lemma Sentence'),
#       ('followingsentence',   'Following Sentence'), 
#       ('other', 'Other'),  
#    ]
#    CONTAINS_LEMMA_CHOICES = [
#       ('True', 'Contains Lemma'),  
#       ('False', 'Does Not Contain Lemma'),
#       ('Unknown', 'Unknown'),
#    ]
#    #use contains not has_ or is_ as not BooleanField, because it is possible that the sentence does not contain a lemma, but it is not known if it contains a lemma or not, so it is better to use a CharField with choices
#    contains_lemma = models.CharField(
#       max_length=10,  null=False, choices=CONTAINS_LEMMA_CHOICES, default='Unknown') #ensure need to register if the sentence contains a lemma, so that it is possible to distinguish between the different types of sentences in the database
#    sentence_type = models.CharField(
#       max_length=20,  null=False, choices=SENTENCE_TYPE, default='other') #ensure need to register the sentence type, so that it is possible to distinguish between the different types of sentences in the database
#    sentence = models.TextField()
#    wordsinsentence = models.IntegerField()

# class Word(models.Model): # check sentiment analysis, if it is possible to use the sentiment analysis to get the word class, and if it is possible to use the sentiment analysis to get the word position
   
#    WORDCLASS_CHOICES = [
#       #spacy abbreviations: https://spacy.io/api/annotation#pos-tagging
#       ('NOUN', 'Noun'), #not used yet
#       ('VERB', 'Verb'),
#       ('ADJ', 'Adjective'),
#       ('ADV', 'Adverb'),
#       ('PRON', 'Pronoun'), #not used yet
#       ('DET', 'Determiner'), #not used yet
#       ('ADP', 'Adposition'), #not used yet
#       ('CONJ', 'Conjunction'), #not used yet
#       ('NUM', 'Numeral'), #not used yet
#       ('PART', 'Particle'), #not used yet
#       ('INTJ', 'Interjection'), #not used yet
#       ('obj', 'Object'), # not a mistake object is written in lowercase, because it is not a part of speech, but a syntactic function
#       ('X', 'Other'), #not generatede  but just in case, I added it to the choices ( sign of problems in the data)
#    ]
#    word = models.CharField(max_length=250) #even Iceland, Welsh or Dutch has no words with more than 100 characters, so I increased the max_length to 250
#    position = models.IntegerField()
#    wordclass = models.CharField(max_length=50, choices=WORDCLASS_CHOICES)
#    sentence = models.ForeignKey(
#         Sentence, 
#         on_delete=models.CASCADE, 
#         related_name="words"
#     )
   
# class Lemma(models.Model): #lemma is the word in the sentence that is the focus of the analysis, and the sentence is the sentence containing the lemma
   
#    lemma = models.CharField(max_length=250) #even Iceland, Welch or Duch has no words with more than 100 characters, so I increased the max_length to 250
#    lemma_position = models.IntegerField()
   
#    lemma = models.ForeignKey(
#         Sentence,
#         on_delete=models.CASCADE,
#         related_name="lemmas"
#     )


   



# class WordClass(models.Model):
#     navn = models.CharField(max_length=50, unique=True)  # fx "Tillægsord"

#     class Meta:
#         verbose_name_plural = "Word classes"

#     def __str__(self):
#         return self.navn


# class Position(models.Model):
#     name = models.CharField(max_length=50, unique=True)  # fx "Subjekt", "Forfelt"

#     class Meta:
#         verbose_name_plural = "Positions"

#     def __str__(self):
#         return self.navn


# class IdentifiedWords(models.Model):
#     word = models.CharField(max_length=100)  # fx "hurtig"
    
#     # Ét ord har én ordklasse i denne kontekst
#     wordclass = models.ForeignKey(
#         WordClass, 
#         on_delete=models.CASCADE, 
#         related_name="word"
#     )
    
#     # Ét ord kan optræde i FLERE positioner
#     positioner = models.ManyToManyField(
#         Position, 
#         related_name="identified_words"
#     )

#     class Meta:
#         verbose_name_plural = "Identified words"

#     def __str__(self):
#         return f"{self.ord} ({self.ordklasse})"