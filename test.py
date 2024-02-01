import time
import pickle
print()
from dqn_agent import *
from aiBootcamp import *

# Get current time
with open("picklejar/1_12-25.pkl", "rb") as f:
    memory = pickle.load(f)

print(memory)
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