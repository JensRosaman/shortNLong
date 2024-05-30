import time

import numpy as np 
import pandas as pd
import scipy.stats as stats
import matplotlib as plt 
import math
np.random.seed(6)
population_ages1 = stats.poisson.rvs (loc=18, mu=5, size=150000) 
population_ages2 = stats.poisson.rvs (loc=  18, mu=10, size=100000) 
population_ages = np.concatenate((population_ages1, population_ages2))

minnesota_ages1 = stats.poisson.rvs (loc=18, mu=30, size=30) 
minnesota_ages2 = stats.poisson. rvs (loc=18, mu=10, size=20) 
minnesota_ages = np.concatenate((minnesota_ages1, minnesota_ages2))
print( population_ages.mean()) 
print(minnesota_ages.mean())
k = stats.ttest_1samp (a =minnesota_ages,
popmean=population_ages.mean())
print(k.confidence_interval())
"""print(f"Shape of numerical_discard: {np.concatenate(numerical_discard).shape}")
        print(f"Shape of numerical_hand: {np.concatenate(numerical_hand).shape}")
        print(f"Shape of current_score: {np.array([current_score]).shape}")
        print(f"Shape of taken_card: {np.array([taken_card]).shape}")
        print(f"Shape of has_complete_hand: {np.array([int(has_complete_hand)]).shape}")
        print(f"Shape of complete_sets: {np.array(complete_sets).shape}")
        print(f"Shape of complete_runs: {np.array(complete_runs).shape}")
        print(f"Shape of declared_cards_arr: {np.array(declared_cards_arr).shape}")
        print(f"Shape of player_score: {np.array([player_score]).shape}")
        print(f"Shape of discard_valid_in_declared: {np.array([int(discard_valid_in_declared)]).shape}")"""