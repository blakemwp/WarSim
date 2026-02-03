"""
Game logic for the War card game.
"""

import time
from player import Player
from card import card_name, card_value, display_hand

# Delay times for game mode (in seconds)
DELAY_ROUND_START = 1.0
DELAY_CARD_PLAY = 0.5
DELAY_BATTLE_RESULT = 1.5
DELAY_WAR_DECLARE = 2.0
DELAY_WAR_CARDS = 1.0
DELAY_GAME_END = 0.5


def play_round(p1: Player, p2: Player, round_num: int, game_mode: bool = False) -> bool:
    """
    Plays a single round of War.
    
    Returns True if the game should continue, False if a player has won.
    """
    print(f"\n{'='*50}")
    print(f"ROUND {round_num}")
    print(f"{'='*50}")
    print(f"  {p1.status()}")
    print(f"  {p2.status()}")
    
    if game_mode:
        time.sleep(DELAY_ROUND_START)
    
    # Cards at stake in this round
    pot = ""
    
    while True:
        # Draw cards
        card1 = p1.draw_card()
        card2 = p2.draw_card()
        
        # Check if either player ran out of cards
        if card1 is None and card2 is None:
            print("\n  Both players ran out of cards simultaneously! It's a draw!")
            return False
        elif card1 is None:
            print(f"\n  {p1.name} ran out of cards! {p2.name} wins the game!")
            return False
        elif card2 is None:
            print(f"\n  {p2.name} ran out of cards! {p1.name} wins the game!")
            return False
        
        # Add cards to pot
        pot += card1 + card2
        
        print(f"\n  {p1.name} plays: {card_name(card1)}")
        if game_mode:
            time.sleep(DELAY_CARD_PLAY)
        print(f"  {p2.name} plays: {card_name(card2)}")
        if game_mode:
            time.sleep(DELAY_CARD_PLAY)
        
        val1 = card_value(card1)
        val2 = card_value(card2)
        
        if val1 > val2:
            print(f"\n  >> {p1.name} wins this battle!")
            print(f"  >> {p1.name} collects: {display_hand(pot)}")
            p1.add_to_collection(pot)
            if game_mode:
                time.sleep(DELAY_BATTLE_RESULT)
            break
            
        elif val2 > val1:
            print(f"\n  >> {p2.name} wins this battle!")
            print(f"  >> {p2.name} collects: {display_hand(pot)}")
            p2.add_to_collection(pot)
            if game_mode:
                time.sleep(DELAY_BATTLE_RESULT)
            break
            
        else:
            # WAR!
            print(f"\n  ** TIE! Both played {card_name(card1)}! **")
            print("  ** I DECLARE WAR! **")
            if game_mode:
                time.sleep(DELAY_WAR_DECLARE)
            
            # Check how many cards each player has available for war
            p1_available = p1.total_cards()
            p2_available = p2.total_cards()
            
            # Determine how many face-down cards each player can place (max 3)
            # Players need at least 1 card for the final comparison
            p1_facedown = min(3, max(0, p1_available - 1))
            p2_facedown = min(3, max(0, p2_available - 1))
            
            if p1_facedown < 3 or p2_facedown < 3:
                if p1_available == 0 and p2_available == 0:
                    print("\n  Both players have no cards left! It's a draw!")
                    return False
                elif p1_available == 0:
                    print(f"\n  {p1.name} has no cards for war! {p2.name} wins!")
                    return False
                elif p2_available == 0:
                    print(f"\n  {p2.name} has no cards for war! {p1.name} wins!")
                    return False
                
                # At least one player has limited cards
                if p1_facedown < 3:
                    print(f"  ** {p1.name} only has {p1_available} card(s) left - playing final card! **")
                if p2_facedown < 3:
                    print(f"  ** {p2.name} only has {p2_available} card(s) left - playing final card! **")
            else:
                print("  ** Each player puts 3 cards face down... **")
            
            # Each player puts their face-down cards
            war_cards_1 = ""
            war_cards_2 = ""
            
            for i in range(max(p1_facedown, p2_facedown)):
                if i < p1_facedown:
                    c1 = p1.draw_card()
                    if c1:
                        war_cards_1 += c1
                if i < p2_facedown:
                    c2 = p2.draw_card()
                    if c2:
                        war_cards_2 += c2
            
            pot += war_cards_1 + war_cards_2
            
            if war_cards_1:
                print(f"  {p1.name}'s face-down cards: {display_hand(war_cards_1)}")
            if war_cards_2:
                print(f"  {p2.name}'s face-down cards: {display_hand(war_cards_2)}")
            if game_mode:
                time.sleep(DELAY_WAR_CARDS)
            print(f"\n  Total cards in pot: {len(pot)}")
            print("  ** Now comparing the next cards... **")
            if game_mode:
                time.sleep(DELAY_CARD_PLAY)
            # Loop continues to compare next cards
    
    return True


def play_game(hand1: str, hand2: str, name1: str = "Player 1", name2: str = "Player 2", game_mode: bool = False):
    """
    Plays a complete game of War.
    
    Args:
        hand1: Player 1's starting hand.
        hand2: Player 2's starting hand.
        name1: Name for Player 1 (default: "Player 1").
        name2: Name for Player 2 (default: "Player 2").
        game_mode: If True, adds pauses for watching the game unfold.
    """
    p1 = Player(name1, hand1)
    p2 = Player(name2, hand2)
    
    print("\n" + "=" * 50)
    print("         LET THE WAR BEGIN!")
    print("=" * 50)
    print(f"\n{p1.name} starts with: {display_hand(hand1)}")
    print(f"{p2.name} starts with: {display_hand(hand2)}")
    
    if game_mode:
        time.sleep(DELAY_BATTLE_RESULT)
    
    round_num = 1
    max_rounds = 10000  # Safety limit
    
    while round_num <= max_rounds:
        if not play_round(p1, p2, round_num, game_mode):
            break
        
        # Check for winner
        if not p1.has_cards():
            if game_mode:
                time.sleep(DELAY_GAME_END)
            print(f"\n{'*'*50}")
            print(f"  {p2.name} WINS THE GAME!")
            print(f"  Final: {p2.name} has {p2.total_cards()} cards")
            print(f"{'*'*50}")
            break
        elif not p2.has_cards():
            if game_mode:
                time.sleep(DELAY_GAME_END)
            print(f"\n{'*'*50}")
            print(f"  {p1.name} WINS THE GAME!")
            print(f"  Final: {p1.name} has {p1.total_cards()} cards")
            print(f"{'*'*50}")
            break
        
        round_num += 1
    
    if round_num > max_rounds:
        print(f"\n  Game ended after {max_rounds} rounds (safety limit).")
        print(f"  {p1.status()}")
        print(f"  {p2.status()}")

