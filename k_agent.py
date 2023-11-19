import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque
import random
import  tensorflow as tf
from tensorflow.python.keras.optimizers import adam_v2 as Adam
# Define the RL agent class

class Agent:
    def __init__(self, agentID: int, stateSize, actionSize) -> None:
        self.stateSize = stateSize
        self.actionSize = actionSize
        self.agentID = agentID

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Agent):
            return self.agentID == other.agentID
        return False

    def request_declare(self, state: dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        pass

    def request_card2Play(self, state: dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        if np.random.rand() < self.epsilon:
            # Explore: choose a random action
            return np.random.choice(self.action_size)
        else:
            # Exploit: choose the action with the highest Q-value
            state_representation = self._state_to_representation(state)
            q_values = self.q_table[state_representation, :]
            return np.argmax(q_values)


    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""