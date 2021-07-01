"""
This file is the module containing all the functions regarding the lexicon
"""

import os
import json

from config import *

from misc_functions import *

#
# Function to read the lexicon from its path and then return it in the form of a dictionary
#
def readLexicon():
    lexicon = dict()
    with open(LEXICON_PATH,"r",encoding='utf-8') as lexFile:
        lexicon = json.load(lexFile)
    
    return lexicon


#
# This function takes in the index specifying if the documents of dataset have been indexed or not and then creates the lexicon from those
# documents which have not been indexed yet and ignores the ones that have been indexed before. It writes the lexicon to a file and returns it
#

def buildLexicon(docIndex):
    # Creating the empty variables for containing the lexicon and the tokens
    lexiconf = dict()
    filtered_tokens = list()

    # Reading the file containing information whether a document has been indexed
    try:
        isIndexed = readIsIndexed()
    except (FileNotFoundError, IOError):
        isIndexed = list()

    # Walking through the dataset and checking if a document has been indexed
    for (_,_,files) in os.walk(DATA_PATH):
            for file in files:
                path = os.path.join(DATA_PATH,file)
                docID = str(docIndex[path])
                if docID not in isIndexed:
                    # The function being called reads, tokenizes and stems the tokens along with other filters
                    # It goes through both the title and the text of the specific document
                    filtered_tokens += filter_and_tokenize_file(file)
                    filtered_tokens += filter_and_tokenize_file(file,True)
    
    # Removing duplicate words
    words = set(filtered_tokens)

    # Checking if the lexicon exists already
    try:
        lexiconf = readLexicon()
    except (FileNotFoundError, IOError):
        lexiconf = dict()

    # Assigning wordIDs to words
    for word in words:
        if lexiconf.get(word) == None:
            lexiconf[word] = len(lexiconf)

    #Storing the lexicon and returning it
    with open(LEXICON_PATH,"w+",encoding='utf-8') as lex:
        json.dump(lexiconf,lex)

    return lexiconf

    
