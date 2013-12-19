'''
Created on 24-Nov-2013

@author: tushar
'''

from bs4 import BeautifulSoup
import re
from stemming.porter2 import stem
import pickle
import time

stopwords = set()

def getStopWords():
    stopfile = open("stoplist.txt")
    for stopword in stopfile:
        stopwords.add(stopword.rstrip())
    stopfile.close()

def getHtmlDoc(doc_url):
    doc = open(doc_url)
    soup = BeautifulSoup(''.join(doc))
    text = soup.pre.contents[0].split()
    
    # handle dots (".") U.S. becomes US
    text = ''.join(e for e in str(text) if e != '.')
    
    # remove punctuation
    text = re.sub('[^a-zA-Z0-9\n\.]', ' ', text).rstrip()

    return text
    
    
def process():
    
    term_dict = dict()
    count_prefix_initial = '0000';
    count = 1;
    htmlPath = 'C:\\Users\\tushar\\Desktop\\cacm.tar\\CACM-' # path to your cacm documents.
    file_suffix = '.html'

    while count <= 3204:
        flag = False
        countPrefix = count_prefix_initial[0:(len(count_prefix_initial)-len(str(count)))]
        fileName = str(htmlPath+countPrefix+str(count)+ file_suffix)
        print(fileName)
        
        text = getHtmlDoc(fileName);
        text = str(text).replace('\n', ' ')
        
        
        myvalues = re.split(" ", str(text))
        docid = 'CACM-' + countPrefix + str(count)
        
        doclen = 0
        for term in myvalues:
            
            if (term == '' or term == ' '): continue
            
            if term not in stopwords:
                # make it lower case
                term = str(term).lower()
                doclen += 1;
            pattern = 'ca\d{6}'
            matched = re.match(pattern, term)
            if (matched != None):
                flag = True
                
            if ((flag == True) and (term == 'pm' or term == 'am')): break
    
        flag = False
        for term in myvalues:
            
            if (term == '' or term == ' '): continue
            
            #remove stop words and perform stemming.
            if term not in stopwords:
                
                # make it lower case
                term = str(term).lower()
            
                term = stem(term)
                if term not in term_dict.keys():
                    term_dict[term] = dict()
                     
                if (docid in term_dict[term].keys()):
                    term_dict[term][docid][0] = doclen 
                    term_dict[term][docid][1] += 1;
                else:
                    term_dict[term][docid] = [0,0]
                    term_dict[term][docid][0] = doclen
                    term_dict[term][docid][1] = 1;                

            pattern = 'ca\d{6}'
            matched = re.match(pattern, term)
            if (matched != None):
                flag = True
            
            if ((flag == True) and (term == 'pm' or term == 'am')): break
        count += 1;
    
    output = open('inverted_index.pkl', 'wb');
    pickle.dump(term_dict, output);
    output.close()


start_time = time.time()
getStopWords()
process()
print("Total time taken is {} seconds...".format(time.time() - start_time))
