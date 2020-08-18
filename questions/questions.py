import nltk
import sys
import os
import math
import string
import copy
nltk.download('punkt')
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files= {}
    for f in os.listdir(directory):
        a= open(os.path.join(directory, f), "r")
        files[f]= a.read()
    return files
    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    # """
    final= list()
    rem= set(string.punctuation)
    rem.update(nltk.corpus.stopwords.words("english"))
    for word in nltk.tokenize.word_tokenize(document):
        word= word.lower()
        if word not in rem:
            final.append(word)
    return final
    raise NotImplementedError
    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    count={}
    idfs={}
    N= len(documents)
    for filename in documents:
        for w in set(documents[filename]):
            if w in count:
                count[w]+=1
            else:
                count[w]= 1 
    for word, val in count.items():
        idfs[word]= math.log(N/val)
    return idfs#only words that appear in atleast one document
    raise NotImplementedError
    # total = len(documents)
    # idfs = {}
    # for content in documents.values():
    #     for word in content:
    #         count = 0
    #         if word not in idfs.keys():
    #             for filename in documents:
    #                 if word in documents[filename]:
    #                     count += 1
    #             idfs[word] = math.log(total/count)
    # return idfs     


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf={filename : 0 for filename in files}
    for filename in files:
        for word in query:
            tfidf[filename]+= idfs[word]* files[filename].count(word)


    L= sorted(tfidf, key=lambda  k: tfidf[k], reverse=True)
    return L[:n]
    raise NotImplementedError

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    print(query)
    def get_qd(x):
        count=0
        for word in sentences[x[0]]:
            if word in query:
                count+=1
        return count/len(sentences[x[0]])

    score= {}
    for sentence in sentences:
        s=0
        for word in query:
            if word in set(sentences[sentence]):
                s+= idfs[word]
        score[sentence]= s
    sorted_tups= sorted(score.items(), key = lambda x: x[1], reverse=True)
    sorted_score= [j for i, j in sorted_tups]
    i=0
    while i< len(sorted_score):
        sen, sc= sorted_tups[i]
        if sorted_score.count(sc)> 1:
            k= i+1
            reps= []
            reps.append(sorted_tups[i])
            while k< len(sorted_score) and sorted_tups[k][1]== sc:
                reps.append(sorted_tups[k])
                k+=1
            reps.sort(key = get_qd, reverse = True)
            sorted_tups[i:k]= reps
            i= k
        else:
            i+=1
    # return sorted_tups[:n]
   
    return [i for i, j in sorted_tups[:n]]
    raise NotImplementedError


if __name__ == "__main__":
    main()
