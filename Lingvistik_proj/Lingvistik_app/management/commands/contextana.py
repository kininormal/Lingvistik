from django.core.management.base import BaseCommand
from collections import defaultdict
from pathlib import Path
import re
import graphviz  
import spacy
from html import escape
from graphviz import Digraph
from ... models import  LemmaSentence

from .statsservices.handle_useing_spacy import process_triplet
class Command(BaseCommand):

   help = 'Traning Graphviz'
  
   def handle(self, *args, **kwargs):

  
      lemma_sentence_records = LemmaSentence.objects.all()    
      print(f"There are {len( lemma_sentence_records )} lemma sentence records of LemmaSentence class")
      for lemma_sentence_obj in lemma_sentence_records: 
         prev_obj = getattr(lemma_sentence_obj , 'previous_sentence', None) 
         fol_obj = getattr(lemma_sentence_obj , 'following_sentence', None) 
        
         
         # hits is List[MarkerHit]
         hits = process_triplet(lemma_sentence_obj.findingID, prev_obj.previous_sentence, lemma_sentence_obj.lemma_sentence, fol_obj.following_sentence, lemma_sentence_obj.lemma)
         
         print(f"length of hits: {len(hits)}")
         for hit in hits:
            #can I read a MarkerHit obj directly
            print(f"Modifyer  {hit.marker_text} with category  {hit.marker_category}  occured in {hit.sentence_position}. Distance to lemma (negatie if in previous) { hit.distance}")
            
         
         

        
         
     
      
         
            
      
      self.stdout.write(self.style.SUCCESS('Successfully Toulmins model for argumentation to analyse eg meaning, sentiment.'))
      
