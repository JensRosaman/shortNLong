import random
import copy
import itertools

class Game:
    """Class representing a phase 10 game. Should be serializable"""

    def __init__(self, state=None):
        if state is not None:
            try:
                self._deck = state['deck']
                self._discard = state['discard']
                self._hands = state['hands']
                self._players = state['players']
                self._playorder = state['playorder']
                self._turn = state['turn']
                return
            except KeyError:
                # State does not have all of the keys,
                # assume that the Game is empty
                self._deck = Stack()
                self._discard = Stack()
                self._hands = []
                self._players = []
                self._playorder = []
                self._turn = 1

    def start_game(self, player_ids, decks=2):
        """player_ids is a list of player ids that is used to identify whose turn it is"""
        self._deck = Stack()
        self._deck.make_deck(decks)
        self._deck.shuffle()

        self._hands = self._deck.deal(10, len(player_ids))
        self._players = []

        self._turn = 1

        for i in range(len(self._hands)):
            self._players.append(Player(pid=player_ids[i], hand=self._hands[i], pset=Stack()))

        # Randomize play order
        self._playorder = shuffle(range(len(player_ids)))

        self._discard = Stack()
        self._discard += self._deck.draw()

    @property
    def turn(self):
        player_index = self._playorder[self._turn % len(self._players)]

        sets = []
        for i in self._playorder:
            if i is not player_index:
                sets.append(self._players[i]._set)

        return Turn(self._players[player_index], sets, self._deck, self._discard)

    def next(self):
        if self._discard[-1] == Card(' X'):
            self._turn += 2
        else:
            self._turn += 1

    def __repr__(self):
        return "Game({'deck' : %s, 'players' : %s, 'discard' : %s, 'hands' : %s, 'playorder' : %s, 'turn' : %s})" \
                % (repr(self._deck), repr(self._players), repr(self._discard), repr(self._hands), \
                        repr(self._playorder), repr(self._turn))


class Turn:
    def __init__(self, player, sets, deck, discard):
        self._player = player
        self._discard = discard
        self._deck = deck
        self._sets = sets

    @property
    def player(self):
        return self._player

    @property
    def hand(self):
        return self._player._hand

    def discard_at(self, index):
        c = self.hand.take_at(index)
        self._discard += c

    def draw_discard(self):
        self.hand += self._discard.draw()

    def draw_deck(self):
        self.hand += self._deck.draw()

    @property
    def discard(self):
        return self._discard

    @property
    def sets(self):
        return self._sets

    def __str__(self):
        return """Player '%s' 
        Hand %s
        Set %s
        Cards in deck %s
        Cards in discard %s""" % \
               (str(self._player._id), str(self._player._hand), str(self._player._set), \
                str(self._deck.card_count), str(self._discard.card_count))


class Player:
    def __init__(self, pid, hand=None, pset=None):
        """pid is a key that will be used to identify the player with a login name
        hand is a Stack that represents the player's hand
        pset is a Stack that represents the player's current set
        """
        self._id = pid

        if hand:
            self._hand = hand
        else:
            self._hand = Stack()

        if pset:
            self._set = pset
        else:
            self._set = Stack()

    def __repr__(self):
        return "Player(pid=%s, hand=%s, pset=%s)" % (repr(self._id), repr(self._hand), repr(self._set))


class Phase:
    pass

class Phase1 (Phase):
    pass

class Phase2 (Phase):
    pass

class Phase3 (Phase):
    pass

class Phase4 (Phase):
    pass

class Phase5 (Phase):
    pass

class Phase6 (Phase):
    pass

class Phase7 (Phase):
    pass

class Phase8 (Phase):
    pass

class Phase9 (Phase):
    pass

class Phase10 (Phase):
    pass

class Card:
    """Represents a single card"""
    @property
    def val(self):
        return self._point_value

    def __init__(self, code):
        """
        Code is Suit letter (H,C,D,S) followed by rank (A,2,3,4,5,6,7,8,9,T,J,Q,K,X)
        where T is 10 and X is joker
        """
        if not isinstance(code, str):
            raise CardError('Cannot create Card without string code')

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
            raise CardError('Invalid suit code \'%s\'' % s)

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
             raise CardError('Invalid rank code %s', r)

    def __str__(self):
        if self._rank is not 'Joker':
            return self._rank + ' of ' + self._suit
        else:
            return self._rank

    def __repr__(self):
        return "Card(%s)" % repr(self._code)

    def __cmp__(self, other):
        if isinstance(other, Card):
            return 4*(self._rank_value - other._rank_value) + self._suit_value - other._suit_value
        elif isinstance(other, Stack):
            # There will be one True for each element of other, so the only way to get 0
            # is to subtract the card count - 1
            return sum(self == i for i in other) - other.card_count - 1
        else:
            raise NotImplementedError('Cannot compare Card to unknown type %s' % other.__class__)

def shuffle(items):
    if len(items) > 0:
        r = range(len(items))
        r.reverse()

        for i in r:
            j = random.randint(0, i)
            tmp = items[i]
            items[i] = items[j]
            items[j] = tmp

        return items

class CardError (Exception):
    """
    Represents an error in creation or use of card class
    """
    pass

class Stack:
    """
    Defines a collection of cards with helper methods to combine stacks, 
    shuffle cards, and create full decks
    """ 
    def __init__(self, cards=None):
        if cards is not None:
            if isinstance(cards, Stack):
                self._cards = cards._cards[:]
            elif isinstance(cards, list):
                self._cards = []
                for i in cards:
                    if isinstance(i, Card):
                        self.append(i)
                    elif isinstance(i, str):
                        self.append(Card(i))
            else:
                self._cards = []
        else:
            self._cards = []

    def __getitem__(self, index):
        return self._cards[index]

    def __setitem__(self, key, value):
        self._cards[key] = value

    def __delitem__(self, key):
        del self._cards[key]

    def append(self, c):
        self._cards.append(c)

    def shuffle(self):
        """Perform the Fisher-Yates shuffle"""
        if len(self._cards) == 0: 
            raise CardError('Cannot shuffle an empty Stack') 
        
        self._cards = random.shuffle(self._cards)

    def take_at(self, index):
        """Take the card at specific index, removing it from stack"""
        if index not in range(len(self._cards)):
            raise CardError('index out of bounds:  %d (0 to %d possible)' % (index, len(self._cards)))

        tmp = self._cards[index]
        del self._cards[index]
        return tmp

    @property
    def score(self):
        return sum(i.val for i in self._cards)

    def __iadd__(self, other):
        """In place addition of one stack to another stack. The second stack is emptied in this case"""
        if isinstance(other, Card):
            self._cards.append(other)
        elif isinstance(other, Stack):
            self._cards.extend(other._cards)
            other._cards = []
        else:
            raise CardError('Cannot add an unhandled type to Stack')

        return self

    def sort(self, by='both'):
        if self.card_count:
            if by == 'rank':
                self._cards.sort(key=lambda x: x._rank_value)
            elif by == 'suit':
                self._cards.sort(key=lambda x: x._suit_value)
            elif by == 'both':
                self._cards.sort()

    @property
    def runs(self):
        """Returns possible runs in a stack"""
        res = self._preprocess_cards()
        ranks = res['ranks']
        cards = []
        kings = [] 

        for i in itertools.izip(ranks, res['sets']):
            # Get kings and jokers
            if i[0] == 0xd:
                # King
                kings = i[1] 
            elif i[0] == 0xe:
                # Joker
                pass
            else:
                # Any other card
                cards.append(i)

        # Sort cards
        cards.sort(key=lambda x: x[0])

        # iterate over len(cards)-1 because can't have a run starting at the 
        # last card
        runs = []
        skip = -1 

        for i in range(len(cards)-1):
            if i <= skip:
                continue

            run = [cards[i][1]]
            prev = cards[i][0]

            for j in range(i+1, len(cards)):
                if prev == cards[j][0]-1:
                    # This is a run. Append to run
                    run.append(cards[j][1])
                    prev = cards[j][0]
                    skip = j
                else:
                    break

            if len(run) >= 2:
                runs.append(run)

        # Try to join found sequences using kings
        if len(kings) == 0 or len(runs) < 2:
            return runs

        nk = len(kings)
        runs_with_wilds = []

        for x, y in itertools.permutations(runs, 2):
            # Note the -1. If a card is missing, the difference will be 2, not 1
            req_kings = y[0][0]._rank_value - x[-1][0]._rank_value - 1

            if abs(req_kings) <= nk and req_kings > 0:
                # We have enough kings to join the pair
                tmp = []
                tmp.extend(x)
                tmp.append(req_kings * kings)
                tmp.extend(y)
                runs_with_wilds.append(tmp)

        if len(runs_with_wilds) > 0:
            runs.append(runs_with_wilds) 

        return runs

    def _issequence(list1, list2):
        """Function receives two lists of tuples of the form
        (rank, [cards of that rank]) and checks if they're a sequence
        It assumes that list1 and list2 are sequences"""

        if list1[-1][0] == list2[0][0]-1:
            # list1,list2 form a sequence
            return True
        if list2[-1][0] == list1[0][0]-1:
            # list2,list1 form a sequence
            return True

        return False

    @property
    def sets(self):
        """Return possible sets in a stack"""
        res = self._preprocess_cards()
        
        sets = []
        for i in itertools.ifilter(lambda x: len(x) >= 2, res['sets']):
            sets.append(i)
        return sets 

    def _preprocess_cards(self):
        """Sorts and analyzes cards"""
        tmp = copy.copy(self) # Perform shallow copy of self, so Cards are references
        tmp.sort(by='rank')

        # Break into sets
        ranks = []
        groups = []
        for k, v in itertools.groupby(tmp, lambda x: x._rank_value):
            groups.append(list(v))
            ranks.append(k)

        return {'ranks' : ranks, 'sets' : groups}

    def set_down(self):
        pass

    def deal(self, cards, players = 3):
        if len(self._cards) < cards * players: 
            raise CardError('Cannot deal that many cards from Stack') 

        hands = []
        for j in range(players):
            hands.append(Stack(self._cards[:cards]))
            del self._cards[:cards]

        return hands

    def draw(self):
        if len(self._cards) == 0: 
            raise CardError('Cannot draw from an empty Stack') 
        return self._cards.pop()

    def make_deck(self, decks=1):
        """Create a stack of one or more decks"""
        self._cards = []
        
        for n in range(decks):
            for i in range(4):
                for j in range(13):
                    self._cards.append(Card(suits[i] + ranks[j]))
            # Add two jokers
            self._cards.append(Card(' X'))
            self._cards.append(Card(' X'))

    @property
    def card_count(self):
        return len(self._cards)

    def __str__(self):
        s = ''
        if self.card_count is not 0:
            for i in self._cards:
                s = s + i._code + ' '
            return s
        else:
            return 'Empty'

    def __repr__(self):
        s = 'Stack(['
        if self.card_count is not 0:
            for i in self._cards:
                s += i.__repr__() + ', '
        s += '])'
        return s

    def __cmp__(self, other):
        if isinstance(other, Stack):
            if self.card_count != other.card_count:
                return -1

            a = copy.deepcopy(self)
            b = copy.deepcopy(other)

            a.sort(by='both')
            b.sort(by='both')
            
            eq = 0
            for i in range(a.card_count): 
                eq += int(a[i] == b[i]) - 1
            return eq

    def __contains__(self, item):
        if isinstance(item, Card):
            return (i == item for i in self)
        elif isinstance(item, Stack):
            if item.card_count > self.card_count:
                return False

            a = sum(i in self for i in item) 
           
            if a == item.card_count and self.card_count >= item.card_count:
                return True
            else:
                return False

    def __iter__(self):
        self._iter_index = 0 
        return self

    def next(self):
        if self._iter_index == self.card_count:
            raise StopIteration
        
        self._iter_index += 1
        return self._cards[self._iter_index - 1]

suits = 'HCDS '
ranks = 'A23456789TJQKX'
suit_names = ['Hearts', 'Clubs', 'Diamonds', 'Spades', None]
rank_names = ['Ace', 'Two', 'Three', 'Four', 'Five', \
                'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', \
                'Queen', 'King', 'Joker']
# Unit tests
if __name__ == '__main__':
    import unittest
    import test_stack
    import test_card
    import test_game
    card_suite = unittest.TestLoader().loadTestsFromTestCase(test_card.TestCardCreation)
    stack_suite = unittest.TestLoader().loadTestsFromTestCase(test_stack.TestStack)
    game_suite = unittest.TestLoader().loadTestsFromTestCase(test_game.TestGame)

    unittest.TextTestRunner(verbosity=2).run( \
            unittest.TestSuite([card_suite, stack_suite, game_suite]))
