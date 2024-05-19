import random
import re
import time
import sys
import tty
import termios
import threading
import os
from colorama import Fore, Style
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Load credentials from my creds file


CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("blackjack_top_scores")

import sys
import tty
import termios
import threading


class KeyboardDisable:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        self.running = False
        self._thread = None

    def start(self):
        if not self.running:
            self.running = True
            tty.setcbreak(self.fd)  # Disable buffering
            self._thread = threading.Thread(target=self._disable_input)
            self._thread.start()

    def stop(self):
        if self.running:
            self.running = False
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            if self._thread is not None:
                self._thread.join()  # Ensure the thread has finished

    def _disable_input(self):
        while self.running:
            try:
                # Use select to check if there's any input without blocking

                if select.select([sys.stdin], [], [], 0.1)[0]:
                    sys.stdin.read(
                        1
                    )  # Read a single character to effectively block input
            except Exception:
                pass


def typingPrint(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)


def update_scores(player_name, score, difficulty_level):
    """
    Update the high scores in the Google Sheets document.

    Args:
        player_name (str): The name of the player.
        score (int): The score of the player.
        difficulty_level (int): The level of difficulty (1 for Beginner,
                                2 for Intermediate, 3 for Advanced).
    """
    try:
        difficulty_words = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
        difficulty_word = difficulty_words.get(difficulty_level, "Unknown")

        topscore = SHEET.worksheet("topscore")

        # Check if the sheet is empty (only contains the header row)

        if len(topscore.get_all_values()) == 1:
            next_row = 2  # Start from the second row if the sheet is empty
        else:
            next_row = len(topscore.col_values(1)) + 1
        topscore.update_cell(next_row, 1, player_name)
        topscore.update_cell(next_row, 2, score)
        topscore.update_cell(next_row, 3, difficulty_word)
        print("Scores updated successfully.")
    except Exception as e:
        print("Error updating scores:", e)


def view_high_scores():
    """
    Display the top 10 high scores from my Google
    Sheets topscore worksheet.
    """
    topscore = SHEET.worksheet("topscore")
    high_scores = topscore.get_all_values()

    print("\nTop 10 High Scores:\n")

    data_rows = high_scores[1:]

    if not any(data_rows):
        print("\nNo high scores yet!")
    else:
        header = high_scores[0]
        print(f"{' | '.join(header)}")
        print("-" * 30)

        data_rows.sort(key=lambda x: int(x[1]), reverse=True)

        for i, score in enumerate(data_rows[:10], 1):
            print(f"{i}. {score[0]} | {score[1]} | {score[2]}")


card_categories = ["Hearts", "Diamonds", "Clubs", "Spades"]
cards_list = [
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
]
deck = [
    (card, category) for category in card_categories for card in cards_list
]

# Color constants


BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL

disable = KeyboardDisable()


def card_value(card):
    """
    Get the value of a card.

    Args:
        card (tuple): A tuple representing the card (rank, suit).

    Returns:
        int: The value of the card.
    """
    if card[0] in ["Jack", "Queen", "King"]:
        return 10
    elif card[0] == "Ace":
        return 11
    else:
        return int(card[0])


'''
def typingPrint(text):
    """
    Print text gradually, simulating typing.

    Args:
        text (str): The text to print.
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)

'''


def get_username():
    """
    Get the username from the user.

    Returns:
        str: The username entered by the user.
    """
    print(
        r"""
.------.            _     _            _    _            _
|A_  _ |.          | |   | |          | |  (_)          | |
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   <
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
      |  \/ K|                            _/ |
      `------'                           |__/
"""
    )

    while True:
        first_name = input("Enter your first name: \n")
        if re.match(r"^[A-Za-z]+$", first_name):
            return first_name.title()
        else:
            disable.start()
            try:
                typingPrint(
                    "Please enter a valid first name with only letters.\n",
                    delay=0.1,
                )
            finally:
                disable.stop()


def display_username(username):
    """
    Display a welcome message with the username.

    Args:
        username (str): The username to display.
    """
    disable.start()
    try:
        typingPrint(f"Welcome {username}!\n", delay=0)
    finally:
        disable.stop()


def select_difficulty():
    """
    Prompt the user to select a difficulty level.

    Returns:
        int: The selected difficulty level (1 for Beginner,
        2 for Intermediate, 3 for Advanced).
    """
    disable.start()
    
    difficulty_levels = {
        1: "Beginner",
        2: "Intermediate",
        3: "Advanced",
    }
    
    typingPrint("\nSelect difficulty level:\n")
    for level, desc in difficulty_levels.items():
        typingPrint(f"{level}. {desc}\n")
    
    disable.stop()
    
    choice = None
    while choice not in ["1", "2", "3"]:
        choice = input("Enter either 1, 2, or 3: \n")
        if choice not in ["1", "2", "3"]:
            typingPrint("Please choose 1, 2, or 3 only\n")

    level = int(choice)

    disable.start()
    try:
        typingPrint(
            f"Great, you have chosen the {difficulty_levels[level]} level\n"
        )
    finally:
        disable.stop()

    return level





def display_instructions():
    """
    Display the game instructions to the user.
    """
    disable.start()
    try:
        typingPrint("\nGame Instructions\n")
        typingPrint(
            "Your goal is to achieve a score as close to"
            " 21 as possible without going over 21.\n"
        )
        typingPrint("Jack, Queen, and King cards" " are worth 10 points.\n")
        typingPrint(
            "Aces are worth either 1 or 11," " whichever is more favorable.\n"
        )
        typingPrint("You will be asked if you want another card.\n")
        typingPrint(
            "Enter 'play' to request another card or 'stop' to stop.\n"
        )
        typingPrint("Exceed 21 and you lose!\n")
        typingPrint(
            "Should you decide to stop, the dealer (the computer)\n"
            "will then draw cards until its score is at least 17.\n"
        )
        typingPrint("The player with the highest score wins!\n")
    finally:
        disable.stop()


def display_cards_ascii(cards):
    """
    Display ASCII representation of the given cards.

    Args:
        cards (list of tuples): List of tuples representing the cards.
    """
    suit_symbols = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Clubs": "♣",
        "Spades": "♠",
    }

    if isinstance(cards, tuple):
        cards = [cards]
    lines = ["" for _ in range(6)]

    for rank, suit in cards:
        if rank == "Ace":
            rank_str = " A "
        elif rank == "Jack":
            rank_str = " J "
        elif rank == "Queen":
            rank_str = " Q "
        elif rank == "King":
            rank_str = " K "
        else:
            rank_str = f" {rank} "
        suit_symbol = suit_symbols[suit]

        lines[0] += " _________ "
        lines[1] += f"|{rank_str:<2}       |"
        lines[2] += "|         |"
        lines[3] += f"|    {suit_symbol}    |"
        lines[4] += "|         |"
        lines[5] += f"|_______{rank_str:>1}|"
    for line in lines:
        disable.start()
        try:
            typingPrint(line + "\n")
        finally:
            disable.stop()

def player_turn(deck, player_card):
    """
    Simulate the player's turn in the game.

    Args:
        deck (list): The deck of cards.
        player_card (list of tuples): List of tuples
        representing the player's cards.

    Returns:
        bool: True if the player continues playing,
        False if they bust or choose to stop.
    """
    disable.start()
    try:
        while True:
            player_score = sum(card_value(card) for card in player_card)
            typingPrint("\nYour cards:\n")
            for card in player_card:
                display_cards_ascii(card)
            typingPrint(f"\nYour score: {player_score}\n")

            if player_score >= 21:
                if player_score == 21:
                    typingPrint(f"{YELLOW}Your score is 21!{RESET}\n")
                else:
                    typingPrint(
                        f"{RED}Your score is over 21! You lose!{RESET}\n"
                    )
                return False
            choice = input(
                'What do you want to do? ("play" to request'
                ' another card, "stop" to finish game): \n'
            ).lower()
            
            if choice not in ["play", "stop"]:
                typingPrint(
                    f"{RED}You must choose" f" to either Play or Stop{RESET}\n"
                )
                continue
                
            if choice == "play":
                new_card = deck.pop()
                player_card.append(new_card)
                player_score = sum(card_value(card) for card in player_card)
                typingPrint("You drew:\n")
                display_cards_ascii(new_card)
            else:
                break
    finally:
        disable.stop()
    return True



def computer_turn(deck, computer_card, difficulty_level):
    """
    Simulate the computer's turn in the game.

    Args:
        deck (list): The deck of cards.
        computer_card (list of tuples): List of tuples representing
        the computer's cards.
        difficulty_level (int): The level of difficulty (1 for Beginner,
        2 for Intermediate, 3 for Advanced).

    Returns:
        bool: True if the computer continues playing,
        False if it busts or chooses to stop.
    """
    disable.start()
    try:
        while True:
            computer_score = sum(card_value(card) for card in computer_card)
            if computer_score >= 17:
                break  # Break out of the loop if the score is 17 or higher
            if random.random() < 0.5:
                new_card = deck.pop()
                computer_card.append(new_card)
            else:
                break  # Break out of the loop with 50% probability
            typingPrint("\nComputer's Cards:\n")
            for card in computer_card:
                display_cards_ascii(card)
            if computer_score > 21:
                print("Computer's Score:", computer_score)
                print(f"{RED}Computer is over 21, you win!{RESET}")
                return False
            return True
    finally:
        disable.stop()


def determine_winner(player_card, computer_card, username, difficulty_level):
    """
    Determine the winner of the game.

    Args:
        player_card (list of tuples): List of tuples
        representing the player's cards.
        computer_card (list of tuples): List of tuples
        representing the computer's cards.
        username (str): The username of the player.
        difficulty_level (int): The level of difficulty
        (1 for Beginner, 2 for Intermediate, 3 for Advanced).
    """
    player_score = sum(card_value(card) for card in player_card)
    computer_score = sum(card_value(card) for card in computer_card)

    typingPrint("\nYour Cards: ")
    for card in player_card:
        typingPrint(f"{card[0]} of {card[1]}, ")
    typingPrint("\n")
    typingPrint(f"Your Score: {player_score}\n")
    typingPrint("\nComputer Cards:\n")
    for card in computer_card:
        typingPrint(f"{card[0]} of {card[1]}, ")
    typingPrint("\n")
    typingPrint(f"Computer Score: {computer_score}\n")

    if player_score == computer_score:
        print("\nIt's a tie!\n")
    elif player_score == 21:
        print("\nCongratulations! You have a Blackjack!\n")
        print("\nUpdating scores...")
        update_scores(username, player_score, difficulty_level)
    elif player_score <= 21 and (
        player_score > computer_score or computer_score > 21
    ):
        print("\nYou win!\n")
        print("\nUpdating scores...")
        update_scores(username, player_score, difficulty_level)
    else:
        print(f"\n{BLUE}You lose!{RESET}")


def restart_game():
    """
    Prompt the user to restart the game.

    Returns:
        bool: True if the user wants to restart, False otherwise.
    """
    if os.environ.get("RUNNING_ON_HEROKU"):
        return False
    else:
        try:
            choice = input("Do you want to play again? (yes/no): \n").lower()
            if choice not in ["yes", "no"]:
                raise ValueError("Invalid choice. Please enter 'yes' or 'no'.")
            return choice == "yes"
        except ValueError as e:
            typingPrint(f"{RED}{e}{RESET}\n")
            return restart_game()


def main():
    """
    Main function to start the game.
    """
    first_game = True
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        if first_game:
            username = get_username()
            display_username(username)
        else:
            typingPrint("\n Welcome back!!\n")
        if first_game:
            view_scores = input(
                "\nWould you like to view high scores? " "(yes/no): \n"
            ).lower()
            while view_scores not in ["yes", "no"]:
                view_scores = input(
                    "You must choose either 'yes' or 'no' "
                    "for viewing high scores: \n"
                ).lower()
            if view_scores == "yes":
                view_high_scores()
        difficulty_level = select_difficulty()
        global deck
        random.shuffle(deck)

        if first_game:
            view_instructions = input(
                "Would you like to view the instructions?" " (yes/no): \n"
            ).lower()
            while view_instructions not in ["yes", "no"]:
                view_instructions = input(
                    "You must choose either 'yes' or 'no' "
                    "for viewing instructions: \n"
                ).lower()
            if view_instructions == "yes":
                display_instructions()
        player_card = [deck.pop(), deck.pop()]
        computer_card = [deck.pop(), deck.pop()]

        player_continue = player_turn(deck, player_card)
        if (
            not player_continue
            or sum(card_value(card) for card in player_card) >= 21
        ):
            determine_winner(
                player_card, computer_card, username, difficulty_level
            )
            if not restart_game():
                os.system("cls" if os.name == "nt" else "clear")
                typingPrint("Thank you for playing! Goodbye\n")
                break
            else:
                first_game = False
                continue
        print("\nComputer's turn:")
        computer_continue = computer_turn(
            deck, computer_card, difficulty_level
        )
        if (
            not computer_continue
            or sum(card_value(card) for card in computer_card) >= 21
        ):
            determine_winner(
                player_card, computer_card, username, difficulty_level
            )
            if not restart_game():
                os.system("cls" if os.name == "nt" else "clear")
                print("Thank you for playing! Goodbye\n")
                break
            else:
                first_game = False
                continue
        determine_winner(
            player_card, computer_card, username, difficulty_level
        )

        if not restart_game():
            os.system("cls" if os.name == "nt" else "clear")
            typingPrint("Thank you for playing! Goodbye\n")

            break
        else:
            if first_game:
                first_game = False
            else:
                typingPrint("Welcome back!!\n")


if __name__ == "__main__":
    main()
