"""
Card constants and utilities for the War card game.
"""

# Valid card characters
VALID_CARDS = {'1', 'A', '2', 'D', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'}

# Card values for comparison (higher = better)
CARD_VALUES = {
    '1': 14, 'A': 14,  # Ace is highest
    '2': 2, 'D': 2,    # Deuce
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13
}

# Card display names
CARD_NAMES = {
    '1': 'Ace', 'A': 'Ace',
    '2': '2', 'D': '2',
    '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    'T': '10',
    'J': 'Jack',
    'Q': 'Queen',
    'K': 'King'
}


def card_name(card: str) -> str:
    """Returns the display name of a card."""
    return CARD_NAMES[card]


def card_value(card: str) -> int:
    """Returns the numeric value of a card for comparison."""
    return CARD_VALUES[card]


def display_hand(hand_str: str) -> str:
    """Converts a hand string to a human-readable format."""
    cards = [card_name(char) for char in hand_str]
    return ', '.join(cards)


def validate_hand(hand_str: str) -> tuple[bool, str]:
    """
    Validates a hand string for the War card game.
    
    Returns:
        A tuple of (is_valid, error_message).
    """
    if not hand_str:
        return False, "Hand cannot be empty."
    
    hand_upper = hand_str.upper()
    
    invalid_chars = []
    for char in hand_upper:
        if char not in VALID_CARDS:
            invalid_chars.append(char)
    
    if invalid_chars:
        return False, f"Invalid card character(s): {', '.join(repr(c) for c in invalid_chars)}"
    
    return True, ""
