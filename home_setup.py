import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util import teamslist
from util import league_standings, conf_standings, div_standings#, roster_players, teamstatsplace
from nhlscraper.nhlscraper import teams, standings, players
from nhlscraper.teamcolors import teamcolors

from app import app, engine

position_options = {
    'Forwards': ['Assists', 'Faceoff %', 'Games', 'Goals', 'Hits', 'PIM', 'Points',
        'Time on Ice', 'Time on Ice a Game'],
    'Defenders': ['Assists', 'Faceoff %', 'Games', 'Goals', 'Hits', 'PIM', 'Points',
        'Time on Ice', 'Time on Ice a Game'],
    'C': ['Assists', 'Faceoff %', 'Games', 'Goals', 'Hits', 'PIM', 'Points',
        'Time on Ice', 'Time on Ice a Game'],
    'RW': ['Assists', 'Faceoff %', 'Games', 'Goals', 'Hits', 'PIM', 'Points',
        'Time on Ice', 'Time on Ice a Game'],
    'LW': ['Assists', 'Faceoff %', 'Games', 'Goals', 'Hits', 'PIM', 'Points',
        'Time on Ice', 'Time on Ice a Game'],
    'D': ['Assists', 'Faceoff %', 'Games', 'Goals', 'Hits', 'PIM', 'Points',
        'Time on Ice', 'Time on Ice a Game'],
    'G': ['Games', 'Games Started', 'Goals Against', 'Losses', 'OT', 'Saves',
        'Save %', 'Shots Against', 'Shutouts', 'Time on Ice', 'Wins']
}

standings_options = ['Points', 'Games', 'Wins', 'Losses', 'OT', 'ROW', 'Goals Against', 'Goals Scored']

def league_placements(teamid):
    teamstatsplace = pd.read_sql_table('dailyteamstatsplace', con=engine)
    df = teamstatsplace[teamstatsplace['team.id'] == teamid]
    df_standings = league_standings[league_standings['team.id'] == teamid][['divisionRank', 'conferenceRank', 'leagueRank']]
    for column in df_standings.columns:
        df_standings[column] = df_standings[column].apply(lambda x: str(x) + 'th')
        df_standings[column] = df_standings[column].str.replace('1th', '1st')
        df_standings[column] = df_standings[column].str.replace('2th', '2nd')
        df_standings[column] = df_standings[column].str.replace('3th', '3rd')
    teamname = teamslist[teamslist['id'] == teamid]['name'].iloc[0]
    teamcolor = [v for k,v in teamcolors.items() if k == teamname][0]
    def placement(df, column):
        value = df[column]
        return value
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                'League Rank',
                            ),
                            html.H6(
                                placement(df_standings, 'leagueRank'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Conference Rank'
                            ),
                            html.H6(
                                placement(df_standings, 'conferenceRank'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Division Rank',
                            ),
                            html.H6(
                                placement(df_standings, 'divisionRank'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            )

                        ],
                        id="rank",
                        className="mini_container",
                    ),
                    html.Div(
                        [
                            html.P(
                                'Wins',
                            ),
                            html.H6(
                                placement(df, 'stat.wins'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Losses',
                            ),
                            html.H6(
                                placement(df, 'stat.losses'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'OT',
                            ),
                            html.H6(
                                placement(df, 'stat.ot'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            )
                        ],
                        id="record",
                        className="mini_container",
                    ),
                    html.Div(
                        [
                            html.P(
                                'Goals a Game',
                            ),
                            html.H6(
                                placement(df, 'stat.goalsPerGame'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Goals Against a Game',
                            ),
                            html.H6(
                                placement(df, 'stat.goalsAgainstPerGame'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Goals Goals Against Ratio',
                            ),
                            html.H6(
                                placement(df, 'stat.evGGARatio'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            )
                        ],
                        id="goal",
                        className='mini_container',
                    ),
                    html.Div(
                        [
                            html.P(
                                'Save Percentage',
                            ),
                            html.H6(
                                placement(df, 'stat.savePctRank'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Shooting Percentage',
                            ),
                            html.H6(
                                placement(df, 'stat.shootingPctRank'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Shots a Game',
                            ),
                            html.H6(
                                placement(df, 'stat.shotsPerGame'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Shots Allowed',
                            ),
                            html.H6(
                                placement(df, 'stat.shotsAllowed'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            )
                        ],
                        id="shot",
                        className="mini_container",
                    ),
                    html.Div(
                        [
                            html.P(
                                'Power Play Percentage',
                            ),
                            html.H6(
                                placement(df, 'stat.powerPlayPercentage'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Power Play Opportunities',
                            ),
                            html.H6(
                                placement(df, 'stat.powerPlayOpportunities'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Penalty Kill Percentage',
                            ),
                            html.H6(
                                placement(df, 'stat.penaltyKillPercentage'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Penalty Kill Opportunities',
                            ),
                            html.H6(
                                placement(df, 'stat.penaltyKillOpportunities'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            )
                        ],
                        id="pp",
                        className="mini_container",
                    ),
                    html.Div(
                        [
                            html.P(
                                'Faceoff Win Percentage',
                            ),
                            html.H6(
                                placement(df, 'stat.faceOffWinPercentage'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Faceoffs Taken',
                            ),
                            html.H6(
                                placement(df, 'stat.faceOffsTaken'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Faceoffs Won',
                            ),
                            html.H6(
                                placement(df, 'stat.faceOffsWon'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            ),
                            html.P(
                                'Faceoffs Lost',
                            ),
                            html.H6(
                                placement(df, 'stat.faceOffsLost'),
                                style={'color': teamcolor, 'font-weight': 'bold'}
                            )
                        ],
                        id="faceoff",
                        className="mini_container",
                    ),
                ],
                id="info-container",
                className="row container-display",
                style={'flex-wrap': 'wrap', 'textAlign': 'center'}
            ),
        ],
    )

def home_tabs(teamid):
    teamname = teamslist[teamslist['id'] == teamid]['name'].iloc[0]
    teamcolor = [v for k,v in teamcolors.items() if k == teamname][0]
    return html.Div(
                [
                    dcc.Tabs(id='tabs-home', value='previous', children=[
                        dcc.Tab(label='Previous', value='previous'),
                        dcc.Tab(label='Next', value='next'),
                        dcc.Tab(label='Reddit', value='reddit'),
                    ],
                    colors={
                        'primary': teamcolor,
                        'background': '#F9F9F9',
                        'border': '#D6D6D6',

                    },
                    ),
                    html.Div(id='tabs-home-content')
                ],
                className='pretty_container three columns'
            )

def tablebarplot_standings(standing, teamid, teamcolors, standingsy):
    #teamslist = teams().teams().sort_values(by=['name'])
    teamname = teamslist[teamslist['id'] == teamid]['name'].iloc[0]
    teamcolor = [v for k,v in teamcolors.items() if k == teamname]
    # Build dataframe
    if standing == 'league':
        df = league_standings
    else:
        type_id = teamslist[teamslist['id'] == teamid][standing + '.id'].iloc[0]
        if standing == 'conference':
            df = conf_standings[conf_standings[standing + '.id'] == type_id]
        else:
            df = div_standings[div_standings[standing + '.id'] == type_id]
        df = pd.json_normalize(df['teamRecords'].iloc[0])
    # Clean dataframe
    df = df[['team.id', 'team.name', 'points','gamesPlayed',
        'leagueRecord.wins', 'leagueRecord.losses', 'leagueRecord.ot',
        'row', 'streak.streakCode', 'goalsAgainst', 'goalsScored']]
    team_index = df.index[df['team.id'] == teamid].tolist()
    def f(row):
        logo = app.get_asset_url('/logos/' + str(row['team.id']) + '.svg')
        return '![{0}]({0}#thumbnail)'.format(logo)
    df.insert(loc=0, column='', value=df.apply(f, axis=1))
    df = df[['', 'team.name', 'points', 'gamesPlayed', 'leagueRecord.wins',
        'leagueRecord.losses', 'leagueRecord.ot', 'row', 'streak.streakCode',
        'goalsAgainst', 'goalsScored']]
    df.columns = ['', 'Team', 'Points', 'Games', 'Wins', 'Losses', 'OT',
        'ROW', 'Streak', 'Goals Against', 'Goals Scored']
    # Build table
    table = dash_table.DataTable(
        columns=[
            {'id': c, 'name': c} if c != '' else {'name': c, 'id':c, 'type':'text', 'presentation':'markdown'} for c in df.columns
        ],
        data=df.to_dict('records'),
        #page_size=8,
        sort_action="native",
        style_header={
            'fontWeight': 'bold',
            'font-family': '"Open Sans", sans-serif',
            'textAlign': 'center',
            'font-size': '10px',
            'vertical-align': 'middle',
            'background-color': 'black',
            'color': 'white'
        },
        style_cell={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font-family': '"Open Sans", sans-serif',
            'border': '1px solid #F7F7F7',
            'border-bottom': '1px solid black',
            'font-size': '12px',
            'backgroundColor': '#F7F7F7',
            'maxHeight': '40px',
            'minWidth': '0px', 'maxWidth': '96px',

        },
        style_cell_conditional=[
            {'if': {'column_id': ''},
             'minWidth': '40px', 'width': '50px', 'maxWidth': '40px',
             'textAlign': 'center',},
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Team} = "' + teamname + '"'
                },
                "backgroundColor": teamcolor[0],
                'color': 'white'
            }
        ],
        style_table={
            'maxHeight': '450px',
            'overflowY': 'scroll',
            'vertical-align': 'middle',
            'padding': '0px',
        },
        style_as_list_view=True,
    ),
    if standingsy is None:
        standingsy = 'Points'
    plot = px.bar(df, x='Team', y=standingsy, color='Team',
        color_discrete_map=teamcolors, text=standingsy, height=350)
    plot.update_xaxes(type='category')
    size_x = df[standingsy].max()*0.10
    size_y = df[standingsy].max()*0.10
    for x in plot['data']:
        if x['x'] is not None:
            team = x['legendgroup']
            team_x = x['x']
            team_y = x['y']
            # find logo url based on team name
            teamid_select = teamslist[teamslist['name'] == team]['id'].iloc[0]
            logo = app.get_asset_url('/logos/' + str(teamid_select) + '.svg')
            plot.add_layout_image(
                dict(
                    source=logo,
                    x=np.array(team_x[0]),
                    y=np.array(team_y[0] + size_y),
                ))
    plot.update_layout_images(dict(
            xref="x",
            yref="y",
            sizex=size_x,
            sizey=size_y,
            xanchor='center',
            yanchor='middle'
    ))
    plot.update_layout(showlegend=False)
    plot.update_yaxes(range=[0, df[standingsy].max() + df[standingsy].max()*0.25], showticklabels=False, title=None)
    plot.update_xaxes(showticklabels=False, title=None)
    plot.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
    )
    return table, plot

def table_players(teamid):

    teamname = teamslist[teamslist['id'] == teamid]['name'].iloc[0]
    teamcolor = [v for k,v in teamcolors.items() if k == teamname]
    #df_roster = teams(str(teamid)).roster()
    roster_players = pd.read_sql_table('dailyplayers', con=engine)
    df_roster = roster_players[roster_players['team.id'] == int(teamid)]
    playerlist = df_roster['person.id'].to_list()
    def f(row):
        portrait = app.get_asset_url('/portraits/' + str(row['person.id']) + '.png')
        return '![{0}]({0}#thumbnail)'.format(portrait)
    df_roster.insert(loc=0, column='', value=df_roster.apply(f, axis=1))
    df_roster['jerseyNumber'] = df_roster['jerseyNumber'].apply(lambda x: '#' + str(x))
    df_goalies = df_roster[df_roster['position.abbreviation'] == 'G']
    df_players = df_roster[df_roster['position.abbreviation'] != 'G']
    df_players = df_players[['', 'person.fullName', 'jerseyNumber', 'position.abbreviation', 'stat.timeOnIce',
        'stat.games', 'stat.points', 'stat.assists', 'stat.goals', 'stat.hits',
        'stat.timeOnIcePerGame', 'stat.faceOffPct', 'stat.pim']]
    df_players.columns = ['', 'Player', 'Number', 'Position', 'Time on Ice', 'Games',
        'Points', 'Assists', 'Goals', 'Hits', 'Time on Ice a Game',
        'Faceoff %', 'PIM']
    df_goalies = df_goalies[['', 'person.fullName', 'jerseyNumber', 'position.abbreviation',
        'stat.savePercentage', 'stat.timeOnIce', 'stat.games', 'stat.shutouts',
        'stat.wins', 'stat.losses', 'stat.ot', 'stat.saves', 'stat.gamesStarted',
        'stat.shotsAgainst', 'stat.goalsAgainst']]
    df_goalies.columns = ['', 'Player', 'Number', 'Position', 'Save %', 'Time on Ice',
        'Games', 'Shutouts', 'Wins', 'Losses', 'OT', 'Saves', 'Games Started',
        'Shots Against', 'Goals Against']
    # border color
    border_team = '2px solid ' + str(teamcolor[0])
    table = dash_table.DataTable(
        columns=[
            {'id': c, 'name': c} if c != '' else {'name': c, 'id':c, 'type':'text', 'presentation':'markdown'} for c in df_players.columns
        ],
        data=df_players.to_dict('records'),
        #page_size=6,
        sort_action='native',
        style_header={
            'fontWeight': 'bold',
            'font-family': '"Open Sans", sans-serif',
            'textAlign': 'center',
            'font-size': '10px',
            'vertical-align': 'middle',
            'backgroundColor': teamcolor,
            'color': 'white'
        },
        style_cell={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font-family': '"Open Sans", sans-serif',
            'border': '1px solid #F7F7F7',
            'border-bottom': border_team,
            'font-size': '12px',
            'backgroundColor': '#F9F9F9',
            'color': 'black',
            'maxHeight': '40px',
            'minWidth': '0px', 'maxWidth': '96px',

        },
        style_cell_conditional=[
            {'if': {'column_id': ''},
             'minWidth': '40px', 'width': '50px', 'maxWidth': '40px',
             'textAlign': 'center',},

        ],
        style_table={
            'maxHeight': '359px',
            'overflowY': 'scroll',
            #'overflowX': 'scroll',
            'vertical-align': 'middle',
            'padding': '0px',
        },
        style_as_list_view=True,
    ),
    table_goalies = dash_table.DataTable(
        columns=[
            {'id': c, 'name': c} if c != '' else {'name': c, 'id':c, 'type':'text', 'presentation':'markdown'} for c in df_goalies.columns
        ],
        data=df_goalies.to_dict('records'),
        sort_action='native',
        style_header={
            'fontWeight': 'bold',
            'font-family': '"Open Sans", sans-serif',
            'textAlign': 'center',
            'font-size': '10px',
            'vertical-align': 'middle',
            'backgroundColor': teamcolor,
            'color': 'white'
        },
        style_cell={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'font-family': '"Open Sans", sans-serif',
            'border': '1px solid #F7F7F7',
            'border-bottom': border_team,
            'font-size': '12px',
            'backgroundColor': '#F9F9F9',
            'color': 'black',
            'maxHeight': '40px',
            'minWidth': '0px', 'maxWidth': '96px',

        },
        style_cell_conditional=[
            {'if': {'column_id': ''},
             'minWidth': '40px', 'width': '50px', 'maxWidth': '40px',
             'textAlign': 'center',},

        ],
        style_table={
            #'maxHeight': '359px',
            'overflowY': 'scroll',
            #'overflowX': 'scroll',
            'vertical-align': 'middle',
            'padding': '0px',
        },
        style_as_list_view=True,
    ),
    return table, table_goalies, df_players, df_goalies

def players_plotstats(position, stat, linestat, teamid, players, goalies, players_list, forwards_list, goalie_list):
    if position in players_list:
        df = pd.DataFrame.from_dict(players)
        if position == 'Forwards':
            df = df[df['Position'].isin(forwards_list)]
        elif position == 'Defenders':
            df = df[df['Position'] == 'D']
        else:
            df = df[df['Position'] == position]
    else:
        df = pd.DataFrame.from_dict(goalies)
        df = df[df['Position'] == position]
    df['Time on Ice'] = df['Time on Ice'].str.split(':').apply(lambda x: int(x[0]))
    teamname = teamslist[teamslist['id'] == teamid]['name'].iloc[0]
    teamcolor = [v for k,v in teamcolors.items() if k == teamname]
    # Create figure with secondary y-axis
    plot = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    plot.add_trace(
        go.Bar(x=df['Player'], y=df[stat], name="{}".format(stat)),
        secondary_y=False,
    )
    #plot = px.bar(df, x='Player', y=stat, text=stat)
    plot.update_traces(marker_color=teamcolor[0])
    plot.update_xaxes(type='category')
    size_x = df[stat].max()*0.20
    size_y = df[stat].max()*0.20
    # Build player list
    for data in plot['data']:
        x_list = data['x']
        y_list = data['y']
        player_ids = []
        player_portraits = []
        for player in x_list:
            portrait = df[df['Player'] == player][''].str.extract(r"\[(.*?)\]").iloc[0][0]
            player_ids.append(id)
            player_portraits.append(portrait)
    for x,y,z in zip(x_list, y_list, player_portraits):
        plot.add_layout_image(
            dict(
                source=z,
                x=x,
                y=y+size_y,
            )
        )
    plot.update_layout_images(dict(
            xref="x",
            yref="y",
            sizex=size_x,
            sizey=size_y,
            xanchor='center',
            yanchor='middle'
    ))
    plot.update_yaxes(range=[0, df[stat].max()+20], showticklabels=False, showgrid=False)
    plot.update_xaxes(showgrid=False)
    if linestat is not None:
        plot.add_trace(
            go.Scatter(x=df['Player'], y=df[linestat], name="{}".format(linestat), marker=dict(color='black')),
            secondary_y=True,
        )
        plot.update_layout(showlegend=False)
        plot.update_yaxes(range=[0, df[linestat].max()+20], showticklabels=False, showgrid=False, secondary_y=True)
    plot.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
    )

    return plot

# def players_plotstats(position, stat, linestat, teamid, players, goalies, players_list, forwards_list, goalie_list):
#     if position in players_list:
#         df = pd.DataFrame.from_dict(players)
#         if position == 'Forwards':
#             df = df[df['Position'].isin(forwards_list)]
#         elif position == 'Defenders':
#             df = df[df['Position'] == 'D']
#         else:
#             df = df[df['Position'] == position]
#     else:
#         df = pd.DataFrame.from_dict(goalies)
#         df = df[df['Position'] == position]
#     df['Time on Ice'] = df['Time on Ice'].str.split(':').apply(lambda x: int(x[0]))
#     teamname = teamslist[teamslist['id'] == teamid]['name'].iloc[0]
#     teamcolor = [v for k,v in teamcolors.items() if k == teamname]
#     plot = px.bar(df, x='Player', y=stat, text=stat)
#     plot.update_traces(marker_color=teamcolor[0])
#     plot.update_xaxes(type='category')
#     size_x = df[stat].max()*0.20
#     size_y = df[stat].max()*0.20
#     # Build player list
#     for data in plot['data']:
#         x_list = data['x']
#         y_list = data['y']
#         player_ids = []
#         player_portraits = []
#         for player in x_list:
#             portrait = df[df['Player'] == player][''].str.extract(r"\[(.*?)\]").iloc[0][0]
#             player_ids.append(id)
#             player_portraits.append(portrait)
#     for x,y,z in zip(x_list, y_list, player_portraits):
#         plot.add_layout_image(
#             dict(
#                 source=z,
#                 x=x,
#                 y=y+size_y,
#             )
#         )
#     plot.update_layout_images(dict(
#             xref="x",
#             yref="y",
#             sizex=size_x,
#             sizey=size_y,
#             xanchor='center',
#             yanchor='middle'
#     ))
#     plot.update_yaxes(range=[0, df[stat].max()+20], showticklabels=False)
#     if linestat is not None:
#         plot.add_scatter(
#             x=df['Player'],
#             y=df[linestat],
#             text=df[linestat],
#             name=linestat,
#             marker=dict(
#                 color='black'
#             )
#         )
#         plot.update_layout(showlegend=False)
#     plot.update_layout(
#         margin=dict(l=10, r=10, t=10, b=10),
#         paper_bgcolor="white",
#         plot_bgcolor="white"
#     )
#
#     return plot
