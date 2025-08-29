import pandas as pd 
from ast import literal_eval
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

games_cleaned = pd.read_csv("csv/games_cleaned.csv")

def feature_engineer(df, init):

    df['genres'] = df['genres'].astype(str)
    df['themes'] = df['themes'].astype(str)

    # Encode genres, themes, and company 
    def encode_genre(row):
        if row['genres'] == 'nan' :
            return 0
        else:
            encoding = 0
            for genre in literal_eval(row['genres']):
                encoding += games_cleaned.groupby(genre)['total_rating'].mean()[1]
            
            return encoding/len(literal_eval(row['genres']))
    def encode_theme(row):
        if row['themes'] == 'nan':
            return 0
        else:
            encoding = 0
            for theme in literal_eval(row['themes']):
                encoding += games_cleaned.groupby(theme)['total_rating'].mean()[1]
            
            return encoding/len(literal_eval(row['themes']))
        
    company_mean = games_cleaned.groupby('company')['total_rating'].mean()
    df['companies_encoded'] = df['company'].map(company_mean)
    df['genres_encoded'] = df.apply(encode_genre, axis = 1)
    df['themes_encoded'] = df.apply(encode_theme, axis = 1)

    # K-means
    if init:
        global scaler
        scaler = StandardScaler()
        X_kmeans_train = df[['genres_encoded','themes_encoded','companies_encoded']].copy()
        X_kmeans_train[['genres_encoded','themes_encoded','companies_encoded']] = scaler.fit_transform(X_kmeans_train[['genres_encoded',
                                                                                                                       'themes_encoded',
                                                                                                                       'companies_encoded']])
        global kmeans 
        kmeans = KMeans(n_clusters = 5)
        df['cluster'] = kmeans.fit_predict(X_kmeans_train)
    else:
        X_kmeans = df[['genres_encoded','themes_encoded','companies_encoded']].copy()
        X_kmeans[['genres_encoded','themes_encoded','companies_encoded']] = scaler.transform(X_kmeans[['genres_encoded',
                                                                                                       'themes_encoded',
                                                                                                       'companies_encoded']])
        
        df['cluster'] = kmeans.predict(X_kmeans)

    return df

def init_model():
    # Data cleaning
    global games_cleaned
    games_cleaned = feature_engineer(games_cleaned, init = True)

    # Modeling 
    X_train = games_cleaned[['genres_encoded','themes_encoded','companies_encoded', 'cluster']]
    y_train = games_cleaned['total_rating']
    model = RandomForestRegressor(random_state = 123)
    model.fit(X_train, y_train)

    return model 

def model_predict(genres_list, themes_list, company, model):
    # Data cleaning 
    df = pd.DataFrame({"genres" : [genres_list], "themes" : [themes_list], "company" : company})
    df = feature_engineer(df, init = False)

    X_pred = df[['genres_encoded','themes_encoded','companies_encoded','cluster']]
    print(model.predict(X_pred))

#model_predict(['Shooter'], ['Drama'],"Electronic Arts")
'''
sample_df = pd.DataFrame({"genres" : [['Shooter']], "themes" : [['Drama']], "company" : "Electronic Arts"})
sample_df = feature_engineer(sample_df, init = False)
print(sample_df)
print(games_cleaned)
'''