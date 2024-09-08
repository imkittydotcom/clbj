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

def display_hand(hand, hide_first=False):
    if hide_first:
        return f"[Hidden], {', '.join([f'{rank}{suit}' for rank, suit in hand[1:]])}"
    return ', '.join([f'{rank}{suit}' for rank, suit in hand])

def play_blackjack():
    deck = create_deck()
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    while True:
        print(f"\nYour hand: {display_hand(player_hand)}")
        print(f"Dealer's hand: {display_hand(dealer_hand, hide_first=True)}")

        player_value = calculate_hand_value(player_hand)
        if player_value == 21:
            print("Blackjack! You win!")
            return
        elif player_value > 21:
            print("Bust! You lose.")
            return

        action = input("Do you want to (H)it or (S)tand? ").lower()
        if action == 'h':
            player_hand.append(deck.pop())
        elif action == 's':
            break
        else:
            print("Invalid input. Please enter 'H' or 'S'.")

    dealer_value = calculate_hand_value(dealer_hand)
    print(f"\nDealer's hand: {display_hand(dealer_hand)}")
    
    while dealer_value < 17:
        dealer_hand.append(deck.pop())
        dealer_value = calculate_hand_value(dealer_hand)
        print(f"Dealer hits: {display_hand(dealer_hand)}")

    if dealer_value > 21:
        print("Dealer busts! You win!")
    elif dealer_value > player_value:
        print("Dealer wins!")
    elif dealer_value < player_value:
        print("You win!")
    else:
        print("It's a tie!")

def main():
    print("Welcome to Blackjack!")
    while True:
        play_blackjack()
        play_again = input("Do you want to play again? (Y/N) ").lower()
        if play_again != 'y':
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
