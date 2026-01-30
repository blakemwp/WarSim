"""
Player class for the War card game.
"""

import random
from card import display_hand


def shuffle_string(s: str) -> str:
    """Randomly shuffles the characters in a string."""
    chars = list(s)
    random.shuffle(chars)
    return ''.join(chars)


class Player:
    """Represents a player in the War card game."""
    
    def __init__(self, name: str, hand: str):
        self.name = name
        self.hand = hand        # Current cards to play from
        self.collection = ""    # Won cards waiting to be shuffled into hand
    
    def total_cards(self) -> int:
        """Returns total cards (hand + collection)."""
        return len(self.hand) + len(self.collection)
    
    def has_cards(self) -> bool:
        """Returns True if player has any cards left."""
        return self.total_cards() > 0
    
    def refill_hand(self):
        """Shuffles collection into hand when hand is empty."""
        if len(self.hand) == 0 and len(self.collection) > 0:
            self.hand = shuffle_string(self.collection)
            self.collection = ""
            print(f"  >> {self.name} shuffles their collection into a new hand: {display_hand(self.hand)}")
    
    def draw_card(self) -> str | None:
        """Draws a card from hand. Returns None if no cards available."""
        self.refill_hand()
        if len(self.hand) == 0:
            return None
        card = self.hand[0]
        self.hand = self.hand[1:]
        return card
    
    def add_to_collection(self, cards: str):
        """Adds won cards to the player's collection."""
        self.collection += cards
    
    def status(self) -> str:
        """Returns a status string for the player."""
        return f"{self.name}: {len(self.hand)} in hand, {len(self.collection)} in collection ({self.total_cards()} total)"
