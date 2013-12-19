'''
Created on 24-Nov-2013

@author: tushar
'''

from bs4 import BeautifulSoup
import re
from stemming.porter2 import stem

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
    total = 0
    term_dict = dict()
    count_prefix_initial = '0000';
    count = 1;
    htmlPath = 'C:\\Users\\tushar\\Desktop\\cacm.tar\\CACM-' # path to your cacm documents folder.
    file_suffix = '.html'
    doclen_dict = dict()
    num_terms = 0;
    unique_terms_set = set();
    
    while count <= 3204:
        
        countPrefix = count_prefix_initial[0:(len(count_prefix_initial)-len(str(count)))]
        fileName = str(htmlPath+countPrefix+str(count)+ file_suffix)
        print(fileName)
        
        text = getHtmlDoc(fileName);
        text = str(text).replace('\n', ' ')
        
        
        myvalues = re.split(" ", str(text))
        docid = 'CACM-' + countPrefix + str(count)
        
        doclen = 0
        flag = False
        for term in myvalues:
            
            if (term == '' or term == ' '): continue
            
            pattern = 'CA\d{6}'
            matched = re.match(pattern, term)
            if (matched != None):
                flag = True
            
            # make it lower case
            term = str(term).lower()
                
            term = stem(term)
            num_terms += 1;
            unique_terms_set.add(term)
            doclen += 1;
                
            if ((flag == True) and (term == 'pm' or term == 'am')): break
    
        count += 1;
        doclen_dict[docid] = doclen;
    
    sum = 0;
    counter = 0;
    for val in doclen_dict.keys():
        sum += doclen_dict[val];
        counter += 1;
    average = sum/counter
    print(sum)
    print(counter)    
    print("Average doc len is " + str(average))
    
    print("num terms is " + str(num_terms))
    print("unique terms is " + str(len(unique_terms_set)))

process()