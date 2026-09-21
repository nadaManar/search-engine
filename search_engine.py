import csv
import re 
import math

from collections import Counter

print('Search engine starting...')

#PART 1
def get_stopwords(path):
    with open(path,'r',encoding='UTF-8') as f :
        stopwords = set(line.strip() for line in f)
    return stopwords

def read_csv(path):
    with open(path, mode='r' ,encoding='UTF-8', newline='') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    return data

data = read_csv('TED_transcripts.csv')
STOPWORDS = get_stopwords('stop_words.txt')

#PART 2
#extracting the words
#For each word, store which documents (URLs) it appears in and how many times.

#read verb.csv file
def read_verb(path):
    with open(path, mode='r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        data = [row for row in csv_reader]
    
    #mapping -> key: verb, value: base verb (ex: (asked,ask))
    verbs = {}
    for verb in data:
        for tense in ['Tense 1', 'Tense 2', 'Tense 3', 'Tense 4']:
            verbs[verb[tense]] = verb['Verb']
    return verbs

verbs = read_verb('verb.csv')

def preprocess_text(text):
    #Lowercase, remove punctuation, split, and remove stopwords.
    text = re.sub(r'[^\w\s]', ' ', text).lower()
    words = text.split()
    words = [w for w in words if w not in STOPWORDS]
    #convert verbs to base conjugation
    words = [verbs[w] if w in verbs else w for w in words]
    return words

index = {} #empty dictionary

for i in range(len(data)):
    url = data[i]['url'].strip()
    words = preprocess_text(data[i]['transcript'])
    word_count = Counter(words)

    for word, count in word_count.items():
        if word not in index:
            index[word] = {} #Creates an empty dictionary for the word 
        index[word][url] = count

#convert plural words(only checking plural words with 's' -> ex: dog - dogs)
def plurals():
    for w in index.keys():
        for url,count in index[w].items():
            #check if w is a plural word
            if (w[:len(w)-1] in index and w[len(w)-1] == 's'):
                index[w][url] = 0
                try:
                    index[w[:len(w)-1]][url] = index[w[:len(w)-1]][url] + count
                except:
                    #url key not found
                    index[w[:len(w)-1]][url] = count                 

plurals()

#PART 3
#tf - frequency of the word within the document
def compute_tf(word,document):
    transcript = ''
    url = document.strip()
    for i in range(len(data)):
        #find the transcript of the url
        if data[i]['url'].strip() == url:
            transcript = data[i]['transcript']
            break
    if transcript != '':
        processed_words = preprocess_text(transcript)
        #if the word is in the transcript
        if word in processed_words:
            total_words = len(processed_words)
            # number of occurences in that document / total number of words in that document
            return index[word][url] / total_words
        else:
            return 0
    else:
        return 0

#idf - inverse frequency of the word across all documents
def compute_idf(word):
    total_number_of_documents = len(data)
    try:
        total_number_of_documents_with_that_word = len(index[word])
        return math.log10(total_number_of_documents/total_number_of_documents_with_that_word)
    except:
        return 0
        
def compute_tf_idf(word,url):
    return compute_tf(word,url)*compute_idf(word)

def sort_key(entry):
    matched_words, total_score, url = entry
    #decending
    return (-matched_words, -total_score)

def search_answers(query_words):
    results = []

    for i in range(len(data)):
        url = data[i]['url'].strip()
        tf_idf_scores = [compute_tf_idf(w, url) for w in query_words if w in index]
        matched_words = sum(1 for score in tf_idf_scores if score > 0)
        total_score = sum(tf_idf_scores)

        if total_score > 0:
            results.append((matched_words, total_score, url))

    results.sort(key=sort_key)

    return [(score, url) for _, score, url in results]

#PART 4
query = ''
query = input('Please write your search, if you want to close please write \'ext\'\n')

while (query.lower() != 'ext'):
    query_words = preprocess_text(query)
    query_words = [w[:len(w)-1] if w[:len(w)-1] in index and w[len(w)-1] == 's' else w for w in query_words]
    query_words = list(set(query_words))
    
    while (query_words == ['']):
        query = input('Please enter a none empty query\n')
        query_words = query.split(' ')
    if(query.lower() != 'ext'):
        results=search_answers(query_words)
        if results:
            print("\ntop 10 matching TED talks :")
            for score,url in results[:10]:
                print(f"Score: {score: .4f}   | {url}")
                for w in query_words:
                    tf_idf = compute_tf_idf(w,url)
                    if(tf_idf != 0):
                        print(f"Score of {w} : {tf_idf}")
        else:
            print("no matching documents found")
        query = input('Please write your search, if you want to close please write \'ext\'')