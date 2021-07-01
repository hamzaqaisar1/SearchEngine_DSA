from django.shortcuts import render
from .forms import SearchEngine
from lexicon import *
from forward_index.forward_index import *
from inverted_index.inverted_index import *
from config import *
from searching.searching import Searching


# Create your views here.

#
# Building two different functions to display the same view but the other one is rendered when the 'Build Index' link is clicked on the front page
#


#
# Defining the front page view
#
def index(request):
    context = dict()
    # Searching for the specified word sent in through the post request
    if request.method == 'POST':
            form = SearchEngine(request.POST)
            if form.is_valid():
                files = list()
                makePaths()
                buildForwardIndex()
                buildInvertedIndex()
                searcher = Searching()
                # Dealing with the exception when the queried word is not found in the lexicon
                try:
                    results = searcher.search(form.cleaned_data["your_query"])
                except:
                    context = {"form":form,"error": "Invalid Query: {}".format(form.cleaned_data["your_query"]) }
                    return render(request,'myEngine/index.html',context)
                context = {"form":form,"results":results}
    # If it is a GET request simply display the form
    else:
        form = SearchEngine()
        context = {"form": form}
            
    return render(request, 'myEngine/index.html',context)

# A view for when the 'Build Index' button is clicked so as to make sure the required functions are called 
def buildIndex(request):
    context = dict()
    if request.method == 'POST':
            form = SearchEngine(request.POST)
            if form.is_valid():
                files = list()
                makePaths()
                searcher = Searching()
                try:
                    results = searcher.search(form.cleaned_data["your_query"])
                except:
                    context = {"form":form,"error": "Invalid Query: {}".format(form.cleaned_data["your_query"]) }
                    return render(request,'myEngine/index.html',context)
                context = {"form":form,"results":results}
    else:
        # Only change from the above function is that we are calling the following two functions
        makePaths()
        buildForwardIndex()
        buildInvertedIndex()
        form = SearchEngine()
        context = {"form": form}
    return render(request,'myEngine/index.html',context)