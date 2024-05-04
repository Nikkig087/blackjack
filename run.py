import random
from pprint import pprint 
# Global variables
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(card, category) for category in card_categories for card in cards_list]
 
def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])
 
def get_username():
    return input("Enter your username: ")

def display_username(username):
    pprint(f'Welcome {username}!')

def select_difficulty():
    '''
    function to ask user to chose a difficulty level to play the game as
    '''

    difficulty_levels = {
        1: "Beginner",
        2: "Intermediate",
        3: "Advanced"
    }
    pprint("select difficulty level:")
    pprint("1. Beginner")
    pprint("2. Intermediate")
    pprint("3. Advanced")
    choice = input("Enter either 1,2,3: ")
    while choice not in ['1','2','3']:
        pprint("Please choose 1, 2 or 3 only")
        choice =input("Enter either 1,2,3: ")
    level = int(choice)
    print( f"Great, you have chosen the {difficulty_levels[level]} level")

##difficulty = select_difficulty()
##pprint(difficulty)

def display_instructions():
    '''
    Instructions on how to play the game and the rules.
    '''
    
    print ("Game Instructions\n")
    print("Your goal is to achieve a score as close to 21 as possible but not going over 21\n")
    print("Jack,Queen,King cards are worth 10 points.\nAces are worth either 1 or 11, whichever is more favourable.\n")
    print("You will be asked if you want another card.\nEnter 'play' to request another card or 'stop' to stop.\n")
    print("Exceed 21 and you lose!!\n")
    print("Should you wish to stop, the dealer (the computer) will then draw cards until its score is at least 17\n")
    print ("The player with the highest score wins!!\n")
    

#display_instructions()

def player_turn(deck, player_card):
    while True:
        player_score = sum(card_value(card) for card in player_card)
        print("Your card: ", player_card)
        print("Your score: ", player_score)

        choice = input('What do you want to do?["play" to request another card, "stop" to finish game]: ').lower()

        while choice not in ["play","stop"]:
            print("You must choose to either Play or Stop")
            choice = input('What do you want to do?["play" to request another card, "stop" to finish game]: ').lower()
        
        if choice == "play":
            new_card = deck.pop()
            player_card.append(new_card)
        elif choice == "stop":
            break

        if player_score > 21:
            print("Your Cards: ", player_card)
            print("Your Score: ", player_score)
            print ("Your over 21, you loose!!")
            return False
        
        return True 

def computer_turn(deck, computer_card):
    while True:
        computer_score = sum(card_value(card) for card in computer_card)
 
        if computer_score >= 17:
            break  
 
        new_card = deck.pop()
        computer_card.append(new_card)
 
    return computer_card


def determine_winner(player_card, computer_card):
    player_score = sum(card_value(card) for card in player_card)
    computer_score = sum(card_value(card) for card in computer_card)
 
    if player_score > 21:
        print("Your Cards: ", player_card,"\n")
        print("Your Score: ", player_score)
        print("You lose! (Player Score is exceeding 21)")
    elif computer_score > 21:
        print("Your Cards: ", player_card)
        print("Your Score: ", player_score)
        print("Computer Cards: ", computer_card)
        print("Computer Score: ", computer_score)
        print("You win! (Computer Score is exceeding 21) ")
    elif player_score > computer_score:
        print("Your Cards: ", player_card)
        print("Your Score: ", player_score)
        print("Computer Cards: ", computer_card)
        print("Computer Score: ", computer_score)
        print("You win! (Player Has High Score than Computer)")
    elif computer_score > player_score:
        print("Your Cards:", player_card)
        print("Your Score:", player_score)
        print("Computer Cards:", computer_card)
        print("Computer Score:", computer_score)
        print("Computer wins! (Computer Has High Score than Player)")
    else:
        print("Your Cards:", player_card)
        print("Your Score:", player_score)
        print("Computer Cards:", computer_card)
        print("Computer Score:", computer_score)
        print("It's a tie.")


def main():
    # Initialize the game
    username = get_username()
    display_username(username)
    difficulty = select_difficulty()
    if difficulty == 1:
        deck_multiplier = 1  # Beginner level
    elif difficulty == 2:
        deck_multiplier = 2  # Intermediate level
    else:
        deck_multiplier = 4  # Advanced level
    global deck
    deck = deck * deck_multiplier  #  deck size is based on difficulty level the user chose
    random.shuffle(deck)

    # give option to display instructions
    view_instructions = input("Would you like to view the instructions? (yes/no): ").lower()
    if view_instructions == "yes":
        display_instructions()

    # Initialize the cards for both the player and computer
    player_card = [deck.pop(), deck.pop()]
    computer_card = [deck.pop(), deck.pop()]

    # Player's turn
    player_continue = player_turn(deck, player_card)
    if not player_continue or sum(card_value(card) for card in player_card) > 21:
        # End game if player loses or goes over 21
        determine_winner(player_card, computer_card)
        return

    # Computer's turn
    print("Computer's turn:")
    computer_card = computer_turn(deck, computer_card)
    computer_score = sum(card_value(card) for card in computer_card)
    print("Computer's cards:", computer_card)
    print("Computer's score:", computer_score)

    # Determine winner
    determine_winner(player_card, computer_card)

if __name__ == "__main__":
    main()
