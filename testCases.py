import threading
import time

from ShortNLong import *
from agents import GuiAgent, RandAgent, RuleBased
from web_ui.app import app, run_app
from dqn_agent import DQNAgent
import matplotlib.pyplot as plt

def d(lista):
    sets = {}
    for card in lista:
        if card in sets:
            sets[card] += 1
        else:
            sets[card] = 1

    return lista


def count_card_occurrences(listor):
    card_counts = {}  # Initialize an empty dictionary to store card counts
    
    for card in listor:
        if card in card_counts:
            card_counts[card] += 1  # Increment the count
        else:
            card_counts[card] = 1  # Initialize count to 1

    return card_counts


def start_game(guiagent=False):
    url = app.url_for("index",_external=True)
    #spelare = [RuleBased(1),RuleBased(2),RuleBased(3),GuiAgent(agentID=4, apiUrl=url), GuiAgent(agentID=5, apiUrl=url)]
    spelare = [GuiAgent(1),DQNAgent(2),DQNAgent(3),DQNAgent(4),GuiAgent(5)]
    spel = Game(playerIDS=spelare, guiActive=True, appUrl=url)
    spel.start_game()
    return spel.playerScores

def plot_playerScores():
    spelare = [RuleBased(1),RuleBased(2),DQNAgent(3),DQNAgent(agentID=4), DQNAgent(agentID=5)]
    totScores = {agent:0 for agent in spelare}
    for i in range(5):
        spel = Game(playerIDS=spelare)
        spel.reset_game()
        spel.round = 1
        spel.round_loop()
        spel._update_score_table()
        for agent, score in spel.playerScores.items():
            totScores[agent] += score

    xValues = [str(agent) for agent in spelare]
    yValues = list(totScores.values())

    plt.bar(xValues, yValues)
    plt.xlabel('Players')
    plt.ylabel('Total Scores')
    plt.title('Total Scores After 5 Rounds')
    plt.savefig('plots/3.png')



if __name__ == "__main__":
    plot_playerScores()