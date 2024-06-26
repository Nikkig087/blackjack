import random
import re
import time
import sys
import os
import termios
from colorama import Fore, Style
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("blackjack_top_scores")


def disable_input():
    """
    Disable terminal input echo.

    This function disables the echoing of input characters to the terminal.
    When input echo is disabled, characters typed by the user are not displayed
    on the screen. This is useful for scenarios like entering a password or
    any other sensitive input.

    Returns:
        list: The old terminal settings if the input is a TTY, otherwise None.
    """
    fd = sys.stdin.fileno()
    if os.isatty(fd):
        old_settings = termios.tcgetattr(fd)
        new_settings = termios.tcgetattr(fd)
        new_settings[3] = new_settings[3] & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
        return old_settings
    return None


def enable_input(old_settings):
    """
    Re-enable terminal input echo.

    This function restores the terminal settings to their original state,
    re-enabling the echoing of input characters. This means that characters
    typed by the user will again be displayed on the screen. It should be
    called after `disable_input` to ensure the terminal behaves as expected.

    Parameters:
        old_settings (list): The terminal settings to be restored. This should
                             be the value returned by `disable_input`.
    """
    fd = sys.stdin.fileno()
    if os.isatty(fd) and old_settings:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        termios.tcflush(fd, termios.TCIOFLUSH)


def typingPrint(text, delay_before=0, delay_after=0):
    """
    Print text gradually, simulating typing, with optional
    delays before and after.
    Parameters:
    - text: The text to be printed.
    - delay_before: Delay in seconds before starting to print text.
    - delay_after: Delay in seconds after printing the text.
    """
    old_settings = disable_input()

    if delay_before > 0:
        time.sleep(delay_before)
    for char in text:
        time.sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()
    if delay_after > 0:
        time.sleep(delay_after)
    sys.stdout.flush()  # Ensure output is flushed
    enable_input(old_settings)


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

        if len(topscore.get_all_values()) == 1:
            next_row = 2
        else:
            next_row = len(topscore.col_values(1)) + 1
        topscore.update_cell(next_row, 1, player_name)
        topscore.update_cell(next_row, 2, score)
        topscore.update_cell(next_row, 3, difficulty_word)
        typingPrint("Scores updated successfully.\n")
    except Exception as e:
        typingPrint("Error updating scores:", e)


def view_high_scores():
    """
    Display the top 10 high scores from my Google Sheets topscore worksheet.
    """
    old_settings = disable_input()

    try:

        topscore = SHEET.worksheet("topscore")
        high_scores = topscore.get_all_values()

        typingPrint("Top 10 High Scores:\n", delay_before=0, delay_after=0)

        data_rows = high_scores[1:]

        if not any(data_rows):
            typingPrint("No high scores yet!\n", delay_before=0, delay_after=0)
        else:
            header = high_scores[0]
            print(f"{' | '.join(header)}")
            print("-" * 30)

            data_rows.sort(key=lambda x: int(x[1]), reverse=True)

            for i, score in enumerate(data_rows[:10], 1):
                print(f"{i}. {score[0]} | {score[1]} | {score[2]} \n")
    finally:
        enable_input(old_settings)


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


BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT


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
            typingPrint(
                f"{RED}{BRIGHT}Please enter a valid first"
                f"name with only letters. {RESET} \n"
            )


def display_username(username):
    """
    Display a welcome message with the username.

    Args:
        username (str): The username to display.
    """
    print(" ")
    typingPrint(f"Welcome {username}! \n")


def select_difficulty():
    """
    Prompt the user to select a difficulty level.
    Returns:
        int: The selected difficulty level (1 for Beginner,
        2 for Intermediate, 3 for Advanced).
    """
    difficulty_levels = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
    typingPrint("Select difficulty level:\n")
    for level, desc in difficulty_levels.items():
        typingPrint(f"{level}. {desc}\n")
    choice = input("Enter either 1, 2, or 3: \n")
    while choice not in ["1", "2", "3"]:
        typingPrint(f"{RED}{BRIGHT}Please choose 1, 2, or 3 only: {RESET} \n")
        choice = input("")
    level = int(choice)
    print(" ")
    typingPrint(
        f"Great, you have chosen the" f" {difficulty_levels[level]} level\n"
    )
    print(" ")
    return level


def display_instructions():
    """
    Display the game instructions to the user.
    """
    typingPrint("Game Instructions\n")
    typingPrint(
        "Your goal is to achieve a score as close to"
        " 21 as possible but not over 21. \n"
    )
    typingPrint("Jack, Queen, and King cards" " are worth 10 points.\n")
    typingPrint(
        "Aces are worth either 1 or 11," " whichever is more favorable.\n"
    )
    typingPrint("You will be asked if you want another card.\n")
    typingPrint("Enter 'play' to request another card or 'stop' to stop.\n")
    typingPrint("Exceed 21 and you lose!\n")
    typingPrint(
        "Should you decide to stop, the dealer (the computer)\n"
        "will then draw cards until its score is at least 17.\n"
    )
    typingPrint("The player with the highest score wins! \n")


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
    lines = [" " for _ in range(6)]
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
        lines[0] += " ___________ "
        lines[1] += f"|{rank_str:<2}         | "
        lines[2] += "|            | "
        lines[3] += f"|    {suit_symbol}       | "
        lines[4] += "|            | "
        lines[5] += f"|________{rank_str:>1} | "
    for line in lines:
        print(line + "\n")


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
    while True:
        player_score = sum(card_value(card) for card in player_card)
        print(" \n")
        typingPrint("Your cards:\n")
        display_cards_ascii(player_card)
        typingPrint(f"Your score: {player_score} \n")

        if player_score >= 21:
            if player_score == 21:
                typingPrint(
                    f"{YELLOW}Congratulations! You have a Blackjack!!{RESET}\n"
                )
            else:
                typingPrint(f"{RED}Your score is over 21! You lose!{RESET}\n")
            return False
        typingPrint('What do you want to do? ("play" to'
                    ' request another card, "stop" to finish game): \n')
        sys.stdout.flush()
        choice = input().lower()
        while choice not in ["play", "stop"]:
            typingPrint(
                f"{RED}{BRIGHT}You must choose to either Play or Stop{RESET}\n"
            )
            sys.stdout.flush()
            choice = input().lower()
        if choice == "play":
            new_card = deck.pop()
            player_card.append(new_card)
            player_score = sum(card_value(card) for card in player_card)
            typingPrint("You drew:\n")
            typingPrint("\n")
            display_cards_ascii(new_card)
        else:
            print("\n")
            break
    return True


def computer_turn(deck, computer_card, difficulty_level):
    """
    Simulate the computer's turn in the game.

    Args:
        deck (list): The deck of cards.
        computer_card (list of tuples):
        List of tuples representing the computer's cards.
        difficulty_level (int): The level of difficulty
        (1 for Beginner, 2 for Intermediate, 3 for Advanced).

    Returns:
        bool: True if the computer continues playing,
        False if it busts or chooses to stop.
    """
    while True:
        computer_score = sum(card_value(card) for card in computer_card)
        if computer_score >= 17:
            break
        if random.random() < 0.5:
            new_card = deck.pop()
            computer_card.append(new_card)
        else:
            break
    typingPrint("Computer's Cards: \n")
    display_cards_ascii(computer_card)
    if computer_score > 21:
        print("Computer's Score:", computer_score)
        print(f"{RED}Computer is over 21,{YELLOW} you win!{RESET} \n")
        return False
    return True


def determine_winner(player_card, computer_card, username, difficulty_level):
    """
    Determine the winner of the game.

    Args:
        player_card (list of tuples):
        List of tuples representing the player's cards.
        computer_card (list of tuples):
        List of tuples representing the computer's cards.
        username (str): The username of the player.
        difficulty_level (int): The level of difficulty
        (1 for Beginner, 2 for Intermediate, 3 for Advanced).
    """
    player_score = sum(card_value(card) for card in player_card)
    computer_score = sum(card_value(card) for card in computer_card)
    typingPrint(f"Computer Score: {computer_score} \n")
    typingPrint(f"Your Score: {player_score} \n")

    if player_score == computer_score:
        typingPrint("It's a tie! \n")
    elif player_score == 21:
        typingPrint("Updating scores... \n")
        update_scores(username, player_score, difficulty_level)
    elif player_score <= 21 and (
        player_score > computer_score or computer_score > 21
    ):
        typingPrint(f"\n{YELLOW}You win!{RESET} \n")
        typingPrint("\nUpdating scores... \n")
        update_scores(username, player_score, difficulty_level)
    else:
        typingPrint(f"\n{BLUE}You lose!{RESET} \n")


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
                raise ValueError(
                    f"{RED}{BRIGHT}Invalid choice."
                    f"Please enter 'yes' or 'no'. {RESET}\n"
                )
            return choice == "yes"
        except ValueError as e:
            typingPrint(f"{RED}{e}{RESET} \n")
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
            typingPrint(f"Welcome back {username}!! \n")
        if first_game:
            print(" \n")
            typingPrint("Would you like to view high scores? (yes/no): \n")
            sys.stdout.flush()
            view_scores = input().lower()
            while view_scores not in ["yes", "no"]:
                typingPrint(
                    f"{RED}{BRIGHT}You must choose either 'yes'"
                    f" or 'no' for viewing high scores: {RESET} \n"
                )
                sys.stdout.flush()
                view_scores = input().lower()
            if view_scores == "yes":
                print(" \n")
                view_high_scores()
        print(" \n")
        difficulty_level = select_difficulty()
        global deck
        random.shuffle(deck)

        if first_game:
            typingPrint(
                "Would you like to view the instructions? (yes/no): \n"
            )
            sys.stdout.flush()
            view_instructions = input().lower()
            while view_instructions not in ["yes", "no"]:
                typingPrint(
                    f"{RED}{BRIGHT}You must choose either 'yes' or"
                    f" 'no' for viewing instructions:{RESET} \n"
                )
                sys.stdout.flush()
                view_instructions = input().lower()
            if view_instructions == "yes":
                print("\n")
                display_instructions()
                print("\n")
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
                typingPrint("Thank you for playing! Goodbye \n")
                break
            else:
                first_game = False
                continue
        typingPrint("Computer's turn: \n")
        sys.stdout.flush()
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
                typingPrint("Thank you for playing! Goodbye \n")
                break
            else:
                first_game = False
                continue
        determine_winner(
            player_card, computer_card, username, difficulty_level
        )

        if not restart_game():
            os.system("cls" if os.name == "nt" else "clear")
            typingPrint("Thank you for playing! Goodbye \n")
            break
        else:
            if first_game:
                first_game = False


if __name__ == "__main__":
    main()
