def start_game(self):
    """Starts the gameplay loop"""
    # assing value to players list and start first round
    self.deck = Deck()
    self._hand_out_cards(6)

    # laying out starting cards
    self.discardDeck.append(self.deck.remove_card([self.deck.deck[-1]]))
    print(
        f"Game started, current laying card is {str(self.discardDeck[-1])}. Gameplay order is {self._playOrder} \n {self.players}")

    # start of gameplay loop
    self._playOrder = list(self.players)
    gameLoop = True
    while gameLoop:
        # Loops through the players, two for loops so each player takes turns starting
        for i in self._playOrder:
            self.round += 1  # next turn starting
            for k, l in self.players.items():
                l.turn = self.round
            # Gameplay loop for the diffrent rounds
            notStopped = True
            while notStopped:  # Stopping occurs when a player finnishes their stick
                for agentOfCurrentPlayer in self._playOrder:  # i is the agent obj of the current player
                    self.currentPlayer = self.players[
                        i]  # indexs players after the id - gives the player object of the current player
                    self.currentPlayer.turn = True
                    current_player_index = self._playOrder.index(agentOfCurrentPlayer)

                    while True:  # loops until no one picks from discard or the players whos turn it is picks a card
                        # -------------------checks if anyone wants to pick from discard
                        agentsRequests = {}
                        self.send_state()

                        if len(self.discardDeck) <= 0:
                            break  # cant take from empty deck
                        for agent in self.players:
                            state = self.get_current_state(playerId=agent)
                            useraction = agent.request_take_discard(state)
                            if useraction:  # if the user wants to take the card
                                agentsRequests[agent] = useraction

                        if agentsRequests:  # if an agent has requested to take from discard
                            # Sort the players in agentsRequests based on their proximity to the current player and get the first next in line player
                            # ask chatgpt cuz idfk
                            agentToPick = sorted(agentsRequests.keys(), key=lambda player: (self._playOrder.index(
                                player) - current_player_index) % self.numOfPlayers)[0]
                            # if it isn't playerTopPicks turn - give penalty and loop again
                            if not (agentOfCurrentPlayer == agentToPick):
                                # hands cards to the penalized player
                                self._take_discard(self.players[agentToPick])
                            elif agentOfCurrentPlayer == agentToPick:
                                self.currentPlayer.add_card(self.discardDeck[-1])
                                self.currentPlayer.takenCard = True
                        else:  # No agent picks from discard - proceed to their turn
                            break

                    # start of the turn of the current player - starts when picking up a card
                    if not self.currentPlayer.takenCard:
                        self.currentPlayer.add_card(
                            self.deck.remove_card(top=True))  # takes the top card of the deck n adds it to hand
                        self.currentPlayer.takenCard = True
                        self.send_state()

                    stateOfPlayer = self.get_current_state(i)  # updates the current state for the current player

                    # check if want to declaren
                    if self.currentPlayer.__complete_hand__():
                        if agentOfCurrentPlayer.request_declare(stateOfPlayer):
                            self.currentPlayer.declare_hand()
                            self.declaredCards[agentOfCurrentPlayer] = self.currentPlayer.declared
                            print(f"{agentOfCurrentPlayer} deklarerar")
                            self.send_state()

                    if len(self.declaredCards) > 1 and (len(self.currentPlayer.declared["runs"]) > 0 or len(
                            self.currentPlayer["sets"]) > 0):  # check if i
                        agentOfCurrentPlayer.request_lay_cards()
                        self.send_state()

                    # request what card to play n play it
                    cardToPlay = agentOfCurrentPlayer.request_card2Play(state=stateOfPlayer)
                    self.discardDeck.append(self.currentPlayer.hand[cardToPlay])
                    self.send_state()
                    self.currentPlayer.takenCard = False
                    # next round starting