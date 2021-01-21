import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_table

import pandas as pd
import plotly_express as px

from app import app, engine

from util import teamslist

from nhlscraper.teamcolors import teamcolors
from teams.home.home_setup import *
#from teams.home.previous.previous import layout_previous
from teams.home.reddit.reddit import layout_reddit


def layout_home(teamid):
    return html.Div(
        [
            league_placements(teamid),
            html.Div(
                [
                    home_tabs(teamid),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id='drop-standings',
                                        options = [
                                            {'label': 'League', 'value': 'league'},
                                            {'label': 'Conference', 'value': 'conference'},
                                            {'label': 'Division', 'value': 'division'},
                                        ],
                                        clearable=False,
                                        persistence=True,
                                        persistence_type='local',
                                        value='division'
                                    )
                                ],
                                className="dcc_control"
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(id='table-standings')
                                        ],
                                        className="pretty_container eight columns"
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Dropdown(
                                                        id='drop-standingsgraph',
                                                        options = [
                                                            {'label': i, 'value': i} for i in standings_options
                                                        ],
                                                        value='Points'
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(id='graph-standings')
                                                ]
                                            ),
                                        ],
                                        className="pretty_container four columns",
                                        style={'flex': '1'}
                                    ),
                                ],
                                className="row flex-display",
                            ),
                            dcc.Store(id='store-goalies'),
                            dcc.Store(id='store-players'),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Div(id='table-goalies'),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(id='table-players')
                                                        ]
                                                    ),
                                                ],
                                                className="pretty_container eight columns"
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id='drop-positions',
                                                                        options=[{'label': k, 'value': k} for k in position_options.keys()],
                                                                        clearable=False,
                                                                        value='C'
                                                                    ),
                                                                ],
                                                                className="four columns"
                                                            ),
                                                            html.Div(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id='drop-stats',
                                                                        clearable=False,
                                                                    ),
                                                                ],
                                                                className="four columns"
                                                            ),
                                                            html.Div(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id='drop-linestats',
                                                                    ),
                                                                ],
                                                                className="four columns"
                                                            )
                                                        ],
                                                        className="row flex-display",
                                                    ),
                                                    html.Div(id='plot-players')
                                                ],
                                                className="pretty_container four columns"
                                            )
                                        ],
                                        className="row flex-display",
                                    )
                                ]
                            )
                        ],
                        className="pretty_container nine columns",
                        style={'flex': '1'}
                    )

                ],
                className="row flex-display",
            )
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
)

# Tabs callback
@app.callback(Output('tabs-home-content', 'children'),
              [Input('tabs-home', 'value'),
              Input('drop-team', 'value'),])
def render_content(tab, teamid):
    if tab == 'previous':
        return  None
    elif tab == 'next':
        return html.Div(
            [
                html.H6('TBD')
            ],
            className="mini_container"
        )
    else:
        return layout_reddit(teamid)

@app.callback([Output('table-standings', 'children'),
               Output('graph-standings', 'children'),
               Output('table-players', 'children'),
               Output('table-goalies', 'children'),
               Output('store-players', 'data'),
               Output('store-goalies', 'data')],
              [Input('drop-team', 'value'),
               Input('drop-standings', 'value'),
               Input('drop-standingsgraph', 'value')]
              )

def build_teamoverview(teamid, standing, standingsy):
    table, plot = tablebarplot_standings(standing, teamid, teamcolors, standingsy)
    table_nongoalies, table_goalies, players, goalies = table_players(teamid)
    plot.layout.xaxis.fixedrange = True
    plot.layout.yaxis.fixedrange = True
    plot.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text="hockeyviewer.com",
                #textangle=-30,
                opacity=0.1,
                font=dict(color='black', size=25),
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                showarrow=False,
            )
        ]
    )
    plot.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    plot.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    return table, dcc.Graph(figure=plot), table_nongoalies, table_goalies, players.to_dict('records'), goalies.to_dict('records')

@app.callback(
    [Output('drop-stats', 'options'),
    Output('drop-linestats', 'options')],
    [Input('drop-positions', 'value')])
def set_stat_options(selected_positions):
    stat_options = [{'label': i, 'value': i} for i in position_options[selected_positions]]
    linestat_options = [{'label': i, 'value': i} for i in position_options[selected_positions]]
    return stat_options, linestat_options

@app.callback(
    [Output('drop-stats', 'value'),
    Output('drop-linestats', 'value')],
    [Input('drop-stats', 'options')])
def set_stat_value(available_options):
    stat_value = available_options[0]['value']
    linestat_value = available_options[0]['value']
    return stat_value, linestat_value

@app.callback(
    Output('plot-players', 'children'),
    [Input('drop-positions', 'value'),
    Input('drop-stats', 'value'),
    Input('drop-linestats', 'value'),
    Input('drop-team', 'value'),
    Input('store-players', 'data'),
    Input('store-goalies', 'data')]
)

def plot_player_stats(position, stat, linestat, teamid, players, goalies):
    if players is None:
        table_nongoalies, table_goalies, players, goalies = table_players(teamid)
    players_list = ['C', 'RW', 'LW', 'D', 'Forwards', 'Defenders']
    forwards_list = ['C', 'RW', 'LW']
    goalie_list = ['G']
    plot = players_plotstats(position, stat, linestat, teamid, players, goalies, players_list, forwards_list, goalie_list)
    plot.layout.xaxis.fixedrange = True
    plot.layout.yaxis.fixedrange = True
    plot.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text="hockeyviewer.com",
                #textangle=-30,
                opacity=0.1,
                font=dict(color='black', size=25),
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                showarrow=False,
            )
        ]
    )
    plot.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    plot.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

    return dcc.Graph(figure=plot)
