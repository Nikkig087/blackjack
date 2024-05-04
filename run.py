import random

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


def player_turn(deck, player_card):
    while True:
        player_score = sum(card_value(card) for card in player_card)
        print("\nYour cards:", ', '.join(f"{card[0]} of {card[1]}" for card in player_card))
        print("Your score:", player_score)
        choice = input('What do you want to do? ["play" to request another card, "stop" to finish game]: ').lower()
        while choice not in ["play", "stop"]:
            print("You must choose to either Play or Stop")
            choice = input('What do you want to do? ["play" to request another card, "stop" to finish game]: ').lower()
            # Print generating image

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
            print("You drew:", f"{new_card[0]} of {new_card[1]}")
            if player_score > 21:
                print("Your Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in player_card))
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
        print("Computer drew:", f"{new_card[0]} of {new_card[1]}")
        if computer_score > 21:
            print("Computer's Cards:", ', '.join(f"{card[0]} of {card[1]}" for card in computer_card))
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


def main():
    # Initialize the game
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
