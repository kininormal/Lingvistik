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
   
   
class Sentence(models.Model): #leme sentenced and the previous and following sentences are stored in this model, and the words in the sentence are stored in the WordsInSentenceInfo model
   class Meta:
      ordering = ['findingID']
   findingID = models.TextField()   
   SENTENCE_TYPE = [
      ('previous', 'Previous'),
      ('lemmasentence', 'Lemma Sentence'),
      ('followingsentence',   'Following Sentence'),   
   ]
   sentence_type = models.CharField(
      max_length=20,  null=False, choices=SENTENCE_TYPE, default='lemmasentence')
   sentence = models.TextField()
   wordsinsentence = models.IntegerField()

class Word(models.Model): # check sentiment analysis, if it is possible to use the sentiment analysis to get the word class, and if it is possible to use the sentiment analysis to get the word position

   WORDCLASS_CHOICES = [
      #spacy abbreviations: https://spacy.io/api/annotation#pos-tagging
      ('NOUN', 'Noun'), #not used yet
      ('VERB', 'Verb'),
      ('ADJ', 'Adjective'),
      ('ADV', 'Adverb'),
      ('PRON', 'Pronoun'), #not used yet
      ('DET', 'Determiner'), #not used yet
      ('ADP', 'Adposition'), #not used yet
      ('CONJ', 'Conjunction'), #not used yet
      ('NUM', 'Numeral'), #not used yet
      ('PART', 'Particle'), #not used yet
      ('INTJ', 'Interjection'), #not used yet
      ('obj', 'Object'), # not a mistake object is written in lowercase, because it is not a part of speech, but a syntactic function
      ('X', 'Other'), #not generatede  but just in case, I added it to the choices ( sign of problems in the data)
   ]
   word = models.CharField(max_length=250) #even Iceland, Welsh or Dutch has no words with more than 100 characters, so I increased the max_length to 250
   position = models.IntegerField()
   wordclass = models.CharField(max_length=50, choices=WORDCLASS_CHOICES)
   sentence = models.ForeignKey(
        Sentence, 
        on_delete=models.CASCADE, 
        related_name="words"
    )
   
class Lemma(models.Model): #lemma is the word in the sentence that is the focus of the analysis, and the sentence is the sentence containing the lemma

   findingID = models.TextField()
   lemma = models.CharField(max_length=250) #even Iceland, Welch or Duch has no words with more than 100 characters, so I increased the max_length to 250
   lemma_position = models.IntegerField()
   
   lemma = models.ForeignKey(
        Sentence,
        on_delete=models.CASCADE,
        related_name="lemmas"
    )

class SentenceModifier(models.Model):
   class Meta:
      ordering = ['findingID']
   findingID = models.TextField()
   sentence_position = models.TextField()
   contains_lemma = models.BooleanField()

class WordsInSentenceInfo(models.Model):
   class Meta:
      ordering = ['findingID']
   findingID = models.TextField()
   word =  models.TextField()
   wordclass =  models.TextField()
   wordposition = models.IntegerField()


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