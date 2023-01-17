# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 22:08:11 2023

@author: sifis
"""

import nltk   
nltk.download('vader_lexicon') #the nltk uses the pretrained model called Vader which has to be downloaded.
# Vader uses bag of words and looks at each word and scores it individually without considering the relationship between the words or context
import pandas as pd
import numpy  
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns
import emoji

from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

#Load the Roberta model 
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

# Download the model from the website
model = AutoModelForSequenceClassification.from_pretrained(roberta) 

#load tokenizer to convert our text into numbers to pass them into our model
tokenizer = AutoTokenizer.from_pretrained(roberta)

pd.set_option('display.max_columns', None)   # to show all the columns
#pd.set_option('display.max_rows', None)

#READING THE DATA
df = pd.read_excel('TechLabsDataset.xlsx')

#subset of only those companies with text/written reviews      #3398
with_reviews = df[df['review_EN'].notna()]     
#print(with_reviews)

#testing with the first 10 entries
#with_reviews = with_reviews.iloc[:10,:]

negative = []
neutral = []
positive = []

for idx, review in with_reviews.iterrows():    #iterating through the df to get just the reviews
    review_text = review.loc['review_EN']


# Sentiment Analysis
#example = "I like data science, it is interesting"

# first convert the text into PyTorch Tensors and then pass that into the model
    encoded_text = tokenizer(review_text, return_tensors='pt') 
#print(encoded_text)

# pass the encoded text into the model for sentiment analysis
#output = model(encoded_text['input_ids'], encoded_text['attention_mask']) #specifying the keys from the tokenizer output
#an easier way to do the same
    output = model(**encoded_text) #it unpacks the encoded_text dictionary and then passes it to the model 
#print(output) 
# the output is a tensor which we convert using the softmax function
    scores = output[0][0].detach().numpy()   # the tensor values we want are in an inner list
#when converting a torch.tensor to np.ndarray you must explicitly remove the computational graph of the tensor using the detach() command.
#print(scores)
    scores = softmax(scores)      #passing the scores into a softmax function
   
    negative.append(scores[0]*100)
    neutral.append(scores[1]*100)
    positive.append(scores[2]*100)

#Adding columns for the compound sentiment value and the sentiment for both models
with_reviews["Negative"]= negative
with_reviews["Neutral"]= neutral
with_reviews["Positive"]= positive


# Adds the maximum value from the three columns
#with_reviews['Max'] = with_reviews[['Negative', 'Neutral', 'Positive']].max(axis=1)   

#Getting a subset of the data frame inorder to get the column with the max value hence our sentiment
sliced = with_reviews[['Negative', 'Neutral', 'Positive']]
#Adding a new column with the Sentiment 
sliced['Roberta_Sentiment'] = sliced.idxmax(axis=1)
#print(sliced)
# combining the two data frames
combined_df = pd.merge(with_reviews, sliced, on=['Negative', 'Neutral', 'Positive'],
         how='right')
print(combined_df)

#writing to excel
combined_df.to_excel("Sent_Analysis_Roberta.xlsx") 

   
#DistilBert Model    
#sent_pipeline = pipeline("sentiment-analysis") 
#pipeline_result = sent_pipeline(example)