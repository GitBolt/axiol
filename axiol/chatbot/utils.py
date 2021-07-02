import nltk
import numpy
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')

stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = numpy.zeros(len(words), dtype=numpy.float32)

    for index, w in enumerate(words):
        if w in sentence_words: 
            bag[index] = 1

    return bag