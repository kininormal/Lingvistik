from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
from graphviz import Digraph
from ... models import  LemmaSentence, Lemma, Word, VisualizationOfLemmaSentence
class Command(BaseCommand):

   help = 'Traning Graphviz'
  
   def handle(self, *args, **kwargs):
      #clean  VisualizationOfLemmaSentence
      init_viz_records =  VisualizationOfLemmaSentence.objects.all().delete()
      print(f"Initialized to {len( init_viz_records )} visualizationrecords of LemmaSentence before creating visualizationrecords")
      
      
      #Build graph form lemma(s) as gramma relasts to lemma
      lemma_sentence_records = LemmaSentence.objects.all()
      lemma_records  = Lemma.objects.all()
      word_records = Word.objects.all()
            
      print(f"There are {len( lemma_sentence_records )} lemma sentence records of LemmaSentence class")
      print(f"There are a total of  {len( lemma_records  )} lemma records  and {len(word_records)} word records")
      
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
         #print(f"Sentens ID {sentence_for_visualization_ID } with lemma {sentence_lemma} and {len(lemma_sentence_lemma_records )} records of lemmas" )
         called = called + 1
         visualize_sentence_lemmas(lemma_sentence_lemma_records, lemma_sentence)
         
      
      print(f"visualize_sentence_lemmas was called {called} times")
      
      visualization_records = VisualizationOfLemmaSentence.objects.all()
      print(f"There are {len(visualization_records )} records with  visualization of lemmas after visualize_sentence_lemmas" )

         
      
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
   W_SCALE = 1.0
   has_more_than_one_lemma = False

   if(len(lemma_objects_lemma_records)) > 1:
      has_more_than_one_lemma = True
   
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
      has_more_than_one_lemma = True
      dot.edge(prev_name, name, label=str(pos - prev_pos))  # label optional
   #word records to relate to lemma
   #
   # level 2 connections to  lemmas
   #
   word_records = lemma_record.words_analysis_focus.all()
   #start by only considering sentences with one lemma - NO need to use spacy and sentence to figure out witch lemma the word relate to -> "modify" (adjektive adverb)
   if  has_more_than_one_lemma == False:
   #only one name otherwise nanes are in  nodes.append((name, rec.lemma_position))
      #relate words to lemma. sort words by  position  Show  word,  position and  wordclass 
      #place according to  position myby length of connection 
      for index, w_rec in enumerate( word_records):
          w_name = number_to_letter(index + 1)
          w_name =  w_name + '1'  # add 1 name to avoid AA problems
          x  = w_rec.position * W_SCALE
          dot.node(w_name , w_rec.word, pos=f"{x},0!")   # "!" pins the node
          dot.edge(name,  w_name , constraint='false') 
   else:
     print("MORE THAN ONE LEMMA NOT HANDELD YET")
   
   
   
   svg_string_graphviz = dot.pipe(format="svg", encoding="utf-8")
   svg_string = clean_svg(svg_string_graphviz)
   VisualizationOfLemmaSentence.objects.create(sentence_and_context_svg = svg_string,
                                               related_findingID = lemma_record.findingID,)