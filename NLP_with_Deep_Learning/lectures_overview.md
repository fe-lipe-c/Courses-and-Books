# Natural Language Processing with Deep Learning

### Lecture 1: Word Vectors I - Introduction, SVD and Word2Vec.

#### 1.1 Introduction to Natural Language Processing

#### 1.2 Word Vectors

**One-hot vector** Represent every word as an $\mathbb{R}^{|V|\times 1}$ vector with all $0$s and one $1$ at the index of that word in the sorted English language.

**SVD Based Methods**  In this class of methos, to find word embeddings (word vectors), we first loop over a massive dataset and accumulate word co-occurrence counts in some form of a matrix $X$, and then perform Singular Value Decomposition on $X$ to get a $USV^{T}$. We then use the rows of $U$ as the word embeddings for all words in our dictionary. 

#### 1.3 SVD Based Methods

**Word-Document Matrix** Loop over billions of documents and for each time word $i$ appears in document $j$, we add one to entry $X_{ij}$. This is a very large matrix ($\mathbb{R}^{|V| \times M}$) and it scales with the number of documents ($M$). 

**Window based Co-occurrence Matrix** In this method we count the number of times each word appears inside a window of a particular size around the word of interest. The matrix $X$ stores co-occurrences of words, thereby becoming an affinity matrix. 
