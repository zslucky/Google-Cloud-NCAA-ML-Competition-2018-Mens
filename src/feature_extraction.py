import pandas as pd

def extract_season_teams_mean_score(df_tourney, tourney_name):
    """
        Extract every seasons teams mean scores
            - teams mean score in every season
            - teams mean score in every season as a wining team
            - teams mean score in every season as a lose team
    """
    df = pd.DataFrame({})

    ### Teams mean score
    renamed_win_columns = {'WTeamID': 'team_id', 'WScore': 'team_score'}
    renamed_lose_columns = {'LTeamID': 'team_id', 'LScore': 'team_score'}

    df_teams_win_mean = df_tourney.groupby(['Season', 'WTeamID'])['WScore'].mean().reset_index().rename(columns=renamed_win_columns)
    df_teams_lose_mean = df_tourney.groupby(['Season', 'LTeamID'])['LScore'].mean().reset_index().rename(columns=renamed_lose_columns)

    df_teams_mean_concat = pd.concat([df_teams_win_mean, df_teams_lose_mean])
    df_teams_mean = df_teams_mean_concat.groupby(['Season', 'team_id'])['team_score'].mean().reset_index()

    df_teams_win_mean = df_teams_win_mean.rename(columns={'team_score': tourney_name + '_win_score_mean'})
    df_teams_lose_mean = df_teams_lose_mean.rename(columns={'team_score': tourney_name + '_lose_score_mean'})
    df_teams_mean = df_teams_mean.rename(columns={'team_score': tourney_name + '_score_mean'})

    df = df_teams_mean.merge(df_teams_win_mean, on=['Season', 'team_id'], how='left', left_index=False, right_index=False)
    df = df.merge(df_teams_lose_mean, on=['Season', 'team_id'], how='left', left_index=False, right_index=False)

    return df

def extract_season_teams_max_score(df_tourney, tourney_name):
    """
        Extract every seasons teams mean scores
            - teams max score in every season
            - teams max score in every season as a wining team
            - teams max score in every season as a lose team
    """
    df = pd.DataFrame({})

    ### Teams mean score
    renamed_win_columns = {'WTeamID': 'team_id', 'WScore': 'team_score'}
    renamed_lose_columns = {'LTeamID': 'team_id', 'LScore': 'team_score'}

    df_teams_win_max = df_tourney.groupby(['Season', 'WTeamID'])['WScore'].max().reset_index().rename(columns=renamed_win_columns)
    df_teams_lose_max = df_tourney.groupby(['Season', 'LTeamID'])['LScore'].max().reset_index().rename(columns=renamed_lose_columns)

    df_teams_max_concat = pd.concat([df_teams_win_max, df_teams_lose_max])
    df_teams_max = df_teams_max_concat.groupby(['Season', 'team_id'])['team_score'].max().reset_index()

    df_teams_win_max = df_teams_win_max.rename(columns={'team_score': tourney_name + '_win_score_max'})
    df_teams_lose_max = df_teams_lose_max.rename(columns={'team_score': tourney_name + '_lose_score_max'})
    df_teams_max = df_teams_max.rename(columns={'team_score': tourney_name + '_score_max'})

    df = df_teams_max.merge(df_teams_win_max, on=['Season', 'team_id'], how='left', left_index=False, right_index=False)
    df = df.merge(df_teams_lose_max, on=['Season', 'team_id'], how='left', left_index=False, right_index=False)

    return df

def extract_season_teams_min_score(df_tourney, tourney_name):
    """
        Extract every seasons teams mean scores
            - teams min score in every season
            - teams min score in every season as a wining team
            - teams min score in every season as a lose team
    """
    df = pd.DataFrame({})

    ### Teams mean score
    renamed_win_columns = {'WTeamID': 'team_id', 'WScore': 'team_score'}
    renamed_lose_columns = {'LTeamID': 'team_id', 'LScore': 'team_score'}

    df_teams_win_min = df_tourney.groupby(['Season', 'WTeamID'])['WScore'].min().reset_index().rename(columns=renamed_win_columns)
    df_teams_lose_min = df_tourney.groupby(['Season', 'LTeamID'])['LScore'].min().reset_index().rename(columns=renamed_lose_columns)

    df_teams_min_concat = pd.concat([df_teams_win_min, df_teams_lose_min])
    df_teams_min = df_teams_min_concat.groupby(['Season', 'team_id'])['team_score'].max().reset_index()

    df_teams_win_min = df_teams_win_min.rename(columns={'team_score': tourney_name + '_win_score_min'})
    df_teams_lose_min = df_teams_lose_min.rename(columns={'team_score': tourney_name + '_lose_score_min'})
    df_teams_min = df_teams_min.rename(columns={'team_score': tourney_name + '_score_min'})

    df = df_teams_min.merge(df_teams_win_min, on=['Season', 'team_id'], how='left', left_index=False, right_index=False)
    df = df.merge(df_teams_lose_min, on=['Season', 'team_id'], how='left', left_index=False, right_index=False)

    return df


def extract_season_teams_score(df_tourney, tourney_name):
    """
        Extract every seasons teams scores
            - teams mean score
            - teams max
            - teams min
    """
    df_season_teams_mean_score = extract_season_teams_mean_score(df_tourney, tourney_name)

    return df_season_teams_mean_score

def concat_all_games(df_ncaa, df_regular, df_secondary):
    """
        concat all games
    """
    print('Concat all games...')
    year_limit = 2015
    WLoc = {'A': 1, 'H': 2, 'N': 3}
    SecondaryTourney = {'NIT': 1, 'CBI': 2, 'CIT': 3, 'V16': 4, 'Regular': 5 ,'NCAA': 6}
    drop_cols = ['Season', 'SecondaryTourney', 'WLoc', 'id', 'teams_id', 'WTeamID', 'LTeamID', 'WScore', 'LScore', 'DayNum', 'NumOT', 'win_loc']

    df_ncaa['SecondaryTourney'] = 'NCAA'
    df_regular['SecondaryTourney'] = 'Regular'

    df_games = pd.concat([df_ncaa, df_regular], axis=0, ignore_index=True)
    df_games = pd.concat([df_games, df_secondary], axis=0, ignore_index=True)
    df_games = df_games[df_games['Season'] > 2014]

    df_games['team_1'] = df_games[['WTeamID', 'LTeamID']].apply(lambda x: x[0] if x[0] < x[1] else x[1], axis=1)
    df_games['team_2'] = df_games[['WTeamID', 'LTeamID']].apply(lambda x: x[0] if x[0] > x[1] else x[1], axis=1)
    df_games['id'] = df_games[['Season', 'team_1', 'team_2']].apply(lambda x: '_'.join(map(str, x)) , axis=1)
    df_games['teams_id'] = df_games[['team_1', 'team_2']].apply(lambda x: '_'.join(map(str, x)) , axis=1)
    df_games['result'] = df_games[['team_1', 'WTeamID']].apply(lambda x: 1.0 if x[0] == x[1] else -1.0, axis=1)
    df_games['win_loc'] = df_games['WLoc'].map(WLoc)
    df_games['tourney_type'] = df_games['SecondaryTourney'].map(SecondaryTourney)
    df_games['team_1_loc'] = df_games[['team_1', 'WTeamID', 'win_loc']].apply(
        lambda x: 3 if x[2] == 3 else (2 if x[0] == x[1] else 1), axis=1)

    df_teams_ncaa_mean = extract_season_teams_mean_score(df_ncaa[df_ncaa['Season'] > year_limit], 'ncaa')
    df_teams_regular_mean = extract_season_teams_mean_score(df_regular[df_regular['Season'] > year_limit], 'regular')
    df_teams_secondary_mean = extract_season_teams_mean_score(df_secondary[df_secondary['Season'] > year_limit], 'secondary')

    df_games = df_games.merge(df_teams_ncaa_mean.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_ncaa_mean.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.merge(df_teams_regular_mean.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_regular_mean.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.merge(df_teams_secondary_mean.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_secondary_mean.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    ########
    df_teams_ncaa_max = extract_season_teams_max_score(df_ncaa[df_ncaa['Season'] > year_limit], 'ncaa')
    df_teams_regular_max = extract_season_teams_max_score(df_regular[df_regular['Season'] > year_limit], 'regular')
    df_teams_secondary_max = extract_season_teams_max_score(df_secondary[df_secondary['Season'] > year_limit], 'secondary')

    df_games = df_games.merge(df_teams_ncaa_max.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_ncaa_max.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.merge(df_teams_regular_max.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_regular_max.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.merge(df_teams_secondary_max.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_secondary_max.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    ##########
    df_teams_ncaa_min = extract_season_teams_min_score(df_ncaa[df_ncaa['Season'] > year_limit], 'ncaa')
    df_teams_regular_min = extract_season_teams_min_score(df_regular[df_regular['Season'] > year_limit], 'regular')
    df_teams_secondary_min = extract_season_teams_min_score(df_secondary[df_secondary['Season'] > year_limit], 'secondary')

    df_games = df_games.merge(df_teams_ncaa_min.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_ncaa_min.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.merge(df_teams_regular_min.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_regular_min.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.merge(df_teams_secondary_min.rename(columns={'team_id': 'team_1'}), on=['Season', 'team_1'], how='left')
    df_games = df_games.merge(df_teams_secondary_min.rename(columns={'team_id': 'team_2'}), on=['Season', 'team_2'], how='left', suffixes=['', '_team_2'])

    df_games = df_games.drop(drop_cols, axis=1).fillna(0.0)

    return df_games
