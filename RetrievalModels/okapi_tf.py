'''
Created on 26-Oct-2013

@author: tushar
'''
import re
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

# vector space model - okapi tf(part 1)
def calculateOktf():
    outfile = open("outfile_problem1.txt", "w")
    for query in queriesdict:
        result = dict()
        sentence = queriesdict[query]
        sentence = str(sentence).rstrip()
        words = sentence.split(" ")
        for queryTerm in words:
            print(queryTerm)
            invListDict = dict()
            invListDict, ctf, df = parseInvertedList(queryTerm)
              
            tfQuery = calculateTfInQuery(queryTerm, words)
            querylen = calculateQueryLength(words)
            avgquerylen = calculateAvgQueryLength()
            queryOktf = tfQuery/(tfQuery + 0.5 + 1.5*querylen/avgquerylen)
                
            for documentid in invListDict:
                tf = invListDict[documentid][1]
                doclen = invListDict[documentid][0]
                docOktf = tf/(tf + 0.5 + 1.5*doclen/288)
              
                score = (docOktf * queryOktf)
                
                if documentid in result.keys():
                    result[documentid] += score
                else:
                    result[documentid] = score
                
                
        sortedres = sorted(result.items(), key=lambda x: x[1], reverse=True)
        i = 0
        for docIdScore in sortedres[:1000]:
            i += 1
            print(query, "Q0", doclistMap[str(docIdScore[0])], i, docIdScore[1], "Exp")
            outfile.write(str(query) + " Q0 " + str(doclistMap[str(docIdScore[0])]) + " " + str(i) + " " + str(docIdScore[1]) +  " Exp\n")
    outfile.close()

            

processQuery()
mapInternalDocIdsToExternal()
calculateOktf()