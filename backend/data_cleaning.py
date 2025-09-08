from igdb.wrapper import IGDBWrapper
import pandas as pd
from ast import literal_eval


def transform_data(df):
    genre_mapping = pd.read_csv("mapping/genre_mapping.csv")
    theme_mapping = pd.read_csv("mapping/theme_mapping.csv")

    # Clean missing values
    df.dropna(subset = "total_rating", inplace = True)

    # Maps genre and theme 
    def map_genre_data(row):
        if (type(row['genres']) is float) or (len(row['genres']) == 0):
            return None
        mapped_genre = []
        for genre_id in row['genres']:
           mapped_genre.append(genre_mapping[genre_mapping['id'] == genre_id].iloc[0, 1])
        
        return mapped_genre
    
    def map_theme_data(row):
        if (type(row['themes']) is float) or (len(row['themes']) == 0):
            return None
        mapped_theme = []
        for theme_id in row['themes']:
           mapped_theme.append(theme_mapping[theme_mapping['id'] == theme_id].iloc[0, 1])
        return mapped_theme
    
    df['genres'] = df.apply(map_genre_data, axis = 1)
    df['themes'] = df.apply(map_theme_data, axis = 1)

    # Encodes genre and theme
    genres_encoded = pd.get_dummies(df['genres'].explode()).groupby(level = 0).sum()
    themes_encoded = pd.get_dummies(df['themes'].explode()).groupby(level = 0).sum()
    df = pd.concat([df, genres_encoded,themes_encoded], axis = 1)

    return df

