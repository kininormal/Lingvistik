from django.db import models
import re
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
   
   
class LemmaSentence(models.Model):
   class Meta:
      ordering = ['findingID']
    
   findingID = models.CharField(max_length=500, db_index=True)
   lemma = models.CharField(max_length=250, default='')
   lemma_sentence =  models.TextField()
   @property
   def words_in_lemma_sentence(self): # = models.IntegerField(null=True, blank=False) #Null is allowed, Indicate not set
      words = re.findall(r'\b\w+\b',  self.lemma_sentence)
      return len(words)
   
class PreviousSentence(models.Model):
   
   lemma_sentence_for_previous = models.OneToOneField(LemmaSentence, related_name='previous_sentence', on_delete=models.CASCADE)
   
   previous_sentence =  models.TextField()
   #use contains not has_ or is_ as not BooleanField, because it is possible that the sentence does not contain a lemma, but it is not known if it contains a lemma or not, so it is better to use a CharField with choices
   @property
   def words_in_previous_sentence(self):
      words = re.findall(r'\b\w+\b',  self.previous_sentence)
      return len(words)
   
   
  
      
class FollowingSentence(models.Model):
   
   lemma_sentence_for_following = models.OneToOneField(LemmaSentence, related_name='following_sentence', on_delete=models.CASCADE)
   
   following_sentence =  models.TextField()
   #use contains not has_ or is_ as not BooleanField, because it is possible that the sentence does not contain a lemma, but it is not known if it contains a lemma or not, so it is better to use a CharField with choices
   @property
   def words_in_following_sentence(self):
      words = re.findall(r'\b\w+\b',  self.following_sentence)
      return len(words)
   

   
class Word(models.Model): # check sentiment analysis, if it is possible to use the sentiment analysis to get the word class, and if it is possible to use the sentiment analysis to get the word position
   
   lemmasentencewords = models.ForeignKey(LemmaSentence, related_name='words_analysis_focus' ,on_delete=models.CASCADE, null=True, blank=True)
   previoussentencewords = models.ForeignKey(PreviousSentence, related_name='words_previous' ,on_delete=models.CASCADE, null=True, blank=True)
   followingsentencewords = models.ForeignKey(FollowingSentence, related_name='words_following' ,on_delete=models.CASCADE, null=True, blank=True)
   
   WORDCLASS_CHOICES = [
      #spacy abbreviations used: spacy abbreviations: https://spacy.io/api/annotation#pos-tagging
      ('NOUN', 'Noun'), 
      ('VERB', 'Verb'),
      ('ADJ', 'Adjective'),
      ('ADV', 'Adverb'),
      ('PRON', 'Pronoun'), 
      ('DET', 'Determiner'), 
      ('ADP', 'Adposition'), 
      ('CONJ', 'Conjunction'), 
      ('NUM', 'Numeral'), 
      ('PART', 'Particle'), 
      ('INTJ', 'Interjection'), 
      #('obj', 'Object'), # not a mistake object is written in lowercase, because it is not a part of speech, but a syntactic function
      ('X', 'Other'), 
   ]
   word = models.CharField(max_length=250) #even Iceland, Welsh or Dutch has no words with more than 100 characters, so I increased the max_length to 250
   position = models.IntegerField()
   wordclass = models.CharField(max_length=50, choices=WORDCLASS_CHOICES)
   #https://forum.djangoproject.com/t/setting-up-models-with-multiple-foreign-key-relationships/26758
    # #https://dev.to/doridoro/django-several-foreignkey-relations-hj5
 
   
class Lemma(models.Model): #lemma is the word in the sentence that is the focus of the analysis, and the sentence is the sentence containing the lemma

   lemmasentencelemmas = models.ForeignKey(LemmaSentence, related_name='analysis_focus' ,on_delete=models.CASCADE, null=True, blank=True)
   previoussentencelemmas = models.ForeignKey(PreviousSentence, related_name='previous' ,on_delete=models.CASCADE, null=True, blank=True)
   followingsentencelemmas = models.ForeignKey(FollowingSentence, related_name='following' ,on_delete=models.CASCADE, null=True, blank=True)
   
   lemma = models.CharField(max_length=250) #even Iceland, Welch or Duch has no words with more than 100 characters, so I increased the max_length to 250
   lemma_position = models.IntegerField()
   #https://dev.to/doridoro/django-several-foreignkey-relations-hj5     NOT NULL constraint failed: Lingvistik_app_lemma.followingsentence_id
   
   

class VisualizationOfLemmaSentence(models.Model):
   class Meta:
         ordering = ['related_findingID']
   
   sentence_and_context_svg = models.TextField() 
   related_findingID = models.CharField(max_length=500, db_index=True)
   
   
class ToulminVisualization(models.Model):
   class Meta:
         ordering = ['related_findingID']
   
   toulmin_svg = models.TextField() 
   related_findingID = models.CharField(max_length=500, db_index=True)
   
