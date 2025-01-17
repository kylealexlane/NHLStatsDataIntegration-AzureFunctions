import pandas as pd
import requests
import psycopg2
from datetime import datetime
from ...ignore import hostname, username, password, database, engine
import sys
import time
import io
import os


def fetchGameAndPopulate(startDate, endDate):

    ### TESTING
    # startDate = '2019-01-03'
    # endDate = '2019-01-06'

    # startDate = '2010-01-09'
    # endDate = '2011-01-09'
    #####

    print('Reading csv and starting to loop through...')
    totalTime = time.time()
    i = 0
    wd = os.getcwd()
    file_path = wd+'/DailyNHLStats/output/csv/gamesList-'+startDate+'-'+endDate+'.csv'
    gamesList = pd.read_csv(file_path)  # Fetching from csv

    for index, row in gamesList.iterrows():

        myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = myConnection.cursor()

        i += 1
        print(i)
        print(row[1])

        # Break to continue incomplete scripts
        # if i < 650:
        #     continue

        gamePk = str(row[1])
        # If using gamePk

        ### TESTING
        # gamePk = '2018020322'
        # response = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + gamePk + "/feed/live")
        # gameData = response.json()
        ######

        print("Fetching all game info....")
        response = requests.get("https://statsapi.web.nhl.com/api/v1/game/"+str(row[1])+"/feed/live")
        s = time.time()
        gameData = response.json()

        print(time.time() - s)
        print("Formatting cleaning game details data ...")
        s = time.time()
        # Preventing errors if data missing
        gd = gameData['gameData'] if 'gameData' in gameData else {}
        g = gd['game'] if 'game' in gd else {}
        dt = gd['datetime'] if 'datetime' in gd else {}
        status = gd['status'] if 'status' in gd else {}
        teams = gd['teams'] if 'teams' in gd else {}
        venue = gd['venue'] if 'venue' in gd else {}

        # game info
        gamepk = g['pk'] if 'pk' in g else None
        gameSeason = g['season'] if 'pk' in g else None
        gameType = g['type'] if 'type' in g else None

        # datetime info
        dateTime = dt['dateTime'] if 'dateTime' in dt else None
        endDateTime = dt['endDateTime'] if 'endDateTime' in dt else None

        # status info
        abstractGameState = status['abstractGameState'] if 'abstractGameState' in status else None
        codedGameState = status['codedGameState'] if 'codedGameState' in status else None
        detailedState = status['status']['detailedState'] if 'status' in status else None
        statusCode = status['statusCode'] if 'statusCode' in status else None
        startTimeTBD = status['startTimeTBD'] if 'startTimeTBD' in status else None

        # teams info
        away = teams['away'] if 'away' in teams else {}
        home = teams['home'] if 'home' in teams else {}
        awayId = away['id'] if 'id' in away else None
        awayFranchiseId = away['franchiseId'] if 'franchiseId' in away else None
        homeId = home['id'] if 'id' in home else None
        homeFranchiseId = home['franchiseId'] if 'franchiseId' in home else None

        # venue info
        venueId = venue['id'] if 'id' in venue else None
        venueName = venue['name'] if 'name' in venue else None
        venueLink = venue['link'] if 'link' in venue else None

        # Live Data - prevent errors
        liveData = gameData['liveData'] if 'liveData' in gameData else {}
        boxscore = liveData['boxscore'] if 'boxscore' in liveData else {}
        bsteams = boxscore['teams'] if 'teams' in boxscore else {}

        ##### Live data - boxscore info
        bshome = bsteams['home'] if 'home' in bsteams else {}
        homestats = bshome['teamStats'] if 'teamStats' in bshome else {}
        hometss = homestats['teamSkaterStats'] if 'teamSkaterStats' in homestats else {}

        bsaway = bsteams['away'] if 'away' in bsteams else {}
        awaystats = bsaway['teamStats'] if 'teamStats' in bsaway else {}
        awaytss = awaystats['teamSkaterStats'] if 'teamSkaterStats' in awaystats else {}

        # Home boxscore info
        homegoals = hometss['goals'] if 'goals' in hometss else None
        homepim = hometss['pim'] if 'pim' in hometss else None
        homeshots = hometss['shots'] if 'shots' in hometss else None
        homeppperc = hometss['powerPlayPercentage'] if 'powerPlayPercentage' in hometss else None
        homeppgoals = hometss['powerPlayGoals'] if 'powerPlayGoals' in hometss else None
        homeppopp = hometss['powerPlayOpportunities'] if 'powerPlayOpportunities' in hometss else None
        homefowperc = hometss['faceOffWinPercentage'] if 'faceOffWinPercentage' in hometss else None
        homeblocked = hometss['blocked'] if 'blocked' in hometss else None
        hometakeaways = hometss['takeaways'] if 'takeaways' in hometss else None
        homegiveaways = hometss['giveaways'] if 'giveaways' in hometss else None
        homehits = hometss['hits'] if 'hits' in hometss else None

        # Away boxscore info
        awaygoals = awaytss['goals'] if 'goals' in awaytss else None
        awaypim = awaytss['pim'] if 'pim' in awaytss else None
        awayshots = awaytss['shots'] if 'shots' in awaytss else None
        awayppperc = awaytss['powerPlayPercentage'] if 'powerPlayPercentage' in awaytss else None
        awayppgoals = awaytss['powerPlayGoals'] if 'powerPlayGoals' in awaytss else None
        awayppopp = awaytss['powerPlayOpportunities'] if 'powerPlayOpportunities' in awaytss else None
        awayfowperc = awaytss['faceOffWinPercentage'] if 'faceOffWinPercentage' in awaytss else None
        awayblocked = awaytss['blocked'] if 'blocked' in awaytss else None
        awaytakeaways = awaytss['takeaways'] if 'takeaways' in awaytss else None
        awaygiveaways = awaytss['giveaways'] if 'giveaways' in awaytss else None
        awayhits = awaytss['hits'] if 'hits' in awaytss else None

        results = {'gamepk': gamePk,
                   'game_season': gameSeason,
                   'game_type': gameType,
                   'date_time': dateTime,
                   'end_date_time': endDateTime,
                   'abstract_game_state': abstractGameState,
                   'coded_game_state': codedGameState,
                   'detailed_state': detailedState,
                   'status_code': statusCode,
                   'start_time_tbd': startTimeTBD,
                   'away_id': awayId,
                   'away_franchise_id': awayFranchiseId,
                   'home_id': homeId,
                   'home_franchise_id': homeFranchiseId,
                   'venue_id': venueId,
                   'venue_name': venueName,
                   'venue_link': venueLink,
                   'home_goals': homegoals,
                   'home_pim': homepim,
                   'home_shots': homeshots,
                   'home_ppperc': homeppperc,
                   'home_ppgoals': homeppgoals,
                   'home_ppopp': homeppopp,
                   'home_fowperc': homefowperc,
                   'home_blocked': homeblocked,
                   'home_takeaways': hometakeaways,
                   'home_giveaways': homegiveaways,
                   'home_hits': homehits,
                   'away_goals': awaygoals,
                   'away_pim': awaypim,
                   'away_shots': awayshots,
                   'away_ppperc': awayppperc,
                   'away_ppgoals': awayppgoals,
                   'away_ppopp': awayppopp,
                   'away_fowperc': awayfowperc,
                   'away_blocked': awayblocked,
                   'away_takeaways': awaytakeaways,
                   'away_giveaways': awaygiveaways,
                   'away_hits': awayhits,
                   }

        print(time.time() - s)
        print("Deleting game details data in db....")
        s = time.time()
        gameDetails = pd.DataFrame(data=results, index=['i',])

        string = "DELETE FROM nhlstats.game_details WHERE gamepk = %s ;" % gamePk
        cur.execute(string)
        myConnection.commit()
        gameDetails.to_sql('game_details', schema='nhlstats', con=engine, if_exists='append', index=False)

        playResults = {'game_id': [],
                   'game_date': [],
                   'event_idx': [],
                   'event_id': [],
                   'period': [],
                   'period_type': [],
                   'ordinal_num': [],
                   'period_time': [],
                   'period_time_remaining': [],
                   'away_goals': [],
                   'home_goals': [],
                   'x_coords': [],
                   'y_coords': [],
                   'team_id': [],
                   'team_name': [],
                   'team_tri_code': [],
                   'player1_id': [],
                   'player1_name': [],
                   'player1_type': [],
                   'player2_id': [],
                   'player2_name': [],
                   'player2_type': [],
                   'player3_id': [],
                   'player3_name': [],
                   'player3_type': [],
                   'player4_id': [],
                   'player4_name': [],
                   'player4_type': [],
                   'event_type': [],
                   'event_code': [],
                   'event_type_id': [],
                   'event_desc': [],
                   'event_second_type': []
                   }

        def toDateTime(date):
            datetime.datetime.strptime(date, '%Y-%m-%d')

        print(time.time() - s)
        print("Formatting and cleaning all play data ....")
        s = time.time()

        # Live plays might be empty in older cases
        plays = liveData['plays'] if 'plays' in liveData else {}
        allPlays = plays['allPlays'] if 'allPlays' in plays else {}


        for index, play in enumerate(allPlays):
            playResults['game_id'].append(gamepk)
            playResults['game_date'].append(dateTime)
            playResults['event_idx'].append(play['about']['eventIdx'])
            playResults['event_id'].append(play['about']['eventId'])
            playResults['period'].append(play['about']['period'])
            playResults['period_type'].append(play['about']['periodType'])
            playResults['ordinal_num'].append(play['about']['ordinalNum'])
            playResults['period_time'].append(play['about']['periodTime'])
            playResults['period_time_remaining'].append(play['about']['periodTimeRemaining'])
            playResults['away_goals'].append(play['about']['goals']['away'])
            playResults['home_goals'].append(play['about']['goals']['home'])
            playResults['x_coords'].append(play['coordinates']['x'] if len(play['coordinates']) > 0 and 'x' in play['coordinates'] else None)
            playResults['y_coords'].append(play['coordinates']['y'] if len(play['coordinates']) >0 and 'y' in play['coordinates'] else None)
            playResults['team_id'].append(play['team']['id'] if 'team' in play else None)
            playResults['team_name'].append(play['team']['name'] if 'team' in play else None)
            playResults['team_tri_code'].append(play['team']['triCode'] if 'team' in play and 'triCode' in play['team'] else None)
            playResults['player1_id'].append(play['players'][0]['player']['id'] if 'players' in play else None)
            playResults['player1_name'].append(play['players'][0]['player']['fullName'] if 'players' in play else None)
            playResults['player1_type'].append(play['players'][0]['playerType'] if 'players' in play else None)
            playResults['player2_id'].append(play['players'][1]['player']['id'] if ('players' in play) & (len(play['players']) > 1 if 'players' in play else False) else None)
            playResults['player2_name'].append(play['players'][1]['player']['fullName'] if ('players' in play) & (len(play['players']) > 1 if 'players' in play else False) else None)
            playResults['player2_type'].append(play['players'][1]['playerType'] if ('players' in play) & (len(play['players']) > 1 if 'players' in play else False) else None)
            playResults['player3_id'].append(play['players'][2]['player']['id'] if ('players' in play) & (
                 len(play['players']) > 2 if 'players' in play else False) else None)
            playResults['player3_name'].append(play['players'][2]['player']['fullName'] if ('players' in play) & (
                 len(play['players']) > 2 if 'players' in play else False) else None)
            playResults['player3_type'].append(play['players'][2]['playerType'] if ('players' in play) & (
                 len(play['players']) > 2 if 'players' in play else False) else None)
            playResults['player4_id'].append(play['players'][3]['player']['id'] if ('players' in play) & (
                 len(play['players']) > 3 if 'players' in play else False) else None)
            playResults['player4_name'].append(play['players'][3]['player']['fullName'] if ('players' in play) & (
                 len(play['players']) > 3 if 'players' in play else False) else None)
            playResults['player4_type'].append(play['players'][3]['playerType'] if ('players' in play) & (
                 len(play['players']) > 3 if 'players' in play else False) else None)
            playResults['event_type'].append(play['result']['event'])
            playResults['event_code'].append(play['result']['eventCode'])
            playResults['event_type_id'].append(play['result']['eventTypeId'])
            playResults['event_desc'].append(play['result']['description'] if 'description' in play['result'] else None)
            playResults['event_second_type'].append(play['result']['secondaryType'] if 'secondaryType' in play['result'] else None)

        allPlays = pd.DataFrame(data=playResults)

        print(time.time() - s)
        print('Deleting game play data from db...')
        s = time.time()
        cur.execute("DELETE FROM nhlstats.allplays WHERE game_id = %s ;" % gamePk)
        myConnection.commit()

        print(time.time() - s)
        print('Pushing play data to db...')
        s = time.time()

        allPlays['x_coords'] = allPlays['x_coords'].fillna(0.0).astype(int)
        allPlays['y_coords'] = allPlays['y_coords'].fillna(0.0).astype(int)
        allPlays['team_id'] = allPlays['team_id'].fillna(0.0).astype(int)
        allPlays['player1_id'] = allPlays['player1_id'].fillna(0.0).astype(int)
        allPlays['player2_id'] = allPlays['player2_id'].fillna(0.0).astype(int)
        allPlays['player3_id'] = allPlays['player3_id'].fillna(0.0).astype(int)
        allPlays['player4_id'] = allPlays['player4_id'].fillna(0.0).astype(int)



        columns = list(allPlays.columns.values)

        output = io.StringIO()
        # ignore the index
        allPlays.to_csv(output, sep='\t', header=False, index=False)
        output.getvalue()
        # jump to start of stream
        output.seek(0)

        connection = engine.raw_connection()
        cursor = connection.cursor()
        # null values become ''
        cursor.copy_from(output, 'nhlstats.allplays', null="", columns=(columns))
        connection.commit()
        cursor.close()
        print(time.time() - s)

        # allPlays.to_sql('allplays', schema='nhlstats', con=engine, if_exists='append', index=False)

        # commit sql
        # Close communication with the database
        cur.close()
        myConnection.close()

    print(time.time() - totalTime)


if __name__ == '__main__':
    script_name = sys.argv[0]
    num_args = len(sys.argv)
    args = str(sys.argv)
    print("Running: ", sys.argv[0])
    if num_args != 3:
        sys.exit('Need three arguments!')
    print("The arguments are: ", str(sys.argv))
    fetchGameAndPopulate(sys.argv[1], sys.argv[2])

    # fetchGameAndPopulate('2018-01-09', '2019-01-09')






