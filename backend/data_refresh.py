from igdb.wrapper import IGDBWrapper
import pandas as pd
import warnings
from data_backfill import data_backfill
from requests import post
import os

# Disables FutureWarning
warnings.simplefilter(action = 'ignore', category = FutureWarning)

# API variables 
#response = post('https://id.twitch.tv/oauth2/token?client_id=w7r7cmzkm0etx41ula5aq00oatzc4c&client_secret=u7jjy34lwqjddnms6ini0il27gfg13&grant_type=client_credentials')
response = post("https://id.twitch.tv/oauth2/token?client_id=w7r7cmzkm0etx41ula5aq00oatzc4c&client_secret="+str(os.getenv("CLIENT_SECRET"))+"&grant_type=client_credentials")
client_id = 'w7r7cmzkm0etx41ula5aq00oatzc4c'
print(response.json())
token = response.json()['access_token']
companies = ["Electronic Arts", "Riot Games", "Square Enix", "Epic Games", "Nintendo"]

# Obtains new company data 
company_df = pd.DataFrame()
games_cleaned = pd.read_csv("csv/games_cleaned.csv")
for company in companies:
    wrapper = IGDBWrapper(client_id, token)
            
    company_request = wrapper.api_request(
                'companies',
                f'fields updated_at, name; where name = "{company}";'
            )
    company_json = company_request.decode('utf-8')

    company_df = pd.concat([company_df, pd.read_json(company_json)], ignore_index = True)


games_cleaned['updated_at'] = pd.to_datetime(games_cleaned['updated_at'])

# Data refresh 
if games_cleaned.groupby('company')['updated_at'].max().to_list() < company_df['updated_at'].to_list():
    data_backfill(companies, client_id, token)
    print("New data loaded.")
else:
    print("No new data.")
