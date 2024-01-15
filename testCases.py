from ShortNLong import *
from agents import GuiAgent, RandAgent, Mormor
from web_ui.app import app, run_app


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

               #GuiAgent(agentID=i,apiUrl=url)

    spelare = [Mormor(1),Mormor(2),Mormor(3),GuiAgent(agentID=4, apiUrl=url), GuiAgent(agentID=5, apiUrl=url)]
    spel = Game(playerIDS=spelare, guiActive=True, appUrl=url)
    spel.start_game()
    score = spel.playerScores
    print(score)


def simulate_game():

        bob = GuiAgent(1)
        spel = Game([bob], guiActive=True) #spelareObj.__run_of_four__()
        spel.deck = Deck()
        spel._hand_out_cards(10)
        spel.send_state()
        #spelareObj = spel.players[bob]
        #trissar = spelareObj.__3_of_a_kind__()
        #print(trissar)
        #spelareObj.round = 2
        #h = spelareObj.hand
        #print(trissar)


if __name__ == "__main__":
   # start_game()
   # simulate_game()
   # bob = HumanAgent(1)
    start_game()