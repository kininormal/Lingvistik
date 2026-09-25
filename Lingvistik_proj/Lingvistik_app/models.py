from django.db import models
   
# Create your models here.
class ParsedSentence(models.Model):
   class Meta:
      ordering = ['findingID']
   findingID = models.TextField()
   sentence =  models.TextField()
   sentence_svg_html = models.TextField() 
   prev_sentence = models.TextField() 
   prev_sentence_svg_html = models.TextField()
   follow_sentence = models.TextField()
   follow_sentence_svg_html  = models.TextField() 
   treesentences = models.TextField()
   treesentences_svg_html = models.TextField()  # just store the raw SVG string
   
class SentenceModifier(models.Model):
   class Meta:
      ordering = ['findingID']
   findingID = models.TextField()
   sentence_position = models.TextField()
   contains_lemma = models.BooleanField()
   