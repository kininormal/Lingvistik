
from django.core.management.base import BaseCommand

from schemdraw import config

class Command(BaseCommand):

    def handle(self, *args, **options):

      import nltk

      print("NLTK:", nltk.__version__)
      
      import os

      print("PATH:")
      print(os.environ.get("PATH"))
      
      import spacy
      
      print("SPACY:", spacy.__version__)

      # import torch

      # print("TORCH:", torch.__version__)

      





# from django.core.management.base import BaseCommand
# import nltk
# from schemdraw import config
# import spacy
# from pathlib import Path
# import pandas as pd
# from huggingface_hub import login
# from datasets import load_dataset, get_dataset_config_names, concatenate_datasets

# from .statsservices.handle_useing_spacy import use_spacy_for_text_processing
# from .statsservices.handle_corpus_building import handle_gutenberg_corpora_build
# from .statsservices.texthandling import clean_text


# class Command(BaseCommand):

#    help = 'Update data basis'

#    def handle(self, *args, **kwargs):
#       # Load English spaCy model
#       nlp_en = spacy.load("en_core_web_sm")
#       nlp_da = spacy.load("da_core_news_sm")
#       # You can specify the quality parameter here or get it from args/kwargs
#       #create empty language_df
#       language_df = pd.DataFrame()
      
          

#       list_of_names  = [ ['head', 'body part'], ['foot', 'body part' ], ['smell', 'sensory'], ['heart', 'organ'], ['eye', 'body part'], 
#                         ['ear', 'body part'], ['nose', 'body part'], ['mouth', 'body part'], ['hand', 'body part'], ['arm', 'body part'], 
#                         ['leg', 'body part'], ['brain', 'organ'], ['liver', 'organ'], ['kidney', 'organ'], ['gut', 'organ'],
#                         ['stomach', 'organ'], ['lung', 'organ']]
      
#       import transformers
#       from transformers import pipeline
#       print("from transformers import pipeline achieved")
#       subjectivity_classifier = pipeline(
#          "text-classification",
#          model="GroNLP/mdebertav3-subjectivity-english"
#       )
#       print("I am after  pipeline")
#       print(subjectivity_classifier(
#          "That is what you have in your head, I know and what you would certainly say if my father were not by."
#       ))
      
      
      
      
      
      
#       for part in list_of_names[:1]: #test with only two works for now -with two body names head and foot
#          designation = part[0]
#          body_category = part[1]
#          #for every designation and body_category create a new language_df with english and danish data
#          language_df = None
#          #add english text from corpus to language_df
#          language_df  = update_english_data(language_df, designation, body_category, 'English',  nlp_en)
#          #add danish text from corpus to language_df
#          # designation are in english - Tenplate for next version - not used yet - but could be used to create a more structured approach to the lexicon and translations
#          #update_danish_data(language_df, designation, body_category, 'danish') focus on engisk soo far
#          #Handle 'spacytextblob' already exists in pipeline problem - should be handled in a more efficient way later
#          # for i, row in language_df.iterrows():
#          #    text = row['Text']
#          #    polarity, subjectivity = polarity_and_subjectivity_analysis_with_spacy(text, nlp_en)
#          #    language_df.at[i, 'Polarity'] = polarity
#          #    language_df.at[i, 'Subjectivity'] = subjectivity
#          #Test only 42 rows in language_df for now - to be able to handle it in memory and not run out of memory - should be handled in a more efficient way later
#          # for i, row in language_df.iterrows():
#          #    print(f"Row {i}: tekst er {row['Text']}") # AS EXPECTED - but not the whole text - only the first 500 characters - should be handled in a more efficient way later
#          #    #Problem with 'spacytextblob' already exists in pipeline.
#          #    # print(f"Row {i}: Polarity={row['Polarity']}, Subjectivity={row['Subjectivity']}")
#       print('Language df after registration -  ONLY ENGLISH ONLY two works SO FAR:')
#       rows, columns = language_df.shape
#       print(f"Rows in main function:  {rows}")
#       print("First rows in main function:")
#       print( language_df.head())
#       print("Last rows in main function:")
#       print( language_df.tail())
         
#       self.stdout.write(self.style.SUCCESS('Successfully updated language data - just initial start.'))
# def  update_english_data(df, designation, body_category, language, nlp_lang): #LOOK at 'clean up' lang is here but then set later in work loop - should be set in function and not in loop - but for now it is set in loop
  
#    BASE_DIR = Path(__file__).resolve().parents[4] #go to Lingvistik from Lingvistik_proj/Lingvistik_app/management/commands/stats.py, 4 levels to 
#    map_name_for_sources = 'corpora/gutenberg/'
#    MY_CORPUS_PATH = BASE_DIR / map_name_for_sources
#    #Allow the path of MY_CORPUS_PATH for PlaintextCorpusReader
#    nltk.data.path.append(str(MY_CORPUS_PATH)) #DO NOT USE allowed NLTK_PATH in allowed virtual environment map - Works from NLTK are then "lost" and not found by PlaintextCorpusReader - only works for nltk.corpus.gutenberg
#    works, my_gutenberg = handle_gutenberg_corpora_build(MY_CORPUS_PATH, language)
   
  
#    #loop though works and process each work   
#    for work in works[:1]: #can be limited to n works with works[:n] does it wok outside NTLK 18 works and 12 works from my_gutenberg - total 30 works - can be limited to n works with works[:n] does it wok outside NTLK 18 works and 12 works from my_gutenberg - total 30 works
#       # ----------------------------------
#       # Build basis for English language data for current work
#       # ----------------------------------
#       df = handle_current_english_work(df,my_gutenberg, work, designation, body_category, nlp_lang)
#       #fileid source and language  are knowen in work
    
      
   
#    #export to excel
#    rows, columns = df.shape
#    print(f"Rows in function for english ALL handled works:  {rows}")
#    print("English language data updated!")
#    return df
# def update_danish_data(df,  designation, body_category, lang):
#    print("Starting to update Danish language data...")
#    dataset_name = "danish-foundation-models/danish-gigaword"
#    configs = get_dataset_config_names(dataset_name)

#    # 2. Loop igennem og hent "train"-splittet for hver kilde
#    all_data = {}
#    for config in configs:
#       # Vi springer 'default' over, hvis du vil hente de specifikke kilder rent
#       if config == "default":
#          continue
#       all_data[config] = load_dataset(dataset_name, name=config, split="train")
      
#    print(f"Fetched {len(all_data)} subsets from the Danish Gigaword dataset.")
#    # Samler alle de hentede subsets til ét stort datasæt
#    full_danish_gigaword = concatenate_datasets(list(all_data.values()))
#    print(f"Total number of samples in full Danish Gigaword dataset: {len(full_danish_gigaword)}")
   
#    #Build basis for danish language data
#    # Implement the logic to update Danish language data here
#    #Danish sets
#    sampleLst = []
#    danish_set = load_dataset(dataset_name, split = "train")
#    sample = danish_set[1] # see "Data Instances" below
#    print('danish set index 1 keys', sample.keys())
#    print('danish text index 1', sample["text"][:500])
#    #next_sample  = danish_set[2]
#    #print('danish set index 2 keys', next_sample.keys())
#    #print('danish text index 2', next_sample["text"][:500])
#    #Take first 10
#    sampleLst = list(danish_set.take(100))  # 100 første elementer
#    for memberNr, sampleMember in enumerate(sampleLst):
#       words = nltk.word_tokenize(sampleMember["text"], language=lang)
#       text_obj = nltk.Text(words)
#       print(f"--- Sample {memberNr} ---")
#       text_obj.concordance(designation)


#    print("Danish language data updated! - no implementation yet  testing it seems to work danis not handled")



# def handle_current_english_work(df, my_gutenberg, work, designation, body_category, nlp_lang):
#    source = work["source"]
#    lang = work["language"]
#    name_of_work = work["fileid"]
#    # ----------------------------------
#    # Clean text according to Gutenberg corpus
#    # ----------------------------------
#    if source == "NLTK Gutenberg":       
#       raw_text = nltk.corpus.gutenberg.raw(name_of_work)          
#       text = clean_text(raw_text)
#    elif source == "Project Gutenberg":              
#       raw_text =  my_gutenberg.raw(name_of_work)          
#       text = clean_text(raw_text)
#    else:          
#       print(f"PROBLEM: Unknown source: {source}. Skipping work: {name_of_work}")        
#       return df  # Skip processing for unknown sources
   
#    # ----------------------------------
#    # Process text with spaCy
#    # ----------------------------------
#    data = use_spacy_for_text_processing(text, name_of_work, source, designation, body_category, lang, nlp_lang)
#    # ----------------------------------
#    # Create dataframe
#    # ----------------------------------
#    new_data = pd.DataFrame(
#       data,
#          columns=[
#             'Text',
#             'Found word',
#             'Lemma',
#             'Sentences polarity',
#             'Sentences subjectivity',
#             'Chars polarity',
#             'Chars subjectivity',
#             'Three sentences polarity',
#             'Three sentences subjectivity',
#             'Designation',
#             'Body category',
#             'Language',
#             'Source',
#             'Name of work'
#          ]
#    )
#    #Here 'Text' is the sentence where the word was found, 'Found word' is the actual word found, 'Lemma' is the base form of the word, 'Body name' is the designation (e.g., head, foot), 'Body category' is the category of the body part (e.g., organ, sensory), 'Language' is the language of the text, 'Source' is where the text came from (e.g., NLTK Gutenberg, Project Gutenberg), and 'Name of work' is the identifier for the specific work in the corpus.
#    #WRONG PLACE - should be done for each sentence and not for the whole text - but for now it is done for the whole text - should be done in the loop above for each sentence
#    # print("Type of new_data:", type(new_data))
#    # print("Can I access text as expected:", new_data['Text'])
#    # text = new_data['Text']
#    # polarity, subjectivity = polarity_and_subjectivity_analysis_with_spacy(text.to_string(), nlp_lang) # text is Series, convert to string for analysis
#    # print(f"Polarity: {polarity}, Subjectivity: {subjectivity}")
#    # ----------------------------------
#    # Append to existing dataframe
#    # ----------------------------------
#    df = pd.concat(
#       [df, new_data],
#       ignore_index=True
#    )
#    #WRONG PLACE
#    # rows, columns = df.shape
#    # print(f"Columns before adding polarities and subjectivities in function for english current work:  {columns}")
#    # #Does this work as expected
#    # df['Polarity'] = polarity
#    # df['Subjectivity'] = subjectivity   
#    # print(f"Columns After adding polarities and subjectivities in function for english current work:  {columns}")
  
#    # ----------------------------------
#    # Export
#    # ----------------------------------
#    df.to_excel(
#       designation + '_lingvistik.xlsx',
#       index=False
#    )

#    print('Head of df with attributes in function:')
#    print(df.head())
#    return df



# #about stats.py:  https://www.geeksforgeeks.org/python/custom-django-management-commands/      #about manage.py stats