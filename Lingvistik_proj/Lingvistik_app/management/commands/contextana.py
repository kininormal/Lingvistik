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
      init_viz_records, details =  ToulminVisualization.objects.all().delete()
      print(f"TEST FASE Initialized to {init_viz_records} Toulmin visualizationrecords")
  
      lemma_sentence_records = LemmaSentence.objects.all()    
      print(f"There are {len( lemma_sentence_records )} lemma sentence records of LemmaSentence class")
      for lemma_sentence_obj in lemma_sentence_records: 
         prev_obj = getattr(lemma_sentence_obj , 'previous_sentence', None) 
         fol_obj = getattr(lemma_sentence_obj , 'following_sentence', None) 
         #
         # First lemma_sentence
         #
         # hits is List[MarkerHit]
         hits = process_triplet(lemma_sentence_obj.findingID, prev_obj.previous_sentence, lemma_sentence_obj.lemma_sentence, fol_obj.following_sentence, lemma_sentence_obj.lemma)
         print(f"length of hits: {len(hits)}")
         # for hit in hits:
         #    #can I read a MarkerHit obj directly
         #    print(f"Handle this to be visualized with the following setup")
         #    print(f"For {hit.sentence_position} sentence there are word {hit.marker_text} with category  {hit.marker_category}")
         
         #get all current categories of meaning modifiers 
         
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
             
         prev_intensifier_str ='NONE'  
         prev_downtoner_str = 'NONE'
         prev_negation_str = 'NONE'
         prev_hedge_str = 'NONE'
         prev_reinforcer_str = "NONE"
         prev_concession_str = 'NONE'
         lemma_intensifier_str ='NONE'  
         lemma_downtoner_str = 'NONE'
         lemma_negation_str = 'NONE'
         lemma_hedge_str = 'NONE'
         lemma_reinforcer_str = "NONE"
         lemma_concession_str = 'NONE'
         follow_intensifier_str ='NONE'  
         follow_downtoner_str = 'NONE'
         follow_negation_str = 'NONE'
         follow_hedge_str = 'NONE'
         follow_reinforcer_str = "NONE"
         follow_concession_str = 'NONE'
         for hit in hits:
            match  hit.sentence_position:
               case 'previous':
                  print(f"Relate to previous sentence")  
               case 'lemma':
                  print(f"Relate lemma sentence")  
               case 'following':
                  print(f"Relate to following sentence") 
               case _:
                  print(f"UNKNOWEN ") 

         graph = Digraph("toulmin_lemma")
         graph.attr(rankdir="TB", splines="polyline")
         
         #previous
         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E9F1FA">
            <TR><TD><B>Previous sentence</B></TD></TR>
            <TR><TD PORT="strength">certainly</TD></TR>
         </TABLE>
         >'''
         graph.node("before", #node name
                    label=label)
         
         #lemma
         label = f'''<
         <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0"
               CELLPADDING="8" BGCOLOR="#E3F2E7">
            <TR><TD><B>Lemma sentence</B></TD></TR>
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
         svg_string = clean_svg(svg_string_graphviz) # sting svg_string_graphviz contains eg doc type ans XML version info

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