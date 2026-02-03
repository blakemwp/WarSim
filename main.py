"""
War Card Game Simulator - Entry Point
"""

import random
from card import validate_hand, display_hand
from game import play_game


def create_random_deck() -> tuple[str, str]:
    """
    Creates a shuffled 52-card deck and deals 26 cards to each player.
    
    Returns:
        A tuple of (hand1, hand2) strings.
    """
    # Standard deck: 4 of each card (A, 2-9, T, J, Q, K)
    # Using 'A' for Ace and '2' for Deuce in the generated deck
    card_types = "A23456789TJQK"
    deck = list(card_types * 4)  # 4 of each = 52 cards
    random.shuffle(deck)
    
    hand1 = ''.join(deck[:26])
    hand2 = ''.join(deck[26:])
    return hand1, hand2


def get_valid_hand(player_name: str) -> str:
    """Prompts the user for a valid hand, re-prompting on invalid input."""
    while True:
        hand_input = input(f"Enter {player_name}'s hand: ").strip()
        is_valid, error_msg = validate_hand(hand_input)
        
        if is_valid:
            return hand_input.upper()
        else:
            print(f"Invalid hand: {error_msg}")
            print("Please try again.\n")


def get_player_name(player_num: int) -> str:
    """Prompts for a player name, defaulting to 'Player X' if empty."""
    default_name = f"Player {player_num}"
    name = input(f"Enter name for {default_name} (or press Enter for default): ").strip()
    return name if name else default_name


def main():
    """Main entry point for the War card game."""
    print("=" * 50)
    print("           WAR CARD GAME SIMULATOR")
    print("=" * 50)
    print("\nCard notation:")
    print("  1 or A: Ace    |  2 or D: Deuce  |  3-9: Number")
    print("  T: 10          |  J: Jack        |  Q: Queen    |  K: King")
    print("\nExample: K2T4J59 = King, 2, 10, 4, Jack, 5, 9")
    print("-" * 50 + "\n")
    
    # Get player names
    name1 = get_player_name(1)
    name2 = get_player_name(2)
    print()
    
    # Select game mode
    while True:
        mode_input = input("Select mode - [G]ame (with pauses) or [Q]uick (instant): ").strip().upper()
        if mode_input in ('G', 'GAME'):
            game_mode = True
            print("  >> Game mode selected - enjoy watching the battle!\n")
            break
        elif mode_input in ('Q', 'QUICK'):
            game_mode = False
            print("  >> Quick mode selected - instant simulation!\n")
            break
        else:
            print("Invalid selection. Please enter 'G' for Game mode or 'Q' for Quick mode.\n")
    
    # Check for random dealing
    first_input = input(f"Enter {name1}'s hand (or 'R' for random deal): ").strip().upper()
    
    if first_input == 'R':
        hand1, hand2 = create_random_deck()
        print("\n  >> Shuffling a fresh 52-card deck...")
        print("  >> Dealing 26 cards to each player...\n")
        print(f"{name1}'s hand: {display_hand(hand1)}\n")
        print(f"{name2}'s hand: {display_hand(hand2)}\n")
    else:
        # Validate the first input as a hand
        while True:
            is_valid, error_msg = validate_hand(first_input)
            if is_valid:
                hand1 = first_input
                break
            else:
                print(f"Invalid hand: {error_msg}")
                print("Please try again.\n")
                first_input = input(f"Enter {name1}'s hand: ").strip().upper()
        
        print(f"{name1}'s hand: {display_hand(hand1)}\n")
        
        hand2 = get_valid_hand(name2)
        print(f"{name2}'s hand: {display_hand(hand2)}\n")
    
    # Summary
    print("-" * 50)
    print("Both hands ready!")
    print(f"  {name1}: {display_hand(hand1)} ({len(hand1)} cards)")
    print(f"  {name2}: {display_hand(hand2)} ({len(hand2)} cards)")
    print("-" * 50)
    
    # Play the game
    play_game(hand1, hand2, name1, name2, game_mode)


if __name__ == "__main__":
    main()
