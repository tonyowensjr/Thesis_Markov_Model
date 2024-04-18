from constants import *

import argparse
import numpy as np
import pandas as pd
import zipfile

def prepare_bash_df(df):
    df['end_play_outs'] = (df['EVENT_OUTS_CT'] + df['OUTS_CT'])
    df['date'] = pd.to_datetime(df.GAME_ID.str[3:7] + '-' + df.GAME_ID.str[7:9] + '-' + df.GAME_ID.str[9:11])
    df['year'] = df.GAME_ID.str[3:7].astype(int)
    df['home_team'] = df.GAME_ID.str[:3]

    # df['batting_team'] = (df['home_team'] * df['BAT_HOME_ID']) + (df['AWAY_TEAM_ID'] * (1 - df['BAT_HOME_ID']))
    df['batting_team'] = df['BAT_HOME_ID']
    df['pitching_team'] = (df['home_team'] * (1 - df['BAT_HOME_ID'])) + (df['AWAY_TEAM_ID'] * df['BAT_HOME_ID'])
    df['end_game'] = df['GAME_END_FL'] == 'T'

    df['runs_scored'] = np.sum((df[['RUN1_DEST_ID', 'RUN2_DEST_ID',
        'RUN3_DEST_ID','BAT_DEST_ID']] > 3),axis=1)

    df['runs_scored_exp'] = np.sum((df[['RUN1_DEST_ID', 'RUN2_DEST_ID',
        'RUN3_DEST_ID','BAT_DEST_ID']] > 3),axis=1)

    df['event_category'] = df['EVENT_CD'].map(EVENT_DICT)
    df.loc[(df.DP_FL == 'T'),'event_category'] = 'Double Play'
    df.loc[(df.TP_FL == 'T'),'event_category'] = 'Triple Play'

    df['start_state'] = df['OUTS_CT'].astype(str) + ':' + df['BASE1_RUN_ID'].notnull().astype(int).astype(str) +\
':' + df['BASE2_RUN_ID'].notnull().astype(int).astype(str) + ':' + df['BASE3_RUN_ID'].notnull().astype(int).astype(str)

    df['BASE1_DEST'] = (df['BAT_DEST_ID'] == 1) ^ (df['RUN1_DEST_ID'] == 1) \
        ^ (df['RUN2_DEST_ID'] == 1) ^ (df['RUN3_DEST_ID'] == 1)
    df['BASE2_DEST'] = (df['BAT_DEST_ID'] == 2) ^ (df['RUN1_DEST_ID'] == 2) \
        ^ (df['RUN2_DEST_ID'] == 2) ^ (df['RUN3_DEST_ID'] == 2)
    df['BASE3_DEST'] = (df['BAT_DEST_ID'] == 3) ^ (df['RUN1_DEST_ID'] == 3) \
        ^ (df['RUN2_DEST_ID'] == 3) ^ (df['RUN3_DEST_ID'] == 3)

    df['end_state'] = (df['end_play_outs'] != 3) * (df['end_play_outs'].astype(str) + ':' + df['BASE1_DEST'].astype(int).astype(str) +\
':' + df['BASE2_DEST'].astype(int).astype(str) + ':' + df['BASE3_DEST'].astype(int).astype(str))

    df['pre_state'] = df['start_state'].map(STATE_MAP)
    df['post_state'] = df['end_state'].map(STATE_MAP)
    df['post_state2'] = df.post_state + (25 * df.runs_scored)

    df['post_state3'] = df.post_state
    df.loc[(df.post_state == 25) & (df.runs_scored == 1),'post_state3'] = 26
    df.loc[(df.post_state == 25) & (df.runs_scored == 2),'post_state3'] = 27
    df.loc[(df.post_state == 25) & (df.runs_scored == 3),'post_state3'] = 28


    df['pre_state_cat'] = pd.Categorical(df['pre_state'],categories=range(1,26),ordered=True)
    df['post_state_cat'] = pd.Categorical(df['post_state'],categories=range(1,26),ordered=True)
    df['post_state2_cat'] = pd.Categorical(df['post_state2'],categories=range(1,126),ordered=True)
    df['post_state3_cat'] = pd.Categorical(df['post_state3'],categories=range(1,29),ordered=True)

    df['transition'] = df['pre_state'].astype(str) + df['post_state'].astype(str)

    new_cols = {'BAT_ID':'batter_id','PIT_ID':'pitcher_id','AWAY_TEAM_ID':'vis_team','BAT_HAND_CD':'batter_hand',
 'PIT_HAND_CD':'pitcher_hand','EVENT_CD':'event_scoring','EVENT_ID':'event_id','GAME_ID':'game_id','INN_CT':'inning'}

    df.columns = [x if x not in new_cols.keys() else new_cols[x] for x in df.columns]

    df.batter_hand = df.batter_hand.str.lower()
    df.pitcher_hand = df.pitcher_hand.str.lower()   

    return df

def bash_load(start_year:int,end_year:int,create=False):
    if create:
        for year in range(start_year,end_year+1):
            with zipfile.ZipFile(f'/eve_files/{year}eve.zip', 'r') as zip_ref:
                zip_ref.extractall(f'/eve_files/{year}eve')
    col_names = pd.read_csv("http://bayesball.github.io/baseball/fields.csv").Header
    pbp_df_full = pd.concat([pd.read_csv('/Users/tonyowens/Downloads/{year}eve/all{year}.csv'.format(year=x),
                                     header=None,
                                     names=col_names,low_memory=False) \
                                        for x in range(start_year,end_year+1)])
    df = prepare_bash_df(pbp_df_full)

    return df[BASH_COLS]


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument('--start_year', type=int, default=1963,
                        help='The year to start the data collection')
    parser.add_argument('--end_year', type=int, default=2023,
                        help='The year to end the data collection')
    parser.add_argument('--train', type=bool, default=False,
                        help="Indicate whether the model pertains to training \
                            data for the Neural Network")
    start_year = parser.parse_args().start_year
    end_year = parser.parse_args().end_year
    train = parser.parse_args().train

    data = bash_load(start_year,end_year)

    if train:
        data.to_csv('data/train_data.csv')
        data.to_pickle('data/train_data.pkl')
    else:
        data.to_csv('data/bash_data.csv')
        data.to_pickle('data/bash_data.pkl')

if __name__ == '__main__':
    main()
