from flask import Flask, request, jsonify
app = Flask(__name__)


# Endpoint to start a new game
@app.route('/', methods=['get'])
def start_game():
    return jsonify({'game_id': '12345'})


def game():
    class Player:
        def __init__(self,player_id,cards):
            self.hand = cards
            self.id = player_id
            self.complete_hand = False
            self.round = 1

            self.set_count = 0
            self.run_count = 0

        # ----------Win conditions ----------------

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


















