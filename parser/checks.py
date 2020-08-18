import nltk
nltk.download('punkt')
txt= "Hello everyone. Welcome to GeeksforGeeks."
li= nltk.tokenize.word_tokenize(txt)
print(li[0])