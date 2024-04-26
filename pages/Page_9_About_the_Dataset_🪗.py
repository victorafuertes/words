import streamlit as st
import nltk
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

st.title('ABOUT THE DATASET')

st.header('DATA SOURCES FOR THIS PROJECT')

st.image('BANNER.png', caption='Sources: Billboard (Year-End Charts 2006-2023), Genius (Lyrics) & Spotify (Genres)')
st.write("DATAFRAME SHAPE:")
st.write(df.shape)
st.dataframe(df)
st.write('Here is what the actual Dataframe for this project looks like.')
st.write('- I started out initially with the Year, Rank, Title & Artist columns which I was able to obtain via the Billboard Year end charts which ranged from 2006 to 2023')
st.write('- I was then able to obtain the Lyrics using a combination of the Genius API along with LyricsGenius, because lyrics are surprisingly inaccesible')
st.write('- Lastly, I obtained the Genre column via the Spotify API. (Specifically, the artist associated genre(s) because the Spotify API doesnt return track Genre(s))')
st.write('- I then used nltk to tokenize the Lyrics and Genres columns and then did a whole lot of cleaning, specifically on the lyrics.')
st.write('Someone literally wrote in the ENTIRE SCRIPT for "STAR WARS: THE LAST JEDI" as the Lyrics for one of the entries in the list. There were a few instances of this kind of situation which resulted in some entries being removed from the dataframe; partly because it seems that Genius allows some users to edit the Lyrics content of songs, which of course results in people trying to advertise some strange product or just Star Wars I guess.')
st.write('')
st.write('')
st.subheader("DESCRIBE METHOD:")
st.write(df.describe())

 
