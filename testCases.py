from ShortNLong import *
from agents import GuiAgent, randAgent
from web_ui.app import url_for , app , socketio
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

def start_game():

    url = f'http://localhost:5000/'

    spelare = [1, 2, 3, 4, 5]
    for i in spelare:
        if i == 2:
            spelare[spelare.index(i)] = randAgent(agentID=i)
            continue
        spelare[spelare.index(i)] = GuiAgent(agentID=i,apiUrl=url)

    spel = Game(playerIDS=spelare, guiActive=True, appUrl=url)  # spelareObj.__run_of_four__()    spel.start_game()
    spel.start_game()
def simulate_game():

        bob = GuiAgent(1)
        #bob = HumanAgent(1)
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

