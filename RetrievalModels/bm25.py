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

#  bm25 model (part 5)
def bm25():
    outfile = open("outfile_problem5.txt", "w")
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
            
            for documentid in invListDict:
                tf = invListDict[documentid][1]
                doclen = invListDict[documentid][0]
                num_words = 84678
                avg_doclen = 288
                
                K=0
                v=0
                z=0
                K=float((.3)+(.9*(doclen/avg_doclen))) # this formula uses k1 = 1.2
                # I have used different values of k1 between 0 to 2 and mentioned the
                # result in the project report
                
                v=float(101*tfQuery/(100+tfQuery))
                y=float((2.2*tf)/(K+tf))
                z = math.log(float((1/((df+.5)/(num_words+.5-df)))))
                bm=float(z*v*y)
                
                if documentid in result.keys():
                    result[documentid] += bm
                else:
                    result[documentid] = bm

        sortedres = sorted(result.items(), key=lambda x: x[1], reverse=True)
        i = 0
        for docIdScore in sortedres[:1000]:
            i += 1
            print(query, "Q0", doclistMap[str(docIdScore[0])], i, docIdScore[1], "Exp")
            outfile.write(str(query) + " Q0 " + str(doclistMap[str(docIdScore[0])]) + " " + str(i) + " " + str(docIdScore[1]) +  " Exp\n")
    outfile.close()

            

processQuery()
mapInternalDocIdsToExternal()
bm25()