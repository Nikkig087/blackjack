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
    return f"Great, you have chosen the {difficulty_levels[level]} level"

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
