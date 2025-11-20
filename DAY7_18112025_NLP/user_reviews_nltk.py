import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import pandas as pd
import numpy as np


reviews = []
final_words_arr = []
lemma_words_arr = []

def extract_final_words(arr):
    final_words = []
    for word in arr:
        if word not in stopwords.words('english'):
            final_words.append(word)
    return final_words

def extract_lemmas(arr):
    lemmas = []       
    for word in arr:
        word = WordNetLemmatizer().lemmatize(word)
        lemmas.append(word)
    return lemmas
        
            
def sentiment_analyse(sentiment_text):
    res = ""
    # print(sentiment_text)
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    # print("Polarity Score" , score)

    if score['neg'] > score['pos']:
        # print("Negative Sentiment\n")
        res = "Negative"
    elif score['neg'] < score['pos']:
        # print("Positive Sentiment\n")
        res = "Positive"
    else:
        # print("Neutral Sentiment\n")
        res="Neutral"
    return res , score


'''
This main is for Product Reveiws from a E commerce Platform
'''

# if __name__ == "__main__":
#     with open('./user_reviews.txt' , 'r' , encoding="utf-8") as f:
#         for line in f:
#             r = line.strip()
#             r = r.lower()
#             # print(r+"\n")
#             reviews.append(r)
#     # print(reviews)     
#     for review in reviews:
#         cleaned_r = review.translate(str.maketrans('', '', string.punctuation))
#         tokenized_words = word_tokenize(cleaned_r, "english")
#         # print(tokenized_words)
#         final_words = extract_final_words(tokenized_words)
#         # print(final_words)
#         final_words_arr.append(final_words)
#         lemmas = extract_lemmas(final_words)
#         # print(lemmas)
#         lemma_words_arr.append(lemmas)
#         # print("Review --- ", review)
#         sentiment_analyse(' '.join(lemmas))
#         # sentiment_analyse(cleaned_r)
#         # print(senti)
        
        
'''
Twitter Sentiment Analysis
'''

if __name__ == "__main__":
    df = pd.read_csv("./twitter_training.csv")
    tweets = df['Review'].loc[:99].to_list()
    # print(tweets)
    sentiment = []
    scores=[]
    for t in tweets:
        cleaned_r = str(t).translate(str.maketrans('', '', string.punctuation))
        tokenized_words = word_tokenize(cleaned_r, "english")
        final_words = extract_final_words(tokenized_words)
        final_words_arr.append(final_words)
        lemmas = extract_lemmas(final_words)
        lemma_words_arr.append(lemmas)
        res,score = sentiment_analyse(cleaned_r)
        sentiment.append(res)
        scores.append(score)
    df1 = df.loc[:99,:].copy()
    # print(df1)
    df1['Sentiment_Predicted'] = sentiment
    df1['Score'] = scores
    print(df1[['Sentiment' , 'Sentiment_Predicted']])
    acc = (df1['Sentiment'] == df1['Sentiment_Predicted']).sum()
    print("Accuracy" , acc)
        