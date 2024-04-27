import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Define function to load data
@st.cache_data()
def load_data():
    df = pd.read_csv('Main_Data.csv')
    return df

# Define function to tokenize and filter lyrics
@st.cache_data()
def tokenize_and_filter(text):
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
    tokens = text.split()  
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in custom_stopwords]
    return filtered_tokens

# Define function to get sentiment score
@st.cache_data()
def get_sentiment_score(text):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(' '.join(text))['compound']

# Define function to calculate genre metrics
@st.cache_data()
def calculate_metrics(df, genres):
    genre_popularity = {}
    genre_word_count = {}
    genre_sentiment_score = {}

    for genre in genres:
        genre_data = df[df['Genres'].str.contains(genre, case=False, na=False)]
        
        genre_popularity[genre] = len(genre_data)
        
        genre_word_count[genre] = genre_data['Processed Lyrics'].apply(len).mean()
        
        genre_sentiment_score[genre] = genre_data['Processed Lyrics'].apply(get_sentiment_score).mean()

    return genre_popularity, genre_word_count, genre_sentiment_score

# Main function
def main():
    df = load_data()
    df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)
    
    st.title('Genre Analysis')
    
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

    def tokenize_and_filter(text):
        tokens = text.split() 
        filtered_tokens = [token.lower() for token in tokens if token.lower() not in custom_stopwords]
        return filtered_tokens

    df['Processed Lyrics'] = df['Lyrics'].apply(tokenize_and_filter)

    all_genres = df['Genres'].str.split(',').explode().str.strip()
    genre_freq = nltk.FreqDist(all_genres)

    default_genres = [genre for genre, _ in genre_freq.most_common(10)]

    st.title('Genre Analysis')
    add_fundamental_genres = st.sidebar.checkbox("Fundamental Genres", False)

    if add_fundamental_genres:
        fundamental_genres = ['Blues', 'R&B', 'Country', 'Electronic', 'Folk', 
                            'Hip hop', 'Jazz', 'Latin', 'Reggae', 'Rock']
        target_genres = fundamental_genres
        st.write("Analyzing the Fundamental Genres based on popularity, average word count and, sentiment score.")
    else:
        target_genres = st.sidebar.multiselect("Select Genres:", all_genres.unique(), default=default_genres)
        if not target_genres:
            target_genres = default_genres
        st.write("Analyzing the Top 10 genres based on popularity, average word count, and sentiment score.")

    genre_popularity, genre_word_count, genre_sentiment_score = calculate_metrics(df, target_genres)

    st.subheader("Popularity and Average Word Count by Genre")
    metrics_df = pd.DataFrame({'Genre': target_genres,
                            'Popularity': [genre_popularity.get(genre, 0) for genre in target_genres],
                            'Avg Word Count': [genre_word_count.get(genre, 0) for genre in target_genres]})
    st.table(metrics_df)

    plt.figure(figsize=(10, 6))
    plt.bar(genre_sentiment_score.keys(), genre_sentiment_score.values(), color='skyblue')
    plt.xlabel('Genre')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Score by Genre')
    plt.xticks(rotation=45)
    st.pyplot(plt)

#RUN MAIN
if __name__ == "__main__":
    main()
