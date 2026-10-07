import matplotlib.pyplot as plt
from ..models import SentenceInAnalyticalContext


import io
import base64
def fig_to_base64(fig, dpiq):
    buff = io.BytesIO()
    fig.savefig(buff, format='png', dpi= dpiq, bbox_inches="tight")
    buff.seek(0)
    string = base64.b64encode(buff.read()).decode("utf-8")
    plt.close(fig)
    plt.clf() # added
    return string
def make_grafical_presentation(records):
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
            x = w.grafical_X_position
            y = w.grafical_Y_position

            # Lag 1: selve ordet
            ax.text(
               x, y, w.word,
               fontsize=12,
               color="black",
               zorder=10
            )

            # Lag 2: grammatisk klasse (transparent)
            ax.text(
               x, y, w.wordclass,
               fontsize=10,
               color="red",
               alpha=0.35,     # ← gør det transparent
               zorder=20       # ← ligger ovenpå ordet
            )

      # plt.gca().invert_yaxis()  # hvis du bruger tekst‑koordinater som i NLP
      plt.tight_layout()
    
      fig = plt.gcf()
      return fig_to_base64(fig, 600)
      
            # words_in_previous_sentence = previous_record.words_in_sentence 
            # words_in_following_sentence =   following_record.words_in_sentence
            # total_number_of_words = record.words_in_sentence +  words_in_previous_sentence + words_in_following_sentence
            # print(f"Total number of words in the context of the analysis for sentence record ID: {record.findingID} is: {total_number_of_words}")
            # for word in words: #lemma sentence words are registered in the database as WordObjectForAnalysis objects, and linked to the SentenceInAnalyticalContext object, so it is possible to get the words for the lemma sentence from the database, and it is not necessary to get the words for the previous and following sentences, because they are not necessary for the analysis
            #    print(f"Word record ID: {word.id}, word: {word.word}, wordclass: {word.wordclass}, position: {word.position}, sentence ID: {word.sentence.findingID}")
            #    x = word.position_x

               
            #    current_word = word.word
            #    current_gramma = word.wordclass # spacy abbreviation Current only adjective, verb or adverb in record
            #    word_grafical_X_position = word.grafical_X_position # word position
            #    word_grafical_Y_position =  word.grafical_Y_position # 0  lemma sentence
            # previous_words = previous_record.words.all()
            # print(f"Found {len(previous_words)} previous words in gramma classes for analysis")
            # following_words = following_record.words.all() 
            # print(f"Found {len(following_words)} following words in gramma classes for analysis")
            # lemmas = record.lemmas.all() #lemma sentence lemmas are registered in the database as LemmaObjectForAnalysis objects, and linked to the SentenceInAnalyticalContext object, so it is possible to get the lemmas for the lemma sentence from the database, and it is not necessary to get the lemmas for the previous and following sentences, because they are not necessary for the analysis
            # for lemma in lemmas: 
            #    print(f"Lemma record ID: {lemma.id}, lemma: {lemma.lemma}, lemma_position: {lemma.lemma_position}, sentence ID: {lemma.sentence.findingID}")
   else:
      print("Test fase records was empy- use build_view_models to build records")