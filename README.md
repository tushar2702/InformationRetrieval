InformationRetrieval
====================

Building an Information Retrieval system and related algorithms.

1) Web Crawler in Java: 
Implemented web crawler using www.ccs.neu.edu as the starting seed. Compared results obtained from GNU wget utility to crawl CIS college website starting with the same seed. Generated a file of the first 100 unique links, restricting the links to web pages and pdfs that are on this site.

2) PageRank algorithm in Python:
Given access to an in-link representation of the web graph, i.e., for each page p, a list of the pages q that link to p, implemented the iterative PageRank algorithm on a collection of 183,811 web documents. To test convergence, calculated perplexity of PageRank distribution until these values no longer change in the units position for at least four iterations. Also performed an analysis on top 10 pages sorted by page rank and in link counts using the Lemur web interface provided.

3) Search Engine in Python:
Implemented five different retrieval models for a given set of 25 queries and evaluate the top 1000 ranked list of documents returned by each model. Also, build the inverted index of the documents provided and run queries on this index.
