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
    """R"""
    def __init__(self) -> None:
        # creates the deck where each item is a card object
        self.deck = []
        suits = 'HCDS'
        ranks = 'A23456789TJQK'
        for suit in suits:
            for rank in ranks:
                code = suit + rank
                self.deck.append(Card(code))

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
    print(deck.deck[1]._code)