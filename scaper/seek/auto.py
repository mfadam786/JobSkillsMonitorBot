"""
This file contains code that will be used to automate scraping, model training and loading data into database
"""
import pandas as pd
from pathlib import Path
import unicodedata
import ast
import numpy as np
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import subprocess
from gensim.models.phrases import Phrases, Phraser
from gensim.models import phrases
from gensim.models.phrases import Phrases

subprocess.run("scrapy crawl seek")

scraped_df = pd.read_csv("../data/scraped.csv", comment="#")


def fix_content(x):
    if type(x) != type(np.nan):

        arr = []
        for i in ast.literal_eval(x):
            arr.append(unicodedata.normalize("NFKD", i).strip())
        return " ".join(np.asarray(arr).flatten().tolist())


scraped_df["fixed_content"] = scraped_df["main_content"].transform(fix_content)

scraped_df = scraped_df.dropna(subset=["fixed_content"])

scraped_df["sent_tokens"] = scraped_df["fixed_content"].transform(lambda x : sent_tokenize(x))

sent_corp = [
]

stop_words = set(stopwords.words("english"))

for i in scraped_df["sent_tokens"].values:
    for sentence in i:

        sent = word_tokenize(sentence)
        sent_clean = []
        for word in sent:
            if word.isalpha() and word not in stop_words:
                sent_clean.append(word.lower())
        # word.lower() for word in sent if word.isalpha() and word not in stop_words
        sent_corp.append(sent_clean)


bigram = Phrases(sent_corp, min_count=25)

a_words = ["senior", "junior", "intermediate", "beginner", "database", "data", "web", "frontend", "backend", "fullstack",
           "security", "software", "marketing", "programming", "development", "product","technology", "advanced",
           "scientific", "research" ]

b_words="""engineer
scientist
assistant
leader
developer
admin
administrator
worker
lead
expert
programmer
intern
analyst
researcher
professional
architect
administration
manager
management""".split("\n")

manual_bigrams = []

for i in a_words:
    for j in b_words:
        manual_bigrams.append(f"{i}_{j}")

frozen_phrases = bigram.freeze()

for b in manual_bigrams:
    frozen_phrases.phrasegrams[b] = float('inf')

model = Word2Vec(frozen_phrases[sent_corp], min_count=5,workers=24, sg = 0)

model.save("../models/word2vec_bi_manual_cb.model")



