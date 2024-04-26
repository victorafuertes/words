import streamlit as st
import nltk
nltk.download('punkt')
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# Function to tokenize and filter out non-alphanumeric tokens
def tokenize_and_filter(text):
    tokens = nltk.word_tokenize(text)
    # Filter out non-alphanumeric tokens
    filtered_tokens = [token for token in tokens if re.match(r'^\w+$', token)]
    return filtered_tokens

# Function to tokenize and separate genres by commas
def tokenize_and_split_genres(genres):
    if pd.isna(genres):  # Handle missing values
        return []
    else:
        return re.split(r',\s*', genres)
    
#------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION I - LOADING CSV - TOKENIZING:

csv_directory = ('Main_Data.csv')

df = pd.read_csv(csv_directory)

# Apply tokenization and filtering to the "Lyrics" column
df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

# Count the tokens in each row for lyrics
df['Word Count'] = df['Processed Lyrics'].apply(len)

# Apply tokenization and splitting to the "Genres" column
df['Processed Genres'] = df['Genres'].apply(tokenize_and_split_genres)

# Count the tokens in each row for genres
df['Genre Count'] = df['Processed Genres'].apply(len)

# Drop unnecessary columns
df.drop(columns=['Lyrics', 'Entry #'], inplace=True)


#-------------------------------------------------------------------------------------------------------------------------------------------------
# SECTION II - CREATING VARIABLES AND FUNCTIONS TO BE CALLED IN STREAMLIT: 

# BRIEFS SUMMARY STATS 
TOTAL_WORDS = df['Word Count'].sum()
TOTAL_UNIQUE_WORDS = len(set(word for sublist in df['Processed Lyrics'] for word in sublist))
TOTAL_ENTRIES = len(df)
TOTAL_GENRES = len(set(genre for sublist in df['Processed Genres'] for genre in sublist))
TOTAL_SONGS = df['Title'].nunique()
TOTAL_ARTISTS = df['Artist'].nunique()
AVG_WORD_COUNT_PER_SONG = TOTAL_WORDS / TOTAL_SONGS
#----------------------------------------------------------------------------------------------------------------------------------------------
# SECTION III - STREAMLIT: 

st.title('WORDS, WORDS, WORDS!')
st.header('The state of Popular Song Lyrics over the years (2006-2023)')
st.write('')
st.subheader('SUMMARY')
st.write("The goal of this project was to study the word count of popular song lyrics over time. I wanted to observe any present changes essentially based on the hypothesis that music has become much more 'repetitive'.")
st.write('For this purpose, I gathered the Top 100 Songs from the Billboard year end charts for the years 2006-2023, acquired their lyrics through Genius and their associated Genres through Spotify.')
st.write('My hypothesis was based on the common assumption that music has become more repetitive over the years. I was expecting to observe an increase in overall word count and a decrease (or no increase) in unique word count. However, my findings, went against my hypothesis and preconceptions.')
st.write('Results indicate that for Popular song lyrics, between 2006 and 2023, there has been a 10.06 percent decrease in the average unique words per song as well as a 22.578 percent decrease in average word count.  ')


st.subheader('SOURCES')
st.image('BANNER.png', caption='Sources: Billboard (Year-End Charts 2006-2023), Genius (Lyrics) & Spotify (Genres)')


 
