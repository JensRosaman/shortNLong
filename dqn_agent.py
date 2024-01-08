import numpy as np
import random
import pandas as pd

import os

from keras import Input, Model

os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential, load_model
from datetime import datetime

class DQNAgent:
    def __init__(self, agentID: int, buildNew = False) -> None:
        self.agentID = agentID


        # Define DQN parameters
        self.state_size =  18  # Define the size of the state space
        self.action_size = 2  # Define the size of the action space
        self.memory = []  # Use this to store experiences for experience replay
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration-exploitation trade-off
        self.epsilon_decay = 0.995  # Decay rate for epsilon
        self.epsilon_min = 0.01  # Minimum epsilon value
        self.learning_rate = 0.001  # Learning rate for the neural network

        # Build the Q-network
        if os.path.exists(fr"saved_models/{self.agentID}") and not buildNew:
            self.load_model(fr"saved_models/{self.agentID}")
        else:
            self.model = self.build_model()

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def build_model(self):
        def build_model(self):
            input_layer = Input(shape=(your_input_size,))
            common_hidden = Dense(24, activation='relu')(input_layer)

            # Output branch for declare action
            declare_output = Dense(1, activation='sigmoid', name='declare_output')(common_hidden)

            # Output branch for lay cards and card2Play actions
            action_output = Dense(self.action_size, activation='linear', name='action_output')(common_hidden)

            # Output branch for take discard action
            take_discard_output = Dense(1, activation='sigmoid', name='take_discard_output')(common_hidden)

            model = Model(inputs=input_layer, outputs=[declare_output, action_output, take_discard_output])
            model.compile(loss=['binary_crossentropy', 'mse', 'binary_crossentropy'],
                          optimizer=Adam(learning_rate=self.learning_rate, clipnorm=1.0, clipvalue=0.5))

            return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        # Experience replay
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, file_path=None):
        if file_path is None:
            file_path = fr"saved_models/{self.agentID}"# {datetime.now()}"
        # Save the model to a file
        self.model.save(file_path)

    def load_model(self, file_path):
        # Load the model from a file
        self.model = load_model(file_path)

    def request_declare(self, state: dict) -> bool:
        # For example, if the model predicts declaring with a probability greater than 0.5
        return self.model.predict(self.preprocess_state(state))[0][0] > 0.5

    def request_lay_cards(self,state) -> int:
        return self.act(self.preprocess_state(state))
    def request_card2Play(self, state: dict) -> int:
        # Implement your logic for choosing a card to play using DQN
        return self.act(self.preprocess_state(state))

    def request_take_discard(self, state: dict) -> bool:
        # Implement your logic for taking a discard using DQN
        # For example, if the model predicts taking the discard with a probability greater than 0.5
        return self.model.predict(self.preprocess_state(state))[0][1] > 0.5

    def preprocess_state(self, state: dict) -> np.ndarray:
        # Implement state preprocessing if needed
        # To Convert the state dictionary to a suitable input format for the neural ne

        def one_hot_encode_suit(suit_value, num_suits):
            one_hot_vector = np.zeros(num_suits)
            one_hot_vector[suit_value] = 1
            return one_hot_vector

        def one_hot_encode_rank(rank_value, num_ranks):
            one_hot_vector = np.zeros(num_ranks)
            one_hot_vector[rank_value] = 1
            return one_hot_vector

        def card_to_numerical(card):
            if card is None:
                # Handle None card
                suit_value = -1
                rank_value = -1
            else:

                suit_value = card._suit_value
                rank_value = card._rank_value

            #  4 suits and 13 ranks
            num_suits = 4
            num_ranks = 13

            # One-hot encode suit and rank separately
            one_hot_encoded_suit = one_hot_encode_suit(suit_value, num_suits)
            one_hot_encoded_rank = one_hot_encode_rank(rank_value, num_ranks)

            # Concatenate suit and rank one-hot vectors
            one_hot_encoded_card = np.concatenate((one_hot_encoded_suit, one_hot_encoded_rank), axis=None)

            return one_hot_encoded_card

        def one_hot_encode_int(currentInt, numPosInt):
            one_hot_vector = np.zeros(numPosInt)
            one_hot_vector[currentInt - 1] = 1  # Subtract 1 to convert round number to index
            return one_hot_vector

        round_number = one_hot_encode_int(state["round"])
        numerical_discard = [card_to_numerical(card) for card in state["discard"]]
        win_conditions = np.array(state["winConditions"]["sets"], state["winConditions"]["runs"])
        play_order = [one_hot_encode_int(player.id.AgentID,5) for player in state["playOrder"]]
        current_player = one_hot_encode_int(state["currentPlayer"].id.agentID)
        is_current_player = state["isCurrentPlayer"]
        numerical_hand = [card_to_numerical(card) for card in state["hand"]]
        current_score = state["currentScore"]
        taken_card = state["takenCard"]
        has_complete_hand = state["hasCompleteHand"]
        run_count = state["runCount"]
        set_count = state["setCount"]
        complete_sets = [[card_to_numerical(card) for card in lst] for lst in state["completeSets"]]
        complete_runs = [[card_to_numerical(card) for card in lst] for lst in state["completeRuns"]]
        declared_cards = {
            player.id.AgentID: [card_to_numerical(card) for card in lst]
            for player, lst in state["declaredCards"].items()
        }
        player_score = state["playerScore"]
        available_to_lay_to = state["availableToLayTo"]
        discard_valid_in_declared = state["discardValidInDeclared"]

        state_vector = np.concatenate((
            round_number,
            np.concatenate(numerical_discard),
            win_conditions,
            np.concatenate(play_order),  # Concatenate one-hot encoded play_order
            np.array([current_player]),
            np.array([int(is_current_player)]),
            np.concatenate(numerical_hand),
            np.array([current_score]),
            np.array([taken_card]),
            np.array([int(has_complete_hand)]),
            np.array([run_count]),
            np.array([set_count]),
            np.array(complete_sets),
            np.array(complete_runs),
            np.concatenate([item for sublist in declared_cards.values() for item in sublist]),
            np.array([player_score]),
            np.array([available_to_lay_to]),
            np.array([int(discard_valid_in_declared)])
        ), axis=None)

        return state_vector

        """
        s = {
            "discard": [card_to_numerical(card) for card in state["discard"]],
            "round": state["round"],
            "winConditions": str(state["winConditions"]),  # Convert dict to string
            "playOrder": [player.agentID for player in state["playOrder"]],
            "currentPlayer": state["currentPlayer"].id.agentID,
            "isCurrentPlayer": state["isCurrentPlayer"],
            "hand": [card_to_numerical(card) for card in state["hand"]],
            "winner": False,
            "currentScore": state["currentScore"],
            "takenCard": state["takenCard"],
            "hasCompleteHand": state["hasCompleteHand"],
            "runCount": state["runCount"],
            "setCount": state["setCount"],
            "completeSets": [[card_to_numerical(card) for card in lst] for lst in state["completeSets"]],
            "completeRuns": [[card_to_numerical(card) for card in lst] for lst in state["completeRuns"]],
            "declaredCards": {player.id.AgentID: [card_to_numerical(card) for card in lst]
                              for player, lst in state["declaredCards"].items()
                              },
            "playerScore": state["playerScore"],
            "availableToLayTo": state["availableToLayTo"],
            "discardValidInDeclared": state["discardValidInDeclared"]
        }
        """




