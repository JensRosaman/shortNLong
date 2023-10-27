from ShortNLong import *

def run(self):
    suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
    sorted_hand = []
    for suit in suits:
        suit_list = []
        for card in self.hand:
            if suit == card._suit:
                suit_list.append(card)
        sorted_hand.append(suit_list)
        
    """Returns the amount of runs of fours in hand along with sorted runs"""
    # Sort the hand by rank and suit
    sorted_hand = sorted(self.hand, key=lambda card: (card._rank_value, card._suit_value))

    # Initialize counters and runs list
    run_count = 0
    consecutive_count = 1
    runs = []

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

    return run_count, runs


if __name__ == "__main__":
    bob = HumanAgent(1)
    spel = Game([bob])
    spel._hand_out_cards(50)
    print(run(spel.players[bob]))