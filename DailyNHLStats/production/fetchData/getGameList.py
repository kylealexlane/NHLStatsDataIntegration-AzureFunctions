import pandas as pd
import requests
import os
import sys


def fetch_games_create_csv(startDate, endDate):
    # startDate = "2018-01-09"
    # endDate = "2019-01-09"
    response = requests.get(
        "https://statsapi.web.nhl.com/api/v1/schedule?startDate="+startDate+"&endDate="+endDate)
    allData = response.json()

    gamesList = []

    for date in allData['dates']:
        for game in date['games']:
            gamesList.append(game['gamePk'])

    s = pd.Series(gamesList)
    wd = os.getcwd()
    file_path = wd+'/DailyNHLStats/output/csv/gamesList-'+startDate+'-'+endDate+'.csv'
    # file_path = '.output/csv/gamesList-'+startDate+'-'+endDate+'.csv'

    # f = open(file_path,"w+")
    # f.close()
    s.to_csv(file_path)


if __name__ == '__main__':
    script_name = sys.argv[0]
    num_args = len(sys.argv)
    args = str(sys.argv)
    print("Running: ", sys.argv[0])
    if num_args != 3:
        sys.exit('Need three arguments!')
    print("The arguments are: ", str(sys.argv))
    fetch_games_create_csv(sys.argv[1], sys.argv[2])

    # fetch_games_create_csv("2018-08-01", "2019-08-01")




