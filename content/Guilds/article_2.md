Title: Bag of Words Example
Date: 2019-07-21
Tags: Python,Machine Learning,BOG, Nima Moradi
Category: Research
Summary: An example of Bag of Words using python

Bag of Words bag of words is one of the most basic ways to represent a word, it is simply a word counter. let us look at an example
```
1 :) John likes to watch movies. Mary likes movies too.

2 :) John also likes to watch football games.
```
if we count the occurrence of each word
```
BoW1 = {"John":1,"likes":2,"to":1,"watch":1,"movies":2,"Mary":1,"too":1};

BoW2 = {"John":1,"also":1,"likes":1,"to":1,"watch":1,"football":1,"games":1};
```
Ok let us see how to implement it in python


```python
# the dataset we use called 20 newsgroup it consist of 20 group with short text 
# scikit have builtin way to load the dataset just like iris and etc.
from sklearn.datasets import fetch_20newsgroups
newsgroups_train = fetch_20newsgroups(subset='train',remove=('headers', 'footers', 'quotes'), shuffle=True, random_state=42)

from pprint import pprint

```


```python
# here we will only work with data section because bag of word don't need labels
pprint(list(newsgroups_train))
```

the first thing bag-of-word do is consist of a corpus of all existing word and make a one-hot vector for each of them.

Now each we have a very large vector with one 1 in each row, we represent each sentence as a vector with for existing word it will show 1 in a corresponding bit and 0 not present.


```python
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
```


```python
from sklearn.feature_extraction.text import CountVectorizer

corpus = newsgroups_train.data

vectorizer = CountVectorizer()
vectorizer.fit_transform(corpus).todense()

print( take(10, vectorizer.vocabulary_.items()) )
```


```python
#  to demonstrate let us consider this corpus 
#  we have 24-word unique word with will be of vector size for each word and every sentence is the summation of its unique binary words
corpus = [
'All my cats in a row',
'When my cat sits down, she looks like a Furby toy!',
'The cats from outer space',
'Sunshine loves to sit like this for some reason.'
]

vectorizer = CountVectorizer()
print( vectorizer.fit_transform(corpus).todense() )
print( vectorizer.vocabulary_ )

```

# Preprocssing

in our above code model will consider cat and cats diffrent word and have may useless word in our bow

####Stopwords 
Stopwords are a collection of common words like 'a','is','the'
which would not contribute too much on the meaning of sentence 
####Stemming
stemming is process of remove prefix and suffix form words, doing this make study and studing a single word,bear in mind that using lemmatization will lead to better result, but it's harder to impelement on your own.


```python
# we use stopwords list from nltk
import nltk
# download stop words if you do not have it with this command {nltk.download('stopwords')}
from nltk.corpus import stopwords


```


```python
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

def process(input_text):
    # Create a regular expression tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    # Create a Snowball stemmer 
    stemmer = SnowballStemmer('english')

    # Get the list of stop words 
    stop_words =  nltk.corpus.stopwords.words('english')
    
    # Tokenize the input string
    tokens = tokenizer.tokenize(input_text.lower())

    # Remove the stop words 
    tokens = [x for x in tokens if not x in stop_words]
    
    # Perform stemming on the tokenized words 
    tokens_stemmed = [stemmer.stem(x) for x in tokens]

    return ' '.join(tokens_stemmed) 
```


```python
for index,item in enumerate(newsgroups_train.data):
    newsgroups_train.data[index] = process(item) 
```


```python
len(newsgroups_train.data)
```


```python
import numpy as np

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(newsgroups_train.data)
print( X_train.shape )

```

### The downsides of Bag of words


1. Vectors assign to each word is meaningless, and for there is a pattern between two semantically similar words and their corresponding vectors.

2. Words are not normalized if we want to a summarized document in our bow model we should show words with the highest score which will be many common words that probably repeated in other documents too.

3. sparseness each word vector is a super long vector with only 1 bit and all other zeros which cause memory inefficiency

nima moradi 21/7/2019  [My page twitter](https://twitter.com/ni_moradi "twitter page nima moradi")
