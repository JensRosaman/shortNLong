from typing import Dict, Any
import numpy as np
import random
import os
from keras import Input, Model

os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras import Input, Model
from keras.layers import Dense , Masking
from keras.optimizers import Adam
from keras.models import Sequential, load_model
from datetime import datetime

class DQNAgent:
    def __init__(self, agentID: int, buildNew = False) -> None:
        self.agentID = agentID


        # Define DQN parameters
        self.action_size = 2  # Define the size of the action space
        self.memory = []  # Use this to store experiences for experience replay
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration-exploitation trade-off
        self.epsilon_decay = 0.995  # Decay rate for epsilon
        self.epsilon_min = 0.01  # Minimum epsilon value
        self.learning_rate = 0.001  # Learning rate for the neural network

        self.inputSize = 14968#14786#9683 #9682 #9206 #5942 # 5942#4412 #5 + 1 + 20 + 1 + 1 + 1 + 1 + 1 + (13*2) + (8*3) + 290 + 1 + 1 # 223
        # Build the Q-network
        if False:#os.path.exists(fr"saved_models/{self.agentID}") and not buildNew:
            self.load_model(fr"saved_models/{self.agentID}")
        else:
            self.model = self.build_model()
           # self.save_model()

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def build_model(self):

        input_layer = Input(shape=(self.inputSize,))
        masked_layer = Masking(mask_value=-1)(input_layer)

        common_hidden = Dense(24, activation='relu')(masked_layer)


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

    def replay(self):
        batch_size = 1
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
            file_path = fr"saved_models/{self.agentID}.keras"# {datetime.now()}"
        # Save the model to a file
        self.model.save(file_path)

    def load_model(self, file_path):
        # Load the model from a file
        self.model = load_model(file_path)

    def request_declare(self, state: dict) -> bool:
        # For example, if the model predicts declaring with a probability greater than 0.5
        return self.model.predict(self.preprocess_state(state))[0][0] > 0.5

    def request_lay_cards(self,state) -> dict[str, bool | Any] | dict[str, bool | Any]:
        """Requests an action asking what player to lay a card to"""
        availableToLayTo = state["availableToLayTo"]
        chosenAgent = random.choice(list(availableToLayTo))
        print(state["completeSets"])
        if len(availableToLayTo[chosenAgent]["runs"]) > 0:  # if run is available lay there
            layToRun = True
        else:
            layToRun = False

        # return the first card in the sets list or the runs list
        if layToRun:
            return {"layToRun": True, "agentToLayTo": chosenAgent,
                    "cardToLay": availableToLayTo[chosenAgent]["runs"][0]}
        return {"layToRun": False, "agentToLayTo": chosenAgent,
                "cardToLay": availableToLayTo[chosenAgent]["sets"][0]}

    def request_card2Play(self, state: dict) -> int:
        # Implement your logic for choosing a card to play using DQN
        return self.act(self.preprocess_state(state))

    def request_take_discard(self, state: dict) -> bool:
        # Implement your logic for taking a discard using DQN
        # For example, if the model predicts taking the discard with a probability greater than 0.5

        return self.model.predict(self.preprocess_state(state))[2] > 0.5

    def preprocess_state(self, state: dict) -> np.ndarray:
        # To Convert the state dictionary to a vector

        def one_hot_encode_suit(suit_value, num_suits):
            one_hot_vector = np.zeros(num_suits)
            one_hot_vector[suit_value] = 1
            for i in range(9):
               one_hot_vector = np.append(one_hot_vector,-1)
            return one_hot_vector

        def one_hot_encode_rank(rank_value, num_ranks):
            one_hot_vector = np.zeros(num_ranks)
            one_hot_vector[rank_value - 1] = 1
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
            one_hot_encoded_card = np.array([one_hot_encoded_suit, one_hot_encoded_rank])

            return one_hot_encoded_card

        def one_hot_encode_int(currentInt, numPosInt):
            one_hot_vector = np.zeros(numPosInt)
            one_hot_vector[currentInt - 1] = 1  # Subtract 1 to convert round number to index
            return one_hot_vector

        round_number = one_hot_encode_int(state["round"],4)
        numerical_discard = [card_to_numerical(card) for card in state["discard"]]
        while len(numerical_discard) < 70:
            numerical_discard.insert(0, card_to_numerical(None))
        numerical_discard = numerical_discard[:70]
        win_conditions = np.array((state["winConditions"]["sets"], state["winConditions"]["runs"]))
        play_order = [one_hot_encode_int(player.agentID,5) for player in state["playOrder"]]
        current_player = one_hot_encode_int(state["currentPlayer"].id.agentID,5)
        is_current_player = state["isCurrentPlayer"]
        numerical_hand = [card_to_numerical(card) for card in state["hand"]]
        current_score = state["currentScore"]
        taken_card = state["takenCard"]
        has_complete_hand = state["hasCompleteHand"]
        run_count = state["runCount"]
        set_count = state["setCount"]
        player_score = state["playerScore"]
        complete_sets = [[card_to_numerical(card) for card in lst] for lst in state["completeSets"]]
        complete_runs = [[card_to_numerical(card) for card in lst] for lst in state["completeRuns"]]
        discard_valid_in_declared = state["discardValidInDeclared"]
        declared_cards = {
            player.agentID: [
    [card_to_numerical(card) for card_set in lst["sets"] for card in card_set],
    [card_to_numerical(card) for run in lst["runs"] for card in run]
        ]        #[[card_to_numerical(card) for card in set for set in lst["sets"]],[card_to_numerical(card) for card in run for run in lst["runs"]]]
            for player, lst in state["declaredCards"].items()
        }
        declared_cards_arr = [[item for sublist in declared_cards[key] for item in sublist] for key in declared_cards]

        while len(declared_cards_arr) < 5:
            declared_cards_arr.append([])
        for lst in declared_cards_arr:
            while len(lst) < 29:
                lst.append(card_to_numerical(None))

        while len(numerical_hand) < 80:
            numerical_hand.append(card_to_numerical(None))

        while len(complete_runs) < 4:
            complete_runs.append([])
        for lst in complete_runs:
            while len(lst) < 9:
                lst.append(card_to_numerical(None))
        complete_runs = complete_runs[:4]

        while len(complete_sets) < 27: # sometimes contains an sub extra array
            complete_sets.append([])
        for lst in complete_sets:
            while len(lst) < 9:
                lst.append(card_to_numerical(None))

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
        ### CHANGE THE LOGIC FOR AVAILIBLETOLAY TO, AI IS NOW LOBOTOMIZED
        #available_to_lay_to = state["availableToLayTo"]
        # value size is
        # 5 + 1 + 20 + 1 + 1 + 1 + 1 + 1 + (13*2) + (8*3) + (5*28) + 1 + 1
        state_vector = np.concatenate((
            round_number,
            np.concatenate(numerical_discard), # 140
            win_conditions, # 2
            np.array(play_order),  # 5
            np.array([current_player]), # 5
            np.array([int(is_current_player)]), # 1
            np.concatenate(numerical_hand),# 20 * 2
            np.array([current_score]),# 1
            np.array([taken_card]),# 1
            np.array([int(has_complete_hand)]), # 1
            np.array([run_count]), # 1
            np.array([set_count]), # 1
            np.array(complete_sets), #
            np.array(complete_runs), #
            np.array(declared_cards_arr),
            #np.concatenate([item for sublist in declared_cards.values() for item in sublist]),
            np.array([player_score]),
            #np.array([available_to_lay_to]),
            np.array([int(discard_valid_in_declared)])
        ), axis=None)
        reshapedVector = np.reshape(state_vector, (1,-1 )) # 4412
        print(reshapedVector)
        print(np.shape(reshapedVector))
        return reshapedVector.astype("float64")

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



#ValueError: Failed to convert a NumPy array to a Tensor (Unsupported object type float).

