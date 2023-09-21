import random
import copy
import itertools

class Card:
    """Represents a single card"""
    @property
    def val(self):
        return self._point_value

    def __init__(self, code): 
        """
        Code is Suit letter (H,C,D,S) followed by rank (A,2,3,4,5,6,7,8,9,T,J,Q,K,X) 
        where T is 10
        """
        if not isinstance(code, str):
            raise Exception('Cannot create Card without string code')

        self._code = code    

        # Set suit
        s = code[0]
        if s == 'H':
            self._suit = 'Hearts'
            self._suit_value = 0x0
        elif s == 'C':
            self._suit = 'Clubs'
            self._suit_value = 0x1
        elif s == 'D':
            self._suit = 'Diamonds'
            self._suit_value = 0x2
        elif s == 'S':
            self._suit = 'Spades'
            self._suit_value = 0x3
        else:
            raise Exception('Invalid suit code \'%s\'' % s)

        # Set rank
        r = code[1]

        if r == 'A':
            self._rank = 'Ace'
            self._point_value = 25
            self._rank_value = 0x1
        elif r == '2':
            self._rank = 'Two'
            self._point_value = 5
            self._rank_value = 0x2
        elif r == '3':
            self._rank = 'Three'
            self._point_value = 5
            self._rank_value = 0x3
        elif r == '4':
            self._rank = 'Four'
            self._point_value = 5
            self._rank_value = 0x4
        elif r == '5':
            self._rank = 'Five'
            self._point_value = 5
            self._rank_value = 0x5
        elif r == '6':
            self._rank = 'Six'
            self._point_value = 5
            self._rank_value = 0x6
        elif r == '7':
            self._rank = 'Seven'
            self._point_value = 5
            self._rank_value = 0x7
        elif r == '8':
            self._rank = 'Eight'
            self._point_value = 5
            self._rank_value = 0x8
        elif r == '9':
            self._rank = 'Nine'
            self._point_value = 5
            self._rank_value = 0x9
        elif r == 'T':
            self._rank = 'Ten'
            self._point_value = 10 
            self._rank_value = 0xa
        elif r == 'J':
            self._rank = 'Jack'
            self._point_value = 10 
            self._rank_value = 0xb
        elif r == 'Q': 
            self._rank = 'Queen'
            self._point_value = 10 
            self._rank_value = 0xc
        elif r == 'K':
            self._rank = 'King'
            self._point_value = 10 
            self._rank_value = 0xd
        else:
             raise Exception('Invalid rank code %s', r)

    def __str__(self):
          return self._rank + ' of ' + self._suit
        
    
    def __repr__(self):
        return "Card(%s)" % repr(self._code)

    def __lt__(self, other):
        if isinstance(other, Card):
            return (self._rank_value, self._suit_value) < (other._rank_value, other._suit_value)
        else:
            raise TypeError("Cannot compare Card to unknown type %s" % other.__class__)

    def __eq__(self, other):
        if isinstance(other, Card):
            return (self._rank_value, self._suit_value) == (other._rank_value, other._suit_value)
        else:
            raise TypeError("Cannot compare Card to unknown type %s" % other.__class__)
        

class Deck:
    """Represents both the deck on the table"""
    def __init__(self) -> None:
        # creates the deck where each item is a card object
        self.deck = []
        suits = 'HCDS'
        ranks = 'A23456789TJQK'
        for round in range(2):
            for suit in suits:
                for rank in ranks:
                    code = suit + rank
                    self.deck.append(Card(code))

        # shufflar kort in place
        FY_Shuffle(self.deck)

        # creates played card deck and plays a starting card
        self.playedCardDeck = [self._removeCard_([-1])]
        self.layingCard = self.playedCardDeck[-1]

    
    def _removeCard_(self, i:list, deck: list) -> list:
        """Removes a card from the deck and returns the item"""
        popped = []
        for item in i:
            popped.append(deck.pop(item))
            return popped
    
    def getTopCards(self, i):
        """gets the  top cards in the played cards deck"""
        return self.playedCardDeck[i:]
    
    def init_new_round(self):
        FY_Shuffle(self.deck)
        # removes the top cards and assings it to the played deck
        self.playedCardDeck = [(self._removeCard_([-1], self.deck))[0]]
        self.layingCard = self.playedCardDeck[-1]



# _______________________________________________________________________________________________


class Player:
    """Handles all action related to a specific player and their hand"""
    def __init__(self, player_id, cards):
        self.hand = cards
        self.id = player_id
        self.complete_hand = False
        self.round = 1
        self.set_count = 0
        self.run_count = 0

    # -------------------------------------Win conditions ----------------------------------------------------------

    def __3_of_a_kind__(self) -> int:
        """Gives the amount of 3 of a kinds in the instances hand"""
        rank_counts = {}
        for card in self.hand:
            rank = card["rank"]
            if rank in rank_counts:
                rank_counts[rank] += 1
            else:
                rank_counts[rank] = 1

        # Check if there are at least two ranks with three cards each
        set_count = 0
        for count in rank_counts.values():
            if count >= 3:
                set_count += 1
        return set_count

    def __has_run_of_four__(self):
        # Create a set to store the unique ranks in the hand
        unique_ranks = set(card["rank"] for card in self.hand)
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

        # Iterate through the ranks and check if there is a sequence of four consecutive ranks
        for rank in ranks:
            if all(rank in unique_ranks for rank in ranks[ranks.index(rank):ranks.index(rank) + 4]):
                self.run_count += 1
    # --------------------------------------------------------------------------------------

    def __complete_hand__(self):
        if self.round == 1:
            print()
        else:
            return False

    def add_a_card(self, cards_to_add: list):
        self.hand += cards_to_add
        self.__complete_hand__()


class Game():
    """Handles all the internal logic of the game"""
        
        




def FY_Shuffle(items: list):
    "implementation of the Fisher-Yates shuffle algorithm "
    if len(items) > 0:
        r = reversed(range(len(items)))
        for i in r:
            j = random.randint(0, i)
            tmp = items[i]
            items[i] = items[j]
            items[j] = tmp
        return items
    

if __name__ == "__main__":
    deck = Deck()
    print(deck.deck[0])