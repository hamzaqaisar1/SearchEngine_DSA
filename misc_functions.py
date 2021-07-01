"""
Describes all of the general functions used throughout the eniter project
"""

import json
import nltk
import os

# Importing for data serialization
import pickle

from config import *

# Importing the stemmig libraries
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

# Tokenizing just the string or word itself at first
def tokenizeString(words):
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()

    # Creating tokens and excluding punctuations
    tokens = nltk.regexp_tokenize(words,r'\w+')

    # Stemming tokens and discarding numbers along with tokens of single words
    filtered_tokens = [ps.stem(lemmatizer.lemmatize(token.lower())) for token in tokens if not(len(token) <= 1) and not(token.isdigit())]

    return filtered_tokens



#
# This function will be used to parse each document of the datatset and converting it into tokens
#
def filter_and_tokenize_file(file,titleRequired=False,rank=False):
    text = ""
    title = ""
    path = os.path.join(DATA_PATH,file)
    data = dict()
    with open(path,"r",encoding='utf8') as f:
        data = json.loads(f.read())
        text += " " + data["text"]
        title += " " + data["title"]

    # Creating lemmatizing objects
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()

    # Returning the rank of the document if required
    if rank == True:
        try:
            print(data["thread"]["domain_rank"])
            return data["thread"]["domain_rank"]
        except:
            return 0

    # Checking if the title tokens were asked for
    if titleRequired == True:
        # Creating tokens and excluding punctuations
        tokens = nltk.regexp_tokenize(title,r'\w+')

        # Stemming tokens and discarding numbers along with tokens of single words
        filtered_tokens = [ps.stem(lemmatizer.lemmatize(token.lower())) for token in tokens if not(len(token) <= 1) and not(token.isdigit())]

        return filtered_tokens
    
    # Returning the text tokens if nothing was specified
    elif titleRequired == False and rank == False:     
        tokens = nltk.regexp_tokenize(text,r'\w+')

        # Stemming tokens and discarding numbers along with tokens of single words
        filtered_tokens = [ps.stem(lemmatizer.lemmatize(token.lower())) for token in tokens if not(len(token) <= 1) and not(token.isdigit())]

        return filtered_tokens
    


#
# The following function generates the DocIDs for all of files in the dataset
#
def generateDocIDs():
    # Retrieving the DocID file if it already exists
    try:
        docIndex = readDocIDs()
    except (FileNotFoundError, IOError):
        docIndex = dict()


    # Going through the files and storing the docIDs
    for (_,_,files) in os.walk(DATA_PATH):
        for file in files:
            path = os.path.join(DATA_PATH,file)
            # Assigning the docIDs only to those documents which have not been indexed
            if docIndex.get(path) == None:
                docIndex[path] = str(len(docIndex))


    # Writing to the index file
    with open(DOC_INDEX_PATH,"w+",encoding='utf-8') as documentIndexFile:
        json.dump(docIndex,documentIndexFile)   

    # Returning the index
    return docIndex          

#
# Function to read the document index
#
def readDocIDs():
    # Reading the documentIndex.json file
    with open(DOC_INDEX_PATH,"r",encoding='utf-8') as documentIndexFile:
        docIndex = json.load(documentIndexFile)

    return docIndex

#
# This function takes all the barrels generated form the forward index and adds them to the already existing barrels or
# create new ones for them based on if they already exist in the Data Barrels
#
def generateBarrels(immediateBarrels):
    for key,value in immediateBarrels.items():
        forwardBarrel = dict()
        try:
            with open(os.path.join(BARREL_PATH,"barrel{}.json".format(key)) ,"r",encoding='utf-8') as forwardBarrelFile:
                forwardBarrel = json.load(forwardBarrelFile)
        except (FileNotFoundError, IOError):
            pass
        
        forwardBarrel.update(value)
        with open(os.path.join(BARREL_PATH,"barrel{}.json".format(key)) ,"w+",encoding='utf-8') as forwardBarrelFile:
            forwardBarrel = json.dump(forwardBarrel,forwardBarrelFile)


#
# This function takes all the barrels generated form the short forward index and adds them to the already existing barrels or
# create new ones for them based on if they already exist in the Data Barrels
#
def generateShortBarrels(immediateBarrels):
    for key,value in immediateBarrels.items():
        shortForwardBarrel = dict()
        try:
            with open(os.path.join(SHORT_BARREL_PATH,"barrel{}.json".format(key)) ,"r",encoding='utf-8') as shortforwardBarrelFile:
                shortForwardBarrel = json.load(shortforwardBarrelFile)
        except (FileNotFoundError, IOError):
            pass
        
        shortForwardBarrel.update(value)
        with open(os.path.join(SHORT_BARREL_PATH,"barrel{}.json".format(key)) ,"w+",encoding='utf-8') as shortforwardBarrelFile:
            shortForwardBarrel = json.dump(shortForwardBarrel,shortforwardBarrelFile)




#
# This function generates the pickle file which stores the list storing whether or not a certian docID has been indexed or not
# It acesses the docIDs from the docIDs file 
#
def generateIsIndexed(indexedDocs):
    try:
        indexedDocs.append(readIsIndexed())
    except (FileNotFoundError, IOError):
        pass

    
    with open(IS_INDEXED_PATH,"wb+") as isIndexedFile:
        pickle.dump(indexedDocs,isIndexedFile)     
          

#
# Reading the file using pickle 
#
def readIsIndexed():
    with open(IS_INDEXED_PATH,"rb") as isIndexedFile:
        isIndexed = pickle.load(isIndexedFile)
    return isIndexed
        


#
# This function generates the pickle file which stores the dictionary which ahs the docIDs and their corresponding domain rank and
# calls the function to map the values to a certain range
#
def generateDomainRanks(ranks):
    try:
        ranks.update(readDomainRanks())
    except (FileNotFoundError, IOError):
        pass

    print(ranks)
    key_max = max(ranks.keys(), key=(lambda k: ranks[k]))
    key_min = min(ranks.keys(), key=(lambda k: ranks[k]))


    ranks = mapRankValues(ranks[key_max],ranks[key_min],ranks)
    
    with open(DOMAIN_RANK_PATH,"w+") as domainRanksFile:
        json.dump(ranks,domainRanksFile)     


#
# Reading the file using pickle 
#
def readDomainRanks():
    with open(DOMAIN_RANK_PATH,"r") as domainRanksFile:
        ranks = json.load(domainRanksFile)
    return ranks

#
# Mapping the ranks between 1 and 100 based on a mathematical formula
#       
def mapRankValues(valMax,valMin,ranks):
    for docID in ranks.keys():
        ranks[docID] = ((1 - 100)*(ranks[docID] - valMin)/(valMax-valMin)) + 100
    return ranks