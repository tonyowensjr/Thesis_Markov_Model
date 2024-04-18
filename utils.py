from typing import Tuple

import math
import numpy as np
import pandas as pd
import polars as pl

def create_lineup_pl(data:pl.DataFrame, game:str = None) -> Tuple[list]:
    """
    Return the lineups for a given game based on the provided data.

    Args:
        data (pl.DataFrame): The data containing the game information.
        game (str, optional): The game ID. If provided, the lineup will be created for this specific game. 
                              If not provided, the lineup will be created for all games in the data.

    Returns:
        Tuple[list]: A tuple containing the home lineup and away lineup as lists of batter IDs.
    """
        
    if game != None:
        game_data = data.filter(pl.col("game_id") == game)
    else:
        game_data = data.__copy__()

    away_lineup = np.concatenate(game_data.filter(pl.col("batting_team") == False).select("batter_id").unique(maintain_order=True)[:9].to_numpy())
    home_lineup = np.concatenate(game_data.filter(pl.col("batting_team") == True).select("batter_id").unique(maintain_order=True)[:9].to_numpy())
    return home_lineup, away_lineup

def run_probs_pl(data:pl.DataFrame) -> dict:
    """
    Calculate the probability of runs scored based on pre-state, post-state, and expected runs scored.

    Args:
        data (pl.DataFrame): A DataFrame containing the data with columns 'pre_state', 'post_state', and 'runs_scored_exp'.

    Returns:
        dict: A dictionary containing the probabilities of runs scored for each combination of pre-state, post-state, and expected runs scored.
    """

    run_vals = data.group_by(['pre_state', 'post_state', 'runs_scored_exp']).agg([pl.count().alias('Frequency')]).to_numpy()
    run_vv = np.array([{} for _ in range(2526)])
    for val in run_vals:
        ind = int(val[0] * 10**(int(math.log(val[1],10) + 1)) + val[1])
        run_vv[ind][val[2]] = val[3]
    for row in range(2526):
        if run_vv[row] == {}:
            continue
        else:
            run_vv[row] = dict(zip(run_vv[row].keys(),np.array(list(run_vv[row].values()))/np.array(list(run_vv[row].values())).sum()))

    fin_dict = {str(x):int(list(run_vv[x].keys())[np.argmax(np.array(list(run_vv[x].values())))]) for x in range(run_vv.shape[0]) if run_vv[x] != {}}
    return fin_dict

def create_transition_probs_pl(data:pl.DataFrame,batter_id:str=  None, pitcher_id:str = None,one_year = None,
                               pitcher_hand:str = None,normalize:bool = True,batter_hand:str = None) -> Tuple[np.ndarray,dict]:
    """
    Create transition probabilities matrix and pre-state count dictionary based on the given data.

    Args:
        data (pl.DataFrame): The input data.
        batter_id (str, optional): The batter ID to filter the data. Defaults to None.
        pitcher_id (str, optional): The pitcher ID to filter the data. Defaults to None.
        one_year (int, optional): The year to filter the data. Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: A tuple containing the transition probabilities matrix and the pre-state count dictionary.
    """

    new_data = data.__copy__()
    if one_year != None:
        new_data = new_data.filter(pl.col("year") == one_year)
    if batter_id != None:
        new_data = new_data.filter(pl.col("batter_id") == batter_id)
    if pitcher_id != None:
        new_data = new_data.filter(pl.col("pitcher_id") == pitcher_id)
    if pitcher_hand != None:
        new_data = new_data.filter(pl.col("pitcher_hand") == pitcher_hand)
    if batter_hand != None:
        new_data = new_data.filter(pl.col("batter_hand") == batter_hand)
    trans_probs = np.zeros([25,25])
    array_vals = new_data.group_by(['pre_state', 'post_state']).agg([
    pl.col('runs_scored_exp').count().alias('Count')]).sort(by=['pre_state', 'post_state']).to_numpy()
    for val in array_vals:
        row = val[0]
        col = val[1]
        trans_probs[row-1,col-1] = val[2]
    pre_state_num = dict(zip(range(1,25),np.int32(trans_probs.sum(axis=1)[:-1])))

    return trans_probs,pre_state_num

def create_transition_row_pl(data:pl.DataFrame,batter_id:str=  None, pitcher_id:str = None,
                               pitcher_hand:str = None,batter_hand:str = None) -> np.ndarray:
    """
    Create transition probabilities row given the starting state based on the given data.

    Args:
        data (pl.DataFrame): The input data.
        batter_id (str, optional): The batter ID to filter the data. Defaults to None.
        pitcher_id (str, optional): The pitcher ID to filter the data. Defaults to None.
        one_year (int, optional): The year to filter the data. Defaults to None.

    Returns:
        np.ndarray : A np array containing the output array.
    """
    # Combine filters into a single expression
    # Start with the full DataFrame

    # Apply filters conditionally
    if batter_id is not None:
        data = data.filter(pl.col("batter_id") == batter_id)
    if pitcher_id is not None:
        data = data.filter(pl.col("pitcher_id") == pitcher_id)
    if pitcher_hand is not None:
        data = data.filter(pl.col("pitcher_hand") == pitcher_hand)
    if batter_hand is not None:
        data = data.filter(pl.col("batter_hand") == batter_hand)

    # Aggregation
    grouped_data = data.group_by('post_state').agg(pl.count().alias('Frequency'))
    vals = grouped_data.to_numpy()

    trans_probs = np.zeros(25)
    vals = data.group_by('post_state').agg([
    pl.count().alias('Frequency')]).to_numpy()
    for val in vals:
        trans_probs[val[0]-1] = val[1]
    return trans_probs

def outcome_pl(data:pl.DataFrame) -> np.ndarray:
    outcome_dict = {str(i):[] for i in range(2526)}
    ind_dict = {str(i):[] for i in range(2526)}
    for val in data.group_by(['pre_state', 'post_state','event_category']).agg([pl.count().alias('Frequency')]).to_numpy():
        ind = str(int(val[0] * 10**(int(math.log(val[1],10) + 1)) + val[1]))
        outcome_dict[ind].append(val[2])
        ind_dict[ind].append(val[3])
    return outcome_dict,ind_dict

def probability_to_american_odds(success,fails):
    probability = success / (success + fails)
    if probability <= 0 or probability >= 1:
        raise ValueError('Probability must be between 0 and 1 (exclusive).')
    
    if probability > 0.5:
        # For favorites (probability > 50%)
        odds = -((probability * 100) / (1 - probability))
    else:
        # For underdogs (probability < 50%)
        odds = (100 - (probability * 100)) / probability
    
    return int(round(odds))

def prob_to_am(probability):
    if probability < 0 or probability > 1:
        raise ValueError('Probability must be between 0 and 1.')

    if probability == 0.5:
        return '+100'
    elif probability < 0.5:
        # Underdog
        american_odds = (100 / probability) - 100
        return f'+{int(american_odds)}'
    else:
        # Favorite
        american_odds = -100 / (1 - probability)
        return f'{int(american_odds)}'
    
def add_ending(number):
    # Convert number to string for easy manipulation
    num_str = str(number)
    # Handle special cases for 11th, 12th, and 13th
    if 10 <= number % 100 <= 13:
        return num_str + 'th'
    # Assign the ordinal ending based on the last digit of the number
    elif num_str.endswith('1'):
        return num_str + 'st'
    elif num_str.endswith('2'):
        return num_str + 'nd'
    elif num_str.endswith('3'):
        return num_str + 'rd'
    else:
        return num_str + 'th'
    
def home_win_p(home_odds, away_odds):
    # Calculate the implied probability for the home team
    if home_odds > 0:
        home_implied_probability = 100 / (home_odds + 100)
    else:
        home_implied_probability = -home_odds / (-home_odds + 100)
    
    # Calculate the implied probability for the away team
    if away_odds > 0:
        away_implied_probability = 100 / (away_odds + 100)
    else:
        away_implied_probability = -away_odds / (-away_odds + 100)
    
    # Calculate the market's total implied probability (including vig)
    market_implied_probability = home_implied_probability + away_implied_probability
    
    # Remove the vig and calculate the true implied probability for the home team
    true_home_implied_probability = home_implied_probability / market_implied_probability
    
    return round(true_home_implied_probability, 4)

def create_transition_probs_pl_new(data:pl.DataFrame,batter_id:str=  None, pitcher_id:str = None,one_year = None,
                               pitcher_hand:str = None,normalize:bool = True,batter_hand:str = None) -> Tuple[np.ndarray,dict]:
    """
    Create transition probabilities matrix and pre-state count dictionary based on the given data.

    Args:
        data (pl.DataFrame): The input data.
        batter_id (str, optional): The batter ID to filter the data. Defaults to None.
        pitcher_id (str, optional): The pitcher ID to filter the data. Defaults to None.
        one_year (int, optional): The year to filter the data. Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: A tuple containing the transition probabilities matrix and the pre-state count dictionary.
    """

    new_data = data.__copy__()
    if one_year != None:
        new_data = new_data.filter(pl.col("year") == one_year)
    if batter_id != None:
        new_data = new_data.filter(pl.col("batter_id") == batter_id)
    if pitcher_id != None:
        new_data = new_data.filter(pl.col("pitcher_id") == pitcher_id)
    if pitcher_hand != None:
        new_data = new_data.filter(pl.col("pitcher_hand") == pitcher_hand)
    if batter_hand != None:
        new_data = new_data.filter(pl.col("batter_hand") == batter_hand)
    trans_probs = np.zeros([25,125])
    array_vals = new_data.group_by(['pre_state', 'post_state2']).agg([
    pl.col('runs_scored').count().alias('Count')]).sort(by=['pre_state', 'post_state2']).to_numpy()
    for val in array_vals:
        row = val[0]
        col = val[1]
        trans_probs[row-1,col-1] = val[2]
    pre_state_num = dict(zip(range(1,25),np.int32(trans_probs.sum(axis=1)[:-1])))
    return trans_probs,pre_state_num

def outcome_pl_new(data:pl.DataFrame) -> np.ndarray:
    outcome_dict = {str(i)+'_'+str(j):[] for i in range(1,26) for j in range(1,126)}
    ind_dict = {str(i)+'_'+str(j):[] for i in range(1,26) for j in range(1,126)}
    for val in data.group_by(['pre_state', 'post_state2','event_category']).agg([pl.len().alias('Frequency')]).to_numpy():
        ind = str(val[0]) + '_' + str(val[1])
        outcome_dict[ind].append(val[2])
        ind_dict[ind].append(val[3])
    return outcome_dict,ind_dict

def create_transition_probs_pl_new_2(data:pl.DataFrame,batter_id:str=  None, pitcher_id:str = None,one_year = None,
                               pitcher_hand:str = None,normalize:bool = True,batter_hand:str = None) -> Tuple[np.ndarray,dict]:
    """
    Create transition probabilities matrix and pre-state count dictionary based on the given data.

    Args:
        data (pl.DataFrame): The input data.
        batter_id (str, optional): The batter ID to filter the data. Defaults to None.
        pitcher_id (str, optional): The pitcher ID to filter the data. Defaults to None.
        one_year (int, optional): The year to filter the data. Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: A tuple containing the transition probabilities matrix and the pre-state count dictionary.
    """

    new_data = data.__copy__()
    if one_year != None:
        new_data = new_data.filter(pl.col("year") == one_year)
    if batter_id != None:
        new_data = new_data.filter(pl.col("batter_id") == batter_id)
    if pitcher_id != None:
        new_data = new_data.filter(pl.col("pitcher_id") == pitcher_id)
    if pitcher_hand != None:
        new_data = new_data.filter(pl.col("pitcher_hand") == pitcher_hand)
    if batter_hand != None:
        new_data = new_data.filter(pl.col("batter_hand") == batter_hand)
    trans_probs = np.zeros([25,28])
    array_vals = new_data.group_by(['pre_state', 'post_state3']).agg([
    pl.col('runs_scored').count().alias('Count')]).sort(by=['pre_state', 'post_state3']).to_numpy()
    for val in array_vals:
        row = val[0]
        col = val[1]
        trans_probs[row-1,col-1] = val[2]
    pre_state_num = dict(zip(range(1,25),np.int32(trans_probs.sum(axis=1)[:-1])))

    return trans_probs,pre_state_num

def outcome_pl_new_2(data:pl.DataFrame) -> np.ndarray:
    outcome_dict = {str(i):[] for i in range(2528)}
    ind_dict = {str(i):[] for i in range(2528)}
    for val in data.group_by(['pre_state', 'post_state3','event_category']).agg([pl.len().alias('Frequency')]).to_numpy():
        ind = str(int(val[0] * 10**(int(np.log10(val[1]) + 1)) + val[1]))
        outcome_dict[ind].append(val[2])
        ind_dict[ind].append(val[3])
    return outcome_dict,ind_dict


def create_transition_probs_pd(data:pd.DataFrame,batter_id:str=  None, pitcher_id:str = None,one_year = None,
                               pitcher_hand:str = None,batter_hand:str = None,general=None) -> Tuple[np.ndarray,dict]:
    """
    Create transition probabilities matrix and pre-state count dictionary based on the given data.

    Args:
        data (pl.DataFrame): The input data.
        batter_id (str, optional): The batter ID to filter the data. Defaults to None.
        pitcher_id (str, optional): The pitcher ID to filter the data. Defaults to None.
        one_year (int, optional): The year to filter the data. Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: A tuple containing the transition probabilities matrix and the pre-state count dictionary.
    """

    # new_data = data.__copy__()
    if one_year != None:
        # new_data = new_data.filter(pl.col("year") == one_year)
        data.query("year == @one_year")
    if batter_id != None:
        # new_data = new_data.filter(pl.col("batter_id") == batter_id)
        data = data.query("batter_id == @batter_id")
    if pitcher_id != None:
        # new_data = new_data.filter(pl.col("pitcher_id") == pitcher_id)
        data = data.query("pitcher_id == @pitcher_id")
    if pitcher_hand != None:
        # new_data = new_data.filter(pl.col("pitcher_hand") == pitcher_hand)
        data = data.query("pitcher_hand == @pitcher_hand")
    if batter_hand != None:
        # new_data = new_data.filter(pl.col("batter_hand") == batter_hand)
        data = data.query("batter_hand == @batter_hand")

    vals = pd.crosstab(index=data['pre_state_cat'],columns=data['post_state_cat'],dropna=False).values
    if vals.shape == (25,25):
        return vals
    return np.zeros([25,25])

def create_transition_probs_pd2(data:pd.DataFrame,batter_id:str=  None, pitcher_id:str = None,one_year = None,
                               pitcher_hand:str = None,batter_hand:str = None,general=None) -> Tuple[np.ndarray,dict]:
    """
    Create transition probabilities matrix and pre-state count dictionary based on the given data.

    Args:
        data (pl.DataFrame): The input data.
        batter_id (str, optional): The batter ID to filter the data. Defaults to None.
        pitcher_id (str, optional): The pitcher ID to filter the data. Defaults to None.
        one_year (int, optional): The year to filter the data. Defaults to None.

    Returns:
        Tuple[np.ndarray, dict]: A tuple containing the transition probabilities matrix and the pre-state count dictionary.
    """

    # new_data = data.__copy__()
    if one_year != None:
        # new_data = new_data.filter(pl.col("year") == one_year)
        data.query("year == @one_year")
    if batter_id != None:
        # new_data = new_data.filter(pl.col("batter_id") == batter_id)
        data = data.query("batter_id == @batter_id")
    if pitcher_id != None:
        # new_data = new_data.filter(pl.col("pitcher_id") == pitcher_id)
        data = data.query("pitcher_id == @pitcher_id")
    if pitcher_hand != None:
        # new_data = new_data.filter(pl.col("pitcher_hand") == pitcher_hand)
        data = data.query("pitcher_hand == @pitcher_hand")
    if batter_hand != None:
        # new_data = new_data.filter(pl.col("batter_hand") == batter_hand)
        data = data.query("batter_hand == @batter_hand")
    # tt1 = data[['pre_state_cat','post_state_cat','date','pitcher_hand','batter_id','year']]
    # pd.options.mode.chained_assignment = None
    # tt1['date_weigh'] = .997 ** ((tt1['date'].max() - tt1.date).dt.days)
    # tt1['timestamp'] = (tt1.date.max() - tt1['date']).astype(int) / 10**9  # Convert to seconds

    # # Apply Simple Exponential Smoothing
    # model = SimpleExpSmoothing((tt1.timestamp.max()-tt1['timestamp']).values)
    # try:
    #     result = model.fit(smoothing_level=.8, optimized=False)
    # except Exception:
    #     return np.zeros([25,25])

    # tt1['smoothed'] = result.fittedvalues
    # if tt1['smoothed'].sum() == 0:
    #     return pd.crosstab(index=tt1['pre_state_cat'],columns=tt1['post_state_cat'],dropna=False).values
    # new_tt = tt1[['pre_state_cat','post_state_cat']].sample(tt1.shape[0],replace=True,weights=tt1['smoothed'])
    
    # return pd.crosstab(index=new_tt['pre_state_cat'],columns=new_tt['post_state_cat'],dropna=False).values
    # vals = pd.crosstab(index=data['pre_state_cat'],columns=data['post_state_cat'],dropna=False).values
    # if vals.sum() == 0:
    #     return general

    # return vals
    vals = pd.crosstab(index=data['pre_state_cat'],columns=data['post_state3_cat'],dropna=False).values
    if vals.shape == (25,28):
        return vals
    return np.zeros([25,28])

def create_lineup_pd(data:pd.DataFrame, game:str = None) -> Tuple[list]:
    """
    Return the lineups for a given game based on the provided data.

    Args:
        data (pl.DataFrame): The data containing the game information.
        game (str, optional): The game ID. If provided, the lineup will be created for this specific game. 
                              If not provided, the lineup will be created for all games in the data.

    Returns:
        Tuple[list]: A tuple containing the home lineup and away lineup as lists of batter IDs.
    """
        
    if game != None:
        data = data.query("game_id == @game")
    # away_lineup = data.query("batting_team == vis_team").batter_id.unique()[:9]
    # home_lineup = data.query("batting_team != vis_team").batter_id.unique()[:9]
    away_lineup = data.query("batting_team == 0").batter_id.unique()[:9]
    home_lineup = data.query("batting_team != 0").batter_id.unique()[:9]
    return home_lineup, away_lineup
