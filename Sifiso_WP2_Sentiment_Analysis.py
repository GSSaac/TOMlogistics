# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:47:45 2022

@author: sifis
"""

import nltk   
nltk.download('vader_lexicon') #the nltk uses the pretrained model called Vader which has to be downloaded.
# Vader uses bag of words and looks at each word and scores it individually without considering the relationship between the words or context
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns
import emoji

from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# initalize our 2 model analyzers
sia = SentimentIntensityAnalyzer()    # Vader Model
sent_pipeline = pipeline("sentiment-analysis")   #DistilBERT model

pd.set_option('display.max_columns', None)   # to show all the columns
#pd.set_option('display.max_rows', None)

#READING THE DATA

df = pd.read_excel('TechLabsDataset.xlsx')

#subset of only those companies with text/written reviews      #3398
with_reviews = df[df['review_EN'].notna()]     
#print(with_reviews)

compound_val_listVader = []
sentiment_listVader = []
sentiment_listPipeline = []
compound_val_listPipeline = []
for idx, review in with_reviews.iterrows():    #iterating through the df to get just the reviews
    review_text = review.loc['review_EN']
    emojis = emoji.distinct_emoji_list(review_text)    #Returns distinct list of emojis from the string
    for is_emoji in emojis:
        demoji_text = emoji.demojize(is_emoji)
        demoji_text = demoji_text.replace("_", " ")  # removing the underscore and the colon from the emoji text
        demoji_text = demoji_text.replace(":", "")
        review_text = review_text.replace(is_emoji, demoji_text)  # replacing the emoji with its text
        
    # Model 1
    sentiment = sia.polarity_scores(review_text) #using the nltk vader3 model to do the sentiment analysis 
    compound = sentiment['compound']   #taking the 'compound' key result
    compound_val_listVader.append(compound)
    if -0.1 < compound < 0.1:          # labelling the sentiments
        sentiment_listVader.append("neutral")
    elif compound > 0:
        sentiment_listVader.append("positive")
    else:
        sentiment_listVader.append("negative")

# Vader doesnt recognise some of the emoji text like thumbs up is analysed as neutral 
  
    # Model 2
    pipeline_result = sent_pipeline(review_text)[0]
    sentiment_listPipeline.append(pipeline_result["label"])
    compound_val_listPipeline.append(pipeline_result["score"])

#Adding columns for the compound sentiment value and the sentiment for both models
with_reviews["Sentiment_com"]= compound_val_listVader
with_reviews["Sentiment"]= sentiment_listVader
with_reviews["Sentiment_com_Pipeline"]= compound_val_listPipeline
with_reviews["Sentiment_Pipeline"]= sentiment_listPipeline
#print(with_reviews)


with_reviews.to_excel("Reviews_withsentiment.xlsx") #writing to excel

#Barplot to check sentiment score vs number of stars
#plt.ylim(-1, 1)
#bgraph = sns.barplot(data= with_reviews, x= "stars_num", y= "Sentiment_com")
#bgraph.set_title("Compound Score vs Star Ratings")
#plt.show()    # why is the graph not plotting from  -1 and 1 ?????

#max_comp= (with_reviews["Sentiment_com"].max())
#min_comp = (with_reviews["Sentiment_com"].min())
#print(max_comp, min_comp)







