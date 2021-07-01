"""
Inverted Index module creating all the functions related to it
"""
import json

from config import *
from misc_functions import *

#
# Importing the following modules so as to read the forward index
#

import forward_index.forward_index
from forward_index.forward_index import readBarrels

#
# Returning a specified barrel based on whether it is for the title tokens or the text tokens
#
def readInvertedBarrels(barrel_id,short=False):
    barrel = dict()
    barrel_path = ""
    if short==False:
        barrel_path = os.path.join(INVERTED_BARREL_PATH, "barrel{}Inverted.json".format(barrel_id))
    else:
        barrel_path = os.path.join(SHORT_INVERTED_BARREL_PATH, "barrel{}Inverted.json".format(barrel_id))


    with open(barrel_path,"r",encoding='utf-8') as invertedBarrel:
        barrel = json.load(invertedBarrel)

    return barrel

#
# This functions creates and inverted barrel from the given forward barrel by using the memory trade-off
#
def createInvertedBarrel(forwardBarrel):
    invertedBarrel = dict()

    for docID,words in forwardBarrel.items():
        for wordID,hitpositions in words.items():
            invertedBarrel[wordID] = dict()
            invertedBarrel[wordID].update({docID : hitpositions})
    
    return invertedBarrel


# This function will read the forward barrels and create the inverted barrels
def buildInvertedIndex():
    # Setting up the initial variables for the inverted index to work
    invertedBarrels = dict()
    shortInvertedBarrels = dict()
    forwardBarrels = dict()
    shortForwardBarrels = dict()

    barrelNum = 0

    

    # Walking through the forward barrels of document's title text and creating inverted barrels by passing it to the above function
    for (_,_,files) in os.walk(SHORT_BARREL_PATH):
            for file in files:
                path = os.path.join(SHORT_BARREL_PATH,file)
                try:
                    shortForwardBarrels[barrelNum] = readBarrels(path)
                # If no forward barrel index for this barrel number, we ignore that number
                except (FileNotFoundError, IOError):
                    shortForwardBarrels[barrelNum] = dict()
                    barrelNum += 1
                    continue
                

                # Creating inverted barrels based on the forward barrels
                shortInvertedBarrels[barrelNum] = createInvertedBarrel(shortForwardBarrels[barrelNum])
                barrelNum += 1

    # Storing all the barrels in their respective files
    for key,value in shortInvertedBarrels.items():
        with open(os.path.join(SHORT_INVERTED_BARREL_PATH,"barrel{}Inverted.json".format(key)) ,"w+",encoding='utf-8') as shortInvertedBarrelFile:
            json.dump(value,shortInvertedBarrelFile)


    barrelNum = 0

    # Walking through the forward barrels of the document's text and creating inverted barrels by passing it to the above function
    for (_,_,files) in os.walk(BARREL_PATH):
            for file in files:
                path = os.path.join(BARREL_PATH,file)
                try:
                    forwardBarrels[barrelNum] = readBarrels(path)
                # If no forward barrel index for this barrel number, we ignore that number
                except (FileNotFoundError, IOError):
                    forwardBarrels[barrelNum] = dict()
                    barrelNum += 1
                    continue
                
                # Creating the inverted barrel from the forward barrel
                invertedBarrels[barrelNum] = createInvertedBarrel(forwardBarrels[barrelNum])
                barrelNum += 1
    
    # Storing te inverted barrel into the respective files
    for key,value in invertedBarrels.items():
        with open(os.path.join(INVERTED_BARREL_PATH,"barrel{}Inverted.json".format(key)) ,"w+",encoding='utf-8') as invertedBarrelFile:
            json.dump(value,invertedBarrelFile)