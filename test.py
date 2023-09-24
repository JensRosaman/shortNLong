class Player:
    def __init__(self, name):
        self.name = name

    def request_action(self):
        if self.name != "Bob":
            return {"takeCard": True}
        else:
            return {"takeCard": False}

    def __repr__(self) -> str:
        return self.name
    
class Game:
    def __init__(self):
        self.players = [Player("Alice"), Player("Bob"), Player("Charlie"), Player("David")]
        self.currentPlayer = self.players[0]

    def get_current_state(self, player):
        # Replace with your state retrieval logic
        return {"player": player.name}

    def simulate_game(self):
        # Initialize player_order
        player_order = self.players

        print(self.players, "is the order")
        # Find the index of the current player
        current_player_index = player_order.index(self.currentPlayer)

        # Calculate the number of players
        num_players = len(player_order)

        # Simulate agent requests (for illustration, all agents request to take a card)
        agentsRequests = {}
        for player in self.players:
            state = self.get_current_state(player)
            useraction = player.request_action()
            if useraction['takeCard']:
                agentsRequests[player] = useraction

        if agentsRequests:
            # Sort players based on their proximity to the current player
            sorted_agents_requests = sorted(agentsRequests.keys(), key=lambda player: (player_order.index(player) - current_player_index) % num_players)

            print(sorted_agents_requests)
            

if __name__ == "__main__":
    game = Game()
    game.simulate_game()
