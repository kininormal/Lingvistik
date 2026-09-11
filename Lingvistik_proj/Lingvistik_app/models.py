from django.db import models
   
# Create your models here.
class ParsedSentence(models.Model):
   findingID = models.TextField()
   treesentences = models.TextField()
   svg_html = models.TextField()  # just store the raw SVG string