from __future__ import division

from sys import path
from os import getcwd
path.append(getcwd() + '/API')

"""library calls"""
from numpy import vstack
from numpy.random import rand

"""API calls"""
from PreProcessingAPI import *
from ClusteringAPI import *
from PostProcessingAPI import *
from BingResultsAPI import *
ClstrObj = ClusteringAPI()
PreObj = PreProcessingAPI()
bingObj = BingResultsAPI()
PostObj = PostProcessingAPI()

__author__ =  'Rohan Agrawal'

def ClusterWeb( searchstring, clusters, searchResults ):
    """
    This is the central function which combined all the elements of the API
    Takes as input the searchstring provided by the user and returns
    clusters.
    Structure of clusters is 
    clusters[searchstring][clusterID] = [[cluster descriptors, , ],[doc Ids, , ]]
    """
    #Storing the list of all stop words
    stopwords = PreObj.getStopwords()
    #Bing web search api Key
    key = 'tfXfeYcUCuEk1sgdW/1vUCRnKx5FTqg9eBwCO05Skvc='
    #Number of search results
    N = 20
   
    filename = 'data'+searchstring+str(N)+'.json'
    try:
        with open('TempFiles/'+filename, 'r') as fp: #get results from file if already stored, avoiding over using the bing api
            result = json.load(fp)
    except:    
        #Get results from Bing Api
        if searchstring == '':
            print 'wtfffffffffffffffffffffffffff'
            return clusters, searchResults
        result = bingObj.getResults(N, searchstring, key, filename)
        if len(result['d']['results']) == 0:
            print 'wtfffffffffffffffffffffffffff2222222222'
            return clusters, searchResults

    sentenceseperator = 'zoxocovobonoaoso'
    dataset, stemmed, searchResults = PreObj.getDataset(sentenceseperator, result, searchstring, searchResults)

    clusterPenalty = 1.15
    vectorizer = ClstrObj.initVectorizer(stopwords, N)
    X = ClstrObj.getVectorSpace(vectorizer,dataset)

    """Do the actual clustering"""
    true_k = ClstrObj.getK(X, clusterPenalty)
    labels, centers = ClstrObj.getClusterLabelsCenters(X, true_k)
    
    if searchstring not in clusters:
        clusters[searchstring] = {}

    for i,l in enumerate(labels):
        if l not in clusters[searchstring]:
            clusters[searchstring][l] = [[],[i]]
        else:
            clusters[searchstring][l][1].append(i)

    #Postprocessing
    for e,i in enumerate(centers):
        result = []
        result = PostObj.getCandidateLabels(20, vectorizer, centers, i, e)
        result = PostObj.cleanRedundantLabels(result, searchstring, sentenceseperator)
        result = PostObj.getOriginalPhrase(result, stemmed)
        ##################if result is not of lenth 3, just extend it to 3 length#####################
        clusters[searchstring][e][0].extend(result[:3])

    return clusters, searchResults
