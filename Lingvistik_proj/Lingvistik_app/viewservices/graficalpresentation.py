import matplotlib.pyplot as plt
from ..models import SentenceInAnalyticalContext
import matplotlib.pyplot as plt
import io
import base64


def gramma_grafical_plt(records, quality):
   print("Number of Sentence records from works to build graphics: ", len(records) )
   
   if len(records) > 0:
      for record in records:
         #print(f"Record ID: {record.id}, sentence: {record.sentence}, contains_lemma: {record.contains_lemma}, sentence_type: {record.sentence_type}, words_in_sentence: {record.words_in_sentence}")
         
         print(f"Sentence record ID: {record.findingID}, sentence: {record.sentence}, contains_lemma: {record.contains_lemma}, sentence_type: {record.sentence_type}, words_in_sentence: {record.words_in_sentence}")
         #Use the sentence_type lemma as anchor to get the words and lemmas for the sentence, because it is not necessary to get the words and lemmas for the previous and following sentences, because they are not necessary for the analysis, and it is not necessary to get the words and lemmas for the previous and following sentences, because they are not necessary for the analysis
         if record.sentence_type == 'lemma_sentence': 
            lemma_sentence_for_analysis_ID = record.findingID  #key ID for current analytical context
            words = record.words.all() # lemma_sentence_for_analysis_ID
            #get related previous and following sentence (able to map lemmas adj, verbs and advebs for "full" analytical context)
            
            previous_record = (
               SentenceInAnalyticalContext.objects
               .filter(findingID=record.findingID)
                  .first()
            )
            following_record = (
               SentenceInAnalyticalContext.objects
                  .filter(findingID=record.findingID)
               .first()
            )


            fig, ax = plt.subplots(figsize=(10, 8))

            for w in words:
                x = w.graphic_X_position
                print(f"graph x {x} ")
                y = w.graphic_Y_position
                print(f"graph y {y} ")
                
                # Layer 1: the word
                ax.text(
                x, y, w.word,
                 fontsize=12,
                 color="black",
                  zorder=10
                )

                # Layer 2: gramma class (transparent)
                ax.text(
                  x, y, w.wordclass,
                  fontsize=10,
                  color="red",
                  alpha=0.35,     # ← gør det transparent
                  zorder=20       # ← ligger ovenpå ordet
             )

      # plt.gca().invert_yaxis()  # hvis du bruger tekst‑koordinater som i NLP
      #plt.tight_layout()
    
      fig = plt.gcf()
      return fig_to_base64(fig, quality)
  
def fig_to_base64(fig, dpiq):
    buff = io.BytesIO()
    fig.savefig(buff, format='png', dpi= dpiq, bbox_inches="tight")
    buff.seek(0)
    string = base64.b64encode(buff.read()).decode("utf-8")
    plt.close(fig)
    plt.clf() # added
    return string