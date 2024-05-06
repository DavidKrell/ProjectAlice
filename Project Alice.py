#!/usr/bin/env python
# coding: utf-8

# In[17]:


import random
import re
import numpy as np

# Paths to the text files (you need to adjust these to your actual file paths!!!)
file_paths = [
    '/Users/nuri/Downloads/Lewis Carroll - Through the Looking-Glass.txt',
    '/Users/nuri/Downloads/Lewis Carroll - Alices Adventures in Wonderland.txt'
]

# Read the entire document as a single string
def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        document = file.read()
    return document

# Load documents
loaded_documents = [load_text_file(path) for path in file_paths]

def generate_random_words(documents, number_of_words=20):
    """
    :param documents, could be one or more documents, from wich the word should be genearated
    :param number_of_words: int, num of words that should be generated, by default = 20.
    :return: list of words.
    """
    words = documents.split()
    
    if len(words) < number_of_words:
        raise ValueError("not eneught words in documents")

    random_words = random.sample(words, number_of_words)
    
    return random_words

documents = " ".join(loaded_documents)

random_words = generate_random_words(documents)

def create_term_document_matrix(documents, terms):
    # Initialize the term-document matrix with zeros
    tdm = np.zeros((len(terms), len(documents)), dtype=int)

    # Compile regular expressions for terms to find sub-string matches
    regexes = [re.compile(rf"{term}", re.IGNORECASE) for term in terms]
    

    # Fill the term-document matrix
    for i, regex in enumerate(regexes):
        for j, doc in enumerate(documents):
            # Use regex to find all occurrences, including partials within words
            matches = regex.findall(doc)
            tdm[i, j] = len(matches)

    return tdm

#Test Strings from Wonderland. Header information from the Book so they are unique
test_strings = ["The", "Millennium", "Fulcrum", "Edition", "1.7"]

#to test just replace random_words with test_strings. they just appear in Wonderland! without The obviously
term_document_matrix = create_term_document_matrix(loaded_documents, random_words)
print(term_document_matrix)
print(random_words)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




