from igdb.wrapper import IGDBWrapper
import pandas as pd
'''
client_id = 'w7r7cmzkm0etx41ula5aq00oatzc4c'
token = 'q3ax0dsj0s3565jvyikqu7kfx90elr'

wrapper = IGDBWrapper(client_id, token)

theme_request = wrapper.api_request(
                'themes',
                f'fields name; limit 500;'
            )

json = theme_request.decode('utf-8')
df = pd.read_json(json)
df.to_csv("mapping/theme_mapping.csv")

''' 
