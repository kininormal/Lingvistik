from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
import spacy
from html import escape
from graphviz import Digraph
from ... models import  LemmaSentence, Lemma, Word, VisualizationOfLemmaSentence

from .statsservices.handle_useing_spacy import find_wordclass_lemma_relations
class Command(BaseCommand):

   help = 'Traning Graphviz'
  
   def handle(self, *args, **kwargs):
      #clean  VisualizationOfLemmaSentence
      init_viz_records, details =  VisualizationOfLemmaSentence.objects.all().delete()
      print(f"TEST FASE Initialized to {init_viz_records} visualizationrecords of LemmaSentence before creating visualizationrecords")
      
    
      #Build graph form lemma(s) as gramma relasts to lemma
      lemma_sentence_records = LemmaSentence.objects.all()
      lemma_records  = Lemma.objects.all()
      word_records = Word.objects.all()
            
      print(f"There are {len( lemma_sentence_records )} lemma sentence records of LemmaSentence class")
      print(f"There are a total of  {len( lemma_records  )} lemma records  and {len(word_records)} word records")
      
      #lemmas with resorded lemma sentences as anchor
     
      for lemma_sentence in lemma_sentence_records: 
         #prepare to visualize related previous and following sentence
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

         sentence_for_visualization_ID = lemma_sentence.findingID  #key ID for current analytical context
         sentence_lemma =  lemma_sentence.lemma # consta
         #print(f"Sentens ID {sentence_for_visualization_ID } with lemma {sentence_lemma} and {len(lemma_sentence_lemma_records )} records of lemmas" )
       
         visualize_sentence_lemmas(lemma_sentence_lemma_records, lemma_sentence)
         
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
  
   #initialize
   nlp_en = spacy.load("en_core_web_sm")
   has_more_than_one_lemma = False
   if(len(lemma_objects_lemma_records)) > 1:
      has_more_than_one_lemma = True
   records = sorted(lemma_objects_lemma_records, key=lambda r: r.lemma_position)
   g = graphviz.Digraph('G')
   nodes = []
   
   
   for index, rec in enumerate(records):
      name = number_to_letter(index + 1)


      g.attr(bgcolor='purple', label='lemma', fontcolor='white')
      

      with g.subgraph(name='cluster_description') as c:
         c.attr(
            fillcolor='blue',
            label='Decription',
            fontcolor='white',
            style='filled'
         )

         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="6" BGCOLOR="white">
            <TR>
                  <TD ALIGN="LEFT"><B>Lemma:</B></TD>
                  <TD ALIGN="LEFT"><I>{escape(str(rec.lemma))}</I></TD>
            </TR>
            <TR>
                  <TD ALIGN="LEFT"><B>Position:</B></TD>
                  <TD ALIGN="LEFT">{escape(str(rec.lemma_position))}</TD>
            </TR>
         </TABLE>
         >'''
         lemma_node_name = f'record_{name}'

         c.node(
         lemma_node_name,
         label=label,
         shape='plain',
         fontname='Arial',
         fontsize='12'
   )
        
   # if more than one lemma in sentence connect  (records is sorted by lemma position )
   
   if len(records) > 1:
      print(f"More than one lemma in sentence wiht id {lemma_record.findingID}")
      
      for rec_index in range(1, len(records)):
         prev_index_name =  rec_index  # name of node is index + 1
         prev_index_name = f'record_{prev_index_name}'
         next_index_name  = rec_index +  1 # name of node is index + 1
         prev_index_name = f'record_{next_index_name}'
         g.edge(prev_index_name ,  prev_index_name)  # connect lemma (line same level )
   #
   # level 2 word records to relate to lemma 
   # see structs.py https://graphviz.readthedocs.io/en/stable/examples.html
   word_records = lemma_record.words_analysis_focus.all()
   #sort word_records according to position
   word_records = sorted( word_records, key=lambda r: r.position)
   #start by only considering sentences with one lemma - NO need to use spacy and sentence to figure out witch lemma the word relate to -> "modify" (adjektive adverb)
   g.attr(rankdir='LR')
   if  has_more_than_one_lemma == False:  # only one lemma with one node name to connet words to  
   #only one name otherwise nanes are in  nodes.append((name, rec.lemma_position))
      #relate words to lemma. sort words by  position  Show  word,  position and  wordclass 
      #place according to  position myby length of connection 
      for index, w_rec in enumerate( word_records):
         unique_word_id = w_rec.pk
         w_node_name = number_to_letter(unique_word_id)
         w_node_name = w_node_name + '1'  #string version af hierarkisk nummerering. Sikre: Trods at fx AA aldrig nås for lemmaer  -max tre lemma observeret i sætning - sikres for at det kan ske 
       
         with g.subgraph(name='cluster_word_description') as c:
            c.attr(
               fillcolor='blue',
               label='Decription',
               fontcolor='white',
               style='filled'
            )
      
            label = f'''<
            <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
                  CELLPADDING="6" BGCOLOR="white">
               <TR>
                  <TD ALIGN="LEFT"><B>Word:</B></TD>
                  <TD ALIGN="LEFT"><I>{escape(str(w_rec.word))}</I></TD>
               </TR>
               <TR>
                  <TD ALIGN="LEFT"><B>Word class:</B></TD>
                  <TD ALIGN="LEFT">{escape(str(w_rec.wordclass))}</TD>
               </TR>
               <TR>
                  <TD ALIGN="LEFT"><B>Position:</B></TD>
                  <TD ALIGN="LEFT">{escape(str(w_rec.position))}</TD>
               </TR>
            </TABLE>
            >'''
                  
            word_node_name = f'record_{w_node_name}'

            c.node(
               word_node_name,
               label=label,
               shape='plain',
               fontname='Arial',
               fontsize='12'
            )
            #connet any current w_node_name to the lemma node (ONLY ONE lemma node HERE of name name ) 
            g.edge(word_node_name, lemma_node_name)  # label optional

       
   else:
      find_wordclass_lemma_relations(lemma_record, nlp_en)
     
               

     
   svg_string_graphviz = g.pipe(format="svg", encoding="utf-8")
   svg_string = clean_svg(svg_string_graphviz) # sting svg_string_graphviz contains eg doc type ans XML version info
   VisualizationOfLemmaSentence.objects.create(sentence_and_context_svg = svg_string,
                                               related_findingID = lemma_record.findingID,)
   
   
