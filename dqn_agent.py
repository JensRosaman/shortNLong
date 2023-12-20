import numpy as np
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense
from keras.optimizers import Adam
import random
import pandas as pd
from datetime import datetime
class DQNAgent:
    def __init__(self, agentID: int) -> None:
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
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
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
            file_path = fr"saved_models/{self.agentID} {datetime.now()}"
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
        # To Convert the state dictionary to a suitable input format for the neural network

        return pd.DataFrame(state,index=[0]).to_numpy()
        # You may need to scale/normalize values and convert categorical variables


