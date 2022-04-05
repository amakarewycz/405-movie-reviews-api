import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers.key_finder import api_key
from helpers.api_call import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from enum import Enum

########### Define a few variables ######
tabtitle = 'Movies'
sourceurl = 'https://www.kaggle.com/tmdb/tmdb-movie-metadata'
sourceurl2 = 'https://developers.themoviedb.org/3/getting-started/introduction'
githublink = 'https://github.com/amakarewycz/405-movie-reviews'

class RatingStyle(Enum):
    Negative = { 'padding': '12px',
                    'font-size': '18px',
                    # 'height': '400px',
                    'border': "thick red solid",
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    }
    Positive = { 'padding': '12px',
                    'font-size': '18px',
                    # 'height': '400px',
                    'border': "thick lime solid",
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    }
    Neutral = { 'padding': '18px',
                    'font-size': '18px',
                    # 'height': '400px',
                    'border': "thick yellow solid",
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    }

    

####### Write your primary function here
def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        final="Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        final="Negative"
    else :
        final="Neutral"
    # responses
    response1=f"Overall sentiment dictionary is : {sentiment_dict}"
    response2=f"{round(sentiment_dict['neg']*100, 2)}"
    response3=f"{round(sentiment_dict['neu']*100, 2)}"
    response4=f"{round(sentiment_dict['pos']*100,2 )}"
    response5=f"{final}"
    return response1, response2, response3, response4, response5


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    dcc.Store(id='tmdb-store', storage_type='session'),
    dcc.Store(id='summary-store', storage_type='session'),
    html.Div([
        html.H1(['Movie Reviews']),
        html.Div([
            html.Div(id='movie-container',children=[
                html.Button(id='eek-button', n_clicks=0, children='Click to randomly select a Movie', style={'color': 'rgb(255, 255, 255)'}),
                html.Div(id='movie-title', children=[]),
                html.Div(id='movie-release', children=[]),
                html.Div(id='movie-overview', children=[]),
            ], style={ 'padding': '12px',
                    'font-size': '22px',
                    # 'height': '400px',
                    'border': 'thick red solid',
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    },
            className='twelve columns'),
        ], className='twelve columns'),
        html.Br(),
    ], className='twelve columns'),
        # Output
    html.Div([
        # Footer
                  html.Div([
                html.H3('Sentiment of movie overview:'),
                html.Table([
                   html.Thead([
                    html.Tr([
                     html.Td(html.Div("Negative / %")),

                     html.Td(html.Div("Neutral / %")),

                     html.Td(html.Div("Positive / %")),
                     html.Td(html.Div("Overall Sentiment"))
                                      ]),
                                      ]),
                 html.Tbody([  
                  html.Tr([
                     html.Td(html.Div(id='output-div-2')),
                     html.Td(html.Div(id='output-div-3')),
                     html.Td(html.Div(id='output-div-4')),
                     html.Td(html.Div(id='output-div-5'))
                             ]),
                             ]),
                    ]),
            ], style={ 'padding': '12px',
                    'font-size': '22px',
                    # 'height': '400px',
                    'border': 'thick blue solid',
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#234553',
                    'textAlign': 'left',
                    },
            className='twelve columns'),  
        html.Br(),
        html.A('Code on Github', href=githublink, target="_blank"),
        html.Br(),
        html.A("Data Source: Kaggle", href=sourceurl, target="_blank"),
        html.Br(),
        html.A("Data Source: TMDB", href=sourceurl2, target="_blank"),
    ], className='twelve columns'),
    ]
)

########## Callbacks

# TMDB API call
@app.callback(Output('tmdb-store', 'data'),
              [Input('eek-button', 'n_clicks')],
              [State('tmdb-store', 'data')])
def on_click(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks==0:
        data = {'title':' ', 'release_date':' ', 'overview':' '}
    elif n_clicks>0:
        data = api_pull(random.choice(ids_list))
    return data

@app.callback([Output('movie-title', 'children'),
                Output('movie-release', 'children'),
                Output('movie-overview', 'children'),
                Output(component_id='output-div-2', component_property='children'),
                Output(component_id='output-div-3', component_property='children'),
                Output(component_id='output-div-4', component_property='children'),
                Output(component_id='output-div-5', component_property='children'),
                Output(component_id='movie-container', component_property='style')
                ],
              [Input('tmdb-store', 'modified_timestamp')],
              [State('tmdb-store', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    else:
        message = sentiment_scores(data['overview'])
        return [data['title'], data['release_date'], data['overview'], \
               message[1],message[2],message[3],message[4],RatingStyle[message[4]].value]

    

############ Deploy
if __name__ == '__main__':
    #print(RatingStyle["Neutral"].value)
    app.run_server(debug=True)
