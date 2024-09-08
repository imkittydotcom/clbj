import random

# Card representations
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card[0] in ['J', 'Q', 'K']:
            value += 10
        elif card[0] == 'A':
            aces += 1
        else:
            value += int(card[0])
    
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    
    return value

def is_soft_17(hand):
    value = calculate_hand_value(hand)
    return value == 17 and any(card[0] == 'A' for card in hand)

def display_hand(hand, hide_first=False):
    if hide_first:
        return f"[Hidden], {', '.join([f'{rank}{suit}' for rank, suit in hand[1:]])}"
    return ', '.join([f'{rank}{suit}' for rank, suit in hand])

def play_blackjack(round_number, score, ruleset):
    deck = create_deck()
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print(f"\nRound {round_number}")
    print(f"Current Score - Wins: {score['wins']}, Losses: {score['losses']}, Ties: {score['ties']}")

    while True:
        print(f"\nYour hand: {display_hand(player_hand)}")
        print(f"Dealer's hand: {display_hand(dealer_hand, hide_first=True)}")

        player_value = calculate_hand_value(player_hand)
        if player_value == 21:
            print("Blackjack! You win!")
            return 'win'
        elif player_value > 21:
            print("Bust! You lose.")
            return 'loss'

        action = input("Do you want to (H)it or (S)tand? ").lower()
        if action == 'h':
            player_hand.append(deck.pop())
        elif action == 's':
            break
        else:
            print("Invalid input. Please enter 'H' or 'S'.")

    dealer_value = calculate_hand_value(dealer_hand)
    print(f"\nDealer's hand: {display_hand(dealer_hand)}")
    
    while dealer_value < 17 or (ruleset == 'casino' and dealer_value == 17 and is_soft_17(dealer_hand)):
        dealer_hand.append(deck.pop())
        dealer_value = calculate_hand_value(dealer_hand)
        print(f"Dealer hits: {display_hand(dealer_hand)}")

    if dealer_value > 21:
        print("Dealer busts! You win!")
        return 'win'
    elif dealer_value > player_value:
        print("Dealer wins!")
        return 'loss'
    elif dealer_value < player_value:
        print("You win!")
        return 'win'
    else:
        print("It's a tie!")
        return 'tie'

def main():
    print("Welcome to Blackjack!")
    
    while True:
        ruleset = input("Choose ruleset - (B)asic or (C)asino: ").lower()
        if ruleset in ['b', 'c']:
            ruleset = 'basic' if ruleset == 'b' else 'casino'
            break
        else:
            print("Invalid input. Please enter 'B' for Basic or 'C' for Casino.")

    print(f"\nYou've selected the {ruleset.capitalize()} ruleset.")
    if ruleset == 'basic':
        print("In this ruleset, the dealer stands on all 17s.")
    else:
        print("In this ruleset, the dealer hits on soft 17.")

    while True:
        try:
            num_rounds = int(input("\nHow many rounds would you like to play? "))
            if num_rounds > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    score = {'wins': 0, 'losses': 0, 'ties': 0}

    for round in range(1, num_rounds + 1):
        result = play_blackjack(round, score, ruleset)
        if result == 'win':
            score['wins'] += 1
        elif result == 'loss':
            score['losses'] += 1
        else:
            score['ties'] += 1

    print("\nGame Over!")
    print(f"Final Score - Wins: {score['wins']}, Losses: {score['losses']}, Ties: {score['ties']}")

if __name__ == "__main__":
    main()
