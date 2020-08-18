import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linksto= corpus[page]
    prob={}
    numberoflinksto= len(linksto)
    numberofkeys= len(corpus)
    
    if numberoflinksto== 0:
        for k in corpus:
            prob[k]= 1/numberofkeys
    else:      
        prob1= (1- damping_factor)/numberofkeys
        prob2= (damping_factor/numberoflinksto) + ((1- damping_factor)/numberofkeys)
        for y in corpus:
            if y in linksto:
                prob[y]= prob2
            else:
                prob[y]= prob1
    return prob
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    firstpage= np.random.choice(list(corpus.keys()))
    pr={}
    for x in corpus:
       pr[x]=0
    pr[firstpage]= 1/n
    i=1
    currentpage= firstpage
    while i!= n:
        trans= transition_model(corpus, currentpage, damping_factor)
        nextpage= np.random.choice(list(trans.keys()), p= list(trans.values()))
        pr[nextpage]+= 1/n
        currentpage= nextpage
        i+= 1
    return pr
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr= {}
    prev={}
    corpus1= {}
    N= len(corpus)
    corpus1= corpus.copy()
    for x in corpus:
        pr[x]= 1/N
        if len(corpus[x])== 0:
            corpus1[x]= set(corpus.keys())
            
    flag= True
    while flag:
        flag= False
        prev= pr.copy()
        for x in pr:
            s=0
            for y in corpus1:
                if x in corpus1[y]:
                    s+= prev[y]/len(corpus1[y])
            pr[x]= (1- damping_factor)/N + damping_factor*s
            pr[x]= round(pr[x], 4)
        for z in pr:
            if abs(pr[z]- prev[z])> 0.001:
                flag= True
                break
    return pr
    raise NotImplementedError


if __name__ == "__main__":
    main()
