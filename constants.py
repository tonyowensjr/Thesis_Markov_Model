########################################################################################
# The map to go from the out and runner code to the state
STATE_MAP = {'0:0:0:0':1,'0:1:0:0':2,'0:0:1:0':3,'0:0:0:1':4,'0:1:1:0':5,'0:1:0:1':6,
             '0:0:1:1':7,'0:1:1:1':8,'1:0:0:0':9,'1:1:0:0':10,'1:0:1:0':11,'1:0:0:1':12,
             '1:1:1:0':13,'1:1:0:1':14,'1:0:1:1':15,'1:1:1:1':16,'2:0:0:0':17,
             '2:1:0:0':18,'2:0:1:0':19,'2:0:0:1':20,'2:1:1:0':21,'2:1:0:1':22,
             '2:0:1:1':23,'2:1:1:1':24,'':25}

########################################################################################
# The columns to compare the current at bat to the past at bats
SHIFT_COLS = ['home_score_ct','away_score_ct','game_id','inn_ct','game_new_fl',
              'game_end_fl','base1_run_id', 'base2_run_id', 'base3_run_id',
              'bat_home_id','end_play_outs']

########################################################################################
# The columns to compare the current at bat to the past at bats
SHIFT_COLS_2 = ['home_score','vis_score','game_id','inning','start_game',
                'end_game','run_1b', 'run_2b', 'run_3b',
              'batting_team','end_play_outs']

########################################################################################
# The path of the retrosheet play by play data by year
# RETROSHEET_PATH = 'retrosheet_files'
RETROSHEET_PATH = 'retrosheet_output'
########################################################################################
# The map to map event codes to what the event represents
EVENT_DICT = { 
    0: "Unknown event", 1: "No event", 2: "Generic out", 3: "Strikeout",
    4: "Stolen base", 5: "Defensive indifference", 6: "Caught stealing", 
    7: "Pickoff error", 8: "Pickoff", 9: "Wild pitch", 10: "Passed ball",
    11: "Balk", 12: "Other advance",13: "Foul error", 14: "Walk",
    15: "Intentional walk", 16: "Hit by pitch", 17: "Interference", 18: "Error",
    19: "Fielder's choice", 20: "Single", 21: "Double", 22: "Triple", 23: "Home run",
    24: "Missing play" }

########################################################################################
# The map to map retrosheet team names to more readable team names
TEAM_ABRVS = {'KCA': 'KC', 'ANA': 'LAA', 'OAK': 'OAK', 'TEX': 'TEX','DET': 'DET','SEA': 'SEA',
 'HOU': 'HOU','CIN': 'CIN','TBA': 'TBR','MIN': 'MIN','NYA': 'NYY','BOS': 'BOS','CLE': 'CLE',
 'BAL': 'BAL','CHA': 'CHW','TOR': 'TOR','MIL': 'MIL','PIT': 'PIT','SLN': 'STL','SDN': 'SD',
 'COL': 'COL','LAN': 'LAD','SFN': 'SFG','ARI': 'ARI','CHN': 'CHC','PHI': 'PHI','ATL': 'ATL',
 'MIA': 'MIA','NYN': 'NYM','WAS': 'WAS'}

########################################################################################
# The map to map Retrosheet team names to full team names
TEAM_FULL_NAMES = {'KCA': 'Kansas City Royals','ANA': 'Los Angeles Angels','OAK': 'Oakland Athletics',
 'TEX': 'Texas Rangers','DET': 'Detroit Tigers','SEA': 'Seattle Mariners','HOU': 'Houston Astros',
 'CIN': 'Cincinnati Reds','TBA': 'Tampa Bay Rays','MIN': 'Minnesota Twins','NYA': 'New York Yankees',
 'BOS': 'Boston Red Sox','CLE': 'Cleveland Guardians','BAL': 'Baltimore Orioles','CHA': 'Chicago White Sox',
 'TOR': 'Toronto Blue Jays','MIL': 'Milwaukee Brewers','PIT': 'Pittsburgh Pirates','SLN': 'St. Louis Cardinals',
 'SDN': 'San Diego Padres','COL': 'Colorado Rockies','LAN': 'Los Angeles Dodgers','SFN': 'San Francisco Giants',
 'ARI': 'Arizona Diamondbacks','CHN': 'Chicago Cubs','PHI': 'Philadelphia Phillies','ATL': 'Atlanta Braves',
 'MIA': 'Miami Marlins','NYN': 'New York Mets','WAS': 'Washington Nationals'}

########################################################################################
# The outcomes which do not result in the completion of an at bat
NON_AB_OUTCOMES = ['Caught stealing','Stolen base','Wild pitch','Pickoff',
                    'Foul error',"['Double' 'Generic out']",'Defensive indifference','Balk','Other advance','Interference',
                    'Passed Ball']
########################################################################################
# The outcomes which result in a hit
HITS = ['Single','Double','Triple','Home run']

########################################################################################
# The outcomes which result in a hit or a walk
HIT_OR_WALK = ['Single','Double','Triple','Home run','Walk','Intentional walk','Passed ball']

########################################################################################
# The columns to keep for the output csv or pkl file
FIN_COLS = ['game_id',
 'date',
 'year',
 'batter_name',
 'pitcher_name',
 'away_team_id',
 'bat_home_id',
 'bat_id',
 'bat_hand_cd',
 'pit_id',
 'pit_hand_cd',
 'game_end_fl',
 'event_tx',
 'runs_scored_exp',
 'pre_state',
 'post_state',
 'event_category',
 'date_num']

########################################################################################
# The columns to keep for the output csv or pkl file
FIN_COLS_2 = ['game_id',
 'date',
 'year',
 'batter_name',
 'pitcher_name',
 'vis_team',
 'batting_team',
 'batter_id',
 'batter_hand',
 'pitcher_id',
'pitcher_hand',
 'end_game',
 'event_scoring',
 'runs_scored_exp',
 'pre_state',
 'post_state',
 'transition',
 'event_category',
 'date_num']

########################################################################################
# The columns to keep for the output csv or pkl file
FIN_COLS_3 = ['game_id',
 'date',
 'year',
 'batter_name',
 'pitcher_name',
 'vis_team',
 'batting_team',
 'batter_id',
 'batter_hand',
 'pitcher_id',
'pitcher_hand',
 'end_game',
 'event_scoring',
 'runs_scored',
 'pre_state',
 'post_state',
 'post_state2',
 'post_state3',
 'event_id',
 'transition',
 'event_category',
 'pre_state_cat',
 'post_state_cat',
 'post_state2_cat',
 'post_state3_cat']

########################################################################################
# The columns used in the bash dataframe
BASH_COLS = ['game_id', 'vis_team', 'batter_id','inning', 'batter_hand', 'pitcher_id', 'pitcher_hand', 
  'event_scoring', 'event_id', 'date', 'year', 'batting_team', 'end_game', 'runs_scored',
    'event_category', 'pre_state', 'post_state', 'post_state2', 'post_state3', 'pre_state_cat', 
    'post_state_cat', 'post_state2_cat', 'post_state3_cat']

########################################################################################
# The columns used to calculate the transition probabilities
TRANSITION_COLS = ['pre_state','post_state','year','batter_id','pitcher_id']

########################################################################################
# The path to for the results of the games
RESULTS_PATH = 'full_retro_files/retrosheets_game_log_teams.csv'

########################################################################################
# The path to for the results of the games
GAME_RESULTS_PATH = 'data/game_results.csv'

########################################################################################
# All retro sheet columns
ALL_RETROSHEET_COLUMNS = ['game_id', 'date', 'event_id', 'batting_team', 'inning', 
                          'outs', 'balls', 'strikes', 'pitch_seq', 'vis_score', 
                          'home_score', 'batter_id', 'batter_hand', 'result_batter_id',
   'result_batter_hand', 'pitcher_id', 'pitcher_hand', 'result_pitcher_id', 
   'result_pitcher_hand', 'def_c', 'def_1b', 'def_2b', 'def_3b', 'def_ss', 'def_lf',
   'def_cf', 'def_rf', 'run_1b', 'run_2b', 'run_3b', 'event_scoring', 'leadoff',
     'pinch_hit', 'batt_def_pos', 'batt_lineup_pos', 'event_type', 'batter_event', 
     'ab', 'hit_val', 'sac_hit', 'sac_fly', 'event_outs', 'dp', 'tp', 'rbi', 
     'wild_pitch','passed_ball', 'fielded_by', 'batted_ball_type', 'bunt', 
     'foul_ground', 'hit_location', 'num_err', 'err_player_1', 
     'err_type_1', 'err_player_2', 'err_type_2', 'err_player_3', 'err_type_3', 
     'batt_dest', 'run_1b_dest', 'run_2b_dest', 'run_3b_dest', 
     'play_on_run_batt', 'play_on_run_1b','play_on_run_2b', 'play_on_run_3b',
       'sb_run_1b', 'sb_run_2b', 'sb_run_3b', 'cs_run_1b', 'cs_run_2b', 
       'cs_run_3b', 'pickoff_run_1b', 'pickoff_run_2b',
           'pickoff_run_3b', 'run_1b_resp_pitcher', 'run_2b_resp_pitcher', 
           'run_3b_resp_pitcher', 'start_game', 'end_game', 'pinch_run_1b', 
           'pinch_run_2b', 'pinch_run_3b', 'pinch_run_1b_player_removed', 
           'pinch_run_2b_player_removed', 'pinch_run_3b_player_removed', 
           'pinch_hit_batter_removed_id', 'pinch_hit_batter_removed_field_pos', 
           'putout1_field_pos', 'putout2_field_pos', 'putout3_field_pos', 
           'assist1_field_pos', 'assist2_field_pos', 'assist3_field_pos', 
           'assist4_field_pos', 'assist5_field_pos', 'pit_id', 'pit_last_name', 
           'pit_first_name', 'bat_id', 'bat_last_name', 'bat_first_name', 'id',
             'home_team', 'vis_team', 'end_play_outs', 'shift_home_score', 
             'shift_vis_score', 'shift_game_id', 'shift_inning', 'shift_start_game',
               'shift_end_game', 'shift_run_1b', 'shift_run_2b', 'shift_run_3b', 
               'shift_batting_team', 'shift_end_play_outs', 'same_inning', 'start_1',
                 'start_2', 'start_3', 'end_1', 'end_2', 'end_3', 'end_1_exp', 
                 'end_2_exp', 'end_3_exp', 'runs_scored', 'runs_scored_exp', 
                 'start_state','end_state', 'pre_state', 'post_state',
                   'transition', 'is_dp', 'is_tp', 'dp_or_tp', 'is_dp_or_tp',
                     'event_category', 'date_num','batter_name', 
                     'pitcher_name', 'year']

BET_TO_RET = {'KAN':'KCA',
 'LAA':'ANA',
 'TAM':'TBA',
 'NYY':'NYA',
 'CWS':'CHA',
 'STL':'SLN',
 'SDG':'SDN',
 'LAD':'LAN',
 'SFO':'SFN',
 'CHC':'CHN',
 'NYM':'NYN',
 }

########################################################################################
# creating the run transition dictionary
RUN_DICT = {
    1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    2: [2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    3: [2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    4: [2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    5: [3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    6: [3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    7: [3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    8: [4, 3, 3, 3, 2, 2, 2, 1, 3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    9: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    10: [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    11: [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    12: [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    13: [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    14: [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    15: [0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    16: [0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 3, 3, 2, 2, 2, 1, 3, 2, 2, 2, 1, 1, 1, 0, 0, 1, 2],
    17: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    18: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    19: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    20: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    21: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 1, 1, 1, 0, 0, 1, 2],
    22: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 1, 1, 1, 0, 0, 1, 2],
    23: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 1, 1, 1, 0, 0, 1, 2],
    24: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 3, 3, 2, 2, 2, 1, 0, 1, 2, 3]
}
