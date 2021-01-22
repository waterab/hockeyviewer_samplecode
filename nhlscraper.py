import pandas as pd
from pandas.io.json import json_normalize
import requests
from bs4 import BeautifulSoup
import json

# Function for requesting json data from url
def nhlrequest(url):
    headers = {
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
         'Cache-Control': 'no-cache',
         'Pragma': 'no-cache'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return json.loads(str(soup.text))

def currentseason():
    url = 'https://statsapi.web.nhl.com/api/v1/seasons/current'
    js = nhlrequest(url)
    df = pd.DataFrame(js['seasons'])
    return df


#GET https://statsapi.web.nhl.com/api/v1/game/ID/boxscore Returns far less detail
#than feed/live and is much more suitable for post-game details including goals,
#shots, PIMs, blocked, takeaways, giveaways and hits.
class boxscore:

    def __init__(self, gameid):
        self.js = nhlrequest('https://statsapi.web.nhl.com/api/v1/game/' + gameid + '/boxscore')

    def hometeam(self):
        df = pd.json_normalize(data=self.js['teams']['home'])
        return df

    def awayteam(self):
        df = pd.json_normalize(data=self.js['teams']['away'])
        return df

#GET https://statsapi.web.nhl.com/api/v1/game/ID/linescore Even fewer details than
#boxscore. Has goals, shots on goal, powerplay and goalie pulled status, number of
#skaters and shootout information if applicable
class linescore:

    def __init__(self, gameid):
        self.js = nhlrequest('https://statsapi.web.nhl.com/api/v1/game/' + gameid + '/linescore')

    def period(self):
        df = pd.json_normalize(data=self.js['periods'])
        return df

    def shootout(self):
        df = pd.json_normalize(data=self.js['shootoutInfo'])
        return df

    def teamstats(self, homeaway):
        df = pd.json_normalize(data=self.js['teams'][homeaway])
        return self.js

    def ppstatus(self):
        df = pd.json_normalize(data=self.js['powerPlayStrength'])
        return df

    def shootoutstatus(self):
        df = pd.json_normalize(data=self.js['hasShootout'])
        return df

    def shootoutstats(self):
        df = pd.json_normalize(data=self.js['shootoutInfo'])
        return df

    def intermissionstatus(self):
        df = pd.json_normalize(data=self.js['intermissionInfo'])
        return df

    def ppinfo(self):
        df = pd.json_normalize(data=self.js['powerPlayInfo'])
        return df

#GET http://statsapi.web.nhl.com/api/v1/game/ID/content Complex endpoint returning
#multiple types of media relating to the game including videos of shots, goals and saves.\
class content:

    def __init__(self, gameid):
        self.js = nhlrequest('https://statsapi.web.nhl.com/api/v1/game/' + gameid + '/content')

    def editorial(self, modifier, video=False):
        if video is False:
            if modifier == 'preview':
                df = pd.json_normalize(data=self.js['editorial']['preview']['items'])
            elif modifier == 'recap':
                df = pd.json_normalize(data=self.js['editorial']['recap']['items'])
            else:
                return ('Error: modifier must be [preview, recap]')
        else:
            if modifier == 'preview':
                df = pd.json_normalize(data=self.js['editorial']['preview']['items'])
            elif modifier == 'recap':
                df = pd.json_normalize(data=self.js['editorial']['recap']['items'][0]['media']['playbacks'])
            else:
                return ('Error: modifier must be [preview, recap]')
        return df

    def media_milestones(self):
        df = pd.json_normalize(data=self.js['media']['milestones']['items'])
        return df

    def highlights_sc(self):
        df = pd.json_normalize(data=self.js['highlights']['scoreboard']['items'])
        return df

    def highlights_gc(self):
        df = pd.json_normalize(data=self.js['highlights']['gameCenter']['items'])
        return df

class players:

    def __init__(self, playerId):
        self.url = 'https://statsapi.web.nhl.com/api/v1/people/' + playerId
        self.playerid = playerId

    def info(self):
        js = nhlrequest(self.url)
        df = pd.json_normalize(data=js['people'])
        return df

    def current_seasonstats(self):
        current_season = currentseason()['seasonId'].iloc[0]
        js = nhlrequest(self.url + '/stats?stats=statsSingleSeason&season' + current_season)
        df = pd.json_normalize(data=js['stats'], record_path=['splits'])
        return df

    def projected_seasonstats(self):
        current_season = currentseason()['seasonId'].iloc[0]
        js = nhlrequest(self.url + '/stats?stats=onPaceRegularSeason&season=' + current_season)
        df = pd.json_normalize(data=js['stats'], record_path=['splits'])
        return df

# Returns data as json for customizing in callback
class standings:
    def __init__(self):
        self.url = 'https://statsapi.web.nhl.com/api/v1/standings/'
        self.types = pd.json_normalize(nhlrequest('https://statsapi.web.nhl.com/api/v1/standingsTypes'))['name'].to_list()

    def standingstype(self, standingstype='byLeague'):
        standingstypes = self.types
        if standingstype not in standingstypes:
            raise ValueError("Invalid type. Expected one of: %s" % standingstypes)
        url = self.url + standingstype
        js = nhlrequest(url)

        return js

class teams:

    def __init__(self, teamid=None):
        self.teamid = teamid
        if self.teamid is not None:
            self.url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(self.teamid)
        else:
            self.url = 'https://statsapi.web.nhl.com/api/v1/teams/'

    # Dataframe for all teams
    def teams(self):
        js = nhlrequest(self.url)
        df = pd.json_normalize(data=js['teams'])
        return df

    # Shows roster of active players for the specified team
    def roster(self):
        js = nhlrequest(self.url + '?expand=team.roster')
        df = pd.json_normalize(data=js['teams'], record_path=['roster', 'roster'], meta=['id', 'name'])
        return df

    # Returns details of the upcoming game for a team
    # Same as above but for the last game played
    def schedule(self, schedule):
        if schedule == 'next':
            js = nhlrequest(self.url + '?expand=team.schedule.next')
            df = pd.json_normalize(data=js['teams'], record_path=['nextGameSchedule', 'dates', 'games'])
            return df
        elif schedule == 'previous':
            js = nhlrequest(self.url + '?expand=team.schedule.previous')
            try:
                df = pd.json_normalize(data=js['teams'], record_path=['previousGameSchedule', 'dates', 'games'])
            except:
                df = pd.DataFrame()
            return df
        else:
            return 'Error: schedule must be [next, previous]'

    # Returns the teams stats for the season
    def stats(self):
        js = nhlrequest(self.url + '?expand=team.stats')
        df = pd.json_normalize(data=js['teams'], record_path=['teamStats', 'splits'])
        return df

    # Return team logo url
    def logo(self):
        if self.teamid is None:
            return 'Error: team id required'
        else:
            url = 'https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/' + str(self.teamid)  + '.svg'
            return url

class schedule:

    def __init__(self):
        self.url = 'https://statsapi.web.nhl.com/api/v1/schedule'

    def season_record(self, season, teamid=None):
        if teamid is None:
            url = self.url + '?season='+ str(season)
        else:
            url = self.url + '?season='+ str(season) + '&teamId=' + str(teamid)
        js = nhlrequest(url)
        df = pd.json_normalize(data=js['dates'], record_path=['games'])
        return df

    # Returns team logos
    # def logo(self, theme, season=None):
    #     # Team logos
    #     url = 'https://records.nhl.com/site/api/franchise?include=teams.id&include=teams.active&include=teams.triCode&include=teams.placeName&include=teams.commonName&include=teams.fullName&include=teams.logos&include=teams.conference.name&include=teams.division.name&include=teams.franchiseTeam.firstSeason.id&include=teams.franchiseTeam.lastSeason.id&include=teams.franchiseTeam.teamCommonName'
    #     js = nhlrequest(url)
    #     df = pd.json_normalize(js['data'], ['teams', 'logos'])
    #     if season is None:
    #         seasonid = currentseason()['seasonId'].iloc[0]
    #         df = df[df['endSeason'] == int(seasonid)] # Isolate current seasons
    #     else:
    #         df = df[df['endSeason'] == int(season)] # Isolate current seasons
    #     if self.teamid is not None:
    #         df = df[df['teamId'] == int(self.teamid)]
    #     # Select based on theme
    #     df = df[df['background'] == theme]
    #
    #     return df
