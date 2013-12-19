'''
Created on 26-Oct-2013

@author: tushar
'''
import re, math
from parseInvList import parseInvertedList

queriesdict = dict()
doclistMap = dict()

def processQuery():
    stopwords = set()
    stopfile = open("stoplist.txt")
    for stopword in stopfile:
        stopwords.add(stopword.rstrip())
         
    queryfile = open("queries.txt")
    for query in queryfile:
        # handle dots (".") U.S. becomes US
        query = ''.join(e for e in query if e != '.')
        
        # remove punctuation
        query = re.sub('[^a-zA-Z0-9\n\.]', ' ', query).rstrip()
        
        # convert to lower case
        query = query.lower()
        
        # remove stop words
        result = query.split(" ")
        str = '';
        for term in result:
            if term == result[0] or term == '' or term == ' ': continue
            if term not in stopwords:
                str += term + ' '
        if result[0] != '' and result[0] != ' ':
            queriesdict[result[0]] = str.rstrip()
    queryfile.close()
    
def mapInternalDocIdsToExternal():
    doclist = open("doclist.txt")
    for pair in doclist:
        pair = pair.rstrip()
        arr = pair.split("   ")
        doclistMap[arr[0]] = arr[1]
    doclist.close()
        
        
def calculateAvgQueryLength():
    sumofquerylengths = 0;
    totalqueries = 25;
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
    outfile = open("outfile_problem4.txt", "w")
    for query in queriesdict:
        result = dict()
        sentence = queriesdict[query]
        sentence = str(sentence).rstrip()
        words = sentence.split(" ")
        for queryTerm in words:
            print(queryTerm)
            invListDict = dict()
            invListDict, ctf, df = parseInvertedList(queryTerm)
              
            for documentid in invListDict:
                tf = invListDict[documentid][1]
                doclen = invListDict[documentid][0]
                corpus_size =24401877
                lambda_val = 0.2
                # I have tried different values of lambda varying from 0.2 to 0.8
                # with intervals of 0.2
                jm=math.log(((lambda_val*tf/doclen)/((1-lambda_val)*ctf/corpus_size)) + 1)
                
                if documentid in result.keys():
                    result[documentid] += jm
                else:
                    result[documentid] = jm

        sortedres = sorted(result.items(), key=lambda x: x[1], reverse=True)
        i = 0
        for docIdScore in sortedres[:1000]:
            i += 1
            print(query, "Q0", doclistMap[str(docIdScore[0])], i, docIdScore[1], "Exp")
            outfile.write(str(query) + " Q0 " + str(doclistMap[str(docIdScore[0])]) + " " + str(i) + " " + str(docIdScore[1]) +  " Exp\n")
    outfile.close()

            

processQuery()
mapInternalDocIdsToExternal()
estimateModelJelinekMercer()