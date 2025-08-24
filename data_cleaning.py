from igdb.wrapper import IGDBWrapper
import pandas as pd
from ast import literal_eval
'''
client_id = 'w7r7cmzkm0etx41ula5aq00oatzc4c'
token = 'q3ax0dsj0s3565jvyikqu7kfx90elr'

wrapper = IGDBWrapper(client_id, token)

theme_request = wrapper.api_request(
                'genres',
                f'fields name; limit 500;'
            )

json = theme_request.decode('utf-8')
df = pd.read_json(json)
df.to_csv("mapping/genre_mapping.csv", index = False)
'''


games_uncleaned = pd.read_csv("games_uncleaned.csv")
genre_mapping = pd.read_csv("mapping/genre_mapping.csv")
theme_mapping = pd.read_csv("mapping/theme_mapping.csv")

def transform_data(df):
    # Clean missing values
    df.dropna(subset = "total_rating", inplace = True)

    # Maps genre and theme 
    def map_genre_data(row):
        mapped_genre = []
        for genre_id in literal_eval(row['genres']):
           mapped_genre.append(genre_mapping[genre_mapping['id'] == genre_id].iloc[0, 1])
        return mapped_genre
    
    def map_theme_data(row):
        mapped_theme = []
        for theme_id in literal_eval(row['themes']):
           mapped_theme.append(theme_mapping[theme_mapping['id'] == theme_id].iloc[0, 1])
        return mapped_theme
    
    df['genres'] = df.apply(map_genre_data, axis = 1)
    df['themes'] = df.apply(map_theme_data, axis = 1)
    print(df)
    

transform_data(games_uncleaned.head())
