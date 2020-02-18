import pandas as pd
import sys
import time
import datetime
import logging
from ..fetchData.getGameList import fetch_games_create_csv
from ..fetchData.importData import fetchGameAndPopulate
from ..transformData.adjustShots import AdjustShots
from ..fetchData.generatePlayerInfo import GeneratePlayerInfo
from ..fetchData.generateTeamInfo import GenerateTeamInfo
from ..yearlySummaries.generateYearlyAverages import GenerateAndPushYearlyAverages
from ..yearlySummaries.generateYearlyGoalieSummaries import GenerateAndPushGoalieSummaries
from ..yearlySummaries.generateYearlyShooterSummaries import GenerateAndPushShooterSummaries
from ..yearlySummaries.generateYearlyTeamAgainstSummaries import GenerateAndPushTeamAgainstSummaries
from ..yearlySummaries.generateYearlyTeamShooterSummaries import GenerateAndPushTeamShooterSummaries

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_row', 100)
pd.set_option('display.max_columns', 50)


def import_daily(startDate, endDate, gameSeason):
    logging.info("\n\n\nRunning daily import... \n\n\n")
    print("\n\n\nRunning daily import... \n\n\n")
    s = time.time()

    logging.info("\n\n\nFetching games list... \n\n\n")
    print("\n\n\nFetching games list... \n\n\n")
    fetch_games_create_csv(startDate, endDate)

    logging.info("\n\n\nImporting Data.... \n\n\n")
    print("\n\n\nImporting Data \n\n\n....")
    fetchGameAndPopulate(startDate, endDate)

    logging.info("\n\n\nAdjusting Shots.... \n\n\n")
    print("\n\n\nAdjusting Shots.... \n\n\n")
    AdjustShots(startDate, endDate)

    logging.info("\n\n\nGenerate player info.... \n\n\n")
    print("\n\n\nGenerate player info.... \n\n\n")
    GeneratePlayerInfo(justnew=True)

    logging.info("\n\n\nGenerate team info.... \n\n\n")
    print("\n\n\nGenerate team info.... \n\n\n")
    GenerateTeamInfo()

    logging.info("\n\n\nGenerate yearly averages.... \n\n\n")
    print("\n\n\nGenerate yearly averages.... \n\n\n")
    GenerateAndPushYearlyAverages(gameSeason)

    logging.info("\n\n\nGenerate goalie summaries.... \n\n\n")
    print("\n\n\nGenerate goalie summaries.... \n\n\n")
    GenerateAndPushGoalieSummaries(gameSeason)

    logging.info("\n\n\nGenerate shooter summaries.... \n\n\n")
    print("\n\n\nGenerate shooter summaries.... \n\n\n")
    GenerateAndPushShooterSummaries(gameSeason)

    logging.info("\n\n\nGenerate team against summaries.... \n\n\n")
    print("\n\n\nGenerate team against summaries.... \n\n\n")
    GenerateAndPushTeamAgainstSummaries(gameSeason)

    logging.info("\n\n\nGenerate team shooter summaries.... \n\n\n")
    print("\n\n\nGenerate team shooter summaries.... \n\n\n")
    GenerateAndPushTeamShooterSummaries(gameSeason)

    print("\n\n\nDone! Time taken....")
    print(time.time() - s)
    print("\n\n\n")
    logging.info('\n\n\nDone! Time taken.... %s \n\n\n', time.time() - s)



def run_import_today():
    startDate = (datetime.datetime.now() + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
    endDate = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    gameSeason = '20192020'
    print('Running between dates: ', startDate, endDate)
    import_daily(startDate, endDate, gameSeason)

if __name__ == '__main__':
    script_name = sys.argv[0]
    num_args = len(sys.argv)
    args = str(sys.argv)
    print("Running: ", sys.argv[0])
    if num_args != 3:
        sys.exit('Need three arguments!')
    print("The arguments are: ", str(sys.argv))
    import_daily(sys.argv[1], sys.argv[2], '20192020')

    # import_daily('2019-10-03', '2019-10-07', '20192020')
