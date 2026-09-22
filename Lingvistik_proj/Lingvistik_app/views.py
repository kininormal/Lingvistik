from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import spacy
from spacy import displacy
from . models import ParsedSentence

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
    
    context = {'page_obj': page_obj}
    
    return render(request, 'Lingvistik_app/treesentences.html', context)

    
    
    