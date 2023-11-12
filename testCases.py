from ShortNLong import *


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


if __name__ == "__main__":
    bob = HumanAgent(1)
    spel = Game([bob]) #spelareObj.__run_of_four__()
    spel.deck = Deck()
    spel._hand_out_cards(50)
    spelareObj = spel.players[bob]
    trissar = spelareObj.__3_of_a_kind__()
    #print(trissar)
    spelareObj.round = 2
    h = spelareObj.hand
    f = count_card_occurrences(h)
    print(spelareObj.declare_hand())
    print(spelareObj.valid_in_declared_run(Card('HA')))

    

    spelareObj.round = 1
    #print(spelareObj.__3_of_a_kind__())