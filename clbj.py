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

def display_score(score):
    return f"Score: W: {score['wins']} L: {score['losses']} T: {score['ties']}"

def get_bet(chips):
    while True:
        bet = input(f"\nYou have {chips} chips. Enter your bet (1-{chips} or 'A' for All In): ").upper()
        if bet == 'A':
            return chips
        try:
            bet = int(bet)
            if 1 <= bet <= chips:
                return bet
            else:
                print(f"Invalid bet. Please enter a number between 1 and {chips}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'A' for All In.")

def play_blackjack(round_number, score, ruleset, chips=None):
    deck = create_deck()
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print(f"\nRound {round_number}")
    print(display_score(score))

    if ruleset == 'casino':
        bet = get_bet(chips)
        print(f"Your bet: {bet} chips")

    while True:
        print(f"\nYour hand: {display_hand(player_hand)}")
        print(f"Dealer's hand: {display_hand(dealer_hand, hide_first=True)}")

        player_value = calculate_hand_value(player_hand)
        if player_value == 21:
            print("Blackjack! You win!")
            return 'win', bet if ruleset == 'casino' else None
        elif player_value > 21:
            print("Bust! You lose.")
            return 'loss', bet if ruleset == 'casino' else None

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
        return 'win', bet if ruleset == 'casino' else None
    elif dealer_value > player_value:
        print("Dealer wins!")
        return 'loss', bet if ruleset == 'casino' else None
    elif dealer_value < player_value:
        print("You win!")
        return 'win', bet if ruleset == 'casino' else None
    else:
        print("It's a tie!")
        return 'tie', 0 if ruleset == 'casino' else None

def get_ruleset():
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
        print("In this ruleset, the dealer hits on soft 17 and you can bet chips.")
    
    return ruleset

def get_num_rounds():
    while True:
        try:
            num_rounds = int(input("\nHow many rounds would you like to play? "))
            if num_rounds > 0:
                return num_rounds
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game(ruleset, score, chips=None):
    num_rounds = get_num_rounds()

    for round in range(1, num_rounds + 1):
        if ruleset == 'casino':
            if chips <= 0:
                print("You're out of chips! Game over.")
                break
            result, bet = play_blackjack(round, score, ruleset, chips)
            if result == 'win':
                score['wins'] += 1
                chips += bet
                print(f"You won {bet} chips!")
            elif result == 'loss':
                score['losses'] += 1
                chips -= bet
                print(f"You lost {bet} chips.")
            else:
                score['ties'] += 1
            print(f"Your current chip balance: {chips}")
        else:
            result, _ = play_blackjack(round, score, ruleset)
            if result == 'win':
                score['wins'] += 1
            elif result == 'loss':
                score['losses'] += 1
            else:
                score['ties'] += 1

    print("\nGame Over!")
    print(display_score(score))
    if ruleset == 'casino':
        print(f"Final chip balance: {chips}")
    
    return chips

def main():
    print("Welcome to Blackjack!")
    
    ruleset = get_ruleset()
    score = {'wins': 0, 'losses': 0, 'ties': 0}
    chips = 100 if ruleset == 'casino' else None

    while True:
        chips = play_game(ruleset, score, chips)

        while True:
            choice = input("\nDo you want to (C)ontinue current game, start a (N)ew game, or (Q)uit? ").lower()
            if choice in ['c', 'n', 'q']:
                break
            else:
                print("Invalid input. Please enter 'C', 'N', or 'Q'.")

        if choice == 'c':
            print("\nContinuing current game...")
            print(display_score(score))
            if ruleset == 'casino':
                print(f"Current chip balance: {chips}")
        elif choice == 'n':
            print("\nStarting a new game...")
            ruleset = get_ruleset()
            score = {'wins': 0, 'losses': 0, 'ties': 0}
            chips = 100 if ruleset == 'casino' else None
        else:
            print("\nThank you for playing Blackjack!")
            break

if __name__ == "__main__":
    main()
