from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import spacy
from spacy import displacy
from . models import ParsedSentence, SentenceInAnalyticalContext, VisualisationOfSentence
from .management.commands.statsservices.handle_svg import prepare_svg


# Indlæs modellen én gang (globalt i filen for bedre ydeevne)
nlp_en = spacy.load("en_core_web_sm")
# Create your views here.
def index(request):
    diagramlist = []
    #https://www.geeksforgeeks.org/python/django-orm-inserting-updating-deleting-data/
    sentence_holder = ParsedSentence.objects.all()
    paginator = Paginator(sentence_holder, 20)  # Show 5 posts per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    for sentence in page_obj.object_list:
        sentence.sentence_svg_html = prepare_svg(
        sentence.sentence_svg_html)
   
    context = {'page_obj': page_obj}
    
    return render(request, 'Lingvistik_app/index.html', context)

def prevfollow(request):
    sentence_holder = ParsedSentence.objects.all()
    paginator = Paginator(sentence_holder, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    for sentence in page_obj.object_list:
            sentence.prev_sentence_svg_html = prepare_svg(
                sentence.prev_sentence_svg_html)
            sentence.sentence_svg_html = prepare_svg(
                sentence.sentence_svg_html)
            sentence.follow_sentence_svg_html = prepare_svg(
                sentence.follow_sentence_svg_html)
    
    context = {'page_obj': page_obj}
    
    return render(request, 'Lingvistik_app/prevfollow.html', context)
def treesentences(request):
    sentence_holder = ParsedSentence.objects.all()
    paginator = Paginator(sentence_holder, 20)  # Show 5 posts per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    for sentence in page_obj.object_list:
        sentence.treesentences_svg_html = prepare_svg(
            sentence.treesentences_svg_html)
       
    context = {'page_obj': page_obj}
    
    return render(request, 'Lingvistik_app/treesentences.html', context)

    
    
def gramma(request):
   visuel_sentence_holder = VisualisationOfSentence.objects.all()
   paginator = Paginator(visuel_sentence_holder , 1)  # Show 5 posts per page
   page_number = request.GET.get('page')
   try:
      page_obj = paginator.get_page(page_number)
   except PageNotAnInteger:
      page_obj = paginator.page(1)
   except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
   for sentence in page_obj.object_list:
            sentence.sentence_svg = sentence.sentence_svg
       
   context = {'page_obj': page_obj}

   return render(request, 'Lingvistik_app/gramma.html',  context)






import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64






def gramma_grafical_plt(records, quality):
   print("Number of Sentence records from works to build graphics: ", len(records) )
   #make empty fig
   fig, ax = plt.subplots(figsize=(12, 8), dpi=600)
   if len(records) > 0:
      for record in records:
         #print(f"Record ID: {record.id}, sentence: {record.sentence}, contains_lemma: {record.contains_lemma}, sentence_type: {record.sentence_type}, words_in_sentence: {record.words_in_sentence}")
         
         #print(f"Sentence record ID: {record.findingID}, sentence: {record.sentence}, contains_lemma: {record.contains_lemma}, sentence_type: {record.sentence_type}, words_in_sentence: {record.words_in_sentence}")
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
            
      ################
         
         fig, ax = plt.subplots(figsize=(12, 8), dpi=600)

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

         plt.tight_layout()

         buf = BytesIO()
         fig.savefig(buf, format="svg")
         svg_data = buf.getvalue().decode("utf-8")
         plt.close(fig)
         return svg_data

      
      
      ######################
            
            
            
#             # graphic for words 
#             for w in words:
#                 x = w.graphic_X_position
#                 print(f"graph x {x} ")
#                 y = w.graphic_Y_position
#                 print(f"graph y {y} ")
                
#                 # Layer 1: the word
#                 ax.text(
#                 x, y, w.word,
#                  fontsize=12,
#                  color="black",
#                   zorder=10
#                 )

#                 # Layer 2: gramma class (transparent)
#                 ax.text(
#                   x, y, w.wordclass,
#                   fontsize=10,
#                   color="red",
#                   alpha=0.35,     # ← gør det transparent
#                   zorder=20       # ← ligger ovenpå ordet
#                )
#             # end graphic for words
#          # end of if sentence to apply graphic for
#       #wrap up graphic for sentence to apply graphic for
#       xs = [w.graphic_X_position for w in words]
#       ys = [w.graphic_Y_position for w in words]

#       ax.set_xlim(min(xs) - 10, max(xs) + 10)
#       ax.set_ylim(min(ys) - 10, max(ys) + 10)


#       # plt.gca().invert_yaxis()  # hvis du bruger tekst‑koordinater som i NLP
#       plt.tight_layout()
    
#       fig = plt.gcf()
#       #ax.text(x=1.0, y=4.0, s="Records to visualize gramma for found", fontsize=12, color="blue")
#       return svg_fig(fig)
#    else:
#       ax.text(x=1.0, y=4.0, s="Did not find records to visualize gramma for", fontsize=12, color="red")
#       return svg_fig(fig)
  
# def svg_fig(fig):
#     buff = io.BytesIO()
#     fig.savefig(buff, format='svg')
#     buff.seek(0)
#     svg_data = buff.getvalue().decode("utf-8")
#     plt.close(fig)
#     plt.clf() # added
#     return svg_data
 
