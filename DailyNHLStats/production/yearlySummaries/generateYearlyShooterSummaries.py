import pandas as pd
from ...ignore import engine
import sys
import time
import io

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_row', 100)
pd.set_option('display.max_columns', 150)


def GenerateAndPushShooterSummaries(gameSeason):

    ### TESTING ###
    # gameSeason = 'all'
    # gameSeason = '20182019'

    ####

    print('fetching data from adjusted shots...')
    s = time.time()

    # Either generate for all or generate based on specific season
    if gameSeason == "all":
        sql = """SELECT adjs.*, gd.game_type, gd.game_season FROM nhlstats.adjusted_shots AS adjs
            LEFT JOIN nhlstats.game_details AS gd ON gd.gamepk = adjs.game_id
            WHERE (gd.game_type = 'R' OR gd.game_type = 'P')
            AND period_type != 'SHOOTOUT'"""
        allShots = pd.read_sql_query(sql, con=engine)
    else:
        sql = """SELECT adjs.*, gd.game_type, gd.game_season FROM nhlstats.adjusted_shots AS adjs
                    LEFT JOIN nhlstats.game_details AS gd ON gd.gamepk = adjs.game_id
                    WHERE (gd.game_type = 'R' OR gd.game_type = 'P')
                    AND gd.game_season = %s
                    AND period_type != 'SHOOTOUT'""" % gameSeason
        allShots = pd.read_sql_query(sql, con=engine)

    print(time.time() - s)
    print('fetching yearly averages data...')
    s = time.time()

    sql = """SELECT * FROM nhlstats.yearly_averages where month = 'year'"""
    yearlyAverages = pd.read_sql_query(sql, con=engine)

    def get_month(row):
        return row['game_date'].month

    def goal_and_value(row, label):
        return row[label] & row['goal_binary']

    def pred_value(row, label):
        if(row[label] == 1):
            return row['pred']
        else:
            return 0

    print(time.time() - s)
    print('Calculating initial metrics and formatting...')
    s = time.time()

    allShotsTempCopy = allShots.copy()
    allShotsTempCopy['month'] = 'year'
    allShots['month'] = allShots.apply(lambda row: get_month(row), axis=1)

    allShots = pd.concat([allShots, allShotsTempCopy])

    allShots['wrist_shot_goal'] = allShots.apply(lambda row: goal_and_value(row, 'wrist_shot'), axis=1)
    allShots['backhand_goal'] = allShots.apply(lambda row: goal_and_value(row, 'backhand'), axis=1)
    allShots['slap_shot_goal'] = allShots.apply(lambda row: goal_and_value(row, 'slap_shot'), axis=1)
    allShots['snap_shot_goal'] = allShots.apply(lambda row: goal_and_value(row, 'snap_shot'), axis=1)
    allShots['tip_in_goal'] = allShots.apply(lambda row: goal_and_value(row, 'tip_in'), axis=1)
    allShots['deflected_goal'] = allShots.apply(lambda row: goal_and_value(row, 'deflected'), axis=1)
    allShots['wrap_around_goal'] = allShots.apply(lambda row: goal_and_value(row, 'wrap_around'), axis=1)

    allShots['wrist_shot_pred'] = allShots.apply(lambda row: pred_value(row, 'wrist_shot'), axis=1)
    allShots['backhand_pred'] = allShots.apply(lambda row: pred_value(row, 'backhand'), axis=1)
    allShots['slap_shot_pred'] = allShots.apply(lambda row: pred_value(row, 'slap_shot'), axis=1)
    allShots['snap_shot_pred'] = allShots.apply(lambda row: pred_value(row, 'snap_shot'), axis=1)
    allShots['tip_in_pred'] = allShots.apply(lambda row: pred_value(row, 'tip_in'), axis=1)
    allShots['deflected_pred'] = allShots.apply(lambda row: pred_value(row, 'deflected'), axis=1)
    allShots['wrap_around_pred'] = allShots.apply(lambda row: pred_value(row, 'wrap_around'), axis=1)

    tempShots = allShots.copy()

    shotsGrouped = tempShots.groupby(['player1_id', 'game_season', 'month', 'game_type'])

    print(time.time() - s)
    print('Calculating grouped metrics per player...')
    s = time.time()

    # Define the aggregation procedure outside of the groupby operation
    aggregations = {
        'goal_binary': 'sum',
        'wrist_shot': 'sum',
        'backhand': 'sum',
        'slap_shot': 'sum',
        'snap_shot': 'sum',
        'tip_in': 'sum',
        'deflected': 'sum',
        'wrap_around': 'sum',

        'wrist_shot_pred': 'sum',
        'backhand_pred': 'sum',
        'slap_shot_pred': 'sum',
        'snap_shot_pred': 'sum',
        'tip_in_pred': 'sum',
        'deflected_pred': 'sum',
        'wrap_around_pred': 'sum',

        'wrist_shot_goal': 'sum',
        'backhand_goal': 'sum',
        'slap_shot_goal': 'sum',
        'snap_shot_goal': 'sum',
        'tip_in_goal': 'sum',
        'deflected_goal': 'sum',
        'wrap_around_goal': 'sum',
        'dist': 'mean',
        'ang': 'mean',
        'pred': 'sum'
    }

    metrics = shotsGrouped.agg(aggregations)

    counts = shotsGrouped.agg({'pred': 'count'})

    metrics = metrics.merge(counts, on=['player1_id', 'game_season', 'month', 'game_type'], how='inner', suffixes=('', '_count'))

    def get_perc(row, label):
        return (row[label] / row['pred_count'])

    def get_pred_perc(row, label, label2):
        if row[label2] == 0:
            return 0
        return (row[label] / row[label2])

    def get_perc_specific(row, label, countLabel):
        if row[countLabel] == 0:
            return 0
        return (row[label] / row[countLabel])

    print(time.time() - s)
    print('Calculating frequencies and percents...')
    s = time.time()

    metrics.reset_index()
    metrics['shooting_perc'] = metrics.apply(lambda row: get_perc(row, 'goal_binary'), axis=1)
    metrics['wrist_shot_freq'] = metrics.apply(lambda row: get_perc(row, 'wrist_shot'), axis=1)
    metrics['backhand_freq'] = metrics.apply(lambda row: get_perc(row, 'backhand'), axis=1)
    metrics['slap_shot_freq'] = metrics.apply(lambda row: get_perc(row, 'slap_shot'), axis=1)
    metrics['snap_shot_freq'] = metrics.apply(lambda row: get_perc(row, 'snap_shot'), axis=1)
    metrics['tip_in_freq'] = metrics.apply(lambda row: get_perc(row, 'tip_in'), axis=1)
    metrics['deflected_freq'] = metrics.apply(lambda row: get_perc(row, 'deflected'), axis=1)
    metrics['wrap_around_freq'] = metrics.apply(lambda row: get_perc(row, 'wrap_around'), axis=1)

    metrics['pred_shooting_perc'] = metrics.apply(lambda row: get_perc(row, 'pred'), axis=1)
    metrics['goals_aa_per_shot'] = metrics['shooting_perc'] - metrics['pred_shooting_perc']

    metrics['pred_shooting_perc_wrist_shot'] = metrics.apply(lambda row: get_pred_perc(row, 'wrist_shot_pred', 'wrist_shot'), axis=1)
    metrics['pred_shooting_perc_backhand'] = metrics.apply(lambda row: get_pred_perc(row, 'backhand_pred', 'backhand'), axis=1)
    metrics['pred_shooting_perc_slap_shot'] = metrics.apply(lambda row: get_pred_perc(row, 'slap_shot_pred', 'slap_shot'), axis=1)
    metrics['pred_shooting_perc_snap_shot'] = metrics.apply(lambda row: get_pred_perc(row, 'snap_shot_pred', 'snap_shot'), axis=1)
    metrics['pred_shooting_perc_tip_in'] = metrics.apply(lambda row: get_pred_perc(row, 'tip_in_pred', 'tip_in'), axis=1)
    metrics['pred_shooting_perc_deflected'] = metrics.apply(lambda row: get_pred_perc(row, 'deflected_pred', 'deflected'), axis=1)
    metrics['pred_shooting_perc_wrap_around'] = metrics.apply(lambda row: get_pred_perc(row, 'wrap_around_pred', 'wrap_around'), axis=1)


    metrics['wrist_shot_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'wrist_shot_goal', 'wrist_shot'), axis=1)
    metrics['backhand_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'backhand_goal', 'backhand'), axis=1)
    metrics['slap_shot_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'slap_shot_goal', 'slap_shot'), axis=1)
    metrics['snap_shot_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'snap_shot_goal', 'snap_shot'), axis=1)
    metrics['tip_in_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'tip_in_goal', 'tip_in'), axis=1)
    metrics['deflected_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'deflected_goal', 'deflected'), axis=1)
    metrics['wrap_around_shooting_perc'] = metrics.apply(lambda row: get_perc_specific(row, 'wrap_around_goal', 'wrap_around'), axis=1)


    print(time.time() - s)
    print('renaming and formatting...')
    s = time.time()

    metrics = metrics.reset_index()
    columns = {
        'game_season': 'year_code',
        'pred_count': 'num_shots',
        'goal_binary': 'num_goals',
        'pred': 'sum_xgoals',
        'shooting_perc': 'avg_shoot_perc',
        'pred_shooting_perc': 'avg_xgoals',

        'pred_shooting_perc_wrist_shot': 'avg_xgoals_wrist_shot',
        'pred_shooting_perc_backhand': 'avg_xgoals_backhand',
        'pred_shooting_perc_slap_shot': 'avg_xgoals_slap_shot',
        'pred_shooting_perc_snap_shot': 'avg_xgoals_snap_shot',
        'pred_shooting_perc_tip_in': 'avg_xgoals_tip_in',
        'pred_shooting_perc_deflected': 'avg_xgoals_deflected',
        'pred_shooting_perc_wrap_around': 'avg_xgoals_wrap_around',

        'wrist_shot': 'wrist_shot_num',
        'backhand': 'backhand_num',
        'slap_shot': 'slap_shot_num',
        'snap_shot': 'snap_shot_num',
        'tip_in': 'tip_in_num',
        'deflected': 'deflected_num',
        'wrap_around': 'wrap_around_num',
        'dist': 'mean_dist',
        'ang': 'mean_ang'
    }

    dropColumns = [
        'wrist_shot_goal',
        'backhand_goal',
        'slap_shot_goal',
        'snap_shot_goal',
        'tip_in_goal',
        'deflected_goal',
        'wrap_around_goal',
    ]

    fomattedDf = metrics.rename(index=str, columns=columns)
    fomattedDf = fomattedDf.drop(dropColumns, axis=1)

    print(time.time() - s)
    print('Joining with yearly averages and calculating metrics...')
    s = time.time()

    withYearly = fomattedDf.merge(yearlyAverages, on=['year_code', 'game_type'], how='left', suffixes=('', '_ya'))


    def compare_yearly_diff(row, label):
        l2 = label + "_ya"
        return (row[label] - row[l2])

    def compare_yearly_relative(row, label):
        l2 = label + "_ya"
        return (row[label] / row[l2])

    # Get metrics vs yearly average
    withYearly['shot_quality'] = withYearly.apply(lambda row: compare_yearly_relative(row, 'avg_xgoals'), axis=1)

    withYearly['avg_shoot_perc_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_shoot_perc'), axis=1)
    withYearly['wrist_shot_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'wrist_shot_freq'), axis=1)
    withYearly['backhand_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'backhand_freq'), axis=1)
    withYearly['slap_shot_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'slap_shot_freq'), axis=1)
    withYearly['snap_shot_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'snap_shot_freq'), axis=1)
    withYearly['tip_in_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'tip_in_freq'), axis=1)
    withYearly['deflected_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'deflected_freq'), axis=1)
    withYearly['wrap_around_freq_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'wrap_around_freq'), axis=1)
    withYearly['avg_xgoals_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals'), axis=1)
    # withYearly['goals_aa_per_shot_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'goals_aa_per_shot'), axis=1)

    withYearly['avg_xgoals_wrist_shot_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_wrist_shot'), axis=1)
    withYearly['avg_xgoals_backhand_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_backhand'), axis=1)
    withYearly['avg_xgoals_slap_shot_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_slap_shot'), axis=1)
    withYearly['avg_xgoals_snap_shot_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_snap_shot'), axis=1)
    withYearly['avg_xgoals_tip_in_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_tip_in'), axis=1)
    withYearly['avg_xgoals_deflected_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_deflected'), axis=1)
    withYearly['avg_xgoals_wrap_around_aa'] = withYearly.apply(lambda row: compare_yearly_diff(row, 'avg_xgoals_wrap_around'), axis=1)

    withYearly['wrist_shot_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'wrist_shot_shooting_perc'), axis=1)
    withYearly['backhand_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'backhand_shooting_perc'), axis=1)
    withYearly['slap_shot_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'slap_shot_shooting_perc'), axis=1)
    withYearly['snap_shot_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'snap_shot_shooting_perc'), axis=1)
    withYearly['tip_in_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'tip_in_shooting_perc'), axis=1)
    withYearly['deflected_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'deflected_shooting_perc'), axis=1)
    withYearly['wrap_around_shooting_perc_aa'] = withYearly.apply(
        lambda row: compare_yearly_diff(row, 'wrap_around_shooting_perc'), axis=1)

    print(time.time() - s)
    print('dropping irrelevant columns...')
    s = time.time()

    yearlyColumnsToDrop = ['month_ya',  'num_shots_ya',  'num_goals_ya',  'sum_xgoals_ya',  'avg_shoot_perc_ya',  'avg_xgoals_ya',  'avg_xgoals_wrist_shot_ya',  'avg_xgoals_backhand_ya',  'avg_xgoals_slap_shot_ya',
                           'avg_xgoals_snap_shot_ya',  'avg_xgoals_tip_in_ya',  'avg_xgoals_deflected_ya',  'avg_xgoals_wrap_around_ya',  'wrist_shot_num_ya',  'backhand_num_ya',  'slap_shot_num_ya',  'snap_shot_num_ya',
                           'tip_in_num_ya',  'deflected_num_ya',  'wrap_around_num_ya',  'wrist_shot_pred_ya',  'backhand_pred_ya',  'slap_shot_pred_ya',  'snap_shot_pred_ya', 'tip_in_pred_ya',  'deflected_pred_ya',
                           'wrap_around_pred_ya',  'wrist_shot_freq_ya',  'backhand_freq_ya',  'slap_shot_freq_ya',  'snap_shot_freq_ya',  'tip_in_freq_ya',  'deflected_freq_ya',  'wrap_around_freq_ya',
                           'wrist_shot_shooting_perc_ya',  'backhand_shooting_perc_ya',  'slap_shot_shooting_perc_ya',  'snap_shot_shooting_perc_ya',  'tip_in_shooting_perc_ya',  'deflected_shooting_perc_ya',
                           'wrap_around_shooting_perc_ya',  'mean_dist_ya',  'mean_ang_ya', 'goals_aa_per_shot_ya', 'created']

    tempWithYearly = withYearly.copy()
    tempWithYearly = tempWithYearly.drop(yearlyColumnsToDrop, axis=1)

    print(time.time() - s)
    print('Calculating ranks...')
    s = time.time()

    playerIds = tempWithYearly['player1_id']
    years = tempWithYearly['year_code']
    gameTypes = tempWithYearly['game_type']
    months = tempWithYearly['month']

    grouped = tempWithYearly.drop(columns=['player1_id']).groupby(['year_code', 'game_type', 'month'])

    pctile_ranks = grouped.rank(pct=True)
    ranks = grouped.rank(pct=False)

    pctile_ranks = pctile_ranks.reset_index()
    ranks = ranks.reset_index()

    ranks['player1_id'] = playerIds
    ranks['year_code'] = years
    ranks['game_type'] = gameTypes
    ranks['month'] = months

    pctile_ranks['player1_id'] = playerIds
    pctile_ranks['year_code'] = years
    pctile_ranks['game_type'] = gameTypes
    pctile_ranks['month'] = months

    print(time.time() - s)
    print('combining ranks...')
    s = time.time()

    allRanks = pctile_ranks.merge(ranks, on=['player1_id', 'year_code', 'month', 'game_type'], how='inner',
                             suffixes=('_pctile', '_rank'))

    print(time.time() - s)
    print('deleting from db...')
    s = time.time()

    if gameSeason == "all":
        sql = """DELETE from nhlstats.yearly_shooter_summaries"""
    else:
        sql = """DELETE FROM nhlstats.yearly_shooter_summaries
                               WHERE year_code = %s""" % gameSeason
    connection = engine.connect()
    connection.execute(sql)

    cols = {'player1_id': 'id'}

    # Pushing values to yearly_shooter_summaries
    formattedDf = tempWithYearly.rename(index=str, columns=cols).round(3)
    print(time.time() - s)
    print('pushing to db...')
    s = time.time()

    columns = list(formattedDf.columns.values)

    output = io.StringIO()
    # ignore the index
    formattedDf.to_csv(output, sep='\t', header=False, index=False)
    output.getvalue()
    # jump to start of stream
    output.seek(0)

    connection = engine.raw_connection()
    cursor = connection.cursor()
    # null values become ''
    cursor.copy_from(output, 'nhlstats.yearly_shooter_summaries', null="", columns=(columns))
    connection.commit()
    cursor.close()
    print(time.time() - s)


    # Delete ranked data from ranks table
    print(time.time() - s)
    print('deleting from ranks db...')
    s = time.time()

    if gameSeason == "all":
        sql = """DELETE from nhlstats.yearly_shooter_ranks"""
    else:
        sql = """DELETE FROM nhlstats.yearly_shooter_ranks
                                   WHERE year_code = %s""" % gameSeason
    connection = engine.connect()
    connection.execute(sql)

    # Push ranked data to ranks table
    formattedDf = allRanks.rename(index=str, columns=cols).round(3)
    formattedDf = formattedDf.drop(columns=['index_pctile', 'index_rank'])
    print(time.time() - s)
    print('pushing to ranks db...')
    s = time.time()

    columns = list(formattedDf.columns.values)

    output = io.StringIO()
    # ignore the index
    formattedDf.to_csv(output, sep='\t', header=False, index=False)
    output.getvalue()
    # jump to start of stream
    output.seek(0)

    connection = engine.raw_connection()
    cursor = connection.cursor()
    # null values become ''
    cursor.copy_from(output, 'nhlstats.yearly_shooter_ranks', null="", columns=(columns))
    connection.commit()
    cursor.close()
    print(time.time() - s)



if __name__ == '__main__':
    script_name = sys.argv[0]
    num_args = len(sys.argv)
    args = str(sys.argv)
    print("Running: ", sys.argv[0])
    if num_args != 2:
        sys.exit('Need two arguments!')
    print("The arguments are: ", str(sys.argv))
    GenerateAndPushShooterSummaries(sys.argv[1])
    # GenerateAndPushShooterSummaries("all")
    # GenerateAndPushShooterSummaries("20182019")

