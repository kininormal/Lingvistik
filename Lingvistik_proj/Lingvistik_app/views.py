from django.shortcuts import render, HttpResponse, redirect

import spacy
from spacy import displacy
from . models import ParsedSentence

# Indlæs modellen én gang (globalt i filen for bedre ydeevne)
nlp_en = spacy.load("en_core_web_sm")
# Create your views here.
def index(request):
    
    #https://www.geeksforgeeks.org/python/django-orm-inserting-updating-deleting-data/
    sentence_obj_holder = ParsedSentence.objects.all()
    print("sentences in sentence_obj_holder ", len(sentence_obj_holder))
    sentencediagramNr = 0
    text = "Django gør det nemt at integrere spacy."
    for sentenceElement in  sentence_obj_holder:
        sentencediagramNr =  sentencediagramNr +1
        svg_html = sentenceElement.svg_html
  
        #make variable 
        sentencevariable  = f"sentence_{sentencediagramNr}"
        context = f"context_{sentencediagramNr}"
        context = {
                sentencevariable: svg_html
            }
    sentencediagramNr = 0
    for showSentence in range(sentencediagramNr):
        #sentencediagramNr = sentencediagramNr +1
        #if sentencediagramNr == 1
        #  context = f"context_{sentencediagramNr}"
        #elif:
        # context = context|f"context_{sentencediagramNr}"
        pass
    
    doc = nlp_en(text)
    
    # Generer den rå HTML/SVG-streng
    svg_html = displacy.render(doc, style="dep", page=False)
    
    context = {
        'dependency_chart': svg_html
    }
    return render(request, 'Lingvistik_app/index.html', context)
    