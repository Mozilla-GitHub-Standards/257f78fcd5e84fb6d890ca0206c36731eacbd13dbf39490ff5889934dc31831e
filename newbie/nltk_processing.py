import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

wn.ensure_loaded()

nltk.download("stopwords")
cachedStopWords = stopwords.words("english")


class NltkProcess:
    def __init__(self):
        nltk.download("stopwords")

    def get_stop_words(self):
        nltk.download("stopwords")
        stopwords.words('english')


def get_tag_suggestions(input_text):
    input_text = input_text.strip()
    stop_words = set(stopwords.words('english'))
    if len(input_text) <= 3:
        return ''
    word_tokens = word_tokenize(input_text)
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    filtered_sentence = [w for w in filtered_sentence if w not in punctuations]
    synonyms = [input_text]
    for w in filtered_sentence:
        for syn in wn.synsets(w):
            for l in syn.lemmas():
                # print(l)
                synonyms.append(l.name())
    return synonyms
