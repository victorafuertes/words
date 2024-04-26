import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import numpy as np
import re
import matplotlib.dates as mdates

# Read the CSV file
df = pd.read_csv('Main_Data.csv')

# Custom list of onomatopoeias and ad libs
custom_stopwords = ['la', 'na', 'oh', 'yeah', 'Ah', 'Eh', 'Oh', 'Uh', 'Ooh', 
                    'ahh', 'ahhh', 'ehh', 'ohh', 'ohhh',
                    'hmm', 'mhm', 'hm', 'mhmm', 'hmmm', 'hmmmmm',
                    'Ha', 'huh', 'ho', 'heh', 'hah', 'Haha', 'hehe', 'hihi', 'hoho', 
                    'ja', 'je', 'ji', 'jo', 'ju', 'jaja', 'jajaja', 'jejeje', 'jijiji',
                    'jojojo', 'jujuju','da', 'de', 'di', 'du', 'da-da-da-da', 
                    'de-de-de-de', 'di-di-di','Ye', 'Yuh', 'yas', 
                    'yup', 'yee', 'uh-huh', 'yass', 'Woo', 
                    'Wee-hoo', 'Yee-hoo', 'woo-hoo', 'woo', 'Ya-hoo', 
                    'whoah', 'whoah-ho', 
                    'La-la', 'la', 'la-di-da', 
                    'sh', 'sho', 'shh', 'shuh', 'sha-ba', 'shabadoobey', 'shoobie',
                    'Ay', 'ayy', 'ayyy', 'ayyyy',
                    'Na-na', 'na', 'nah', 'nuh', 'Hey',
                    'aw', 'aww', 'awww', 'Rr', 'rrr', 'rrrr', 'pr', 'prr', 'prrr',
                    'skrt', 'skrrt', 'skrrrt', 'skiat', 'skeet', 
                    'grr', 'gr', 'grrrr', 'grrrrrrrah', 'git']  # Add more as needed

# Function to tokenize and filter out stopwords, onomatopoeias, and ad libs
def tokenize_and_filter(text):
    tokens = text.split()  # Use split instead of NLTK's word_tokenize for simplicity
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in custom_stopwords]
    return filtered_tokens

# Apply tokenization and filtering to the "Lyrics" column
df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

# Sentiment Analysis
sid = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    return sid.polarity_scores(' '.join(text))['compound']

df['Sentiment Score'] = df['Processed Lyrics'].apply(get_sentiment_score)

# Group by Year and aggregate sentiment scores
yearly_sentiment = df.groupby(pd.to_datetime(df['Year'], format='%Y').dt.year)['Sentiment Score'].mean().reset_index()

# Set up the Streamlit app
st.title('SENTIMENT ANALYSIS OF LYRICAL CONTENT BY YEAR')
st.write("Visualizing sentiment scores for the Billboard Top 100 Year end Charts for the years of 2006-2023.")

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(yearly_sentiment['Year'], yearly_sentiment['Sentiment Score'], color='skyblue')
plt.xlabel('Year')
plt.ylabel('Sentiment Score')
plt.title('Sentiment Score by Year')
plt.xticks(yearly_sentiment['Year'], rotation=45)
plt.ylim(-1, 1)  # Set y-axis limit to -1 to 1 for consistency
plt.grid(axis='y')

# Display the plot
st.pyplot(plt)
st.write('The graph above displays the sentiment score based on the lyrical content of the most popular songs (TOP 100) for each year. I think its particularly interesting how the lowest score for this timeframe happens to be the year 2020 which coincides with start and height of the COVID-19 pandemic.')
st.write('Perhaps for future studies, I think it would be interesting to have a larger year range or perhaps even monthly charts to see if theres any noticeable patters or seasonality to the sentiment scores.')
