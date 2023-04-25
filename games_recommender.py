import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

games_df = pd.read_csv("processed_games_data.csv")

def combine_features(row):
    return str(row['genres']) + " " + str(row['platforms']) + " " + str(row['summary'])
games_df['combined_features'] = games_df.apply(combine_features, axis=1)
vectorizer = TfidfVectorizer(stop_words="english")
features_matrix = vectorizer.fit_transform(games_df['combined_features'])
svd = TruncatedSVD(n_components=100)
features_matrix_svd = svd.fit_transform(features_matrix)
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(features_matrix_svd)

def get_recommendations(title, nn_model, games, top_n=10):
    if title not in games['name'].values:
        return f"Игра с названием '{title}' не найдена в данных."
    index = games[games['name'] == title].index[0]
    distances, indices = nn_model.kneighbors(features_matrix_svd[index].reshape(1, -1), n_neighbors=top_n+1)
    neighbor_indices = indices[0][1:]
    return list(games['name'].iloc[neighbor_indices])

def recommend_games_bot(game_title):
    recommended_games = get_recommendations(game_title, nn, games_df)
    recommendations = "\n".join(recommended_games)

    return recommendations
