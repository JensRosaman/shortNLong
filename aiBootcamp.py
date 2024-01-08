from ShortNLong import *
from agents import GuiAgent, RandAgent, Mormor
from web_ui.app import url_for, app, socketio, run_app
from dqn_agent import DQNAgent


def start_training(guiagent=False):
    url = app.url_for("index", _external=True)

    # GuiAgent(agentID=i,apiUrl=url)

    spelare = [Mormor(1), Mormor(2), Mormor(3), Mormor(4), DQNAgent(5)]
    spel = Game(playerIDS=spelare, guiActive=guiagent, appUrl=url)
    spel.start_game()
    score = spel.playerScores
    print(score)


def simulate_game():
    bob = GuiAgent(1)
    spel = Game([bob], guiActive=True)  # spelareObj.__run_of_four__()
    spel.deck = Deck()
    spel._hand_out_cards(10)
    spel.send_state()
    # spelareObj = spel.players[bob]
    # trissar = spelareObj.__3_of_a_kind__()
    # print(trissar)
    # spelareObj.round = 2
    # h = spelareObj.hand
    # print(trissar)


if __name__ == "__main__":
    # start_game()
    # simulate_game()
    # bob = HumanAgent(1)
    start_training(True)


