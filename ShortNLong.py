import builtins
import random
import itertools
import requests
from typing import List
import json
from Card import Card
debug = False

def print(txt):
    if not debug:
        pass
    builtins.print(txt)
class Deck:
    """Represents the deck on the table  """
    def __init__(self) -> None:

        # creates the deck where each item is a card object
        self._create_deck_()  # declares self.deck
        self.completeDeck = self.deck  # saves for later
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

        if cardsToRemove is not None and not top:
            popped = []
            for item in cardsToRemove:
                popped.append(self.deck.pop(self.deck.index(item)))
            return popped
        elif top:
            return self.deck.pop(-1)
        raise Exception("wack remove_card")

    
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
    def __repr__(self):
        return f"Player({repr(self.id)}, {repr(self.hand)})"

    def __str__(self):
        return f"Agent({self.id})"

    def __hash__(self):
        return int(self.id.agentID)

    def __eq__(self, other):
        if isinstance(other,Player):
            return self.id == other.id
        return False

    def __3_of_a_kind__(self,getSets=True, getCount=False):
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
        sets = [set(lst) for lst in sets]
        sets = [list(st) for st in sets]
        # tar bort de sets som hade dubbletter
        sets = [lst for lst in sets if len(lst) >= 3]

        self.set_count = len(sets)
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
        print(self.hand)
        self.hand = set(self.hand)
        print(self.hand)
        self.hand = list(self.hand)
        print(self.hand)

        self.hand = [card for card in self.hand if card is not None]
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
        self.__run_of_four__()
        runs = self.completedRuns
        self.__3_of_a_kind__()
        sets = self.completedSets

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
        print(f"player {self.id} declares with {self.declared}")
        return self.declared

    def valid_in_declared_run(self,card:Card) -> bool:
        """Checks if the given Card is valid to add in a declared run"""
        for run in self.declared["runs"]:
            if self.valid_in_run(card=card,run=run):
                return True

        return False

    def valid_in_run(self,card,run):
        if (run[0]._suit == card._suit and
                (
                ((card._rank_value == run[-1]._rank_value + 1) and run[-1]._rank_value != 1) or
                    (card._rank_value == run[0]._rank_value - 1)) or
                    (((card._rank_value == 1) and (run[-1]._rank_value == 13)))):
            return True
        return False

    def valid_in_declared_set(self,card) -> bool:
        """Checks if the given Card is valid to add in a declared set"""
        for set in self.declared["sets"]:
            if set[0]._rank == card._rank:
                return True
        else:
            return False

    def lay_card_to_declared(self,card,layToRun) -> dict:
        if layToRun:
            for run in self.declared["runs"]:
                if ((card._rank_value == run[-1]._rank_value + 1) and (run[-1]._rank_value != 1) or# lay to end of run
                        (card._rank_value == 1) and (run[-1]._rank_value == 13)):
                    run.append(card)
                    return self.declared

                elif card._rank_value == run[0]._rank_value - 1: # beginning of run
                    run.insert(0, card)
                    return self.declared
        for set in self.declared["sets"]:
            if set[0]._rank_value == card._rank_value:
                set.append(card)
                return self.declared

        raise Exception("lay card was called but there were no playes to lay to")








    def start_new_round(self, round, cards):
        """Starts a new round by reseting all values"""
        self.hand = cards
        self.complete_hand = False
        self.round = round
        self.set_count = 0
        self.run_count = 0 
        self.turn = False
    

# -------------------------------------------------------------------------------------------------------

# playerId är objekt för att repsentera den som ger instruktioner till spel modulen

class Game:
    """Handles all the internal logic of the game"""
    def __init__(self, playerIDS: list, guiActive = False, appUrl = "http://192.168.0.17:5000/", debugMode = False) -> None:
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
        self.appUrl = appUrl
        self.guiAgents = [agent.agentID for agent in playerIDS if "guiAgent" in agent.__dict__]
        self.playerScores = {}
        self.layMap = {}
        self.winningPlayer = None
        self.turnLimit = 50


    def start_game(self):
        """Starts the gameplay loop"""
        # assing value to players list and start first round
        cardsToHandOut = 6 # cards to hand out every round
        self.layMap = {}
        # start of gameplay loop
        gameLoop = True
        while gameLoop:

            if self.round >= 4:
                print("Game over!")
                return True

            # preparing the game for the next round
            
            self._update_score_table()
            # laying out starting cards
            self._prepare_for_next_round(cardsToHandOut)
            cardsToHandOut += 1

            # updating the turn of each of the players to update their internal logic
            self.round += 1 # next turn starting
            for k, l in self.players.items():
                l.turn = self.round
            turnCounter = 0
            print(f"Round started, current laying card is {str(self.discardDeck[-1])}. Gameplay order is {self._playOrder} \n")
            # Gameplay loop for the different rounds
            notStopped = True
            while notStopped: # Stopping occurs when a player finishes their stick
                if turnCounter > self.turnLimit:
                    break
                # adding one to singify anither turn startin
                turnCounter += 1
                for agentOfCurrentPlayer in self._playOrder: # I am the agent obj of the current player mainloop
                    print(f"new turn starting current player is {agentOfCurrentPlayer.agentID}")
                    self.currentPlayer = self.players[agentOfCurrentPlayer] # indexs players after the id - gives the player object of the current player
                    self.currentPlayer.turn = True
                    self.layMap = self.available_to_lay_cards_to()
                    while True:  # loops until no one picks from discard or the players whose turn it is picks a card
                        # -------------------checks if anyone wants to pick from discard
                        self._check_deck()
                        self.send_state()

                        if len(self.discardDeck) <= 0:
                            print(f"Discard is {self.discardDeck}, ending discard loop")
                            break # cant take from empty deck

                        agentToPick = self.discard_request(
                            current_player_index=self._playOrder.index(agentOfCurrentPlayer))
                        if agentToPick is None:
                            print("no one picks")
                            break

                        elif agentOfCurrentPlayer == agentToPick:
                            if self.currentPlayer.takenCard:  # if player already have picked a card from discard then a penalty folows
                                self.currentPlayer.add_card(self.deck.remove_card(top=True))
                            self.currentPlayer.add_card(self.discardDeck[-1])
                            self.currentPlayer.takenCard = True
                            self.discardDeck.pop(-1)

                        # if it isn't playerTopPicks turn - give penalty and loop again
                        else:
                            # hands cards to the penalized player
                            self._take_discard(playerToPenalize=self.players[agentToPick])
                        print(f"agent {agentToPick.agentID} picks from discard")
                    # end of discard loop
                    self._check_deck()
                    # start of the turn of the current player - starts when picking up a card
                    if not self.currentPlayer.takenCard and len(self.deck.deck) > 0:
                        self.currentPlayer.add_card(self.deck.remove_card(top=True)) # takes the top card of the deck n adds it to hand
                        self.currentPlayer.takenCard = True

                    self.send_state()
                    stateOfPlayer = self.get_current_state(agentOfCurrentPlayer) # updates the current state for the current player

                    # check if we want to declare
                    if self.currentPlayer.__complete_hand__() and not (
                            len(self.currentPlayer.declared["runs"]) > 0 or len(self.currentPlayer.declared["sets"]) > 0
                        ):
                        if agentOfCurrentPlayer.request_declare(stateOfPlayer):
                            self.currentPlayer.declare_hand()
                            self.declaredCards[agentOfCurrentPlayer] = self.currentPlayer.declared
                            print(f"{agentOfCurrentPlayer} deklarerar")
                            self.send_state()

                    elif (len(self.declaredCards) > 1) and (len(self.currentPlayer.declared["runs"]) > 0 or len(self.currentPlayer.declared["sets"]) > 0): # check if i
                        availableLays = self.can_lay_card_to_player(self.currentPlayer)
                        while len(list(availableLays)) > 0:
                            stateOfPlayer = self.get_current_state(agentOfCurrentPlayer)  # updates the current state for the current player
                            print(availableLays)
                            layChoice = agentOfCurrentPlayer.request_lay_cards(stateOfPlayer)  # (agentID
                            print(f"laychoice for {agentOfCurrentPlayer.agentID}  is ",layChoice)
                            self.lay_cards(
                                agentToLayTo=layChoice["agentToLayTo"], cardToLay=layChoice["cardToLay"], layToRun=layChoice["layToRun"], playerLaying=self.currentPlayer
                            )
                            availableLays = self.can_lay_card_to_player(self.currentPlayer)
                            self.send_state()
                    #else:
                        #print(f'complete {self.currentPlayer.__complete_hand__()} , shit in declared: {len(self.currentPlayer.declared["runs"]) > 0 or len(self.currentPlayer.declared["sets"]) > 0}')
                    # request what card to play n play it
                    if (len(self.currentPlayer.declared["runs"]) > 0 or len(self.currentPlayer.declared["sets"]) > 0
                        and len(self.currentPlayer.hand) <= 1
                        ) or (turnCounter > self.turnLimit):
                        if len(self.currentPlayer.hand) == 1:
                            cardToPlay = self.currentPlayer.hand[0]
                            self.discardDeck.append(self.currentPlayer.hand.pop(cardToPlay))
                            self.send_state()
                        print(turnCounter)
                        print(f"Game ended, the winner is {self.currentPlayer}")
                        notStopped = False
                        break

                    cardToPlay = agentOfCurrentPlayer.request_card2Play(state=self.get_current_state(agentOfCurrentPlayer))
                    self.discardDeck.append(self.currentPlayer.hand.pop(cardToPlay))
                    self.send_state()
                    self.currentPlayer.takenCard = False


                    # next round starting
# ---------------------------------------------------------------------------------------------


    def _prepare_for_next_round(self, cardsToHandOut):
        self.deck = Deck()
        self.discardDeck.append(self.deck.remove_card(top=True))
        self._hand_out_cards(cardsToHandOut)

    def _update_score_table(self):
        # first time the table is updated aka first round
        if len(self.playerScores) == 0:
            self.playerScores = {agent: 0 for agent in self.playerIDs}
        else:
            for agent in self.playerIDs:
                self.playerScores[agent] += self.calculate_points(player=self.players[agent])
        if self.round > 1:
            self._playOrder.append(self._playOrder.pop(0))
        else:
            for agent in self.playerIDs:  # creating player instances
                self.players[agent] = Player(player_id=agent, cards=[])
            self._playOrder = list(self.players)

    def discard_request(self,current_player_index):
        """Requests an action from all the agents and returns the agent to pick"""
        askingOrder = self._playOrder[current_player_index:] + self._playOrder[:current_player_index]
        print(askingOrder)
        for agent in askingOrder:
            state = self.get_current_state(playerId=agent)

            if agent.request_take_discard(state):  # if the user wants to take the card
                return agent
        return None


    def _hand_out_cards(self, cardAmount):
        """Hands out cards to players and creates a playerlist, reset deck!!!"""
        cardsToGive = self.deck.hand_out_cards(playerAmount=self.numOfPlayers, cardAmount=cardAmount)
        # creating index to iterate through the players
        i = 0

        for agent, player in self.players.items():
            player.hand = cardsToGive[i]
            i += 1

    def _check_deck(self):
        """Checks if the deck is empty and if it is, assigns the deck to the discard"""
        if len(self.deck.deck) <= 0 < len(self.discardDeck):
            self.deck.deck = [card for card in self.discardDeck][::-1]
            self.discardDeck = []

    def _calculate_penalty(self, positionInStack:int, player:Player):
        """Takes the position of the stack and returns the amount the player has to take"""
        negIndex = positionInStack - len(self.deck.deck)
        cardsOnTop = self.deck.deck[negIndex:]
        penaltyCards = len(cardsOnTop)

        # if it's the players turn avoid extra cards
        if player.turn:
           return penaltyCards - 1
        else:
            return penaltyCards
    
    def _take_discard(self, playerToPenalize: Player):
        """
        Gives the player object a penalty card
            positionInStack - the index of the wanted card, 
        """
        print(playerToPenalize)

        penaltyCard = self.deck.remove_card(top=True)
        playerToPenalize.add_card(penaltyCard) # tar översta kortet från högern och lägger till i handen
        playerToPenalize.add_card(self.discardDeck.pop(-1))

    def declare_hand(self, playerToDeclare) -> None:
        """Declares the hand of the given player"""
        declaredCards = playerToDeclare.declare_hand()
        self.declaredCards[playerToDeclare] = declaredCards

    def can_lay_card_to_player(self,playerToCheck):
        """Checks all the declared cards on the table and gives if the given player can lay a card there """
        validLays = {agent:{"runs":[],"sets":[]} for agent in self.players}

        # setting defualt values so the final dict is set
        for agent in validLays:
            if agent not in self.declaredCards:
                validLays[agent]["runs"] = None
                validLays[agent]["sets"] = None
        for agent in self.declaredCards:
            player = self.players[agent]
            for card in playerToCheck.hand:
                if player.valid_in_declared_run(card):
                    validLays[agent]["runs"].append(card)
                if player.valid_in_declared_set(card):
                    validLays[agent]["sets"].append(card)

            if len(validLays[agent]["runs"]) < 1:
                validLays[agent]["runs"] = None
            if len(validLays[agent]["sets"]) < 1:
                validLays[agent]["sets"] = None

        return {agent: {"runs": [card for card in validLays[agent]["runs"]],"sets": [card for card in validLays[agent]["sets"] ]} for agent in validLays if (validLays[agent]["runs"]) is not None and (len(validLays[agent]["runs"]) > 0 or (validLays[agent]["sets"] is not None and len(validLays[agent]["sets"]) > 0))}

    def card_valid_in_declared(self,card):
        for agent in self.declaredCards:
            player = self.players[agent]
            if player.valid_in_declared_run(card) or player.valid_in_declared_set(card):
                return True
        return False

    def available_to_lay_cards_to(self):
        """Creates a dict with each agent and the players it can lay cards to
        Return agentThatCanLay:{agentThatItcanLayTo:"runs":[],"sets":[]}
        """
        possible_lays = {
            #agent.agentID: #agent:{"runs":[],"sets":[]}} for agent in self.declaredCards
        }
        for agent in self.declaredCards:
            player = self.players[agent]
            possible_lays[agent] = self.can_lay_card_to_player(player)

        return possible_lays

    def lay_cards(self,agentToLayTo,layToRun: bool, playerLaying: Player, cardToLay: Card):
        """Removes the available card and lays it to a declared run/set"""
        playerToLayTo = self.players[agentToLayTo]
        self.declaredCards[agentToLayTo] = playerToLayTo.lay_card_to_declared(card=cardToLay,layToRun=layToRun)
        playerLaying.hand.remove(cardToLay)

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
        elif self.round == 5:
            winConditions["sets"] = 2
            winConditions["runs"] = 1

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

        for a, p in self.players:
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
        """Collects all the current game information available to the player"""
        requestingPlayer = self.players[playerId] # indexes the players dict for the instance of the requested player
        availableToLayTo = self.can_lay_card_to_player(requestingPlayer)
        """
        state = {
            state = {
            "discard": [str(card) for card in self.discardDeck],  # list[str]
            "round": self.round,  # int
            "winConditions": self.current_win_conditions(),  # dict
            "playOrder": [agent.agentID for agent in self._playOrder],
            "currentPlayer": self.currentPlayer,  # player
            "isCurrentPlayer": self.currentPlayer == requestingPlayer,  # bool
            "hand": requestingPlayer.hand,  # list[Card]
            "winner": False,  # bool
            "currentScore": requestingPlayer.get_score(),  # int
            "takenCard": requestingPlayer.takenCard,  # bool
            "hasCompleteHand": requestingPlayer.__complete_hand__(),  # bool
            "runCount": requestingPlayer.run_count,  # int
            "setCount": requestingPlayer.set_count,  # int
            "completeSets": [str(card) for card in requestingPlayer.completedSets],  # list[str]
            "completeRuns": [str(card) for card in requestingPlayer.completedRuns],  # list[str]
            "declaredCards":  {agent.agentID: self.declaredCards[agent] for agent in self.declaredCards},
            "playerScore": self.calculate_points(player=requestingPlayer),
            "availableToLayTo": availableToLayTo #{agent.agentID: {"runs": str([availableToLayTo[agent]["runs"]]),"sets": str([availableToLayTo[agent]["sets"]])} for agent in availableToLayTo}
        }
        """

        state = {
            "discard": self.discardDeck,  # list[card]
            "round": self.round,  # int
            "winConditions": self.current_win_conditions(),  # dict
            "playOrder": self._playOrder,  # list[Player]
            "currentPlayer": self.currentPlayer,  # player
            "isCurrentPlayer": self.currentPlayer == requestingPlayer,  # bool
            "hand": requestingPlayer.hand,  # list[Card]
            "winner": False,  # bool
            "currentScore": requestingPlayer.get_score(),  # int
            "takenCard": requestingPlayer.takenCard,  # bool
            "hasCompleteHand": requestingPlayer.__complete_hand__(),  # bool
            "runCount": requestingPlayer.run_count,  # int
            "setCount": requestingPlayer.set_count,  # int
            "completeSets": requestingPlayer.completedSets,  # list[Card]
            "completeRuns": requestingPlayer.completedRuns,  # list[Card]
            "declaredCards": {player: self.declaredCards[player] for player in self.declaredCards},
            "playerScore": self.calculate_points(player=requestingPlayer),
            "availableToLayTo": availableToLayTo,
            "discardValidInDeclared": False

        }
        if len(self.discardDeck) > 0 and len(self.declaredCards) > 0:
            state["discardValidInDeclared"] = self.card_valid_in_declared(self.discardDeck[-1])
        return state

    def send_state(self):
        """sends a post http to the server with the game state"""
        # no gui active return nothing
        if not self.guiActive:
            return
        url = self.appUrl + "game_state"
        state = self.get_game_state()
        data = json.dumps(state)
        response = requests.post(url=url, data=data, headers={'Content-Type': 'application/json'})
        if not response.ok:
            print(response.text)
            raise Exception("Bad post answer to app.py")
        return

    def get_game_state(self):
        """Creates an overarching game state that represents the whole game suitable for a flask implementation"""
        state = {
            "playerHands" : {playerID.agentID: [str(card) for card in self.players[playerID].hand] for playerID in self.playerIDs},
            "currentPlayer": self.currentPlayer.id.agentID,
            "playOrder": [agent.agentID for agent in self._playOrder],
            "round": self.round,
            "winConditions": self.current_win_conditions(),
            "declaredCards": {agent.agentID: {"runs":[[str(card) for card in cardList] for cardList in self.declaredCards[agent]["runs"]],
                                              "sets":[[str(card) for card in cardList] for cardList in self.declaredCards[agent]["sets"]]}
                              for agent in self.declaredCards}, #{agent.agentID: str(card) for card in list for list in self.declaredCards[agent] for agent in self.declaredCards},
            "playerScores": {agent.agentID: self.players[agent].get_score() for agent in self.players},
            "guiAgents": self.guiAgents,
            "discardDeck": [str(card) for card in self.discardDeck]

        }

        return state






if __name__ == "__main__":
    pass