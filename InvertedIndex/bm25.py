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


#  bm25 (part 5)
def bm25():
    
    pkldata = open('inverted_index.pkl', 'rb');
    term_dict = pickle.load(pkldata);
    pkldata.close()
    
    outfile = open("outfile_problem5.txt", "w")
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
              
            tfQuery = calculateTfInQuery(queryTerm, words)
            
            for documentid in invListDict:
                tf = invListDict[documentid][1]
                doclen = invListDict[documentid][0]
                total_docs = 3204;
                avg_doclen = 54.45 # calculated from cacm_utility.py
                
                K=0
                v=0
                z=0
                K=float((.3)+(.9*(doclen/avg_doclen))) # this formula uses k1 = 1.2
                # I have used different values of k1 between 0 to 2 and mentioned the
                # result in the project report
                
                v=float(101*tfQuery/(100+tfQuery))
                y=float((2.2*tf)/(K+tf))
                z = math.log(float((1/((df+.5)/(total_docs+.5-df)))))
                bm=float(z*v*y)
                
                if documentid in result.keys():
                    result[documentid] += bm
                else:
                    result[documentid] = bm

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
    bm25()
print("Total time taken is {} seconds...".format(time.time() - start_time))
