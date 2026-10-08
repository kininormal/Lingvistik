from django.core.management.base import BaseCommand
import spacy
from pathlib import Path
import pandas as pd

from ... models import  SentenceInAnalyticalContext, VisualisationOfSentence

from .statsservices.meaning import apply_values_to_sentences

class Command(BaseCommand):

   help = 'Update data basis'

   def handle(self, *args, **kwargs):
      # Load English spaCy model
      nlp_en = spacy.load("en_core_web_sm")
      
      BASE_DIR = Path(__file__).resolve().parents[4] 
      figures = 0
      sentences_in_record = SentenceInAnalyticalContext.objects.all()
      print("Number of Sentence to build models for views: ", len( sentences_in_record) )
      for  sentence_obj in sentences_in_record:
         if sentence_obj.sentence_type == 'lemma_sentence': 
            sentence_for_analysis_ID = sentence_obj.findingID  #key ID for current analytical context
            words = sentence_obj.words.all() # lemma_sentence_for_analysis_ID
            #get related previous and following sentence (able to map lemmas adj, verbs and advebs for "full" analytical context)
                        
            previous_record = (
               SentenceInAnalyticalContext.objects
               .filter(findingID=sentence_obj.findingID)
               .first()
            )
            following_record = (
               SentenceInAnalyticalContext.objects
               .filter(findingID=sentence_obj.findingID)
               .first()
            )
            
            figures = figures + 1
            quality = 600
            svg_gramma_figure = gramma_grafical_plt(words, quality)
            print(f"Attempt to write figur number {figures} to record in model  VisualisationOfSentence")
            sentence_record_obj =  VisualisationOfSentence.objects.create(sentence_svg = svg_gramma_figure,
                                                                          sentence= sentence_obj)
           


      
         
                     
      

     
      
      self.stdout.write(self.style.SUCCESS('NOT YET Successfully build grap records.'))
      
      
   
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def gramma_grafical_plt(words, quality):
   
         fig, ax = plt.subplots(figsize=(12, 8), dpi=quality)

         xs = []
         ys = []
         print(f"Number of words in lemma")
         for w in words:
            x = float(w.graphic_X_position)
            y = float(w.graphic_Y_position)
            xs.append(x)
            ys.append(y)

            ax.text(x, y, w.word, fontsize=12, color="black", zorder=10)
            ax.text(x, y, w.wordclass, fontsize=10, color="red", alpha=0.35, zorder=20)

            ax.set_xlim(min(xs) - 10, max(xs) + 10)
            ax.set_ylim(min(ys) - 10, max(ys) + 10)
            
         offsets = {
            "ADJ": (0.3, -0.3),
           # "NOUN": (0.3, 0.3),
            "VERB": (-0.3, -0.3),
            "ADV": (-0.3, 0.3),
         }

         dx, dy = offsets.get(w.wordclass, (0.2, -0.2))
         ax.text(x + dx, y + dy, w.wordclass, ...)

         plt.tight_layout()

         buf = BytesIO()
         fig.savefig(buf, format="svg")
         svg_data = buf.getvalue().decode("utf-8")
         plt.close(fig)
         return svg_data


