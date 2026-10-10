from django.core.management.base import BaseCommand

from pathlib import Path
import re
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
         if len(lemmas_for_sentence) == 1: # simple handling 
            for lemma_content in lemmas_for_sentence:
               # Opret din digraph (du behøver ikke format='svg' her, da vi styrer det via pipe)
               dot = graphviz.Digraph(sentence_id)
               dot.node('0', lemma_content.lemma )  
               #words
               num_words_objs = sentence_object.words.all()
               print(f"Words for lemma   {len( num_words_objs)}")
               dot.node('10', lemma_content.lemma )  
               #gramma of words
               dot.node('20', lemma_content.lemma )  

               # 1. Hent SVG-indholdet som en streng direkte i hukommelsen
               svg_string_graphviz = dot.pipe(format="svg", encoding="utf-8")
               svg_string  = clean_svg(svg_string_graphviz) #  svg_string_graphviz contains eg  doctype  xml info
             
             
               #print(f"SVG string til model:\n {svg_string}")
               # 2. Gem i din Django-model (eksempel)
               # min_model_instans = MinModel.objects.create(svg_content=svg_string)

               # 3. Gem til harddisken, hvis du stadig ønsker filen derpå
               #   with open(f"{sentence_id}.svg", "w", encoding="utf-8") as f:
               #       f.write(svg_string)

               #print(f"SVG gemt i model og som fil for: {sentence_id}")
            
         else:
            print("More than one lemma")    
      
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
      
def clean_svg(svg_string):
   match = re.search(r"<svg.*?</svg>",  svg_string, re.DOTALL)
      
   if match:
      svg_string = match.group(0)
   else:
      print("Ingen SVG fundet i strengen.")
   return svg_string
      
      