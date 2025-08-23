from igdb.wrapper import IGDBWrapper
import pandas as pd
import warnings

# Disables FutureWarning
warnings.simplefilter(action = 'ignore', category = FutureWarning)

# Environnment variables 
client_id = 'w7r7cmzkm0etx41ula5aq00oatzc4c'
token = 'k2kdmgkw64nyj5y3z2kaxh0esvy6pb'

# Get company's published games 
def get_games(company):
    wrapper = IGDBWrapper(client_id, token)

    company_request = wrapper.api_request(
                'companies',
                f'fields *; where name = "{company}";'
            )
    company_json = company_request.decode('utf-8')
    company_published_games_id = pd.read_json(company_json).loc[0, 'published']

    games_df = pd.DataFrame()
    for id in company_published_games_id[0:5]:
        column_request = wrapper.api_request(
                'games',
                f'fields name, genres, themes, aggregated_rating; where id = {id};'
            )
        column_json = column_request.decode('utf-8')
        games_df = pd.concat([games_df, pd.read_json(column_json)], ignore_index = True)
    
    print(games_df)



    
company = "Ubisoft Entertainment"
get_games(company)
