import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

def main():
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

    # Function to calculate sentiment score
    sid = SentimentIntensityAnalyzer()

    def get_sentiment_score(text):
        return sid.polarity_scores(' '.join(text))['compound']

    # Calculate the frequency of each genre
    all_genres = df['Genres'].str.split(',').explode().str.strip()
    genre_freq = nltk.FreqDist(all_genres)

    # Select the top 10 most frequent genres
    default_genres = [genre for genre, _ in genre_freq.most_common(10)]

    # Initialize dictionaries to store metrics for each genre
    genre_popularity = {}
    genre_word_count = {}
    genre_sentiment_score = {}

    # Function to calculate metrics for given genres
    def calculate_metrics(genres):
        for genre in genres:
            # Filter data for the current genre
            genre_data = df[df['Genres'].str.contains(genre, case=False, na=False)]
            
            # Popularity: Count occurrences of the genre
            genre_popularity[genre] = len(genre_data)
            
            # Average Word Count: Calculate average word count for the genre
            genre_word_count[genre] = genre_data['Processed Lyrics'].apply(len).mean()
            
            # Sentiment Analysis: Calculate sentiment score for the genre
            genre_sentiment_score[genre] = genre_data['Processed Lyrics'].apply(get_sentiment_score).mean()

    # Set up the Streamlit app
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

    # Calculate metrics for selected genres
    calculate_metrics(target_genres)

    # Display metrics for each genre as a table
    st.subheader("Popularity and Average Word Count by Genre")
    metrics_df = pd.DataFrame({'Genre': target_genres,
                            'Popularity': [genre_popularity.get(genre, 0) for genre in target_genres],
                            'Avg Word Count': [genre_word_count.get(genre, 0) for genre in target_genres]})
    st.table(metrics_df)

    # Plotting sentiment scores for each genre
    plt.figure(figsize=(10, 6))
    plt.bar(genre_sentiment_score.keys(), genre_sentiment_score.values(), color='skyblue')
    plt.xlabel('Genre')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Score by Genre')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Run the main function
main()
