import keras
from ShortNLong import *
from agents import GuiAgent, RandAgent, Mormor
from web_ui.app import url_for, app, socketio, run_app
from dqn_agent import DQNAgent
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt

class Trainer:
    def __init__(self, agents=None):
        if agents is None:
            agents = [DQNAgent(1), DQNAgent(2), DQNAgent(3), DQNAgent(4), DQNAgent(5)]
        self.agents = agents
        self.game = Game(playerIDS=agents)
        self.epochs = 3
        self.totalScores = {agent: 0 for agent in self.agents}
        pass

    def train_agents(self):
        for i in range(2):
            totalScores = {agent: [] for agent in self.agents}
            for j in range(self.epochs):
                if self.game.start_game(): # game has ended
                    self.reward_agents()
                    self.update_total_scores()
                    # logic for training each agent for next epoch
            bestAgent = self.get_best_agent(totalScores)
            self.agents = [agent.model.set_weights(bestAgent.model.get_weights()) for agent in self.agents if agent is not bestAgent]
            self.plot_img(self.totalScores[bestAgent])

        bestAgent.model.save_model()

    def train_for_round1(self):
        games2play = 10
        weightsFrequence = 15 # how ooften the weights updates
        totalScores = {agent: [] for agent in self.agents}
        for i in range(weightsFrequence):
            for i in range(games2play):
                if self.game.round_loop():
                    bestAgent = self.get_best_agent(totalScores=self.game.playerScores)

                self.game.reset_game()
                self.game.round = 1
        for agent in self.agents:
            if agent.agentID == bestAgent.agentID:
                agent.memory.append((agent.memory_buffer, 1))
            self.replay_agents(bestAgent)
                    self.game.reset_game()


    def update_total_scores(self, table= None):
        for agent in self.agents:
            self.totalScores[agent].append(self.game.playerScores[agent])


    def get_best_agent(self, totalScores) -> DQNAgent:
        highestScore = [0, 0]
        averageScore  = {agent:sum(totalScores[agent]) for agent in totalScores}
        for agent, score in averageScore.items():
            if score > highestScore[1]:
                highestScore[1] = score
                highestScore[0] = agent
        return max(averageScore.items(), key=lambda x: x[1])[0]

    def reward_agents(self):
        pass

    def replay_agents(self,bestAgent):

    def reset(self):
        self.game = Game(playerIDS=self.agents)

    def plot_img(self, yValues, name=hash(random.randint(0, 50))):
        try:
            print(f"{name}")
            xValues = range(1, len(yValues) + 1)
            plt.plot(xValues, yValues)

            plt.xlabel('GameX')
            plt.ylabel('score')
            plt.title('hej')
            plt.savefig(f'line_graph.png')
            plt.close()
        except Exception as e:
            print(e)


def start_training():
    spelare = [DQNAgent(1), DQNAgent(2), DQNAgent(3), DQNAgent(4), DQNAgent(5)]
    spel = Game(playerIDS=spelare)
    spel.start_game()
    score = spel.playerScores
    print(score)




if __name__ == "__main__":
    # start_game()
    # simulate_game()
    # bob = HumanAgent(1)
    #start_training()
    trainer = Trainer()
    trainer.train_agents()


