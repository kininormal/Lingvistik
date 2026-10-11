from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
from graphviz import Digraph
from ... models import LemmaObjectForAnalysis, SentenceInAnalyticalContext
class Command(BaseCommand):

   help = 'Traning Graphviz'
  
     
    ##############################
#     from collections import defaultdict

# lemma_sentences = SentenceInAnalyticalContext.objects.filter(
#     sentence_type='lemma_sentence'
# ).prefetch_related('words', 'lemmas')

# ids = [r.findingID for r in lemma_sentences]
# by_finding = defaultdict(dict)
# for s in SentenceInAnalyticalContext.objects.filter(
#     findingID__in=ids,
#     sentence_type__in=['previous_sentence', 'following_sentence'],
# ).prefetch_related('words'):
#     by_finding[s.findingID][s.sentence_type] = s

# for record in lemma_sentences:
#     previous_record = by_finding[record.findingID].get('previous_sentence')
#     following_record = by_finding[record.findingID].get('following_sentence')
#alsow get sentence if 
#a get lemmas in contest if > 1 need spacy 
    
    #########################



   def handle(self, *args, **kwargs):
      #Build graph form lemma(s) as gramma relasts to lemma
      sentence_records_objs = SentenceInAnalyticalContext.objects.all()
      lemma_sentence_occured = 0
      previous_sentence_occured = 0
      following_sentence_occured = 0
      for sentence_record_obj in sentence_records_objs:
         print(f"Inspecting sentence with id {sentence_record_obj.findingID} ")
         if sentence_record_obj.sentence_type == 'lemma_sentence':
            lemma_sentence_occured = lemma_sentence_occured +1
            words = sentence_record_obj.words.all()
            lemmas = sentence_record_obj.lemmas.all()
            print(f"lemma sentence with id {sentence_record_obj.findingID} . Finding lemma sentence nr {lemma_sentence_occured} must end at 121")
    

    
         if sentence_record_obj.sentence_type == 'previous_sentence':
            previous_sentence_occured = previous_sentence_occured + 1
            print(f"previos sentence  with id {sentence_record_obj.findingID}. finding previos nr { previous_sentence_occured} must be at end >0 and  <= 121")

         if sentence_record_obj.sentence_type == 'following_sentence':
            following_sentence_occured = following_sentence_occured+ 1
            print(f"following sentence_occured with id {sentence_record_obj.findingID}. finding follow nr { following_sentence_occured} must be at end >0 and <= 121")
           
            


# nighbours.get('following_sentence')
      
#       print(f"For lemma sentence with id: {lemma_sentence_record.findingID}  there are a previous with id {previous_record.findingID } and following with id: {following_record.findingID}  ")
  
      
      #    if len(lemmas_for_sentence_objects) == 1: # simple handling 
      #       for lemma_sentence_object in lemmas_for_sentence_objects:
      #          # previou and following related to lemma_content
      #          #https://www.geeksforgeeks.org/python/python-django-queryset-filtering/
      #          previous_sentence  = (
      #             SentenceIn
   #  context = SentenceInAnalyticalContext.objects.filter(findingID=record.findingID)
   #  previous_record = context.filter(sentence_type='previous_sentence').first()
   #  following_record = context.filter(sentence_type='following_sentence').first()
      
      
      
   #    lemma_sentence_records = SentenceInAnalyticalContext.objects.filter(
   #    sentence_type='lemma_sentence'
   #       ).prefetch_related('words', 'lemmas')
      
   #    print(f"Got {len(lemma_sentence_records)} to analyse")
      
   #    for lemma_sentence_record in  lemma_sentence_records:
   #       neighbours = {
   #          s.sentence_type: s
   #          for s in SentenceInAnalyticalContext.objects
   #          .filter(
   #              findingID=lemma_sentence_record.findingID,
   #              sentence_type__in=['previous_sentence', 'following_sentence'],
   #          )
   #          .prefetch_related('words')
   #       }
   #    previous_record = neighbours.get('previous_sentence')
   #    following_record = neAnalyticalContext.objects
   #    #                .filter(findingID=sentence_object.findingID)
      #                .first()
      #             )
      #          following_sentence  = (
      #             SentenceInAnalyticalContext.objects
      #                .filter(findingID=sentence_object.findingID)
      #                .first()
      #             )
      #          # Opret din digraph (du behøver ikke format='svg' her, da vi styrer det via pipe)
      #          dot = graphviz.Digraph(sentence_id)
      #          dot.node('0',  lemma_sentence_object.lemma )  
      #          #words
      #          word_objects_for_lemma_sentence  = lemma_sentence_object.filter(findingID=sentence_id)
      #          print(f"Word objects for lemma   {len(  word_objects_for_lemma_sentence)}")
      #          for index, word_obj in   enumerate(word_objects_for_lemma_sentence):
      #             index_str = str(index)
      #             index_str = f"{index}"
      #             print(f"Word: {word_obj.word} with index {index_str}")
      #             dot.node('10', word_obj.word )   
             
                  
      #          # gramma of words
      #          # dot.node('20', lemma_content.lemma )  

      #          # 1. Hent SVG-indholdet som en streng direkte i hukommelsen
      #          svg_string_graphviz = dot.pipe(format="svg", encoding="utf-8")
      #          svg_string  = clean_svg(svg_string_graphviz) #  svg_string_graphviz contains eg  doctype  xml info
             
             
               # print(f"SVG string til model:\n {svg_string}")
               # 2. Gem i din Django-model (eksempel)
               # min_model_instans = MinModel.objects.create(svg_content=svg_string)

               # 3. Gem til harddisken, hvis du stadig ønsker filen derpå
               #   with open(f"{sentence_id}.svg", "w", encoding="utf-8") as f:
               #       f.write(svg_string)

               # print(f"SVG gemt i model og som fil for: {sentence_id}")
              
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
      
      