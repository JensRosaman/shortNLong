import random
import copy
import itertools
from flask import Flask





### To do!
# check over the remove card functions shit is wonky fr fr
# expand upon the agent class and edit it to be in line with new gameplay loop

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
        """Compares two diffrent instance cards"""
        if isinstance(other, Card):
            return (self._rank_value, self._suit_value) == (other._rank_value, other._suit_value)
        else:
            raise TypeError("Cannot compare Card to unknown type %s" % other.__class__)


class Deck:
    """Represents the deck on the table  """
    def __init__(self) -> None:

        # creates the deck where each item is a card object
        self._create_deck_()
        self.completeDeck = self.deck # saves for later
        # creates played card deck and plays a starting card
        self.init_new_round()

    # old unefficant method 
    """
    def _create_deck_(self) -> None:
        '''Creates a deck and shuffles'''
        self.deck = []
        suits = 'HCDS'
        ranks = 'A23456789TJQK'
        for i in range(2):
            for suit in suits:
                for rank in ranks:
                    code = suit + rank
                    self.deck.append(Card(code))
    """

    # more efficant version using itertools
    def _create_deck_(self) -> None:
        """Creates a deck and shuffles"""
        suits = 'HCDS'
        ranks = 'A23456789TJQK'
        # Use itertools.product to generate all card combinations
        all_cards = [''.join(card) for card in itertools.product(suits, ranks)]
        
        # Duplicate the cards and store them in the deck
        self.deck = [Card(code) for code in all_cards * 2]
        
        # Shuffle the deck
        random.shuffle(self.deck)

    def remove_card(self, cardsToRemove:list = None, top=False) -> None:
        """
        Removes a card from the deck and returns the item
        i - index to remove
        """
        
        if cardsToRemove is not None:
            popped = []
            for item in cardsToRemove:
                popped.append(self.deck.pop(self.deck.index(item)))
            return popped
        elif top:
            return self.deck.pop(-1)

    
    def hand_out_cards(self,playerAmount,cardAmount) -> list:
        """Removes cards from the deck and returns a list of lists with each players hand"""
        playerHands = []
        for player in range(playerAmount):
            cardsToGive = self.remove_card(self.deck[:cardAmount])
            playerHands.append(cardsToGive)
        return playerHands

    def init_new_round(self):
        """Creates a new round by res"""
        random.shuffle(self.deck)
        # removes the top cards and assigns it to the played deck

# _______________________________________________________________________________________________


class Player:
    """Handles all action related to a specific player and their hand"""
    def __init__(self, player_id, cards:list):
        self.hand = cards
        self.id = player_id
        self.complete_hand = False
        self.round = 1
        self.set_count = 0
        self.run_count = 0 
        self.turn = False
        self.takenCard = False

    # ------------------------------------- Win conditions ----------------------------------------------------------

    def __3_of_a_kind__(self) -> None:
        """Gives the amount of 3 of a kinds in the instances hand"""
        rank_counts = {}
        for card in self.hand:
            rank = card._rank
            if rank in rank_counts:
                rank_counts[rank] += 1
            else:
                rank_counts[rank] = 1

        # Check if there are at least two ranks with three cards each
        set_count = 0
        for count in rank_counts.values():
            if count >= 3:
                set_count += 1
        self.set_count = set_count

    def __run_of_four__(self) -> None:
        """Returns the amount of runs of fours in hand"""
        # Create a set to store the unique ranks in the hand
        unique_ranks = set(card._rank for card in self.hand)
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

        # Iterate through the ranks and check if there is a sequence of four consecutive ranks
        for rank in ranks:
            if all(rank in unique_ranks for rank in ranks[ranks.index(rank):ranks.index(rank) + 4]):
                self.run_count += 1

    def __complete_hand__(self, round:int ):
        self.round = round
        self.__3_of_a_kind__()
        self.__run_of_four__()
        if self.round == 1:
            if self.set_count >= 3:
                self.complete_hand = True
                
            else:
                self.complete_hand = False
        
        elif self.round == 2:
            if self.set_count >= 1 and self.run_count >= 1:
                self.complete_hand = True
                
        elif self.round == 3:
            if self.run_count >= 2:
                self.complete_hand = True
                
        elif self.round == 4:
            if self.set_count >= 3:
                self.complete_hand = True
                
        else:
            pass
        return self.complete_hand

    def add_card(self, cards_to_add: list):
        """Adds a card to the deck and checks for win conditions"""
        if not type(cards_to_add) == list:
            cards_to_add = [cards_to_add]
        self.hand += cards_to_add
        self.__complete_hand__()

    def get_score(self):
        """Adds upp the total score of the players hand"""
        score = 0
        for card in self.hand:
            score += card._point_value

    def start_new_round(self, round, cards):
        """Starts a new round by reseting all values"""
        self.hand = cards
        self.complete_hand = False
        self.round = round
        self.set_count = 0
        self.run_count = 0 
        self.turn = False

# -------------------------------------------------------------------------------------------------------


class Agent:
    def __init__(self, agentID:int, isHuman: bool) -> None:
        self.human = True
        self.agentID = agentID
        self.isHuman = isHuman

    def __hash__(self) -> int:
        return self.agentID
    
    def __repr__(self) -> str:
        return str(self.agentID)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Agent):
            return self.agentID == other.agentID
        return False
    

    def request_declare(self, state:dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        ans = input(f"u wnna open your cards? y/n p{self.agentID}")
        if ans == "y":
            return True
        else:
            return False

    def request_card2Play(self, state:dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        print(f"State: {state}")
        ans = input("Vilket kort vill du lägga (skriv index)")
        return int(ans)

    def request_take_discard(self, state:dict) -> bool:
        
        

    def request_action(self, state:dict):
        """Gets the state of the game and returns an answer to the game class"""
        
        agentAction = { # Agent action represents the agents action
            "takeCard": None, # bool if taking card
            "takeFromDiscard": None,
            "indexToTakeFrom": None,

        }
        if self.isHuman: # Checks if it is human player and if input is expected
            print(f"Current state is {state}")

            if state["isCurrentPlayer"] and not state["takenCard"]: # Checks if its the agents turn and have not taken a card
                availableActions = f"""
                1. Take from discard ({state["discard"][-1]})
                2. Take from regular deck
                """
                userAction = input(f"What do you want to do \n {availableActions}")
                if userAction == "1":
                    indexOfWanted = input("Vilket kort bakifrån?")
                    agentAction["takeFromDiscard"] = True
                    agentAction["indexToTakeFrom"] = indexOfWanted
                    agentAction["takeCard"] = True
                    return agentAction
                
            elif state["takenCard"] and state['isCurrentPlayer']: # if player has taken a card and its their turn
                pass

            else:
                raise Exception("Error state does not match current conditions and agent failed to take action")  
            # ------------------------------------------------------------------------- 
        elif not self.isHuman:
            print(f"Current state is {state}")

            if state["isCurrentPlayer"] and not state["takenCard"]: # Checks if its the agents turn and have not taken a card
                pass
            elif state["takenCard"] and state['isCurrentPlayer']: # if player has taken a card and its their turn
                pass
            elif state['isCurrentPlayer']:
                pass
            else:
                availableActions = f"""
                1. Take from discard ({state["discard"][-1]})
                2. Take from regular deck
                """
                userAction = input(f"What do you want to do \n {availableActions}")

                if userAction == "1":
                    indexOfWanted = input("Which card")
                    return {
                        "index" : indexOfWanted
                    }
        

# playerId är objekt för att repsentera den som ger instruktioner till spel modulen

class Game:
    """Handles all the internal logic of the game"""
    def __init__(self, playerIDS: list) -> None:
        self.numOfPlayers = len(playerIDS)
        self.playerIDs = playerIDS
        self.deck = Deck()
        self.players = {}
        self._playOrder = []
        self.discardDeck = []
        self.round = 0
        self.currentPlayer = None

    def start_game(self, playerIDS) -> bool:
        """Starts the gameplay loop"""
     
        # assing value to players list and start first round
        self._hand_out_cards(6)
        self._playOrder = list(self.players)
    
        # laying out starting cards
        self.discardDeck.append(self.deck.remove_card([self.deck.deck[-1]]))
        print(f"Game started, current laying card is {str(self.discardDeck[-1])}. Gameplay order is {self._playOrder} \n {self.players}")

        # start of gameplay loop
        gameLoop = True
        while gameLoop:
            
            # Loops through the players, two for loops so each player takes turns starting
            for i in self._playOrder:
                self.round += 1 # next turn starting
                for i in self._playOrder: # i is the agent obj of the current player
                    agentOfCurrentPlayer = i
                    self.currentPlayer = self.players[i] # indexs players after the id - gives the player object of the current player
                    self.currentPlayer.turn = True
                    current_player_index = self._playOrder.index(self.currentPlayer)
                    

                    while True: # loops until no one picks from discard or the players whos turn it is picks a card
                        # -------------------checks if anyone wants to pick from discard
                        agentsRequests = {}
                        for agent in self.players:
                            state = self.get_current_state(playerId=agent,takenCard=False)
                            useraction = agent.request_action(state)
                            if useraction['takeCard']: # if the user wants to take the card
                                agentsRequests[agent] = useraction
                            
                        if agentsRequests: # if an agent has requested to take from discard
                            #for player in agentsRequests:
                            # Can place for loop here to double check if they want to take with the penalty, now agent dont know the penalty

                            # Sort the players in agentsRequests based on their proximity to the current player and get the first next in line player
                            # ask chatgpt cuz idfk
                            agentToPick = sorted(agentsRequests.keys(), key=lambda player: (self._playOrder.index(player) - current_player_index) % self.numOfPlayers)[0]
                            
                            # if it isnt playerTopPicks turn - give penalty and loop again
                            if not (agentOfCurrentPlayer == agentToPick):
                                # hands cards to the penalized player
                                self._take_discard(self.players[agentToPick])
                            elif agentOfCurrentPlayer == agentToPick:
                                self.currentPlayer.add_card(self.discardDeck[-1])
                                self.currentPlayer.takenCard = True
                        else: # No agent picks from discard - proceed to their turn
                            break

                    # start of the turn of the current player - starts when picking up a card
                    if self.currentPlayer.takenCard:
                        self.currentPlayer.add_card(self.deck.remove_card(top=True)) # takes the top card of the deck n adds it to hand
                    
                    stateOfPlayer = self.get_current_state(i) # updates the current state for the current player
                    
                    # check if want to declare
                    if agentOfCurrentPlayer.request_declare:
                        pass
                    # request what card to play
                    cardToPlay = agentOfCurrentPlayer.request_card2play(state=stateOfPlayer)

                    
                    # cases that define each diffrent 

    def _hand_out_cards(self, cardAmount):
        """Hands out cards to players and creates a playerlist, reset deck!!!"""
        cardsToGive = self.deck.hand_out_cards(playerAmount=self.numOfPlayers, cardAmount=cardAmount)
        # creating index to iterate through the players
        i = 0
        for hand in cardsToGive:
            self.players[self.playerIDs[i]] = Player(player_id=self.playerIDs[i], cards=hand)
            i += 1
            
    def _calculate_penalty(self, positionInStack:int, player:Player):
        """Takes the position of the stack and returns the amount the player has to take"""
        negIndex = positionInStack - len(self.deck.deck)
        cardsOnTop = self.deck.deck[negIndex:]
        penaltyCards = len(cardsOnTop)

        # if its the players turn avoid extra cards
        if player.turn:
           return penaltyCards - 1
        else:
            return penaltyCards
    
    def _take_discard(self, playerToPenalize: Player, positionInStack = None):
        """Gives the player object a penalty card
            positionInStack - the index of the wanted card, 
        """
        penaltyCard = self.deck.remove_card([self.deck[-1]])
        playerToPenalize.add_card([penaltyCard, self.discardDeck[-1]]) # tar översta kortet från högern och lägger till i handen
    
    def current_win_conditions(self):
        """Sets the current win conditions depending on the round"""
        winConditions = {"sets": None, "runs": None}
        if self.round == 1:
            winConditions['sets'] = 2
                
        elif self.round == 2:
            winConditions["sets"] = 1 
            winConditions['runs'] = 1

        elif self.round == 3:
            winConditions["runs"]= 2

        elif self.round == 4:
            winConditions["sets"] = 3
        else:
            raise Exception("No valid round inputed")
        return winConditions
    
    def calculate_points(self,agent= None,player= None):
        """Calculates the points in hand held by the player instance"""
        if agent is None and player is None:
            raise Exception("No arguments given to calculate points, ")
        elif agent is not None and player is None:
            player = self.players[agent]
        elif player is not None:
            pass
        
        return player.get_score()
            
    def get_current_state(self, playerId, takenCard: bool): # taken card represents if the player has taken a card yet at the beginging of a turn
        """Collects all the current game information avalible to the player"""
        requestingPlayer = self.players[playerId] # indexes the players dict for the instance of the requested player
        self.state = {
            "discard": self.discardDeck,
            "round": self.round,
            "winConditions": self.current_win_conditions(),
            "playOrder": self._playOrder,
            "currentPlayer": self.currentPlayer,
            "isCurrentPlayer": self.currentPlayer == requestingPlayer,
            "hand": requestingPlayer.hand,
            "winner": None,
            "currentScore": requestingPlayer.get_score(),
            "situation": takenCard,
            "hasCompleteHand": requestingPlayer.__complete_hand__(self.round),
            "runCount": requestingPlayer.run_count,
            "setCount": requestingPlayer.set_count,
            "takenCard": requestingPlayer.takenCard
        }
        return self.state
    
    
   
if __name__ == "__main__":
    spel = Game([1])
    spel._hand_out_cards(3)
    print(spel.players[1].hand)