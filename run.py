import random
import pygame
import sys

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
    print(r"""
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
""")
    return input("Enter your username: ")


def display_username(username):
    print(f'Welcome {username}!')


def select_difficulty():
    '''
    Function to ask user to choose a difficulty level to play the game.
    '''
    difficulty_levels = {
        1: "Beginner",
        2: "Intermediate",
        3: "Advanced"
    }
    print("Select difficulty level:")
    for level, desc in difficulty_levels.items():
        print(f"{level}. {desc}")
    choice = input("Enter either 1, 2, or 3: ")
    while choice not in ['1', '2', '3']:
        print("Please choose 1, 2, or 3 only")
        choice = input("Enter either 1, 2, or 3: ")
    level = int(choice)
    print(f"Great, you have chosen the {difficulty_levels[level]} level")


def display_instructions():
    '''
    Instructions on how to play the game and the rules.
    '''
    print("\nGame Instructions\n")
    print("Your goal is to achieve a score as close to 21 as possible without going over 21.")
    print("Jack, Queen, and King cards are worth 10 points.")
    print("Aces are worth either 1 or 11, whichever is more favorable.")
    print("You will be asked if you want another card.")
    print("Enter 'play' to request another card or 'stop' to stop.")
    print("Exceed 21 and you lose!")
    print("Should you wish to stop, the dealer (the computer) will then draw cards until its score is at least 17.")
    print("The player with the highest score wins!")


def display_cards_ascii(cards):
    """
    Display the given cards as ASCII art in a row.
    """
    # Define suit symbols
    suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

    # Check if cards is a single tuple or a list of tuples
    if isinstance(cards, tuple):
        cards = [cards]

    # Initialize empty lines list
    lines = ['' for _ in range(6)]

    # Iterate over cards and add their ASCII art to the lines list
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

    # Print each line
    for line in lines:
        print(line)


def player_turn(deck, player_card):
    while True:
        player_score = sum(card_value(card) for card in player_card)
        print("\nYour cards:")
        for card in player_card:
            display_cards_ascii(card)
        print("Your score:", player_score)
        choice = input('What do you want to do? ["play" to request another card, "stop" to finish game]: ').lower()
        while choice not in ["play", "stop"]:
            print("You must choose to either Play or Stop")
            choice = input('What do you want to do? ["play" to request another card, "stop" to finish game]: ').lower()

        print(
r"""
 _    _ _______ _    _ _____   _______ _    _ 
| |  | |__   __| |  | |  __ \ / ____| |  | |
| |__| |  | |  | |__| | |__) | |    | |__| |
|  __  |  | |  |  __  |  ___/| |    |  __  |
| |  | |  | |  | |  | | |    | |____| |  | |
|_|  |_|  |_|  |_|  |_|_|     \_____|_|  |_|   
""")


        if choice == "play":
            new_card = deck.pop()
            player_card.append(new_card)
            player_score = sum(card_value(card) for card in player_card)
            print("You drew:")
            display_cards_ascii(new_card)
            if player_score > 21:
                print("Your Cards:")
                for card in player_card:
                    display_cards_ascii(card)
                print("Your Score:", player_score)
                print("You are over 21, you lose!")
                return False
        elif choice == "stop":
            break
    return True


def computer_turn(deck, computer_card):
    while True:
        computer_score = sum(card_value(card) for card in computer_card)
        if computer_score >= 17:
            break
        new_card = deck.pop()
        computer_card.append(new_card)
        computer_score = sum(card_value(card) for card in computer_card)
        print("Computer drew:")
        display_card_ascii(new_card)
        if computer_score > 21:
            print("Computer's Cards:")
            for card in computer_card:
                display_card_ascii(card)
            print("Computer's Score:", computer_score)
            print("Computer is over 21, you win!")
            return False
    return True


def determine_winner(player_card, computer_card):
    player_score = sum(card_value(card) for card in player_card)
    computer_score = sum(card_value(card) for card in computer_card)
    if player_score <= 21 and (player_score > computer_score or computer_score > 21):
        print("\nYour Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in player_card))
        print("Your Score:", player_score)
        print("Computer Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in computer_card))
        print("Computer Score:", computer_score)
        print("You win!")
    elif computer_score <= 21 and (computer_score > player_score or player_score > 21):
        print("\nYour Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in player_card))
        print("Your Score:", player_score)
        print("Computer Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in computer_card))
        print("Computer Score:", computer_score)
        print("Computer wins!")
    else:
        print("\nYour Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in player_card))
        print("Your Score:", player_score)
        print("Computer Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in computer_card))
        print("Computer Score:", computer_score)
        print("It's a tie.")



# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Over")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
player_win_image = pygame.image.load("player_win_image.png")
computer_win_image = pygame.image.load("computer_win_image.png")
tie_image = pygame.image.load("tie_image.png")

# Function to display game over screen
def game_over_screen(winner):
    screen.fill(WHITE)  # Fill the screen with white color
    
    # Display different images based on the winner
    if winner == "player":
        screen.blit(player_win_image, (0, 0))
    elif winner == "computer":
        screen.blit(computer_win_image, (0, 0))
    else:
        screen.blit(tie_image, (0, 0))

    pygame.display.flip()  # Update the display

# Main loop


def main():
    # Initialize the game
    def main():
        winner = determine_winner(player_card, computer_card)  # Determine the actual winner of the game
        game_over_screen(winner)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    username = get_username()
    display_username(username)
    select_difficulty()
    global deck
    random.shuffle(deck)

    # Give option to display instructions
    view_instructions = input("Would you like to view the instructions? (yes/no): ").lower()
    while view_instructions not in ["yes","no"]:
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
        return

    # Computer's turn
    print("\nComputer's turn:")
    computer_continue = computer_turn(deck, computer_card)
    if not computer_continue or sum(card_value(card) for card in computer_card) >= 21:
        # End game if computer loses or reaches 21
        determine_winner(player_card, computer_card)
        return

    # Determine winner
    determine_winner(player_card, computer_card)


if __name__ == "__main__":
    main()
