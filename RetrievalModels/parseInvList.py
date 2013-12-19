'''
Created on 26-Oct-2013

@author: tushar
'''

import urllib.request, re

def parseInvertedList(word):
    result = dict()
    url = "http://fiji5.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=3&g=p&v=" + word;
    text = urllib.request.urlopen(url).read().decode("UTF-8")
    data = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(text).group(1)
    numbers = re.compile(r'(\d+)',re.DOTALL).findall(data)
    
    ctf,df = float(numbers[0]), float(numbers[1]) #take the ctf and df and convert to float
    inverted_list = map(lambda i: (int(numbers[2 + 3*i]),
                                  float(numbers[3 + 3*i]),
                               float(numbers[4 + 3*i]))
                        ,range(0, (len(numbers) - 2)//3))
     
    for (docid,doclen,tf) in inverted_list:
        result[docid] = [doclen,tf]
    return result, ctf, df


