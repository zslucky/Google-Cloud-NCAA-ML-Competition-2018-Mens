import pandas as pd

def normalize_submission(df_sub):
    """
        Normalize submission df to compute-able data
    """
    df = pd.DataFrame({})

    df['season'] = df_sub['ID'].apply(lambda x: str(x.split('_')[0])).astype(int)
    df['team_1'] = df_sub['ID'].apply(lambda x: str(x.split('_')[1])).astype(int)
    df['team_2'] = df_sub['ID'].apply(lambda x: str(x.split('_')[2])).astype(int)

    return df

def generate_submission(df_sub, df_result):
    """
        Generate submission dataframe
    """
    df = pd.DataFrame({})

    df['ID'] = df_sub[['season', 'team_1', 'team_2']].apply(lambda x: x.join('_'), axis=1)
    df['pred'] = df_result

    return df
