import random
import re
import time
import sys
import os
from colorama import Fore, Style
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from my creds file
CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('blackjack_top_scores')


def update_scores(player_name, score):
    # Access the topscore worksheet in the blackjack_top_scores spreadsheet
    topscore = SHEET.worksheet("topscore")

    # Find the next empty row
    next_row = len(topscore.col_values(1)) + 1

    # Update the worksheet with the player's name and score
    topscore.update_cell(next_row, 1, player_name)
    topscore.update_cell(next_row, 2, score)


# Global variables
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(card, category) for category in card_categories for card in cards_list]

# Color constants
RED = Fore.RED
RESET = Style.RESET_ALL


def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])


def typingPrint(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)


def get_username():
    print(r"""
.------.            _     _            _    _            _
|A_  _ |.          | |   | |          | |  (_)          | |
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   <
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
      |  \/ K|                            _/ |
      `------'                           |__/
""")

    while True:
        first_name = input("Enter your first name: ")
        if re.match(r'^[A-Za-z]+$', first_name):
            return first_name.title()
        else:
            typingPrint("Please enter a valid first name with only letters.\n")


def display_username(username):
    typingPrint(f'Welcome {username}!\n')


def select_difficulty():
    '''
    Function to ask user to choose a difficulty level to play the game.
    '''
    difficulty_levels = {
        1: "Beginner",
        2: "Intermediate",
        3: "Advanced"
    }
    typingPrint("Select difficulty level:\n")
    for level, desc in difficulty_levels.items():
        typingPrint(f"{level}. {desc}\n")
    choice = input("Enter either 1, 2, or 3: ")
    while choice not in ['1', '2', '3']:
        typingPrint("Please choose 1, 2, or 3 only\n")
        choice = input("Enter either 1, 2, or 3: ")
    level = int(choice)
    typingPrint(f"Great, you have chosen the {difficulty_levels[level]} level\n")


def display_instructions():
    '''
    Instructions on how to play the game and the rules.
    '''
    typingPrint("\nGame Instructions\n")
    typingPrint("Your goal is to achieve a score as close to 21 as possible without going over 21.\n")
    typingPrint("Jack, Queen, and King cards are worth 10 points.\n")
    typingPrint("Aces are worth either 1 or 11, whichever is more favorable.\n")
    typingPrint("You will be asked if you want another card.\n")
    typingPrint("Enter 'play' to request another card or 'stop' to stop.\n")
    typingPrint("Exceed 21 and you lose!\n")
    typingPrint("Should you wish to stop, the dealer (the computer) will then draw cards until its score is at least 17.\n")
    typingPrint("The player with the highest score wins!\n")


def display_cards_ascii(cards):
    """
    Display the given cards as ASCII art in a row.
    """
    # Define suit card symbols
    suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

    # Check if cards is a single tuple or a list of tuples
    if isinstance(cards, tuple):
        cards = [cards]

    # Initialize empty lines list
    lines = ['' for _ in range(6)]

    # Iterate over cards and add acsii art for card
    for rank, suit in cards:
        # Determine rank string
        if rank == 'Ace':
            rank_str = ' A '
        elif rank == 'Jack':
            rank_str = ' J '
        elif rank == 'Queen':
            rank_str = ' Q '
        elif rank == 'King':
            rank_str = ' K '
        else:
            rank_str = f' {rank} '

        # Get suit symbol
        suit_symbol = suit_symbols[suit]

        # Add card ASCII art to each line
        lines[0] += ' _________ '
        lines[1] += f"|{rank_str:<2}       |"
        lines[2] += "|         |"
        lines[3] += f"|    {suit_symbol}    |"
        lines[4] += "|         |"
        lines[5] += f"|_______{rank_str:>1}|"

    # Print each line like above
    for line in lines:
        typingPrint(line + "\n")


def player_turn(deck, player_card):
    while True:
        player_score = sum(card_value(card) for card in player_card)
        typingPrint("\nYour cards:\n")
        for card in player_card:
            display_cards_ascii(card)
        typingPrint(f"\nYour score: {player_score}\n")
        choice = input('What do you want to do? ["play" to request another card, "stop" to finish game]: ').lower()
        while choice not in ["play", "stop"]:
            typingPrint(f"{RED}You must choose to either Play or Stop{RESET}\n")
            choice = input('What do you want to do? ["play" to request another card, "stop" to finish game]: ').lower()

        if choice == "play":
            new_card = deck.pop()
            player_card.append(new_card)
            player_score = sum(card_value(card) for card in player_card)
            typingPrint("You drew:\n")
            display_cards_ascii(new_card)
            if player_score > 21:
                typingPrint("Your Cards:\n")
                for card in player_card:
                    display_cards_ascii(card)
                typingPrint(f"Your Score: {player_score}\n")
                typingPrint(f"{RED}You are over 21, you lose!{RESET}\n")
                return False
        elif choice == "stop":
            break
    return True


def computer_turn(deck, computer_card, difficulty_level):
    while True:
        computer_score = sum(card_value(card) for card in computer_card)
        if computer_score >= 17:
            break
        if random.random() < 0.5:
            new_card = deck.pop()
            computer_card.append(new_card)
        else:
            break
    print("Computer's Cards:")
    for card in computer_card:
        display_cards_ascii(card)
    if computer_score > 21:
        print("Computer's Score:", computer_score)
        print(f"{RED}Computer is over 21, you win!{RESET}")
        return False
    return True



def determine_winner(player_card, computer_card):
    player_score = sum(card_value(card) for card in player_card)
    computer_score = sum(card_value(card) for card in computer_card)

    # Display both player's and computer's cards and scores
    typingPrint("\nYour Cards: ")
    for card in player_card:
        typingPrint(f"{card[0]} of {card[1]}, ")
    typingPrint("\n")
    typingPrint(f"Your Score: {player_score}\n")
    typingPrint("\nComputer Cards:\n")
    for card in computer_card:
        typingPrint(f"{card[0]} of {card[1]}, ")
    typingPrint("\n")
       # display_cards_ascii(card)  # Display the computer's cards in ASCII art
    typingPrint(f"Computer Score: {computer_score}\n")

    if player_score <= 21 and (player_score > computer_score or computer_score > 21):
        typingPrint(f"\n{RED}You win!{RESET}\n")
        typingPrint("\n")
    elif computer_score <= 21 and (computer_score > player_score or player_score > 21):
        typingPrint(f"\n{RED}Computer wins!{RESET}\n")
        typingPrint("\n")
    else:
        typingPrint("\nIt's a tie.\n")
        typingPrint("\n")


def restart_game():
    if os.environ.get('RUNNING_ON_HEROKU'):
        # If running on Heroku, don't wait for user input
        return False
    else:
        try:
            choice = input("Do you want to play again? (yes/no): ").lower()
            if choice not in ['yes', 'no']:
                raise ValueError("Invalid choice. Please enter 'yes' or 'no'.")
            return choice == 'yes'
        except ValueError as e:
            typingPrint(f"{RED}{e}{RESET}\n")
            return restart_game()



def clear_screen():
    """
    Clear the terminal screen.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()


def main():
    while True:  # Outer loop for restarting the game
        os.system('cls' if os.name == 'nt' else 'clear')

        # Initialize the game
        username = get_username()
        display_username(username)
        difficulty_level = select_difficulty()  # Store the selected difficulty level
        global deck
        random.shuffle(deck)

        # Give option to display instructions
        view_instructions = input("Would you like to view the instructions? (yes/no): ").lower()
        while view_instructions not in ["yes", "no"]:
            view_instructions = input("You must choose either 'yes' or 'no' for viewing instructions: ").lower()
        if view_instructions == "yes":
            display_instructions()

        # Initialize the cards for both the player and computer
        player_card = [deck.pop(), deck.pop()]
        computer_card = [deck.pop(), deck.pop()]

        # Player's turn
        player_continue = player_turn(deck, player_card)
        if not player_continue or sum(card_value(card) for card in player_card) >= 21:
            # End game if player loses or reaches 21
            determine_winner(player_card, computer_card)
            if not restart_game():
                print("Thank you for playing! Goodbye.")
                break  # Exit outer loop if player chooses not to restart
            else:
                continue  # Restart the game

        # Computer's turn
        print("\nComputer's turn:")
        computer_continue = computer_turn(deck, computer_card, difficulty_level)  # Pass difficulty_level
        if not computer_continue or sum(card_value(card) for card in computer_card) >= 21:
            # End game if computer loses or reaches 21
            determine_winner(player_card, computer_card)
            if not restart_game():
                print("Thank you for playing! Goodbye.")
                break  # Exit outer loop if player chooses not to restart
            else:
                continue  # Restart the game

        # Determine winner after both turns
        determine_winner(player_card, computer_card)
        update_scores(username, sum(card_value(card) for card in player_card))
        if not restart_game():
            print("Thank you for playing! Goodbye.")
            break  # Exit outer loop if player chooses not to restart


if __name__ == "__main__":
    main()
