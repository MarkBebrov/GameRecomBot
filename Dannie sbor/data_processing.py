import json
import pandas as pd
from datetime import datetime

with open("games_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

games_df = pd.DataFrame(data)

games_df.drop_duplicates(subset=['name'], inplace=True)

def process_genres(genres_list):
    if isinstance(genres_list, list):
        return ', '.join([genre['name'] for genre in genres_list])
    return None

games_df['genres'] = games_df['genres'].apply(process_genres)

def process_platforms(platforms_list):
    if isinstance(platforms_list, list):
        return ', '.join([platform['name'] for platform in platforms_list])
    return None

games_df['platforms'] = games_df['platforms'].apply(process_platforms)

def process_release_date(release_dates_list):
    release_dates = []
    if isinstance(release_dates_list, list):
        for date in release_dates_list:
            if isinstance(date, dict) and 'date' in date and date['date'] is not None:
                try:
                    release_dates.append(datetime.utcfromtimestamp(date['date']).strftime('%Y-%m-%d'))
                except OSError:
                    pass
    if release_dates:
        return min(release_dates)
    return None




games_df['release_date'] = games_df['release_dates'].apply(process_release_date)
games_df.drop(columns=['release_dates'], inplace=True)

games_df['rating'].fillna(games_df['rating'].mean(), inplace=True)
games_df['genres'].fillna('Unknown', inplace=True)
games_df['platforms'].fillna('Unknown', inplace=True)
games_df['release_date'].fillna('Unknown', inplace=True)

games_df.to_csv('processed_games_data.csv', index=False)
