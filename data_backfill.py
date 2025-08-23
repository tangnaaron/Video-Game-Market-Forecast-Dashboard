from igdb.wrapper import IGDBWrapper
import pandas as pd
import warnings
import time
from requests.exceptions import HTTPError

# Disables FutureWarning
warnings.simplefilter(action = 'ignore', category = FutureWarning)

# Environnment variables 
client_id = 'w7r7cmzkm0etx41ula5aq00oatzc4c'
token = 'q3ax0dsj0s3565jvyikqu7kfx90elr'

# Get company's published games 
def get_games_df(company):
    wrapper = IGDBWrapper(client_id, token)
    
    games_df = pd.DataFrame()
    company_request = wrapper.api_request(
                'companies',
                f'fields developed, updated_at, name; where name = "{company}";'
            )
    company_json = company_request.decode('utf-8')

    company_df = pd.read_json(company_json)
    company_published_games_id = company_df.loc[0, 'developed']
    
    games_df = pd.DataFrame()
    try:
    
        column_request = wrapper.api_request(
                'games',
                f'fields name, genres, themes, total_rating; limit 500; where id = \
                {tuple(company_published_games_id)};'
            )
        column_json = column_request.decode('utf-8')
        games_df = pd.concat([games_df, pd.read_json(column_json)], ignore_index = True)

            
        games_df['company'] = company 
        games_df['updated_at'] = company_df.loc[0,'updated_at']

        return games_df
    
    except HTTPError:
        print("Too many requests for " + company)
        return 
    

# Electronic Arts, Epic Games, Square Enix with sufficient data
# Riot Games for fun 
companies = ["Electronic Arts", "Riot Games", "Square Enix", "Epic Games"]
games_df = pd.DataFrame()

# Aggregates company game dataset
for company in companies:
    games_df = pd.concat([games_df, get_games_df(company)], ignore_index = True)

print(games_df)



# Need to attach time of last update to each observation corresponding to company 
# Need to also attach company to dataframe 