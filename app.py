import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px

import dash
#from jupyter_dash import JupyterDash
from dash import dcc
#import dash_core_components as dcc
from dash import html

#import dash_core_components as dcc
#import dash_html_components as html


from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_table


import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""Installation  - It should be present in requirements.txt"""

#!pip install jupyter-dash -q
#!pip install dash==2.0.0
#!pip install dash-bootstrap-components

"""Import data"""

df = pd.read_csv('https://raw.githubusercontent.com/srinathkr07/IPL-Data-Analysis/master/matches.csv')


#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Visualization"),#, className="display-4"),
        html.Hr(),
        html.P(
            "IPL Dataset", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Best and Least teams", href = "/page-1", active="exact"),
                dbc.NavLink("Best players", href="/page-2", active="exact"),
                dbc.NavLink("Teams win by runs and wickets", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])



### Question 1 - Fig

def figure1(df):
    
    #container = "The graph you choose for: {}".format(option_slctd)
    #container2 = "Analysis represents that Mumbai Indians has won 109 times being highest"

    df_win_by_counts = df['winner'].value_counts().reset_index().rename(columns = {'index': 'Teams'})

    fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Top 5 teams', 'Least 5 teams'])
    fig.add_trace(go.Pie(labels=df_win_by_counts[:5]['Teams'], values= df_win_by_counts[:5]['winner'],
                        name="Teams", pull=[0.2, 0, 0, 0, 0]), 1, 1)

    fig.add_trace(go.Pie(labels=df_win_by_counts[-5:]['Teams'], values= df_win_by_counts[-5:]['winner'],
                        name="Teams", pull=[0, 0, 0, 0, 0.2]), 1, 2)

    fig.update_layout(title_text='Top and Least 5 winnings based on total matches of {}'.format(df_win_by_counts['winner'].sum()))
    fig.update_traces(textposition='inside', textinfo='label+value')

    return fig

def figure1_bar(df):
  df_win_by_counts = df['winner'].value_counts().reset_index().rename(columns = {'index': 'Teams'})
  fig = px.bar(df_win_by_counts, x= "winner", y="Teams", title="Teams based on winning count")
  fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})

  return fig

### Question 2 - Fig

def figure2(df):
  df_player =df['player_of_match'].value_counts().reset_index().rename(columns = {'index': 'Player'})
  fig = px.bar(df_player[:10], x= "player_of_match", y="Player", title=" Top 10 Players based on no of Man of Matches")
  fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
  return fig


def figure3(df):
  team_win_by_runs=df.groupby('winner').sum()['win_by_runs'].reset_index()
  fig_runs = px.bar(team_win_by_runs, x= "winner", y="win_by_runs", title="Teams winning by runs")
  fig_runs.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
  return fig_runs

def figure4(df):
  team_win_by_wickets=df.groupby('winner').sum()['win_by_wickets'].reset_index()
  fig_wickets = px.bar(team_win_by_wickets, x= "winner", y="win_by_wickets", title="Teams winning by wickets")
  fig_wickets.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
  return fig_wickets

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                html.H6('This is an IPL Dataset of match-by-match from the seasons 2008 to 2019.'),
                html.H6('Five different analysis is done on the dataset with graphs. The observation can be visualized by clicking the options in the sidebar.'),
                html.H6('Below represents the dataset'),
                html.H4('IPL Dataset'),
                dash_table.DataTable(data = df[:15].to_dict('records'), columns = [{"name": i, "id": i} for i in df.columns]),
                
                ]
    elif pathname == "/page-1":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                html.H3('Top 5 and Least 5 teams based on winning count',
                        style={'textAligh': 'center'}),
                dcc.Graph(id='bargraph',
                          figure=figure1(df)),
                dcc.Graph(id='bargraph',
                          figure=figure1_bar(df))
                ]
    elif pathname == "/page-2":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                html.H3('Top 10 players based on Man of Match',
                        style={'textAligh': 'center'}),
                dcc.Graph(id='bargraph',
                         figure=figure2(df))
                ]
    elif pathname == "/page-3":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                html.H3('Teams win by runs',
                        style={'textAligh': 'center'}),
                dcc.Graph(id='bargraph',
                         figure=figure3(df)),
                html.H3('Teams win by wickets',
                        style={'textAligh': 'center'}),
                dcc.Graph(id='bargraph',
                         figure=figure4(df))
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True)

