import keras
from ShortNLong import *
from web_ui.app import url_for, app, socketio, run_app
from dqn_agent import DQNAgent
from operator import itemgetter
from threading import Thread
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
        games2play = 2
        weightsFrequence = 1 # how ooften the fit function is run updates
        totalScores = {agent: [] for agent in self.agents}
        self.game.round = 1
        for i in range(weightsFrequence):
            for j in range(games2play):
                if self.game.round_loop():
                    self.update_total_scores(table=totalScores)

                    bestAgent = None
                    minScore = float("inf")
                    for a , score in self.game.playerScores.items():
                        if score < minScore:
                            minScore = score
                            bestAgent = a

                    for agent in self.agents:
                        if agent.agentID == bestAgent.agentID:
                            agent.add_round_to_memory(True)
                            continue
                        agent.add_round_to_memory(False)
                    self.game.reset_game()
                    self.game.round = 1
            for agent in self.agents:
                agent.save_memory()
            bestAgent = self.get_best_agent(totalScores=totalScores)
            self.replay_agents()

        self.save_agents()

    def update_total_scores(self, table= None):
        if table is None:
            for agent in self.agents:
                self.totalScores[agent].append(self.game.playerScores[agent])
        else:
            for agent in self.agents:
                table[agent].append(self.game.playerScores[agent])


    def get_best_agent(self, totalScores) -> DQNAgent:
        lowestScore = [None, float("inf")]
        averageScore  = {agent: sum(totalScores[agent]) for agent in totalScores}
        for agent, score in averageScore.items():
            if score < lowestScore[1]:
                lowestScore[1] = score
                lowestScore[0] = agent
        return lowestScore[0]

    def reward_agents(self):
        pass

    def replay_agents(self):
        for agent in self.agents:
            agent.replay()
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

    def save_agents(self):
        for agent in self.agents:
            agent.save_model()



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
    trainer.train_for_round1()


