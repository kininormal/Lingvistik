from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
from numpy import rec
import spacy
from html import escape
from graphviz import Digraph
from ... models import  LemmaSentence, Lemma, VisualizationOfPreviousSentence, VisualizationOfFollowingSentence,   Word, VisualizationOfLemmaSentence

from .statsservices.handle_useing_spacy import find_wordclass_lemma_relations
class Command(BaseCommand):

   help = 'Traning Graphviz'
  
   def handle(self, *args, **kwargs):
      #clean  VisualizationOfLemmaSentence
      VisualizationOfLemmaSentence.objects.all().delete()
      VisualizationOfPreviousSentence.objects.all().delete()
      VisualizationOfFollowingSentence.objects.all().delete()
     
      
    
      #Build graph form lemma(s) as gramma relasts to lemma
      lemma_sentence_records = LemmaSentence.objects.all() #Seems to contain words wiht gramma X Figure out WHY WHERE IS  LemmaSentence createded
      lemma_records  = Lemma.objects.all()
      word_records = Word.objects.all()
    
      #lemmas with resorded lemma sentences as anchor
     
      for lemma_sentence in lemma_sentence_records: 
         #get related previous and following
         prev_obj = getattr(lemma_sentence , 'previous_sentence', None) # 1:1 relation to  lemma_sentence
         fol_obj = getattr(lemma_sentence , 'following_sentence', None) # 1:1 relation to  lemma_sentence
        
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
         visualize_previous_sentence(prev_obj,  lemma_sentence, lemma_sentence_records)
         visualize_lemma_sentence(lemma_sentence_lemma_records, lemma_sentence)
         visualize_following_sentence(fol_obj,  lemma_sentence, lemma_sentence_records)
         
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
      
      
      
from graphviz import Graph, Digraph
#primitive visualization of previous sentence and related words in selected gramma classes: See that it works and then improve it to show the lemma(s) in the previous sentence and their relation to the words in selected gramma classes
def visualize_previous_sentence(prev_obj, related_lemma_sentence, lemma_sentence_records):
 #initialize
   has_more_than_one_lemma = False
   # in prev_obj only sentence for prev_obj can be accessed 
   sentence_to_check   = prev_obj.previous_sentence 
   
   lemmas_for_previous = prev_obj.previous.all()  # lemma(s) for previous sentence if any 0 to many
   
   words_for_previous = prev_obj.words_previous.all()  # words for previous sentence if any 0 to many
   
   print(f"FOR previous ther are {len(lemmas_for_previous)} lemmas and {len(words_for_previous)} words in the record")
   
   #check taht contet is aa expeted 
   
   ####Word with gramma X i the record  FIGURE OUT WHY
   for  word_previous in words_for_previous:
      print(f"For word {word_previous.word} with gramma  {word_previous.wordclass} the position is {word_previous.position}  ") 
      
   for  lemma__previous in lemmas_for_previous:
      print(f"lemma   {lemma__previous.lemma} in previous at position {lemma__previous.lemma_position}  ") 
  
  
   #WHY is something going wrong with lemma__previous.lemma  and word_previous.word
   #lemmas
   has_lemmas_for_previous = True if len(lemmas_for_previous) > 0 else False
   has_more_than_one_lemma = True if len(lemmas_for_previous) > 1 else False
   #words
   has_words_for_previous = True if len(words_for_previous) > 0 else False

   g = Digraph('G')
   g.attr(bgcolor='purple', label='Previous Sentence and related words in selected grammar classes', fontcolor='white')
   
  
   if (has_lemmas_for_previous == True) and (has_more_than_one_lemma == False):
      name = 'F'
   #only ome lemma in  lemmas_for_previous at index 0  
      with g.subgraph(name='cluster_description') as c:
               c.attr(
                  fillcolor='blue',
                  label='Lemma decription',
                  fontcolor='white',
                  style='filled'
               )
      
               label = f'''<
               <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
                     CELLPADDING="6" BGCOLOR="white">
                  <TR>
                        <TD ALIGN="LEFT"><B>Lemma:</B></TD>
                        <TD ALIGN="LEFT"><I>{escape(str( lemmas_for_previous[0].lemma ))}</I></TD>
                  </TR>
                  <TR>
                     <TD ALIGN="LEFT"><B>Position</B></TD>
                     <TD ALIGN="LEFT"><I>{escape(str(lemmas_for_previous[0].lemma_position))}</I></TD>
               </TR>
                  <TR>
                        <TD ALIGN="LEFT"><B></B></TD>
                        <TD ALIGN="LEFT"></TD>
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
      
   if  has_more_than_one_lemma == True:
      #More ttan one Lemma must be relatst BUT MUST OLSO BE MORE as more tahn one  lemma sentence
      #direct_objs, nearest_objs  = find_wordclass_lemma_relations(lemma_record, nlp_en)
      pass
      
   
   if has_words_for_previous == False:
      name = 'G'
      with g.subgraph(name='cluster_description') as c:
         c.attr(
            fillcolor='blue',
            label='Lemma decription',
            fontcolor='white',
            style='filled'
         )

         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="6" BGCOLOR="white">
            <TR>
                  <TD ALIGN="LEFT"><B>Word:</B></TD>
                  <TD ALIGN="LEFT"><I>NO WORDS FOUND</I></TD>
            </TR>
            <TR>
               <TD ALIGN="LEFT"><B>Word:</B></TD>
               <TD ALIGN="LEFT"><I>NO WORDS FOUND</I></TD>
         </TR>
            <TR>
                  <TD ALIGN="LEFT"><B>Position:</B></TD>
                  <TD ALIGN="LEFT">NO WORDS FOUND</TD>
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


   if has_words_for_previous == True:
     for index, word_prev in enumerate(words_for_previous):
        name = number_to_letter(index + 1)
        with g.subgraph(name='cluster_description') as c:
           c.attr(
              fillcolor='blue',
              label='Lemma decription',
              fontcolor='white',
              style='filled'
           )
  
           label = f'''<
           <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
                 CELLPADDING="6" BGCOLOR="white">
              <TR>
                    <TD ALIGN="LEFT"><B>Word:</B></TD>
                    <TD ALIGN="LEFT"><I>{escape(str(word_prev.word))}</I></TD>
              </TR>
              <TR>
                  <TD ALIGN="LEFT"><B>Word:</B></TD>
                  <TD ALIGN="LEFT"><I>{escape(str(word_prev.wordclass))}</I></TD>
            </TR>
              <TR>
                    <TD ALIGN="LEFT"><B>Position:</B></TD>
                    <TD ALIGN="LEFT">{escape(str(word_prev.position))}</TD>
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
         
         
   svg_string_graphviz = g.pipe(format="svg", encoding="utf-8")
   VisualizationOfPreviousSentence.objects.create(sentence_and_context_svg=svg_string_graphviz,
                                                 related_findingID = related_lemma_sentence.findingID)
   
def visualize_lemma_sentence(lemma_objects_lemma_records, lemma_record):
  
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

      g.attr(bgcolor='purple', label='Lemma and relatede words in selected gramma classes', fontcolor='white')
      
      with g.subgraph(name='cluster_description') as c:
         c.attr(
            fillcolor='blue',
            label='Lemma decription',
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
        
   if has_more_than_one_lemma == True:
   
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
               fillcolor='orange',
               label='Decription of words',
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
      # direct_objs, nearest_objs is LemmaAndRelatedWords objs contaning  lemmainf: LemmaInLemmaSentence    wordsinf:  LemmaSentenceWords  
      # contains  LemmaSentenceWords: word: str   word_position: int    gramma_class: str   gramma_related_to_word: str  gramma_related_to_word_at_pos: int is_direct_relatede: bool = False  #is_nearest: bool = False
      # class LemmaInLemmaSentence : lemma: str  lemma_position: int  lemma_pk: str  
      direct_objs, nearest_objs  = find_wordclass_lemma_relations(lemma_record, nlp_en)
      print(f"There are {len(direct_objs)} direct related to lemmas and {len( nearest_objs)} related to nearest  ")

   svg_string_graphviz = g.pipe(format="svg", encoding="utf-8")
   VisualizationOfLemmaSentence.objects.create(sentence_and_context_svg = svg_string_graphviz,
                                               related_findingID = lemma_record.findingID,)
   
   
def visualize_following_sentence(fol_obj, related_lemma_sentence, lemma_sentence_records):
  # in prev_obj only sentence for prev_obj can be accessed 
     sentence_to_check   = fol_obj.following_sentence
     
     lemmas_for_follow = fol_obj.following.all()  # lemma(s) for previous sentence if any 0 to many
     
     words_for_follow = fol_obj.words_following.all()  # words for previous sentence if any 0 to many
     
     print(f"FOR previous ther are {len(lemmas_for_follow)} lemmas and {len(words_for_follow)} words in the record")
     
   
     
     #check taht contet is aa expeted 
     
     ####Word with gramma X i the record  FIGURE OUT WHY
     for word_follow in words_for_follow:
        print(f"For word {word_follow.word} with gramma {word_follow.wordclass} the position is {word_follow.position}  ") 
        
     for lemma__follow in lemmas_for_follow:
        print(f"lemma {lemma__follow.lemma} in previous at position {lemma__follow.lemma_position}  ") 
    
    
     #WHY is something going wrong with lemma__previous.lemma  and word_previous.word
     #lemmas
     has_lemmas_for_follow = True if len(lemmas_for_follow) > 0 else False
     has_more_than_one_lemma = True if len(lemmas_for_follow) > 1 else False
     #words
     has_words_for_follow = True if len(words_for_follow) > 0 else False
  
     g = Digraph('G')
     g.attr(bgcolor='purple', label='Previous Sentence and related words in selected grammar classes', fontcolor='white')
     
    
     if (has_lemmas_for_follow == True) and (has_more_than_one_lemma == False):
        name = 'F'
     #only ome lemma in  lemmas_for_previous at index 0  
        with g.subgraph(name='cluster_description') as c:
                 c.attr(
                    fillcolor='blue',
                    label='Lemma decription',
                    fontcolor='white',
                    style='filled'
                 )
        
                 label = f'''<
                 <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
                       CELLPADDING="6" BGCOLOR="white">
                    <TR>
                          <TD ALIGN="LEFT"><B>Lemma:</B></TD>
                          <TD ALIGN="LEFT"><I>{escape(str( lemmas_for_follow[0].lemma ))}</I></TD>
                    </TR>
                    <TR>
                       <TD ALIGN="LEFT"><B>Position</B></TD>
                       <TD ALIGN="LEFT"><I>{escape(str(lemmas_for_follow[0].lemma_position))}</I></TD>
                 </TR>
                    <TR>
                          <TD ALIGN="LEFT"><B></B></TD>
                          <TD ALIGN="LEFT"></TD>
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
        
     if  has_more_than_one_lemma == True:
        #More ttan one Lemma must be relatst BUT MUST OLSO BE MORE as more tahn one  lemma sentence
        #direct_objs, nearest_objs  = find_wordclass_lemma_relations(lemma_record, nlp_en)
        pass
        
     
     if has_words_for_follow == False:
        name = 'G'
        with g.subgraph(name='cluster_description') as c:
           c.attr(
              fillcolor='blue',
              label='Lemma decription',
              fontcolor='white',
              style='filled'
           )
  
           label = f'''<
           <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
                 CELLPADDING="6" BGCOLOR="white">
              <TR>
                    <TD ALIGN="LEFT"><B>Word:</B></TD>
                    <TD ALIGN="LEFT"><I>NO WORDS FOUND</I></TD>
              </TR>
              <TR>
                 <TD ALIGN="LEFT"><B>Word:</B></TD>
                 <TD ALIGN="LEFT"><I>NO WORDS FOUND</I></TD>
           </TR>
              <TR>
                    <TD ALIGN="LEFT"><B>Position:</B></TD>
                    <TD ALIGN="LEFT">NO WORDS FOUND</TD>
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
  
  
     if has_words_for_follow == True:
       for index, word_fol in enumerate(words_for_follow):
          name = number_to_letter(index + 1)
          with g.subgraph(name='cluster_description') as c:
             c.attr(
                fillcolor='blue',
                label='Lemma decription',
                fontcolor='white',
                style='filled'
             )
    
             label = f'''<
             <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
                   CELLPADDING="6" BGCOLOR="white">
                <TR>
                      <TD ALIGN="LEFT"><B>Word:</B></TD>
                      <TD ALIGN="LEFT"><I>{escape(str(word_fol.word))}</I></TD>
                </TR>
                <TR>
                    <TD ALIGN="LEFT"><B>Word:</B></TD>
                    <TD ALIGN="LEFT"><I>{escape(str(word_fol.wordclass))}</I></TD>
              </TR>
                <TR>
                      <TD ALIGN="LEFT"><B>Position:</B></TD>
                      <TD ALIGN="LEFT">{escape(str(word_fol.position))}</TD>
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
           
 
     svg_string_graphviz = g.pipe(format="svg", encoding="utf-8")
     VisualizationOfFollowingSentence.objects.create(sentence_and_context_svg=svg_string_graphviz,
                                                   related_findingID = related_lemma_sentence.findingID) 
   