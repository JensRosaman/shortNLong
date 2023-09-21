# Define the ranks and suits of the cards
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Create a deck of cards
deck = [{"rank": rank, "suit": suit} for rank in ranks for suit in suits]
print(deck)