from django.shortcuts import render, HttpResponse, redirect

import spacy
from spacy import displacy
from . models import ParsedSentence

# Indlæs modellen én gang (globalt i filen for bedre ydeevne)
nlp_en = spacy.load("en_core_web_sm")
# Create your views here.
def index(request):
    sentence_obj_holder = ParsedSentence.objects.all()
    print("sentences in sentence_obj_holder ", len(sentence_obj_holder))
    
    text = "Django gør det nemt at integrere spacy."
    doc = nlp_en(text)
    
    # Generer den rå HTML/SVG-streng
    svg_html = displacy.render(doc, style="dep", page=False)
    
    context = {
        'dependency_chart': svg_html
    }
    return render(request, 'Lingvistik_app/index.html', context)
    