from igdb.wrapper import IGDBWrapper
import pandas as pd
import warnings
from requests.exceptions import HTTPError
from data_cleaning import transform_data

# Disables FutureWarning
warnings.simplefilter(action = 'ignore', category = FutureWarning)

def data_backfill(company_list, client_id, token):
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
        
        try:
        
            column_request = wrapper.api_request(
                    'games',
                    f'fields name, genres, themes, total_rating; limit 500; where id = \
                    {tuple(company_published_games_id)};'
                )
            column_json = column_request.decode('utf-8')
            games_df = pd.read_json(column_json)

                
            games_df['company'] = company 
            games_df['updated_at'] = company_df.loc[0,'updated_at']

            return games_df
        
        except HTTPError:
            print("Too many requests for " + company)
            return 
        
    games_df = pd.DataFrame()

    # Aggregates company game dataset
    for company in company_list:
        games_df = pd.concat([games_df, get_games_df(company)])

    # Cleans company game dataset
    games_df.set_index('id', inplace = True)
    games_df = transform_data(games_df)

    # Exports 
    games_df.to_csv("csv/games_cleaned.csv", index = False)

