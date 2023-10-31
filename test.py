from ShortNLong import *

def runddd(self):
    
    suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
    sorted_hand = []
    for suit in suits:
        suit_list = []
        for card in self.hand:
            if suit == card._suit:
                suit_list.append(card)
        sorted_hand.append(suit_list)


    run_count = 0
    consecutive_count = 1
    runs = []

    # sorting each indivudal list in the sorted_hand
    for suit_list in sorted_hand:
        if len(suit_list) <= 3:
            print("removed: ", suit_list)
            sorted_hand.remove(suit_list)
        else:
            suit_list = sorted(suit_list, key=lambda card: (card._rank_value, card._suit_value))
            for i in range(1, len(suit_list)):
                # Check if the current card forms a run with the previous card
                if (
                    suit_list[i]._rank_value == suit_list[i - 1]._rank_value + 1
                    and suit_list[i]._suit_value == suit_list[i - 1]._suit_value
                ):
                    consecutive_count += 1
                    if consecutive_count == 4:
                        run_count += 1
                        # Store the run as a list of card instances
                        run = [suit_list[i - 3], suit_list[i - 2], suit_list[i - 1], suit_list[i]]
                        runs.append(run)
                else:
                    consecutive_count = 1

    """ 
    # Sort the hand by rank and suit

    
    for i in range(1, len(sorted_hand)):
        # Check if the current card forms a run with the previous card
        if (
            sorted_hand[i]._rank_value == sorted_hand[i - 1]._rank_value + 1
            and sorted_hand[i]._suit_value == sorted_hand[i - 1]._suit_value
        ):
            consecutive_count += 1
            if consecutive_count == 4:
                run_count += 1
                # Store the run as a list of card instances
                run = [sorted_hand[i - 3], sorted_hand[i - 2], sorted_hand[i - 1], sorted_hand[i]]
                runs.append(run)
        else:
            consecutive_count = 1
"""
    return run_count, runs


def run(self):
    suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
    sorted_hand = []
    for suit in suits:
        suit_list = []
        for card in self.hand:
            if suit == card._suit:
                suit_list.append(card)
        if suit_list:
            sorted_hand.append(suit_list)

    run_count = 0
    consecutive_count = 1
    runs = []

    for suit_list in sorted_hand:
        if len(suit_list) <= 0:
            print("removed: ", suit_list)
            continue
        else:
            suit_list = sorted(suit_list, key=lambda card: (card._rank_value, card._suit_value))
            for i in range(1, len(suit_list)):
                print("Checking kort ", suit_list[i])
                # Check if the current card forms a run with the previous card
                if (
                    (suit_list[i]._rank_value == suit_list[i - 1]._rank_value + 1) or #om i värde är en mer än förgående
                    (suit_list[i]._rank_value == 2 and suit_list[i - 1]._rank_value == 1) 
                ) or (
                    suit_list[i]._rank_value == 13 and suit_list[0]._rank_value == 1
                ):
                    consecutive_count += 1
                    if consecutive_count == 4:
                        run_count += 1
                        # Store the run as a list of card instances
                        run = [suit_list[i - 3], suit_list[i - 2], suit_list[i - 1], suit_list[i]]
                        runs.append(run)
            
                else:
                    consecutive_count = 1
    return runs

if __name__ == "__main__":
    bob = HumanAgent(1)
    spel = Game([bob])
    spel._hand_out_cards(1)
    spel.players[bob].hand.extend([
        Card("CK"),  # 11
        Card("CQ"),  # 12
        Card("CJ"),  # 13
        Card("CA"),  # 14
    ])
    print(run(spel.players[bob]) )