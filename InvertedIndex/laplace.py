'''
Created on 26-Oct-2013

@author: tushar
'''

import re, math
from queries import loadQueries
from stemming.porter2 import stem
import pickle
import time

queriesdict = dict() # this stores the processed queries
doclistMap = dict()


def processQuery():
    stopwords = set()
    stopfile = open("stoplist.txt")
    for stopword in stopfile:
        stopwords.add(stopword.rstrip())
    
    queries = loadQueries()
    for queryString in queries.keys():
        
        query = queries[queryString];
        
        # handle dots (".") U.S. becomes US
        query = ''.join(e for e in query if e != '.')
        
        # remove punctuation
        query = re.sub('[^a-zA-Z0-9\n\.]', ' ', query).rstrip()
        
        # remove stop words
        result = query.split(" ")
        mystr = '';
        for term in result:
            if term == '' or term == ' ': continue
            if term not in stopwords:
                # convert to lower case
                term = str(term).lower()
                term = str(stem(term))
                mystr += term + ' '
        queriesdict[queryString] = mystr.rstrip()
        
        
def calculateAvgQueryLength():
    sumofquerylengths = 0;
    totalqueries = 64;
    for query in queriesdict:
        sentence = queriesdict[query]
        words = sentence.split(" ")
        sumofquerylengths += len(words);
    average = sumofquerylengths/totalqueries
    return average
    
    
def calculateTfInQuery(queryTerm, words):
    count = 0
    for term in words:
        if (term == queryTerm):
            count += 1
    return count

def calculateQueryLength(words):
    count = 0
    for term in words:
        count += 1
    return count

# Model estimation: Maximum likelihood (part 3)
def estimateModelLaplaceSmoothing():
    
    pkldata = open('inverted_index.pkl', 'rb');
    term_dict = pickle.load(pkldata);
    pkldata.close()
    
    outfile = open("outfile_problem3.txt", "w")
    for query in queriesdict:

        tempresult = dict()
        map_term_invlist = dict()
        
        result = dict()
        sentence = queriesdict[query]
        sentence = str(sentence).rstrip()
        words = sentence.split(" ")
        mylist = list()
        invListDict = dict()
        
        for queryTerm in words:
            ctf = 0
            if (queryTerm not in term_dict.keys()): continue
            invListDict = term_dict[queryTerm]
            for docid in invListDict:
                ctf += invListDict[docid][1] 
            df = len(invListDict)
            
            map_term_invlist[queryTerm] = invListDict # mapping each term with its inverted list
            
            for documentid in invListDict:
                if documentid in tempresult:
                    mylist = tempresult[documentid]
                    mylist.append(queryTerm)
                    tempresult[documentid] = mylist
                else:
                    tempresult[documentid] = [queryTerm]
            
        for queryTerm in words:
            print(queryTerm)
            invListDict = dict()
            if (queryTerm not in map_term_invlist.keys()): continue
            invListDict = map_term_invlist[queryTerm]
       
            for documentid in tempresult.keys():
                
                k = 11343.0; # total unique words 
                
                if queryTerm in tempresult[documentid]:
                    doclen = invListDict[documentid][0]
                    tf = invListDict[documentid][1]
                    p = float((tf + 1)/(doclen + k))
                    
                else:
                    mylist = tempresult[documentid]
                    doclen = map_term_invlist[mylist[0]][documentid][0]
                    p = float(1.0/(doclen + k)) 
                    
                if documentid in result.keys():
                    result[documentid] += math.log(p)
                else:
                    result[documentid] = math.log(p)
                
        sortedres = sorted(result.items(), key=lambda x: x[1], reverse=True)
        i = 0
        for docIdScore in sortedres[:1000]:
            i += 1
            print(query, "Q0", docIdScore[0], i, docIdScore[1], "Exp")
            outfile.write(str(query) + " Q0 " + str(docIdScore[0]) + " " + str(i) + " " + str(docIdScore[1]) +  " Exp\n")
    outfile.close()

            

processQuery()
start_time = time.time()
for i in range(1,101):
    estimateModelLaplaceSmoothing()
print("Total time taken is {} seconds...".format(time.time() - start_time))
