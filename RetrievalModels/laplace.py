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

# Model estimation: Maximum likelihood laplace smoothing(part 3)
def estimateModelLaplaceSmoothing():
    
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
            invListDict, ctf, df = parseInvertedList(queryTerm)
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
            invListDict = map_term_invlist[queryTerm]
       
            for documentid in tempresult.keys():
                
                k = 166054.0; # total unique words 
                
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
            print(query, "Q0", doclistMap[str(docIdScore[0])], i, docIdScore[1], "Exp")
            outfile.write(str(query) + " Q0 " + str(doclistMap[str(docIdScore[0])]) + " " + str(i) + " " + str(docIdScore[1]) +  " Exp\n")
    outfile.close()

            

processQuery()
mapInternalDocIdsToExternal()
estimateModelLaplaceSmoothing()