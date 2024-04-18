from constants import *

import markov_simulation_model as ms
import numpy as np
import pandas as pd
import utils


def multiple_sims(game_data,games,iters,game_results):
    rep_sim = []
    home_run_vals = np.zeros([len(games),iters])
    away_run_vals = np.zeros([len(games),iters])
    for i,game in enumerate(games):
        how,aww,home_runs,away_runs,margins,nrfis,home_vec,away_vec =run_sims(game_data,iters,game)
        
        run_vec = np.array(home_vec) + np.array(away_vec)
        spread_vec = np.array(home_vec) - np.array(away_vec) 
        home_run_vals[i] = home_vec
        away_run_vals[i] = away_vec

        game_info = game_results.query('game_id == @game')


        home_score = game_info.home_score.iloc[0]
        away_score = game_info.away_score.iloc[0]

        game_ou = game_info.Close_OU.iloc[0]
        game_total = game_info.runs_scored.iloc[0]
        game_nrfi = game_info.is_nrfi.iloc[0]
        game_spread = game_info.Run_Line.iloc[0]
        game_margin = game_info.home_score.iloc[0] - game_info.away_score.iloc[0]
        spread_cover = (((game_margin > (-1*game_spread)) and (game_spread < 0)) or (game_margin > (-1*game_spread) and (game_spread > 0)))
        sim_total = (home_runs + away_runs)/iters
        spread_percentage = np.mean(((spread_vec > (-1*game_spread)) & (game_spread < 0)) | ((spread_vec > (-1*game_spread)) & (game_spread > 0)))

        rep_sim.append(pd.DataFrame({'game_id':game,'home_wins':how,'away_wins':aww,'home_did_win':game_info.home_win,'sim_home_win': how > aww,
                                     'home_mean_sim_score':home_runs/iters,'away_mean_sim_score':away_runs/iters,
                                     'home_median_sim_score':np.median(home_vec),'away_median_sim_score':np.median(away_vec),
                                     'sim_total':sim_total,
                                     'nrfi_percentage':nrfis/iters,
                                     'game_nrfi':game_nrfi,
                                     'home_score':home_score,
                                    'away_score':away_score,
                                    'game_margin':game_margin,
                                    'game_spread':game_spread,
                                    'game_spread_cover':spread_cover,
                                    'game_total':game_total,
                                    'game_ou':game_ou,
                                    'game_over':game_total > game_ou,
                                    'sim_over':sim_total > game_ou,
                                    'spread_percentage':spread_percentage,
                                    'correct_spread':((spread_percentage) >= .5) == spread_cover,
                                    'over_percentage':(run_vec > game_ou).mean(),
                                    'correct_ou':((run_vec > game_ou).mean() >= .5) == (game_total > game_ou),
                                    'correct_nrfi':((nrfis/iters) >= .5) == game_nrfi,
                                     'margins':margins}))
    
    return pd.concat(rep_sim),home_run_vals,away_run_vals


def run_sims(data:pd.DataFrame,iters:int,game_id:str):
    # filter out all data except the chosen game
    game_data = data.query("game_id == @game_id")
    # date of the game as a datatime object
    date = pd.to_datetime(game_id[7:9]+ '-'  + game_id[9:11]  + '-' + game_id[3:7])

    yr = int(game_id[3:7])
    window_data = data.query("date < @date and year >= (@yr - 3)")

    # create the transition matrix for all before the game in question
    general_transition = utils.create_transition_probs_pd2(window_data)

    home_pitcher = game_data.query("batting_team == 0").pitcher_id.iloc[0]
    away_pitcher = game_data.query("batting_team == 1").pitcher_id.iloc[0]

    # # extract the arm sides of the starting pitchers for the home and away teams
    home_pitcher_side = game_data.query("pitcher_id == @home_pitcher").pitcher_hand.iloc[0]
    away_pitcher_side = game_data.query("pitcher_id == @away_pitcher").pitcher_hand.iloc[0]

    # create the transition matrices for the home and away pitches 
    home_sim = utils.create_transition_probs_pd2(window_data,pitcher_id=home_pitcher)
    away_sim = utils.create_transition_probs_pd2(window_data,pitcher_id=away_pitcher)


    # create the lineups for the home and away teams
    home_lineup,away_lineup = utils.create_lineup_pd(game_data,game=game_id)

    bat_trans_dict = {}

    full_lineup = np.concatenate((home_lineup,away_lineup))

    lineup_info = [utils.create_transition_probs_pd2(window_data,batter_id = full_lineup[x],pitcher_hand = away_pitcher_side) if x < 9 else utils.create_transition_probs_pd2(window_data,batter_id = full_lineup[x],pitcher_hand = home_pitcher_side) for x in range(18)]

    bat_trans_dict = dict(zip(full_lineup,[lineup_info[x] for x in range(18)]))

    # create the transition matrices for the home and away pitches 
    home_sim = utils.create_transition_probs_pd2(window_data,pitcher_id=home_pitcher)
    away_sim = utils.create_transition_probs_pd2(window_data,pitcher_id=away_pitcher)

    full_sim_lineups = np.array([home_lineup,away_lineup])
    

    return ms.markov_sim(games = iters,year = yr,
                       transition = general_transition,
                       batter_trans = bat_trans_dict,
                        pitcher_trans = list([home_sim,away_sim]),
                       lineups= full_sim_lineups)