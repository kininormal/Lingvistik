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