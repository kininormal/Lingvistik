from django.db import models
   
# Create your models here.
class ParsedSentence(models.Model):
   findingID = models.TextField()
   sentence =  models.TextField()
   sentences_svg_html = models.TextField() 
   treesentences = models.TextField()
   treesentences_svg_html = models.TextField()  # just store the raw SVG string