'''
Created on 26-Oct-2013

@author: tushar
'''
import re, math
from queries import loadQueries
from stemming.porter2 import stem
import pickle
import time

queriesdict = dict()
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

#  Jelinek-Mercer smoothing (part 4)
def estimateModelJelinekMercer():
    
    pkldata = open('inverted_index.pkl', 'rb');
    term_dict = pickle.load(pkldata);
    pkldata.close()
    
    outfile = open("outfile_problem4.txt", "w")
    for query in queriesdict:
        result = dict()
        sentence = queriesdict[query]
        sentence = str(sentence).rstrip()
        words = sentence.split(" ")
        for queryTerm in words:
            print(queryTerm)
            invListDict = dict()
            
            ctf = 0
            if (queryTerm not in term_dict.keys()):
                continue
            invListDict = term_dict[queryTerm]
            for docid in invListDict:
                ctf += invListDict[docid][1] 
            df = len(invListDict)
              
            for documentid in invListDict:
                tf = invListDict[documentid][1]
                doclen = invListDict[documentid][0]
                num_terms = 174469
                lambda_val = 0.2
                # I have tried different values of lambda varying from 0.2 to 0.8
                # with intervals of 0.2
                jm=math.log(((lambda_val*tf/doclen)/((1-lambda_val)*ctf/num_terms)) + 1)
                
                if documentid in result.keys():
                    result[documentid] += jm
                else:
                    result[documentid] = jm

        sortedres = sorted(result.items(), key=lambda x: x[1], reverse=True)
        i = 0
        for docIdScore in sortedres[:1000]:
            i += 1
            print(query, "Q0", str(docIdScore[0]), i, docIdScore[1], "Exp")
            outfile.write(str(query) + " Q0 " + str(docIdScore[0]) + " " + str(i) + " " + str(docIdScore[1]) +  " Exp\n")
    outfile.close()
            

processQuery()
start_time = time.time()
for i in range(1,101):
    estimateModelJelinekMercer()
print("Total time taken is {} seconds...".format(time.time() - start_time))
