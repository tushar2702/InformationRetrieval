'''
Created on 06-Oct-2013

@author: tushar
'''
import math;
import sys;

P = list(); # set of all pages
M = dict(); # dictionary that holds all in links to each page
d = 0.85; # damping/teleportation factor
L = dict(); # dictionary to store number of out links from each page
S = list(); # set of sink nodes
PR = dict(); # Holds Page rank of each page
perplexityList = list(); # list that maintians last four values of perplexity

def main(filename):
    readGraph(filename);
    computePageRank();
    print("Done. Please see the output file 'perplexity.txt' for perplexity values...")
    

def readGraph(filename):
    print("Execution in progress. Please Wait...");
    graphFile = open(filename);
    for line in graphFile:
        line = line.rstrip();
        x = line.split(' ');
        p = x[0];
        P.append(p);
        M[p] = list();
        for i in range(1, len(x)):
            M[p].append(x[i]);
            
    graphFile.close();
    
    for node in M.keys():
        for val in M.get(node):
            if (val in L.keys()):
                newValue = L.get(val) + 1;
                L[val] = newValue;
            else:
                L[val] = 1;
                
    for p in P:
        if (p not in L.keys()):
            if (p not in S):
                S.append(p);

def computePageRank():
    perplexityFile = open('perplexity.txt' , 'w');
    newPR = dict(); # temporary PR dictionary
    N = len(P);
    H = 0;
    for p in P:
        PR[p] = 1/N;
        H -= (PR[p] * math.log(PR[p],2));
    perplexity = math.pow(2, H);
    perplexityFile.write('Perplexity after 1 iteration:'.ljust(40) + str(perplexity).ljust(40) + '\n');
    iterationNumber = 2;
    while(isNotConverged(perplexity)):
        sinkPR = 0
        for p in S: # calculate total sink PR
            sinkPR += PR[p];
        for p in P:
            newPR[p] = (1-d)/N; # teleportation
            newPR[p] += d*sinkPR/N; # spread remaining sink PR evenly
            for q in M[p]: # pages pointing to p
                newPR[p] += d*PR[q]/L[q]; # add share of PageRank from in-links
        H = 0;
        for p in P:
            PR[p] = newPR[p];
            H -= (PR[p] * math.log(PR[p],2));
        perplexity = math.pow(2, H);
        perplexityFile.write('Perplexity after {} iterations:'.ljust(40).format(iterationNumber) + 
                             str(perplexity).ljust(40) + '\n');
        iterationNumber+=1;
    perplexityFile.close();   
        
def isNotConverged(perplexity):
    if (perplexityList.__len__() > 4):
        perplexityList.__delitem__(0);
    perplexityList.append(int(perplexity));
    if (perplexityList.__len__() < 4):
        return True;
    else:
        val1 = str(perplexityList[0]).__getitem__(len(str(perplexityList[0]))-1);
        val2 = str(perplexityList[1]).__getitem__(len(str(perplexityList[1]))-1);
        val3 = str(perplexityList[2]).__getitem__(len(str(perplexityList[2]))-1);
        val4 = str(perplexityList[3]).__getitem__(len(str(perplexityList[3]))-1);
        
        if (val1 == val2 and val1 == val3 and val1 == val4):
            return False;
        perplexityList.__delitem__(0);
        return True; 
        

if __name__ == '__main__':
    main(sys.argv[1])
