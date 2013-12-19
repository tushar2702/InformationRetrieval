'''
Created on 30-Nov-2013

@author: tushar
'''

import re
from bs4 import BeautifulSoup

def loadQueries():
    
    queries_dict = dict()
    queryFile = open("cacm.query",'r')
    queries = BeautifulSoup(queryFile)
    for query in queries:
        query = str(query).replace('\n', ' ')
        query = str(query).replace('  ', ' ')
        if query == '' or query == ' ': continue
        data = re.compile(r'.*?<doc>(.*?)</doc>', re.DOTALL).match(str(query)).group(1)
        query_num = re.compile(r'.*?<docno>(.*?)</docno>',re.DOTALL).match(data).group(1)
        query_data = data.replace("<docno>"+re.compile(r'.*?<docno>(.*?)</docno>',re.DOTALL).match(data).group(1)+"</docno>","")
        query_num = str(query_num).strip()
        query_data = str(query_data).strip()
        queries_dict[query_num] = query_data
    return queries_dict

loadQueries()