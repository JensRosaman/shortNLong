from ShortNLong import *
from agents import GuiAgent, RandAgent, Mormor
from web_ui.app import url_for, app, socketio, run_app
from dqn_agent import DQNAgent
from operator import itemgetter
class Trainer:
    def __init__(self, agents):
        self.agents = agents
        self.game = Game(playerIDS=agents)
        self.epochs = 15
        pass

    def train_agents(self):

        for i in range(self.epochs):
            if self.game.start_game(): # game has ended
                self.reward_agents()
                # logic for training each agent for next epoch
        bestModel = self.get_best_agent()

    def get_best_agent(self):
        highestScore = [0,0]
        for agent , score in self.game.playerScores:
            if score > highestScore[1]:
                highestScore[1] = score
                highestScore[0] = agent
        return max(self.game.playerScores.iteritems(), key=self.game.playerScores.itemgetter(1))[0]

    def reward_agents(self):
        pass
    def reset(self):
        self.game = Game(playerIDS=self.agents)







def start_training(guiagent=False):
    url = app.url_for("index", _external=True)

    # GuiAgent(agentID=i,apiUrl=url)

    spelare = [Mormor(1), Mormor(2), Mormor(3), Mormor(4), DQNAgent(5)]
    spel = Game(playerIDS=spelare, guiActive=guiagent, appUrl=url)
    spel.start_game()
    score = spel.playerScores
    print(score)




if __name__ == "__main__":
    # start_game()
    # simulate_game()
    # bob = HumanAgent(1)
    start_training(True)


