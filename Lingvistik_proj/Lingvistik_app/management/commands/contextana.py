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

   help = 'Traning Graphviz'
  
   def handle(self, *args, **kwargs):
      
      #Initializations
         #Test fase delete created ToulminVisualization
      ToulminVisualization.objects.all().delete()
         #
      lemma_sentence_records = LemmaSentence.objects.all()    
      print(f"There are {len( lemma_sentence_records )} lemma sentence records of LemmaSentence class")
         #relevant marker_categories
      for marker_category, obj  in  SENTENCEMARKERS.items():
         print(f"Found marker category: {marker_category} in  SENTENCEMARKERS")
      

      #handle ToulminVisualization of lemma record
      for lemma_sentence_obj in lemma_sentence_records: 
         prev_obj = getattr(lemma_sentence_obj , 'previous_sentence', None) 
         fol_obj = getattr(lemma_sentence_obj , 'following_sentence', None) 
         #
         # hits is List[MarkerHit]
         hits = process_triplet(lemma_sentence_obj.findingID, prev_obj.previous_sentence, lemma_sentence_obj.lemma_sentence, fol_obj.following_sentence, lemma_sentence_obj.lemma)
         print(f"lengths: {len(hits)}")
        
         #first primitive approach
         prev_intensifier_filtered = [
                  hit for hit in hits
                  if hit.sentence_position == 'previous'
                  and hit.marker_category == 'intensifier'
               ]
         
         lemma_intensifier_filtered = [
                  hit for hit in hits
                  if hit.sentence_position == 'lemma'
                  and hit.marker_category == 'intensifier'
               ]
         
         follow_intensifier_filtered = [
                  hit for hit in hits
                  if hit.sentence_position == 'following'
                  and hit.marker_category == 'intensifier'
               ]
        
         prev_intensifier_str = ''
         lemma_intensifier_str = ''
         follow_intensifier_str = ''
         if len(prev_intensifier_filtered) == 0:
            prev_intensifier_str ='NONE' 
         else:
            for prev_intensifier in prev_intensifier_filtered:
              prev_intensifier_str = f"{prev_intensifier_str}, {prev_intensifier.marker_text}"
        
         if len(lemma_intensifier_filtered) == 0:
            lemma_intensifier_str ='NONE'
         else:
            for lemma_intensifier in lemma_intensifier_filtered:
               lemma_intensifier_str  = f"{lemma_intensifier_str}, {lemma_intensifier.marker_text}"  
         
         if len(follow_intensifier_filtered) == 0:
            follow_intensifier_str ='NONE'
         else: 
            for follow_intensifier in follow_intensifier_filtered:
               follow_intensifier_str = f"{follow_intensifier_str}, {follow_intensifier.marker_text}" 
               
         print(f"prev_intensifier_str is {prev_intensifier_str}") 
         print(f" lemma_intensifier_str is {lemma_intensifier_str}")     
         print(f" follow_intensifier_str is {follow_intensifier_str}")        
      #NB NB co pilot        
      #    filtered = [
      #    hit for hit in hits
      #    if hit.relation_state == wanted_relation_state
      #    and hit.context_cat == wanted_context_cat
      # ]
         # filtering efter en 
        # relation_hits = [hit for hit in hits if hit.relation_state == "parent"]
         
         
                  
         # SENTENCEMARKERS = {
         #     "intensifier": {
         #         "very", "really", "extremely", "highly", "deeply", "utterly",
         #         "completely", "totally", "absolutely",
         #     },
         #     "downtoner": {
         #         "rather", "fairly", "quite", "somewhat", "slightly", "barely",
         #         "hardly", "almost",
         #     },
         #     "negation": {
         #         "not", "never", "neither", "nor", "no",
         #     },
         #     "hedge": {
         #         "perhaps", "probably", "possibly", "apparently", "seemingly", "maybe",
         #     },
         #     "reinforcer": {
         #         "certainly", "clearly", "indeed", "undoubtedly", "surely", "definitely",
         #     },
         #     "concession": {
         #         "but", "however", "although", "though", "yet", "nevertheless",
         #         "nonetheless", "still",
         #     },
         # }
             
         # prev_intensifier_str ='NONE'  
         # prev_downtoner_str = 'NONE'
         # prev_negation_str = 'NONE'
         # prev_hedge_str = 'NONE'
         # prev_reinforcer_str = "NONE"
         # prev_concession_str = 'NONE'
         # lemma_intensifier_str ='NONE'  
         # lemma_downtoner_str = 'NONE'
         # lemma_negation_str = 'NONE'
         # lemma_hedge_str = 'NONE'
         # lemma_reinforcer_str = "NONE"
         # lemma_concession_str = 'NONE'
         # follow_intensifier_str ='NONE'  
         # follow_downtoner_str = 'NONE'
         # follow_negation_str = 'NONE'
         # follow_hedge_str = 'NONE'
         # follow_reinforcer_str = "NONE"
         # follow_concession_str = 'NONE'
        

         graph = Digraph("toulmin_lemma")
         graph.attr(rankdir="TB", splines="polyline")
         
         #previous TEST WHERE ERRO IN LABEL
         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E9F1FA">
            <TR><TD COLSPAN="2"> <FONT FACE="Tahoma"
                  POINT-SIZE="13"
                  COLOR="#000000"><B>Previous sentence</B></FONT></TD>
            </TR>
            <TR>
               <TD PORT="strength" BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                 POINT-SIZE="11"
                 COLOR="#FFFFFF">
                 <I>Intensifiers: </I></FONT> 
               </TD>
               <TD BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                                POINT-SIZE="11"
                                COLOR="#FFFFFF">
                  {escape(str(prev_intensifier_str))}</FONT> 
               </TD>
            </TR>
            <TR>
               <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                 POINT-SIZE="11"
                 COLOR="#111111">
                 <I>Downtoners: </I>{escape(str(prev_intensifier_str))}</FONT>
               </TD>
               <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                                POINT-SIZE="11"
                                COLOR="#111111">
                  {escape(str(prev_intensifier_str))}</FONT>
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
                  {escape(str(prev_intensifier_str))}</FONT> 
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
                  {escape(str(prev_intensifier_str))}</FONT> 
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
                  {escape(str(prev_intensifier_str))}</FONT> 
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
                  {escape(str(prev_intensifier_str))}</FONT>
               </TD>
            </TR>
         </TABLE>
         >'''
         graph.node("before", #node name
                    label=label)
         
         #lemma
         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E3F2E7">
            <TR><TD><B>Lemma sentence</B></TD></TR>
             <TR> <TD BGCOLOR="#faebd7">Intensifiers: {escape(str(lemma_intensifier_str))} </TD></TR>
            <TR><TD PORT="head">  {escape(str(lemma_sentence_obj.lemma))}</TD></TR>
         </TABLE>
         >'''
         graph.node("lemma", #node name
                    label=label)

         #following
         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#FFF0DF">
            <TR><TD><B>following sentence</B></TD></TR>
              <TR><TD>Intensifiers:  {escape(str(follow_intensifier_str))} </TD></TR>
            <TR><TD PORT="rebuttal">however</TD></TR>
         </TABLE>
         >'''
         graph.node("after",  #node name
                  label=label)

         graph.edge(
            "before:strength", "lemma:head",
            label="Understøtter?",
            color="#739AC6"
         )

         graph.edge(
            "after:rebuttal", "lemma:head",
            label="Begrænser?",
            color="#D4A066",
            style="dashed",
            constraint="false"
         )
         graph.edge("lemma", "after", style="invis")
         graph.render("toulmin_lemma", format="svg", cleanup=True)
         svg_string_graphviz = graph.pipe(format="svg", encoding="utf-8")
         svg_string = svg_string_graphviz # TRY THIS then use handler in view
         #svg_string = clean_svg(svg_string_graphviz) # sting svg_string_graphviz contains eg doc type ans XML version info

         ToulminVisualization.objects.create(toulmin_svg=svg_string, related_findingID =lemma_sentence_obj.findingID, )


      toulmin_vis_records  =  ToulminVisualization.objects.all()  
      print(f" {len( toulmin_vis_records)} toulmin visualization records was created")
      
         
            
            
      
      self.stdout.write(self.style.SUCCESS('Successfully Toulmins model for argumentation to analyse eg meaning, sentiment.'))
      
def clean_svg(svg_string):
   match = re.search(r"<svg.*?</svg>",  svg_string, re.DOTALL)
      
   if match:
      svg_string = match.group(0)
   else:
      print("Ingen SVG fundet i strengen.")
   return svg_string

#NOT "str as argument" look at this
def tabel_label(prev_intensifier_str ='NONE', lemma_intensifier_str='NONE', follow_intensifier_str='NONE'): # filtered argumet or make it a function to get the filtered args
   #Template for label in graphviz Digraph node, using HTML table to format the label
     # PORT are variables to use in edge connections, see graphviz documentation
     # Previous sentence are variables to use in edge connections, see graphviz documentation
     # first version: Intensifier, Downtoner, Negation, Hedge, Reinforcer, Concession not takean as variables, but could be taken as variables in future versions
   label = f'''<
      <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
            CELLPADDING="8" BGCOLOR="#E9F1FA">
         <TR><TD COLSPAN="2"> <FONT FACE="Tahoma"
               POINT-SIZE="13"
               COLOR="#000000"><B>Previous sentence</B></FONT></TD>
         </TR>
         <TR>
            <TD PORT="strength" BGCOLOR="#0A2342"><FONT FACE="Tahoma"
               POINT-SIZE="11"
               COLOR="#FFFFFF">
               <I>Intensifiers: </I></FONT> 
            </TD>
            <TD BGCOLOR="#0A2342"><FONT FACE="Tahoma"
                              POINT-SIZE="11"
                              COLOR="#FFFFFF">
               {escape(str(prev_intensifier_str))}</FONT> 
            </TD>
         </TR>
         <TR>
            <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
               POINT-SIZE="11"
               COLOR="#111111">
               <I>Downtoners: </I>{escape(str(prev_intensifier_str))}</FONT>
            </TD>
            <TD BGCOLOR="#F5F2EB"> <FONT FACE="Tahoma"
                              POINT-SIZE="11"
                              COLOR="#111111">
               {escape(str(prev_intensifier_str))}</FONT>
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
               {escape(str(prev_intensifier_str))}</FONT> 
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
               {escape(str(prev_intensifier_str))}</FONT> 
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
               {escape(str(prev_intensifier_str))}</FONT> 
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
               {escape(str(prev_intensifier_str))}</FONT>
            </TD>
         </TR>
      </TABLE>
      >'''
   return label