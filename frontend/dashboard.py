import pandas as pd 
import sys
sys.path.append('/Users/aarontang/Desktop/Projects/Video Game Rating Forecast ')
from backend.model import init_model, model_predict
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, ctx
from dash.dependencies import Input, Output

# Imports mapping
genre_df = pd.read_csv("mapping/genre_mapping.csv")
theme_df = pd.read_csv("mapping/theme_mapping.csv")

# Initialize forecast model 
model = init_model()

# Create dashboard 
games_cleaned = pd.read_csv("csv/games_cleaned.csv")

def create_chart(company):
    df = games_cleaned[games_cleaned['company'] == company]
    
    fig = px.bar(df, x = df['name'].to_list(), y = df['total_rating'].to_list())

    fig.update_layout(
        title = "Total Ratings of Various Games by Company",
        xaxis_title = "Game",
        yaxis_title = "Total Rating",
        width = 1600,
        height = 700
    )

    return fig 

# Creates webpage
app = Dash(title = "Video Game Market Forecast Dashboard")
app.layout = html.Div([
    html.H1("Video Game Market Dashboard", style = {'textAlign' : 'center'}),
    html.Div([
        html.Label("View video game ratings across different companies.")
    ], style = {'font-size' : '20px', 'textAlign' : 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'company', 
                     options = games_cleaned['company'].unique(), 
                     clearable = False,
                     placeholder = "Select a company")
        ], style = {'width' : '30%'})     
    ], style = {'display' : 'flex', 'justifyContent' : 'center'}),
    html.Br(),
    html.Div(
        dcc.Graph(id = 'bar_chart', figure = create_chart(company = "Electronic Arts")),
        style = {'overflowX' : 'scroll', 'width' : '1400px', 'height' : '500px', 'margin' : 'auto'}
    ),
    html.Br(),
    html.Div([
        html.Label("Predict video game ratings based on genre and theme.")
    ], style = {'font-size' : '20px', 'textAlign' : 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label("Genre:"),
            dcc.Dropdown(id = 'genre', 
                         options = genre_df['name'].to_list(),
                         placeholder = "Select genre(s):",
                         multi = True,
                         closeOnSelect = False),
        ], style = {'width' : '30%', 'padding-right' : '10px'}),
        html.Div([
            html.Label("Theme:"),
            dcc.Dropdown(id = 'theme', 
                         options = theme_df['name'].to_list(),
                         placeholder = "Select theme(s):",
                         multi = True,
                         closeOnSelect = False)
        ], style = {'width' : '30%', 'padding-left' : '10px', 'padding-right' : '25px'}),
        html.Div([
            html.Br(),
            html.Button("Predict",
                        id = 'predict',
                        title = "Click to predict video game rating based on genre and theme.",
                        n_clicks = 0,
                        style = {'width' : '90px', 'height' : '25px', 
                                 'padding-bottom' : '24px', 'font-size' : '15px',
                                 'alignItems' : 'center', 'textAlign' : 'center',
                                 'padding-top' : '10px', 'justifyContent' : 'center'})
        ])
    ], style = {'display' : 'flex', 'justifyContent' : 'center'}),
    html.Br(),
    html.Br(),
    html.Br()
])

# Updates webpage
@callback(Output('bar_chart', 'figure'),
          Input('company', 'value'),
          Input('genre', 'value'),
          Input('theme', 'value'),
          Input('predict', 'n_clicks'),
          prevent_initial_call = True)
def update_chart_with_prediction(company, genre, theme, predict):
    if company != None:
        if "predict" == ctx.triggered_id:
            if (genre != None) and (theme != None) and (len(genre) != 0) and (len(theme) != 0):
                # Creates prediction
                prediction = model_predict(genre, theme, company, model)
                
                # Graphs prediction with chart 
                fig = create_chart(company)
                fig.add_trace(go.Bar(x = ["New Game"], y = [prediction], 
                                     marker_color = 'green',
                                     hovertext = f"The predicted rating for the new game is {prediction}",
                                     showlegend = False))
                return fig
            else:
                return create_chart(company)
        else:
             return create_chart(company)
    else:
        return create_chart(company = "Electronic Arts")

# Runs dashboard website
if __name__ == '__main__':
    app.run(debug = True)
