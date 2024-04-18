from constants import *

import argparse
import numpy as np
import pandas as pd
import polars as pl
import simulate
import time



def main():

    parser = argparse.ArgumentParser(description='Run simulation')
    parser.add_argument('--num_iters', type=int, default=10_000, help='Number of iterations to run')
    parser.add_argument('--num_games', type=int, default=10_000, help='Number of games to simulate')

    args = parser.parse_args()
    num_iters = args.num_iters
    num_games = args.num_games

    data = pd.read_pickle('data/bash_data.pkl').query("~event_category.isin(@NON_AB_OUTCOMES)")

    game_results = pd.read_csv('data/full_test_set.csv')

    game_ids = game_results.query("game_id in @data.game_id.unique() and game_id in @game_results.game_id.unique()").game_id.values[:num_games]

    start_time = time.time()

    game_df,hrun_vals,arun_vals = simulate.multiple_sims(data,game_ids,num_iters,game_results)
    game_df.to_csv('sim_results/simulation_data.csv')
    np.save('sim_results/home_run_vals.npy', hrun_vals)
    np.save('sim_results/away_run_vals.npy', arun_vals)

    print("Simulation Accuracy %.2f" % (game_df.home_did_win == game_df.sim_home_win).mean())

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()