from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
from graphviz import Digraph
from ... models import  LemmaSentence, VisualizationOfLemmaSentence
class Command(BaseCommand):

   help = 'Traning Graphviz'
  
   def handle(self, *args, **kwargs):
      #Build graph form lemma(s) as gramma relasts to lemma
      lemma_sentence_records = LemmaSentence.objects.all()
            
      print(f"There are {len( lemma_sentence_records )} lemma records in LemmaSentence class")
      
      # total_lemmas = Lemma.objects.all()
      # print(f"There are a total of  {len( total_lemmas)}  Lemma records after createLemmaRecords and createWordRecords")
         
      # total_words_for_analysis = Word.objects.all()
      # print(f"There are a total of  {len(total_words_for_analysis)}  Word records after createWordRecords and createLemmaRecord")
   

      #lemmas with resorded lemma sentences as anchor
      called = 0
      for lemma_sentence in lemma_sentence_records: 
         prev_obj = getattr(lemma_sentence , 'previous_sentence', None) # related previous sentence 1:1 relation
         fol_obj = getattr(lemma_sentence , 'following_sentence', None) # related following sentence 1:1 relation
         #print(f"For lemma sentence with ID: {lemma_record_obj.findingID} \n the sentence is: {lemma_record_obj.lemma_sentence} \n The previous sentence is: {prev_obj.previous_sentence} \n the following is {fol_obj.following_sentence} ")
         lemma_sentence_lemma_records =  lemma_sentence.analysis_focus.all()
         lemma_objects_previous_record = prev_obj.previous.all() # lemmas related  previous sentence  1:m
         lemma_objects_following_record =  fol_obj.following.all() # lemmas related following sentence 1:m
         #encure lenght of 0 if no lemmas and not None Type
         if  lemma_objects_previous_record == None:
               lemma_objects_previous_record = []
         if lemma_objects_following_record  == None:
            lemma_objects_following_record = []

         dot = graphviz.Digraph(comment='First visualisation of lemmas') # one figure per lemma_record_obj
         
         sentence_for_visualization_ID = lemma_sentence.findingID  #key ID for current analytical context
         sentence_lemma =  lemma_sentence.lemma # consta
         print(f"Sentens ID {sentence_for_visualization_ID } with lemma {sentence_lemma} and {len(lemma_sentence_lemma_records )} records of lemmas" )
         called = called + 1
         visualize_sentence_lemmas(lemma_sentence_lemma_records, lemma_sentence)
       
      
      print(f"visualize_sentence_lemmas was called {called} times")
      

         # 
         # return  svg_string

         #lemmas for lemma_record_obj
         #make  figures for lemmas as figure A, B, C ......... 
       
         # 
      
    
      #Check that visualization records are build
      # visualization_records  =  VisualizationOfLemmaSentence.objects.all()  
      # print(f"Found creation of {len(visualization_records)} visualization records")          
               
         # for index, lemma_object_lemma_record in enumerate(lemma_objects_lemma_records):
         #    position =  lemma_object_lemma_record.lemma_position  #figure out how to show this in figure (other than combining with sentence_lemma). If more than one lemma len(lemma_objects_lemma_records) > 1 Is it possible use position difference as length of connection
         #    figure_number = index + 1
         #    figur_letter = number_to_letter(figure_number )
         #    print(f"The figure letter is {figur_letter}")
         #    dot.node(figur_letter, sentence_lemma)
         # #make  edges between figures for lemmas if more than one lemma in  sentence
         # if len(lemma_objects_lemma_records) > 1:  #connections to index 0  (handled)
         #    index_of_last_lemma = len(lemma_objects_lemma_records)
         #    for level_figure_index in range(1, index_of_last_lemma):
         #       current_figure_number = level_figure_index +1
         #       print(f"index for figure at level {level_figure_index}")
         #       current_lemma = lemma_objects_lemma_records[level_figure_index].lemma
         #       current_position = lemma_objects_lemma_records[level_figure_index].lemma_position 
              
         #       previous_figur_letter = number_to_letter( current_figure_number -1) 
         #       current_figur_letter = number_to_letter( current_figure_number)  #make letters to connet current to previous 

         #       composition_figur_letter = f"{ previous_figur_letter}{current_figur_letter}"
              
         #       dot.edges([composition_figur_letter]) #  connet current to previous

         #    # 1. Hent SVG-indholdet som en streng direkte i hukommelsen
         #    svg_string_graphviz = dot.pipe(format="svg", encoding="utf-8")
         #    #svg for record (models.Model)  and use in view NOT MADE YET
         #    svg_string  = clean_svg(svg_string_graphviz) #  svg_string_graphviz from  graphviz  contains eg  doctype and  xml info
            
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

def number_to_letter(n):
  result = []
  while n > 0:
    n, remainder = divmod(n - 1, 26)
    result.append(chr(65 + remainder))
  return ''.join(reversed(result))
      
      
      
from graphviz import Graph
def visualize_sentence_lemmas(lemma_objects_lemma_records, lemma_record):
   SCALE = 0.8  # inches per position unit; increase if boxes overlap

   dot = Graph(
      engine="neato",
      graph_attr={"splines": "false"},
      node_attr={"shape": "box"},
   )

   records = sorted(lemma_objects_lemma_records, key=lambda r: r.lemma_position)

   nodes = []
   for index, rec in enumerate(records):
      name = number_to_letter(index + 1)
      x = rec.lemma_position * SCALE
      dot.node(name, rec.lemma, pos=f"{x},0!")   # "!" pins the node
      nodes.append((name, rec.lemma_position))

   # connect each node to the previous one
   for (prev_name, prev_pos), (name, pos) in zip(nodes, nodes[1:]):
      dot.edge(prev_name, name, label=str(pos - prev_pos))  # label optional
   
   svg_string_graphviz = dot.pipe(format="svg", encoding="utf-8")
   svg_string = clean_svg(svg_string_graphviz)
   VisualizationOfLemmaSentence.objects.create(sentence_and_context_svg = svg_string,
                                               related_findingID = lemma_record.findingID,)