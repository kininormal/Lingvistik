from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import spacy
from spacy import displacy
from . models import ParsedSentence, SentenceInAnalyticalContext
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
    #get data to vizualixe
    records = SentenceInAnalyticalContext.objects.all()
    
    # totsurvivedfig = totsurvivedplot('titanic', quality)
    gramma_figure = gramma_grafical_plt(records, 600)
    context = {"gramma_figure":  gramma_figure}  
    return render(request, 'Lingvistik_app/gramma.html')

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
      return fig_to_base64(fig, quality)
  
def fig_to_base64(fig, dpiq):
    buff = io.BytesIO()
    fig.savefig(buff, format='png', dpi= dpiq, bbox_inches="tight")
    buff.seek(0)
    string = base64.b64encode(buff.read()).decode("utf-8")
    plt.close(fig)
    plt.clf() # added
    return string