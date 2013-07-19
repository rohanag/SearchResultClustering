from PreProcessingAPI import *
PPobj = PreProcessingAPI()

__author__ =  'Rohan Agrawal'

class PostProcessingAPI():
    """
    Contains functions required for post processing , i.e
    post k means clustering, such as removing redundant
    cluster labels, combining search term with candidate 
    cluster label to get a new search term.
    """
    def getCandidateLabels(self, n, vectorizer, centers, i, e):
        """
        Takes input n - number of labels requested,
        vectorizer - vectorizer objec
        centers - k means cluster centers
        i - values of tfidf for each feature of the cluster centers
        e - current cluster e
        Returns all the labels in a list 
        """
        j = 0
        result = []
        while ( j < n ):
            j += 1
            term = vectorizer.get_feature_names()[i.argmax()]
            result.append(term)
            centers[e][i.argmax()] = -100      
        return result
     
    def cleanRedundantLabels(self, result, searchstring, sentenceseperator):
        """
        Candidate lables contained in result contain many redundant
        labels, for e.g. ['polo men', 'polo men women'], the label
        'polo men' is redundant because its information is entirely
        contained in 'polo men women', hence the former label is 
        removed. Similary for a search string "polo", the candidate
        label "polo" is also redundant as it provides no extra
        information about the cluster. Labels which contain the 
        sentence seperator term are also removed as phrases cannot
        extend beyond a sentence.
        """
        searchstring = ' '.join( [PPobj.getStemmed(x) for x in searchstring.split()] )
        result2 = result[:]
        result = []
        #split the results which contain sentence seperator
        for r in result2:
            result.extend(r.split(sentenceseperator))
        result = [x.strip() for x in result]
        #remove label equivalent to the search string
        result = [x for x in result if x != searchstring]
        result = [x for x in result if x not in searchstring]
        result2 = result[:]
        result = []
        for x in result2:
            if set(x.split()).intersection(set(searchstring.split())) == set(x.split()):
                if len(x.split()) > len(searchstring.split()):
                    result.append(x)
            else:
                    result.append(x)
            
        jj = 0
        while jj < len(result):
            if len(result[ jj ]) < 3:
                result[ jj ] = ''
            else:
                #if j is a single term phrase
                if result[ jj ].split() == [result[ jj ]]:
                    if result[ jj ].isalpha() == False:
                        result[ jj ] = ''
                        continue
                #for multi term phrases
                kk = 0
                while kk < len(result):
                    if kk!= jj:
                        if result[ jj ] in result[ kk ] :
                            if jj < kk:
                                result[jj], result[kk] = result[kk], result[jj]
                                result[ kk ] = ''
                                jj = -1
                                break
                            else:
                                result[ jj ] = ''
                        elif set(result[ jj ].split()) == set(result[ kk ].split()):
                            result[ jj ] = ''

                    kk += 1
            jj += 1
            
            
        return result
     
    def getOriginalPhrase(self, result, stemmed): 
        """
        The candidate cluster labels in results are stemmed, 
        so this functions returns their true form
        """
        result2 = filter(None, result) 
        result = []
        for r in result2:
            if r.split() == [r]:
                if r in stemmed:
                   result.append(stemmed[r]) 
            else:
                temp = ''
                for rr in r.split():
                    if rr in stemmed:
                        temp += stemmed[rr] + ' '
                result.append(temp)   
        return result
        
    def getNewSearchString(self, searchstring, newterm):
        """
        Combines the searchstring and new term ( which is the 
        cluster label ) to come up with a new search term, 
        to expand the search in the direction of the cluster
        chosed by the user.
        """
        if set(searchstring.split()).intersection(set(newterm.split())) == set(searchstring.split()):
            searchstring = newterm
        else:
            searchstring += ' ' + newterm    
        return searchstring