from django.core.management.base import BaseCommand

from pathlib import Path

import graphviz  
from graphviz import Digraph
from ... models import LemmaObjectForAnalysis, SentenceInAnalyticalContext
class Command(BaseCommand):

   help = 'Traning Graphviz'

   def handle(self, *args, **kwargs):
      sentence_objects_records = SentenceInAnalyticalContext.objects.all()
      for sentence_object in  sentence_objects_records:
         sentence_id = sentence_object.findingID
         lemmas_for_sentence =  sentence_object.lemmas.all()
         words_for_sentence = sentence_object.words.all()
         print(f"For sentence id {sentence_id} there are  {len(lemmas_for_sentence)} lemmas and {len( words_for_sentence)} words for the lemma sentence to graph")
         #Make it posible to Take previous and ollowing  sentence  into account
         previous_sentence  = (
                        SentenceInAnalyticalContext.objects
                      .filter(findingID=sentence_object.findingID)
                         .first()
                     )
         following_sentence  = (
                        SentenceInAnalyticalContext.objects
                         .filter(findingID=sentence_object.findingID)
                        .first()
                     )
      
      
      dot = Digraph(comment='Min første graf')

      # dot.node('A', 'Sentence')
      # dot.node('B', 'Visualisation')
      # dot.node('C', 'Word')
      dot.node('A', 'King Arthur')  
      dot.node('B', 'Sir Bedevere the Wise')
      dot.node('L', 'Sir Lancelot the Brave')

      dot.edges(['AB', 'AL'])
      dot.edge('B', 'L', constraint='false')

      dot.render('min_graf.svg', view=True)
         
      
      self.stdout.write(self.style.SUCCESS('Successfully ended traning of Graphviz.'))
      
      