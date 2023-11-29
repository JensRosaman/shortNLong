import random
import itertools
import requests
from typing import List






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

    def __hash__(self) -> int:
        return self._point_value

class Deck:
    """Represents the deck on the table  """
    def __init__(self) -> None:

        # creates the deck where each item is a card object
        self._create_deck_()
        self.completeDeck = self.deck # saves for later
        # creates played card deck and plays a starting card
        self.init_new_round()


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

    def remove_card(self, cardsToRemove:list = None, top=False) -> Card:
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
        self.declared = {"runs": [], "sets": []} # dict of all the declared cards
        self.completedRuns = []
        self.completedSets = []

    # ------------------------------------- Win conditions ----------------------------------------------------------

    def __3_of_a_kind__(self,getSets=True, getCount=False) -> None:
        """Gives the amount of 3 of a kinds in the instances hand"""
        rank_counts = {}
        cards_by_rank = {}  # A dictionary to store cards for each rank

        for card in self.hand:
            rank = card._rank
            if rank in rank_counts: #räknar antal av varje rank
                rank_counts[rank] += 1
            else:
                rank_counts[rank] = 1
                cards_by_rank[rank] = [card]
            cards_by_rank[rank].append(card)

        # Check if there are at least two ranks with three cards each
        set_count = 0
        sets = []
        for rank, cards in cards_by_rank.items():
            if len(cards) >= 3:
                set_count += 1
                sets.append(cards)

        # dublicates removing
        ids = set([id(card) for card in list(itertools.chain.from_iterable(sets))])
        for i in range(len(sets)):
            lst = sets[i]
            for card in lst:
                if id(card) in ids:
                    ids.remove(id(card))
                else:
                    sets[i].remove(card)

        # tar bort de sets som hade dubbletter
        sets = [lst for lst in sets if len(lst) >= 3]

        self.set_count = set_count
        self.completedSets = sets

        if getSets and getCount:
            return sets, set_count
        elif getSets:
            return sets
        elif getCount:
            return set_count

    def __run_of_four__(self) -> (int, List[List[Card]]):
        """Returns the amount of runs of fours in hand along with sorted runs"""
        # sorting each card in hand by their suit
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


        # skips the suits where they are not long enough to make a run
        for suit_list in sorted_hand:
            if len(suit_list) <= 0:
                continue
            else:
                suit_list = sorted(suit_list, key=lambda card: (card._rank_value, card._suit_value))
                for i in range(1, len(suit_list)):
                    # Check if the current card forms a run with the previous card
                    if (
                        (suit_list[i]._rank_value == suit_list[i - 1]._rank_value + 1) or #om i värde är en mer än förgående
                        (suit_list[i]._rank_value == 2 and suit_list[i - 1]._rank_value == 1) 
                    ) or (
                        suit_list[i]._rank_value == 13 and suit_list[0]._rank_value == 1
                    ):
                        if suit_list[i]._rank_value == 13 and suit_list[0]._rank_value == 1:
                            consecutive_count += 2
                        else:
                            consecutive_count += 1
                        if consecutive_count == 4:
                            run_count += 1
                            # Store the run as a list of card instances
                            run = [suit_list[i - 3], suit_list[i - 2], suit_list[i - 1], suit_list[i]]
                            runs.append(run)
                
                    else:
                        consecutive_count = 1

        self.run_count = len(runs)
        self.completedRuns = runs
        return runs




    def __complete_hand__(self ):
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
                
        elif self.round == 5:
            if self.run_count > 0 and self.set_count > 1 and ((max([len(i) for i in self.completedSets]) +  max([len(i) for i in self.completedRuns]))) - self.hand < 2:
                self.complete_hand = True

        elif self.round > 5:
            raise Exception("För hög round i complete_hand")
        else:
            raise Exception("Ej integer i round")
        return self.complete_hand

    def add_card(self, cards_to_add: list):
        """Adds a card to the deck and checks for win conditions"""
        if not isinstance(cards_to_add, list):
            cards_to_add = [cards_to_add]
        self.hand += cards_to_add
        self.__complete_hand__()
    
    def remove_id(self, cardToRemove: Card):
        """Removes a card from the hand based on its memory adress"""
        self.hand = [card for card in self.hand if id(card) != id(cardToRemove)]
    def get_score(self):
        """Adds upp the total score of the players hand"""
        score = 0
        for card in self.hand:
            score += card._point_value
        return score
    
    def declare_hand(self) -> dict[str, List[Card]]:
        """Declares the hand and removes the card"""
        # Get the affected cards 
        runs = self.__run_of_four__()
        sets = self.__3_of_a_kind__()
        if self.round == 1:
            # two 3's
            for i in range(2):
                self.declared["sets"].append(sets[i])
                for j in range(len(sets[i])):
                    card = sets[i][j]
                    self.remove_id(cardToRemove=card)
                    #del self.hand[self.hand.index(card)]

        elif self.round == 2:
            # 3 n run
            self.declared["runs"].append(runs[0])
            for card in runs[0]:
                self.remove_id(cardToRemove=card)

            self.declared["sets"].append(sets[0])
            for card in sets[0]:
                self.remove_id(cardToRemove=card)

        elif self.round == 3:
            # two runs
            for i in range(2):
                self.declared["runs"].append(runs[i])
                for card in runs[i]:
                    self.remove_id(cardToRemove=card)
           
        elif self.round == 4:
            # 3 st 3
            for i in range(3):
                self.declared["sets"].append(sets[i])
                for card in sets[i]:
                    self.remove_id(cardToRemove=card)
        
        return self.declared

    def valid_in_declared_run(self,card:Card) -> bool:
        """Checks if the given Card is valid to add in a declared run"""
        for run in self.declared["runs"]:
            if (
                ((card._rank_value == run[-1]._rank_value + 1) and run[-1]._rank_value != 1) or
                (card._rank_value == run[0]._rank_value - 1)):

                return True
        else:
            return False
       
        

    def start_new_round(self, round, cards):
        """Starts a new round by reseting all values"""
        self.hand = cards
        self.complete_hand = False
        self.round = round
        self.set_count = 0
        self.run_count = 0 
        self.turn = False
    

# -------------------------------------------------------------------------------------------------------


class HumanAgent:
    def __init__(self, agentID:int) -> None:
        self.human = True
        self.agentID = agentID
        self.isHuman = True

    def __hash__(self) -> int:
        return self.agentID
    
    def __repr__(self) -> str:
        return f"HumanAgent({self.agentID})"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Agent):
            return self.agentID == other.agentID
        return False
    


# -------------------- Agent requests
    def request_declare(self, state:dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        print(state)
        ans = input(f"u wnna declare your cards? y/n p{self.agentID}")
        if ans:
            return True
        else:
            return False

    def request_card2Play(self, state:dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        print(f"State: {state}")
        ans = input(f"{self.agentID} Vilket kort vill du lägga (skriv index) {state['hand']}")
        return int(ans)

    def request_take_discard(self, state:dict) -> bool:
        """Gets state of the game and returns ans"""
        
        if self.isHuman:
            print(f"Current state is {state}")
            ans = input(f"{self.agentID}Ta kortet från discard? any key for yes")
            if ans:
                return True


            # -------------------------------------------------------------------------
        
class Agent:
    """ serves as the template to create other agent classes of"""
    def __init__(self, agentID:int) -> None:
        self.agentID = agentID

    def __hash__(self) -> int:
        return self.agentID
    
    def __repr__(self) -> str:
        return str(self.agentID)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def request_declare(self, state:dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        pass

    def request_card2Play(self, state:dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        pass        
    def request_take_discard(self, state:dict) -> bool:
        """Gets state of the game and returns ans"""
        

# playerId är objekt för att repsentera den som ger instruktioner till spel modulen

class Game:
    """Handles all the internal logic of the game"""
    def __init__(self, playerIDS: list, guiActive = False) -> None:
        self.numOfPlayers = len(playerIDS)
        self.playerIDs = playerIDS
        self.deck = None
        self.players = {}
        self._playOrder = []
        self.discardDeck = []
        self.round = 0
        self.currentPlayer = None
        self.declaredCards = {}
        self.guiActive = guiActive
        self.guiAgents = [agent.agentID for agent in self.playerIDs if "guiAgent" in agent.__dict__]
        
    def start_game(self):
        """Starts the gameplay loop"""
        # assing value to players list and start first round
        self.deck = Deck()
        self._hand_out_cards(6)
    
        # laying out starting cards
        self.discardDeck.append(self.deck.remove_card([self.deck.deck[-1]]))
        print(f"Game started, current laying card is {str(self.discardDeck[-1])}. Gameplay order is {self._playOrder} \n {self.players}")

        # start of gameplay loop
        self._playOrder = list(self.players)
        gameLoop = True
        while gameLoop:
            # Loops through the players, two for loops so each player takes turns starting
            for i in self._playOrder:
                self.round += 1 # next turn starting
                for k, l in self.players.items():
                    l.turn = self.round
                # Gameplay loop for the diffrent rounds
                notStopped = True
                while notStopped: 
                    for agentOfCurrentPlayer in self._playOrder: # i is the agent obj of the current player
                        self.currentPlayer = self.players[i] # indexs players after the id - gives the player object of the current player
                        self.currentPlayer.turn = True
                        current_player_index = self._playOrder.index(agentOfCurrentPlayer)
                        
                        while True: # loops until no one picks from discard or the players whos turn it is picks a card
                            # -------------------checks if anyone wants to pick from discard
                            agentsRequests = {}
                            if len(self.discardDeck) <= 0:
                                break # cant take from empty deck
                            for agent in self.players:
                                state = self.get_current_state(playerId=agent)
                                useraction = agent.request_take_discard(state)
                                if useraction: # if the user wants to take the card
                                    agentsRequests[agent] = useraction
                                
                            if agentsRequests: # if an agent has requested to take from discard
                                # Sort the players in agentsRequests based on their proximity to the current player and get the first next in line player
                                # ask chatgpt cuz idfk
                                agentToPick = sorted(agentsRequests.keys(), key=lambda player: (self._playOrder.index(player) - current_player_index) % self.numOfPlayers)[0]
                                # if it isn't playerTopPicks turn - give penalty and loop again
                                if not (agentOfCurrentPlayer == agentToPick):
                                    # hands cards to the penalized player
                                    self._take_discard(self.players[agentToPick])
                                elif agentOfCurrentPlayer == agentToPick:
                                    self.currentPlayer.add_card(self.discardDeck[-1])
                                    self.currentPlayer.takenCard = True
                            else: # No agent picks from discard - proceed to their turn
                                break

                        # start of the turn of the current player - starts when picking up a card

                        if not self.currentPlayer.takenCard:
                            self.currentPlayer.add_card(self.deck.remove_card(top=True)) # takes the top card of the deck n adds it to hand
                            self.currentPlayer.takenCard = True
                        stateOfPlayer = self.get_current_state(i) # updates the current state for the current player
                        
                        # check if want to declaren
                        if self.currentPlayer.__complete_hand__():
                            if agentOfCurrentPlayer.request_declare(stateOfPlayer):
                                self.currentPlayer.declare_hand()
                                self.declaredCards[agentOfCurrentPlayer] = self.currentPlayer.declared
                                print(f"{agentOfCurrentPlayer} deklarerar")
                        if len(self.declaredCards) > 1:
                            agentOfCurrentPlayer.request_lay_cards()
                        
                        # request what card to play n play it
                        cardToPlay = agentOfCurrentPlayer.request_card2Play(state=stateOfPlayer)
                        self.discardDeck.append(self.currentPlayer.hand[cardToPlay])
                        if len(self.currentPlayer.hand) <= 0 and len(self.currentPlayer.declared) > 0:
                            print(agentOfCurrentPlayer, " vann börjar nästa runda")
                            continue
                        self.currentPlayer.takenCard = False

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
    
    def _take_discard(self, playerToPenalize: Player):
        """
        Gives the player object a penalty card
            positionInStack - the index of the wanted card, 
        """
        penaltyCard = self.deck.remove_card(top=True)
        playerToPenalize.add_card(penaltyCard) # tar översta kortet från högern och lägger till i handen
        playerToPenalize.add_card(self.discardDeck.pop(-1))

    def declare_hand(self, playerToDeclare) -> None:
        """Declares the hand of the given player"""
        declaredCards = playerToDeclare.declare_hand()
        self.declaredCards[playerToDeclare] = declaredCards

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
    
    def reset_game(self, startAfter:bool):

        for p in self.players:
            p.reset()
        self.deck = None
        self.players = {}
        self._playOrder = []
        self.discardDeck = []
        self.round = 0
        self.currentPlayer = None
        self.declaredCards = {}


        self.start_game()
            
    def get_current_state(self, playerId) -> dict: # taken card represents if the player has taken a card yet at the beginging of a turn
        """Collects all the current game information avalible to the player"""
        requestingPlayer = self.players[playerId] # indexes the players dict for the instance of the requested player
        self.state = {
            "discard": self.discardDeck,#list[card]
            "round": self.round,#int
            "winConditions": self.current_win_conditions(),#dict
            "playOrder": self._playOrder,# list[Player]
            "currentPlayer": self.currentPlayer,# player
            "isCurrentPlayer": self.currentPlayer == requestingPlayer, # bool
            "hand": requestingPlayer.hand, # list[Card]
            "winner": False,#bool
            "currentScore": requestingPlayer.get_score(),#int
            "takenCard": requestingPlayer.takenCard, #bool
            "hasCompleteHand": requestingPlayer.__complete_hand__(), #bool
            "runCount": requestingPlayer.run_count, # int
            "setCount": requestingPlayer.set_count, # int
            "completeSets": requestingPlayer.completedSets, #list[Card]
            "completeRuns": requestingPlayer.completedRuns, # list[Card]
            "declaredCards": {player.ID: self.declaredCard[player] for player in self.declaredCards},

        }
        return self.state

    def send_state(self):
        """sends a post http to the server with the game state"""
        # no gui active return nothing
        if not self.guiActive:
            return

        url = "http://192.168.0.17:5000/game_state"
        response = requests.post(url=url, data=self.get_game_state())
        if not response.ok:
            print(response.text)
            raise Exception("Bad post answer to app.py")
        return

    def get_game_state(self):
        """Creates an overarching game state that represents the whole game suitable for a flask implenetation"""
        return {"bob": 3}
        state = {
            "playerHands" : {playerID: [str(card) for card in self.players[playerID].hand] for playerID in self.playerIDs},
            "currentPlayerID" : self.currentPlayer.id,
            "playOrder": self._playOrder,
            "round": self.round,
            "winConditions": self.current_win_conditions(),
            "declaredCards":  {player.ID: self.declaredCard[player] for player in self.declaredCards},
            "playerScores": {player.ID: player.get_score() for player in self.players},
            "guiAgents": self.guiAgents,

        }
        return state







if __name__ == "__main__":
    pass