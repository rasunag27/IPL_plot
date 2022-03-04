import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px

#!pip install jupyter-dash -q
#!pip install dash==2.0.0
#!pip install dash-bootstrap-components

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


USERNAME_PASSWORD_PAIRS=[['ipl','ipl']]

df = pd.read_csv('https://raw.githubusercontent.com/srinathkr07/IPL-Data-Analysis/master/matches.csv')

df.isna().sum()

df['city'].fillna('Rajkot', inplace=True)
df['winner'].fillna('Royal Challengers Bangalore', inplace=True)
df['player_of_match'].fillna('AJ Tye', inplace=True)

df=df.fillna(0)

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import dash_table

from plotly.subplots import make_subplots
import plotly.graph_objects as go

#app = JupyterDash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
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
                dbc.NavLink("Luckiest venue for each team", href="/page-4", active="exact"),
                dbc.NavLink("Winning probability by winning toss", href="/page-5", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

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
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))

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

def slider(df):
  All_season = df['season'].value_counts().reset_index()['index'].min()
  df1 = df[df['season'] > (All_season - 1)]
  fig=px.bar(df1,x='venue',color='winner',title='Luckiest Venue for Each Team',animation_frame='winner',barmode='relative')
  fig.update_layout(margin=dict(l=80, r=20, t=100, b=200),paper_bgcolor="khaki",title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
  fig['layout']['updatemenus'][0]['pad']=dict(r= 10, t= 150)
  fig['layout']['sliders'][0]['pad']=dict(r= 20, t= 200)
  return fig

def team_win_toss(df):
  All_season = df['season'].value_counts().reset_index()['index'].min()
  df1 = df[df['season'] > (All_season - 1)]
  sun= px.sunburst(df1, path=['toss_winner', 'winner'],title='Winning probability by Winning Toss')
  sun.update_layout(margin = dict(t=100, l=25, r=25, b=25))
  sun.update_traces(textinfo="label+percent parent+value")
  return sun

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center', 'margin-bottom':15}),
                html.H6('The dataset is an IPL Dataset of match-by-match from the seasons 2008 to 2019.', style={'margin-bottom': 15}),
                html.H6('Five different analysis is done on the dataset with graphs. The observation can be visualized by clicking the options in the sidebar.', style={'margin-bottom':25}),
                html.H4('Sample IPL Dataset', style={'margin-bottom': 20}),
                dash_table.DataTable(data = df[:15].to_dict('records'), columns = [{"name": i, "id": i} for i in df.columns], style_data={'color': 'gray','backgroundColor': 'white'},
                                     style_cell={
                                         'height': 'auto',
                                         # all three widths are needed
                                         'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                         'whiteSpace': 'normal'}
                                     ),
                ]
    elif pathname == "/page-1":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center', 'margin-bottom':15}),
                html.H4('Pie chart for top 5 and Least 5 teams based on winning count',
                        style={'textAlign': 'center'}),
                html.H6('Among all seasons, Mumbai Indians have won the maximum with the count of 109 matches and least being Rising Pune Supergaints with only 5 matches',
                        style={'textAlign': 'center', 'margin-bottom':15}),
                dcc.Graph(id='bargraph',
                          figure=figure1(df)),
                html.H4('The below bar graph gives win count of top 10 teams',
                        style={'textAlign': 'center'}),

                dcc.Graph(id='bargraph',
                          figure=figure1_bar(df))
                ]
    elif pathname == "/page-2":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center', 'margin-bottom':15}),
                html.H6('The bar graph represents top 10 players based on Man of Match, we can observe that CH Gayle has been the player of the match for 21 times',
                        style={'textAlign': 'left'}),
                dcc.Graph(id='bargraph',
                         figure=figure2(df))
                ]
    elif pathname == "/page-3":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                html.H6('Most runs are scored by Mumbai Indians with a total of 1886 runs.',
                        style={'textAlign': 'left'}),
                dcc.Graph(id='bargraph',
                         figure=figure3(df)),
                html.H6('Most wickets are taken by Kolkata Night riders with a total of 351 wickets.',
                        style={'textAlign': 'left'}),
                dcc.Graph(id='bargraph',
                         figure=figure4(df))
                ]
    elif pathname == "/page-4":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                dcc.Graph(figure=slider(df))
                ]
    elif pathname == "/page-5":
        return [
                html.H1('IPL Dataset Analysis',
                        style={'textAlign':'center'}),
                dcc.Graph(figure=team_win_toss(df))
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
