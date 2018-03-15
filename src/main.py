import os

import pandas as pd
import numpy as np
import xgboost as xgb

from sklearn.linear_model import LogisticRegression, LinearRegression, Lasso
from sklearn.metrics import log_loss

from submission_transform import normalize_submission, generate_submission
from feature_extraction import extract_season_teams_score, concat_all_games
from feature_mixin import merge_teams_score_to_games
from result_generation import get_season_ncaa_teams_played_result

parent_dir = os.path.join(os.path.dirname(__file__), '..')
dataset_dir = parent_dir + '/dataset'
result_dir = parent_dir + '/results'

regular_compact_results_path = dataset_dir + '/DataFiles/RegularSeasonCompactResults.csv'
ncaa_compact_results_path = dataset_dir + '/DataFiles/NCAATourneyCompactResults.csv'
secondary_compact_results_path = dataset_dir + '/DataFiles/SecondaryTourneyCompactResults.csv'

sample_submission_stage1_path = parent_dir + '/SampleSubmissionStage1.csv'
sample_submission_stage2_path = parent_dir + '/SampleSubmissionStage2.csv'

# Random 0.45 - 0.55 got logloss 0.694075
# Sample 0.5 got logloss 0.693147
# def testing_pred_random(df_sub):
#     """
#         Generate a random Pred result
#         !! Just a joke
#     """
#     df_result = pd.DataFrame({})

#     df_result['ID'] = df_sub['ID']
#     df_result['Pred'] = np.random.random_sample((len(df_sub),)) * 0.1 + 0.45


#     df_result.to_csv(result_dir + '/random_pred.csv', index=False)

#     return df_result


def main():
    """
        Main entry
    """
    df_regular_compact_results = pd.read_csv(regular_compact_results_path)
    df_ncaa_compact_results = pd.read_csv(ncaa_compact_results_path)
    df_secondary_compact_results = pd.read_csv(secondary_compact_results_path)

    df_all_games = concat_all_games(df_ncaa_compact_results, df_regular_compact_results, df_secondary_compact_results)

    # X_test = generate_test(df_all_games)
    # df_all_games = df_all_games[(df_all_games['Season'] == 2018) & (df_all_games['tourney_type'] == 6)]
    # print(df_all_games)
    df_all_games_result_count = df_all_games.groupby(['team_1', 'team_2'])['result'].count().reset_index().rename(columns={'result': 'game_count'})
    df_all_games_result_sum = df_all_games.groupby(['team_1', 'team_2'])['result'].sum().reset_index().rename(columns={'result': 'game_sum'})
    df_all_games_result = df_all_games_result_count.merge(df_all_games_result_sum, how='left', on=['team_1', 'team_2'])
    df_all_games_result['team_1_prob'] = df_all_games_result[['game_count', 'game_sum']].apply(lambda x: 0.5 if x[0] == 0 else ((x[1] + x[0]) / (x[0] * 2)), axis=1)

    # print(df_all_games_result['team_1_prob'])

    df_all_games = df_all_games.merge(df_all_games_result, on=['team_1', 'team_2'], how='left')

    print(df_all_games)

    y = df_all_games['team_1_prob']
    X = df_all_games.drop(['team_1_prob', 'result'], axis=1)

    xgb_params = {
      'eta': 0.05,
      'max_depth': 3,
      'subsample': 0.98,
      'objective': 'binary:logistic',
      'eval_metric': 'logloss',
      # 'base_score': y_mean, # base prediction = mean(target)
      'silent': 1
    }

    dtrain = xgb.DMatrix(X, y)

    cv_result = xgb.cv(xgb_params,
      dtrain,
      num_boost_round=10000,
      early_stopping_rounds=50,
      verbose_eval=50,
      show_stdv=False
    )

    num_boost_rounds = len(cv_result)
    print('num_boost_rounds=' + str(num_boost_rounds))

    model = xgb.train(dict(xgb_params, silent=1), dtrain, num_boost_round=num_boost_rounds)

    y_pred_train = model.predict(dtrain)
    df_result = pd.DataFrame({})

    df_result['team_1'] = df_all_games['team_1']
    df_result['team_2'] = df_all_games['team_2']
    df_result['ID'] = df_result[['team_1', 'team_2']].apply(lambda x: '_'.join(map(str, ['2018', x[0], x[1]])), axis=1)

    df_result['Pred'] = y_pred_train

    df_result = df_result.drop(['team_1', 'team_2'], axis=1)

    df_result = df_result.groupby(['ID'])['Pred'].mean().reset_index()


    df_sub = pd.read_csv(sample_submission_stage2_path)
    df_sub = df_sub.drop(['Pred'], axis=1)


    df_sub = df_sub.merge(df_result, on=['ID'], how='left')

    df_sub = df_sub.fillna(0.5)

    df_sub.to_csv(result_dir + '/xgb_result.csv', index=False)

    # logloss = log_loss(y, y_pred_train)
    # print('logloss = {0:.4f}'.format(logloss))

    # y = list(y[:])
    # print(list(y[:]))

    # reg = LogisticRegression(random_state=42)
    # reg = LinearRegression()
    # # reg = Lasso(alpha=0.1)
    # reg.fit(X, y)

    # score = reg.score(X, y)
    # print('accuracy score {:0.4f}'.format(score))
    # x_pred = reg.predict(X)
    # print(x_pred)
    # logloss = log_loss(y, x_pred)
    # print('logloss = {0:.4f}'.format(logloss))


if __name__ == '__main__':
    main()
    # tp = (1, 2)
    # print(tp[0])
