
#import nltk
#from nltk import word_tokenize
#import string
import json
import re
import pickle
import pandas as pd
#from google.colab import files

# new_str=''
# arr=[]
# def ngrams(tokens, n):
#     if n == 0:
#         return arr
#     if len(tokens) < n - 1:
#         return ngrams(tokens, n-1)
#     else:
#         for j in range(n-1):
#             new_str = ''*(n-1-j)
#             if j == 0:
#                 new_str += tokens[j]
#             else:
#                 for i in reversed(range(n-1)):
#                     if j-i >=0:
#                         new_str += ' '+tokens[j-i]
#             arr.append(new_str)
#         for i in range(len(tokens)):
#             new_str = ''
#             for j in range(n):
#                 if j < n:
#                     if (i + j) < len(tokens):
#                         if j == 0:
#                             new_str += tokens[i+j]
#                         else:
#                             new_str += ' '+tokens[i+j]
#                     else:
#                         new_str += ''
#             arr.append(new_str)
#     return ngrams(tokens, n-1)

# def ngrams_custom(tokens):
#     ngram_token = []
#     temp_token = []
#     new_str = ''
#     n = len(tokens)
#     for j in range(n):
#         if tokens[j] != '':
#             ngram_token.append(tokens[j])
#             if j+1 <= n-1:
#                 temp_token.append(tokens[j] + " " + tokens[j+1])
    
#     for temp in temp_token:
#         ngram_token.append(temp)

#     return ngram_token

#nltk.download('punkt')

def get_extracted_keywords(intent_json_path):
    stopword_file = open("./data/long_stopwords.txt", "r")
    lots_of_stopwords = []
    
    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))
    
    # with open("./data/Intent.json") as json_data:
    with open(intent_json_path, encoding="utf8") as json_data:
        intents = json.load(json_data)
    
    stopwords_plus = []
    words = []
    all_words = []
    classes = []
    documents = {}
    stopwords = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)
    allWords = []

    documents = pd.DataFrame(columns = [ 'Intents', 'Keywords' ])
    
    for intent in intents['data']:
        if len(intent['responses']):
            respo = str(intent['responses'][0])
            arr=[]
            new_str=''
            
            for pattern in intent['patterns']:
                
                words = []
                pattern = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',pattern)
                w = pattern.split(' ')
                w = [(_w.lower()) for _w in w if _w.lower() not in stopwords_plus]
                
                w1 = ' '.join(w)
                
                word = w1
                all_words.append(word)
                if word != '':
                    doc = {'Intents': respo.replace("â€™", "'").strip(), 'Keywords': word.strip()}
                    docavl = documents.loc[(documents['Intents'] == respo.replace("â€™", "'").strip())
                                            & (documents['Keywords'] == word.strip())]
                    # print('docavl', doc)
                    if docavl.empty:
                        documents = documents.append(doc, ignore_index = True)
        
    documents['wordcount'] = documents['Keywords'].map(len)

    return documents, all_words


# stopword_file = open("./data/long_stopwords.txt", "r")
# lots_of_stopwords = []


# with open("./data/Intent.json") as json_data:
#     intents = json.load(json_data)

# for line in stopword_file.readlines():
#     lots_of_stopwords.append(str(line.strip()))

# stopwords_plus = []
# words = []
# all_words = []
# classes = []
# documents = {}
# stopwords = []
# stopwords_plus = stopwords + lots_of_stopwords
# stopwords_plus = set(stopwords_plus)
# allWords = []

# documents = pd.DataFrame(columns = [ 'Intents', 'Keywords' ])

# for intent in intents['data']:
#     respo = str(intent['responses'][0])
    
#     arr=[]
#     new_str=''
    
#     for pattern in intent['patterns']:
        
#         words = []
#         pattern = re.sub(r'[?|$|.|_|(|)|,|&|!]',r'',pattern)
#         w = pattern.split(' ')
#         w = [(_w.lower()) for _w in w if _w.lower() not in stopwords_plus]
        
#         w1 = ' '.join(w)
        
#         word = w1
#         all_words.append(word)
#         if word != '':
#             doc = {'Intents': respo.replace("â€™", "'").strip(), 'Keywords': word.strip()}
#             docavl = documents.loc[(documents['Intents'] == respo.replace("â€™", "'").strip())
#                                     & (documents['Keywords'] == word.strip())]
#             # print('docavl', doc)
#             if docavl.empty:
#                 documents = documents.append(doc, ignore_index = True)
        

# documents['wordcount'] = documents['Keywords'].map(len)


# words = sorted(list(set(words)))
# with open('./pickles/Intent.pkl', 'wb') as f:
#   pickle.dump(documents, f)

# with open('./pickles/ExtractedKeyword.pkl', 'wb') as f:
#   pickle.dump(all_words, f)
#   #files.download('Consumer_ExtractedKeyword.pkl')
    
