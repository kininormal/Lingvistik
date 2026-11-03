from cProfile import label

from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
import spacy
from html import escape
from graphviz import Digraph
from .statsservices.directories import SENTENCEMARKERS
from ... models import  LemmaSentence, ToulminVisualization

from .statsservices.handle_useing_spacy import process_triplet
class Command(BaseCommand):

   help = 'Toulmin like model for argumentation to analyse eg meaning, sentiment.'
  
   def handle(self, *args, **kwargs):
      
      #Initializations
         #Test fase delete created ToulminVisualization
      ToulminVisualization.objects.all().delete()
         # get records from LemmaSentence model, to handle ToulminVisualization of lemma record
      lemma_sentence_records = LemmaSentence.objects.all()    

      #handle ToulminVisualization of lemma record
      for lemma_sentence_obj in lemma_sentence_records: 
         prev_obj = getattr(lemma_sentence_obj , 'previous_sentence', None) 
         fol_obj = getattr(lemma_sentence_obj , 'following_sentence', None) 
         #
         # hits is List[MarkerHit]
         hits = process_triplet(lemma_sentence_obj.findingID, prev_obj.previous_sentence, lemma_sentence_obj.lemma_sentence, fol_obj.following_sentence, lemma_sentence_obj.lemma)
     
         #prepare the context for the three sentences, previous, lemma and following sentence
         prev_filtered, lemma_filtered, follow__filtered = sentence_context(hits)
      
         #make figure content start primitive approach to get intensifiers and downtoners from previous sentence context
         prev_label, lemma_label, follow_label = tabel_labels(prev_filtered, lemma_filtered, follow__filtered, SENTENCEMARKERS) #possible to get current category  intensifiers, downtoners, negations, hedges, reinforcers, concessions fram SENTENCEMARKERS
         
         #make graphviz Digraph for Toulmin model of argumentation, to analyse eg meaning, sentiment.
         graph = Digraph("toulmin_lemma")
         graph.attr(rankdir="TB", splines="polyline")
         
         graph.node("before", #node name
                    label= prev_label,
                    penwidth="3",
                    style="solid",
                    color="#000000",)
        
         graph.node("lemma", #node name
                   label=lemma_label,
                   penwidth="3",
                   style="solid",
                   color="#009900",)

    
         graph.node("after",  #node name
                  label= follow_label,
                  penwidth="3",
                  style="solid",
                  color="#000000",)

         graph.edge(
            "before:strength", "lemma:head",
            label="Folloewd by",
            color="#739AC6",
            penwidth="3",
            style="solid",
         )

         graph.edge(
            "after:rebuttal", "lemma:head",
            label="Folloewd by",
            color="#D4A066",
            penwidth="3",
            style="dashed",
            constraint="false"
         )
         graph.edge("lemma", "after", style="invis")
         svg_string_graphviz = graph.pipe(format="svg", encoding="utf-8") #handle raw svg string from graphviz,in view 
         ToulminVisualization.objects.create(toulmin_svg= svg_string_graphviz, related_findingID =lemma_sentence_obj.findingID, )

      toulmin_vis_records  =  ToulminVisualization.objects.all()  
      print(f" {len( toulmin_vis_records)} toulmin visualization records was created")
      
      self.stdout.write(self.style.SUCCESS('Successfully Toulmins model for argumentation to analyse eg meaning, sentiment.'))
      

def sentence_context(hits):
   prev_filtered = [
      hit for hit in hits
      if hit.sentence_position == 'previous'
   ]
            
   lemma_filtered = [
      hit for hit in hits
      if hit.sentence_position == 'lemma'
   ]

   follow__filtered = [
      hit for hit in hits
      if hit.sentence_position == 'following'
   ]
   
   return prev_filtered, lemma_filtered, follow__filtered


def tabel_labels(prev_sentence_ctx ='NONE', lemma_sentence_ctx='NONE', follow_sentence_ctx='NONE', SENTENCEMARKERS=None): # filtered argumet or make it a function to get the filtered args

   # primitive approach -> custermation of label for previous, lemma and following sentence context high: ability to handle individual marker categories
   prev_table_label = prev_tabel_label(prev_sentence_ctx =prev_sentence_ctx, port_name='strength', SENTENCEMARKERS=SENTENCEMARKERS) # sentencemarkers not used yet
   lemma_table_label = lemma_tabel_label(lemma_sentence_ctx =lemma_sentence_ctx, port_name='head', SENTENCEMARKERS=SENTENCEMARKERS) # sentencemarkers not used yet
   follow_table_label = follow_tabel_label(follow_sentence_ctx =follow_sentence_ctx, port_name='rebuttal', SENTENCEMARKERS=SENTENCEMARKERS) # sentencemarkers not used yet
   
   return prev_table_label, lemma_table_label, follow_table_label 

def marker_category_str(marker_category, sentence_ctx):
   filtered = [
      ctx for ctx in sentence_ctx
      if ctx.marker_category == marker_category
   ]
   return ', '.join(ctx.marker_text for ctx in filtered) if filtered else 'NONE'
         
def prev_tabel_label(prev_sentence_ctx ='NONE', port_name='strength', SENTENCEMARKERS=None): 
   prev_intensifier_str = marker_category_str('intensifier', prev_sentence_ctx)
   prev_downtoner_str = marker_category_str('downtoner', prev_sentence_ctx)
   prev_negation_str = marker_category_str('negation', prev_sentence_ctx)
   prev_hedge_str = marker_category_str('hedge', prev_sentence_ctx)
   prev_reinforcer_str = marker_category_str('reinforcer', prev_sentence_ctx)
   prev_concession_str = marker_category_str('concession', prev_sentence_ctx)
                                         
   label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E9F1FA">
            <TR><TD COLSPAN="2"> <FONT FACE="Tahoma"
                  POINT-SIZE="13"
                  COLOR="#000000"><B>Previous sentence</B></FONT></TD>
            </TR>
            <TR>
               <TD PORT="{port_name}" BGCOLOR="#0A2342">
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#FFFFFF">
                     <I>Intensifiers: </I>
                  </FONT> 
               </TD>
               <TD BGCOLOR="#0A2342">
                  <FONT FACE="Tahoma" POINT-SIZE="11"  COLOR="#FFFFFF">
                     {escape(str(prev_intensifier_str))}
                  </FONT> 
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#F5F2EB"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#111111">
                     <I>Downtoners: </I>
               </FONT>
               </TD>
               <TD BGCOLOR="#F5F2EB"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#111111">
                     {escape(str(prev_downtoner_str))}
                  </FONT>
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#EAECEE"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11"  COLOR="#2C3E50">
                     <I>Negations: </I>
                  </FONT> 
               </TD>
               <TD BGCOLOR="#EAECEE"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#2C3E50">
                     {escape(str(prev_negation_str))}
                  </FONT> 
               </TD>
            </TR>
               <TR>
               <TD BGCOLOR="#E3F2FD"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#311B92">
                     <I>Hedges: </I>
                  </FONT> 
               </TD>
               <TD BGCOLOR="#E3F2FD"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#311B92">
                     {escape(str(prev_hedge_str))}
                  </FONT> 
               </TD>
            </TR>
               <TR>
               <TD BGCOLOR="#D4EFDF"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#0B3D2E">
                     <I>Reinforcers: </I>
                  </FONT> 
               </TD>
               <TD BGCOLOR="#D4EFDF"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#0B3D2E">
                     {escape(str(prev_reinforcer_str))}
                  </FONT> 
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#FFD700"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#000000">
                     <I>Concessions: </I>
                  </FONT>
               </TD>
               <TD BGCOLOR="#FFD700"> 
                  <FONT FACE="Tahoma" POINT-SIZE="11" COLOR="#000000">
                     {escape(str(prev_concession_str))}
                  </FONT>
               </TD>
            </TR>
         </TABLE>
      >'''
   return label
def lemma_tabel_label(lemma_sentence_ctx, port_name='head', SENTENCEMARKERS=None):
   lemma_downtoner_str = marker_category_str('downtoner', lemma_sentence_ctx)
   lemma_intensifier_str = marker_category_str('intensifier', lemma_sentence_ctx)   
   lemma_negation_str = marker_category_str('negation', lemma_sentence_ctx)
   lemma_hedge_str = marker_category_str('hedge', lemma_sentence_ctx)
   lemma_reinforcer_str = marker_category_str('reinforcer', lemma_sentence_ctx)
   lemma_concession_str = marker_category_str('concession', lemma_sentence_ctx)

   label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E9F1FA">
            <TR><TD COLSPAN="2"> <FONT FACE="Tahoma"
                  POINT-SIZE="13"
                  COLOR="#000000"><B>Previous sentence</B></FONT></TD>
            </TR>
            <TR>
               <TD PORT="{port_name}" BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#FFFFFF">
                  <I>Intensifiers: </I></FONT> 
               </TD>
               <TD BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                                 POINT-SIZE="11"
                                 COLOR="#FFFFFF">
                  {escape(str(lemma_intensifier_str))}</FONT> 
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#111111">
                  <I>Downtoners: </I></FONT>
               </TD>
               <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                                 POINT-SIZE="11"
                                 COLOR="#111111">
                  {escape(str(lemma_downtoner_str))}</FONT>
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#EAECEE"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#2C3E50">
                  <I>Negations: </I></FONT> 
               </TD>
               <TD BGCOLOR="#EAECEE"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#2C3E50">
                  {escape(str(lemma_negation_str))}</FONT> 
               </TD>
            </TR>
               <TR>
               <TD BGCOLOR="#E3F2FD"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#311B92">
                  <I>Hedges: </I></FONT> 
               </TD>
               <TD BGCOLOR="#E3F2FD"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#311B92">
                  {escape(str(lemma_hedge_str))}</FONT> 
               </TD>
            </TR>
               <TR>
               <TD BGCOLOR="#D4EFDF"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#0B3D2E">
                     <I>Reinforcers: </I></FONT> 
               </TD>
               <TD BGCOLOR="#D4EFDF"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#0B3D2E">
                  {escape(str(lemma_reinforcer_str))}</FONT> 
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#FFD700"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#000000">
                  <I>Concessions: </I></FONT>
               </TD>
               <TD BGCOLOR="#FFD700"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#000000">
                  {escape(str(lemma_concession_str))}</FONT>
               </TD>
            </TR>
         </TABLE>
      >'''
   return label
def follow_tabel_label(follow_sentence_ctx, port_name='rebuttal', SENTENCEMARKERS=None):
   follow_downtoner_str = marker_category_str('downtoner', follow_sentence_ctx)
   follow_intensifier_str = marker_category_str('intensifier', follow_sentence_ctx)
   follow_negation_str = marker_category_str('negation', follow_sentence_ctx) 
   follow_hedge_str = marker_category_str('hedge', follow_sentence_ctx)
   follow_reinforcer_str = marker_category_str('reinforcer', follow_sentence_ctx)
   follow_concession_str = marker_category_str('concession', follow_sentence_ctx)   
      
   label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E9F1FA">
            <TR><TD COLSPAN="2"> <FONT FACE="Tahoma"
                  POINT-SIZE="13"
                  COLOR="#000000"><B>Previous sentence</B></FONT></TD>
            </TR>
            <TR>
               <TD BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#FFFFFF">
                  <I>Intensifiers: </I></FONT> 
               </TD>
               <TD BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                                 POINT-SIZE="11"
                                 COLOR="#FFFFFF">
                  {escape(str(follow_intensifier_str))}</FONT> 
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#111111">
                  <I>Downtoners: </I></FONT>
               </TD>
               <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                                 POINT-SIZE="11"
                                 COLOR="#111111">
                  {escape(str(follow_downtoner_str))}</FONT>
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#EAECEE"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#2C3E50">
                  <I>Negations: </I></FONT> 
               </TD>
               <TD BGCOLOR="#EAECEE"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#2C3E50">
                  {escape(str(follow_negation_str))}</FONT> 
               </TD>
            </TR>
               <TR>
               <TD BGCOLOR="#E3F2FD"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#311B92">
                  <I>Hedges: </I></FONT> 
               </TD>
               <TD BGCOLOR="#E3F2FD"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#311B92">
                  {escape(str(follow_hedge_str))}</FONT> 
               </TD>
            </TR>
               <TR>
               <TD BGCOLOR="#D4EFDF"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#0B3D2E">
                     <I>Reinforcers: </I></FONT> 
               </TD>
               <TD BGCOLOR="#D4EFDF"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#0B3D2E">
                  {escape(str(follow_reinforcer_str))}</FONT> 
               </TD>
            </TR>
            <TR>
               <TD  PORT="{port_name}" BGCOLOR="#FFD700"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#000000">
                  <I>Concessions: </I></FONT>
               </TD>
               <TD BGCOLOR="#FFD700"> <FONT FACE="Tahoma"
                  POINT-SIZE="11"
                  COLOR="#000000">
                  {escape(str(follow_concession_str))}</FONT>
               </TD>
            </TR>
         </TABLE>
      >'''
   return label
       
             