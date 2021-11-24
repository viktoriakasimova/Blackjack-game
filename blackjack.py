from random import shuffle

game_on = True

# Defining Card, Deck, Hand and Chips classes.

values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    
    def __init__(self):
        suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
        ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
        self.cards = [Card(suit,rank) for suit in suits for rank in ranks] 
    
    def __repr__(self):
        cards_in_deck = ""
        for card in self.cards:
            cards_in_deck += "\n" + card.__repr__()
        return f"This is a deck of {len(self.cards)}:{cards_in_deck}"
               
    def shuffle(self):
        shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop()      

class Hand:
    
    def __init__(self):
        self.cards = []  
        self.value = 0   
        self.aces = 0    
    
    def add_card(self,card):
        
        self.cards.append(card)
        self.value += card.value
        if card.rank == "Ace":
            self.aces += 1
    
    def adjust_for_ace(self):

        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    
    def __init__(self, total):
        self.total = total  
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
# Defining functions to be used in the program.

# The function will prompt the player user for a bet, checking if the amount of chips is enough.
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("\nHow many chips do you want to bet? "))
        except ValueError:
            print("\nYour bet must be an integer!")
        else:
            if chips.bet > chips.total:
                print(f"\nYou don't have enough chips for this bet! You have only {chips.total} chips.")
            else:
                break
                
# The function will be called when the player or the dealer request a hit.
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
# The function will control the behaviour of the while loop later in the game
# depending on whether the player hits or stands.
def hit_or_stand(deck,hand):
    global game_on  
    
    while True:
        action = input("\nDo you want to Hit or Stand? (h/s) ")
        if action[0].lower() == "h":
            hit(deck,hand)
        elif action[0].lower() == "s":
            print("\nPlayer stands, his turn is over. Dealer is playing now.")
            game_on = False
        else:
            print("\nSorry, didn't understand you. Please enter 'h' or 's' only: ")
            continue
        break

# The function will show all cards of the player and one of the two cards of the dealer 
# at the beginning of the game and after the player takes a card.
def show_some_cards(dealer, player):
    print("\nDEALER'S HAND:")
    print("  <card is hidden>")
    print(" ",dealer.cards[1])  
    
    print("\nPLAYER'S HAND:", *player.cards, sep='\n  ')
    print("\nPlayer's Hand value is", player.value)
    
# The function will show all cards of both the player and the dealer at the end of the game.    
def show_all_cards(dealer, player):
    print("\nDEALER'S HAND:", *dealer.cards, sep='\n  ')
    print("\nDealer's Hand value is", dealer.value)
    print("\nPLAYER'S HAND:", *player.cards, sep='\n  ')
    print("\nPlayer's Hand value is", player.value)
    
# The functions are handling different end of game scenarios.
def player_busts(chips):
    print("\nPlayer busted, Dealer wins!")
    chips.lose_bet()

def dealer_busts(chips):
    print("\nDealer busted, Player wins!")
    chips.win_bet()
    
def dealer_wins(chips):
    print("\nDealer wins!")
    chips.lose_bet()
    
def tie():
    print("\nPlayer and dealer have the same amount of points, it's a tie.")

# The function asking if the player wants to play again.
def replay():
    play_again = ""  
    while play_again not in ["y", "n"]:
        play_again = input("Do you want to play again (y/n)? ")
        if play_again not in ["y", "n"]:
            print("Invalid input. Please choose y' or 'n'.")        
    return play_again == "y"  

# THE ACTUAL GAMEPLAY

# Set up the player's chips.
player_chips = Chips(500)

# Print a welcoming message.
print("\nWelcome to BLACKJACK GAME!")
print(f"You have {player_chips.total} chips now.")

while True:

    # Setup of the deck and the players.
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    dealer = Hand()
    for n in range(2):
        player.add_card(deck.deal())
    for n in range(2):
        dealer.add_card(deck.deal())
    
    # Prompt the player for a bet.
    take_bet(player_chips)
    
    # Show both cards of the player but only one card of the dealer.
    show_some_cards(dealer, player)
    
    while game_on:  
        
        # Player hitting.
        hit_or_stand(deck, player)
        
        show_some_cards(dealer, player)
        
        # If total values of player's cards exceeds 21, the dealer wins.
        if player.value > 21:
            player_busts(player_chips)
            break

    # Dealer hitting.
    if player.value <= 21:
        
        while dealer.value < player.value:
            hit(deck, dealer)
    
        # Show all cards of both the player and the dealer.
        show_all_cards(dealer, player)
    
        # Check for different end of game scenarios.
        if dealer.value > 21:
            dealer_busts(player_chips)            
        elif dealer.value > player.value:
            dealer_wins(player_chips)
        else:
            tie()
            
    # Show how many chips the player has in total.
    print(f"\nPlayer has {player_chips.total} chips in total")
    
    # Ask if the player wants to play again.
    if replay():
        game_on = True
        continue
    else:
        print("\nThank you for playing, see you next time!")
        break