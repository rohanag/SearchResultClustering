from __future__ import division
from re import *
from nltk.stem import porter

__author__ =  'Rohan Agrawal'

class PreProcessingAPI():
    """
    contains all functions required for preprocesing
    the text, before running clustering algorithm.
    """
    stemmer = porter.PorterStemmer()

    def getStopwords(self):
        """
        List of stop words taken from http://www.lextek.com/manuals/onix/stopwords2.html
        returns the list in stemmed form (porter stemmer)
        """
        stopwords = [self.getStemmed(line.strip()) for line in open('API/stopwords.txt')]
        stopwords = list(set(stopwords))
        stopwords.append('com')
        stopwords.append('wikipedia')
        stopwords.append('wikipaedia')
        stopwords.append('wiki')
        stopwords.append('html')
        stopwords.append('aspx')
        stopwords.append('jsp')
        return stopwords
        
    def tokenize(self, s):
        """
        Tokenizes a string s, based on all non word characters as defined by python
        Also does not split on '.' if there are numbers on either side.
        e.g. Does not split 1.2 but splits a.b into [a,b]
        """
        return split("\s|(?<!\d)[^\w']+|[^\w']+(?!\d)", s)
        
    def lowercase(self, s):
        """
        returns string s in lowercase as a string
        """
        return s.lower()
        
    def replaceAll(self, s):
        """
        returns the string s with '_' replaced by space, and %2c replaced by a ','
        """
        return s.replace('_',' ').replace('%2c',',')
        
    def filterEmptyStr(self, s):
        """
        takes a list s, and returns the list after removing all
        the empty elements from s
        """
        return filter(None, s)
        
    def getStemmed(self, s):
        """
        takes a string s and returns the stemmed (porter, nltk) version of the word
        """
        return self.stemmer.stem(s)
        
    def extractFromURL(self, s):
        """
        Takes a URL, and returns all words in the URL 
        after the 3rd slash in the url
        e.g. for input http://www.google.com/abcd/efgh 
        ['abcd','efgh'] is returned
        """
        if 'amazon.com' in s or 'ebay.com' in s: #generally contain a lot of noise in the url
            return []
        
        indices = [m.start() for m in finditer('/', s)]
        if len(indices) > 2:
            s = s[indices[2]+1:]
            s = self.tokenize(s)
            s = self.filterEmptyStr(s)    
        
        return s

    def getText(self, i, stemmed):
        """
        Tokenizes text, lowercases, removes empty strings, stems
        and returns a joint string seperated by spaces.
        Also returns a dictionary stemmed,
        stemmed[stemmed word] = Original word
        """
        d = self.tokenize(self.replaceAll(self.lowercase(i)))
        d = [self.lowercase(x) for x in d]
        d = self.filterEmptyStr(d)
        for j,x in enumerate(d):
            stemmed[self.getStemmed(x)] = x
            d[j] = self.getStemmed(x)
        return ' '.join(d), stemmed
        
    def getTextFromURL(self, d, stemmed):
        """
        Tokenizes text, lowercases, removes empty strings, stems URL "d"
        and returns a joint string seperated by spaces. In addition     
        to getText(), this function uses the replaceAll() function
        required to clean the URL.
        Also returns a dictionary stemmed,
        stemmed[stemmed word] = Original word
        """

        url = self.lowercase(d)
        url = self.replaceAll(url)  
        url = self.extractFromURL(url)
        for j,x in enumerate(url):
            stemmed[self.getStemmed(x)] = x
            url[j] = self.getStemmed(x)
        return ' '.join(url), stemmed
        
    def getDataset(self, sentenceseperator, result, searchstring, searchResults):
        """
        Takes as input sentence seperator (so that a phrase will not 
        extend beyond a sentence, for e.g. in " apple. apple product", 
        "apple apple product" cannot be a phrase, but "apple product"
        can be)
        Takes result dictionary which contains results of search from 
        Bing API
        Also takes as input the search string used to get results
        returns dataset after performing all preprocessing task.
        Full stops are replaced by the sentence seperator, so that
        phrases containing the sentence seperator can be removed
        later easily.
        
        """

        dataset = []
        stemmed = {}


        ###Displaying all results to the user and simultaneously preprocessing the text from title, url and description and putting in dataset
        for i in result['d']['results']:
            desc, stemmed = self.getText(i['Description'], stemmed)
            titl, stemmed = self.getText(i['Title'], stemmed)
            url, stemmed = self.getTextFromURL(i['Url'], stemmed)
            if url:
                dataset.append(url + ' ' + sentenceseperator + ' ' + titl + ' ' + sentenceseperator + ' ' + desc)
            else:
                dataset.append(titl + ' ' + sentenceseperator + ' '  + desc)
            if searchstring not in searchResults:
                searchResults[searchstring] = []
            searchResults[searchstring].append([i['Url'],i['Title'],i['Description']])      
        return dataset, stemmed, searchResults