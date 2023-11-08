from ShortNLong import *


def d(lista):
    sets = {}
    for card in lista:
        if card in sets:
            sets[card] += 1
        else:
            sets[card] = 1

    return lista





if __name__ == "__main__":
    bob = HumanAgent(1)
    spel = Game([bob]) #spelareObj.__run_of_four__()
    spel.deck = Deck()
    spel._hand_out_cards(50)
    spelareObj = spel.players[bob]
    trissar = spelareObj.__3_of_a_kind__()
    #print(trissar)
    sets = {}

    print(sets)

    spelareObj.round = 1
    #print(spelareObj.__3_of_a_kind__())