# Blackjack

Blackjack, also known as 21, is a popular card game played worldwide by people of all ages. 
The objective is simple: players aim to beat the dealer's hand without going over the value of 21. 
In this Python-based Blackjack game, players are interacting with the dealer(Computer Dealer). 

The game starts by prompting the player to select a difficulty level, then dealing cards to both the player and the computer. 
The Player can choose to draw additional cards ("hit") or stop drawing ("stand") to try and achieve a score as near to 21 in order to beat the Computer. The computer dealer follows a set of rules based on the chosen difficulty level, adding an element of strategy to the game. 

Once the player decides to stop drawing cards, the computer takes its turn, and the winner is determined based on the total scores of both the player and the computer. This Blackjack game offers an entertaining and challenging experience for players of all skill levels.

This project was built with Python3 as the "Python's Essentials" Project (portfolio project 3) for Code Insitute. 

[Link to live site](https://get-hung.herokuapp.com/)

![Responsive mock-up](assets/images/mockup.JPG)


## Index - Table of Contents

- [Planning](#planning)

- [Design](#design)

- [UX](#ux)
    - [Programm Goals](#programm-goals)
    - [User Stories](#user-stories)

- [Features](#features)
    - [Existing Features](#existing-features)
    - [Future Features](#possible-future-features)

- [Data Model](#data-model)

- [Testing](#testing)
    - [Validator Testing](#validator-testing)
    - [Browser Testing](#browser-testing)
    - [Testing User Stories](#testing-user-stories-functionality)

- [Debugging](#debugging)
    - [Fixed bugs](#fixed-bugs)
    - [Unfixed bugs](#unfixed-bugs)

- [Deployment](#deployment)

- [Credits](#credits)
    - [Data](#data)
    - [Code](#code)
    - [Styling](#styling)


## Planning

The following flowchart (created with [daigrams.net](https://app.diagrams.net/)) visualizes the planning process for this application.

![Flowchart](assets/images/GetHungFlow1.1.png)


## How the Game works

Game Setup:
The game begins with setting up the deck of cards, including shuffling the deck and dealing initial cards to the player and the computer (dealer).

Player Actions:
The player is presented with their initial hand and can choose to either "play" to request another card or "stop" to finish their turn.
If the player's total score exceeds 21, they lose the game immediately.

Computer Actions:
After the player finishes their turn, the computer (dealer) takes its turn according to the difficulty level selected.
The computer will continue to draw cards until its total score is at least 17.

Determining the Winner:
Once both the player and the computer have completed their turns, the winner is determined.
If the player's total score is closer to 21 than the computer's score (without exceeding 21), the player wins.
If the computer's total score is closer to 21 than the player's score (without exceeding 21), the computer wins.
If both the player and the computer have the same score or both exceed 21, it's a tie.

Game Output:
The game displays the final hands of both the player and the computer, along with their respective scores.
It announces the winner or declares a tie.

End of Game:
The game ends after determining the winner.
Players have the option to play again or exit the game.

## UX

### Programm Goals

The goal of this programm is to provide the user with a simple, easy to understand and play game of hangman that can be played multiple times without the challenge being repeated.

### User Stories

**As a user I want to**

New User Goals:
Learn how to play the game efficiently.
Understand the game rules and mechanics.
Enjoy a user-friendly interface for a smooth gaming experience.
Easily navigate through the game's features and options.

Frequent User Goals:
Master the strategies required to win the game consistently.
Explore different difficulty levels to challenge their skills.
Engage in competitive gameplay against the computer.
Provide feedback and suggestions for improving the game's features and usability.

Returning User Goals:
Explore any updates or improvements made to the game since their last play session.
Challenge themselves with different difficulty levels to enhance their skills.
Compete against the computer to achieve higher scores and improve their strategy.
Provide feedback on their experience to help shape future updates and optimizations.


## Features

### Existing Features

**Logo**
- Displays game title using ASCII

![logo](assets/images/logo.JPG)

**Introduction and Rules**
- Gives the user a brief run through the game and how to play it

![game intro](assets/images/intro-rules.JPG)

**Level choice**
- Allows user to choose one of three difficulty levels

![level choice](assets/images/level-choice.JPG)

**Invalid Data Error**
- Informs the user if input data was not valid
- Tells the user which data type is required and what was typed incorrectly
- Displays for invalid level and letter input

![invalid level](assets/images/invalid-level.JPG)

![invalid letter](assets/images/invalid-letter.JPG)

**Cards Drawn display**
- Shows the Cards the player has drawn

![used letters](assets/images/used-letters.JPG)



**Game won message**
- Informs and congratulates user when game is won
- Shows after fully displayed word

![game won message](assets/images/game-won.JPG)

**Game lost message**
- Informs user when game is lost
- Reveals to user the word that was to be guessed

![game lost message](assets/images/game-lost.JPG)

**Restart Game option**
- Offers user the choice to play again after finishing the game

![restart game](assets/images/restart-game.JPG)


### Possible Future Features

**High Scores


## Data Model


*Data Validation*

To make use of the ```try``` and ```except``` statements, I created the two functions ```validate_level``` and ```validate_letter```. Both functions raise a value error if data input by the user is not valid for each specific case. 
In the initial version invalid data was simply handled with a print statement in an ```else``` clause (which may have sufficed in the case of this simple application). But for the sake of writing industry compliant code, I decided to outsource data validation to a specific function that raises a proper error. 

## Testing

### Validator Testing

- HTML, CSS and JavaScript validation does not apply to this project. The template provided by Code Institute as provided to all students is assumed to be tested for the above.
No further change or manipulation of the template's default HTML, CSS and JavaScript files has been performed.

- Python Validator [PEP8](http://pep8online.com/)

    - **Error**: Line too long on 13 lines of code

    - **Solution**: Break up lines of code using ``` \ ```

    No further errors or warnings.

    ![PEP8 results](assets/images/pep8-final-result.JPG)

- Performance, Accessibility, SEO, Best Practices (Lighthouse Chrome DevTools)

    ![Lighthouse results](assets/images/lighthouse-results.JPG)

    As SEO was not an objective of this particular project, I chose to be content with a rating that is barely below 90. 

### Browser Testing

Ensuring all parts of the programm function as expected in all major browsers.

| Browser     | Layout      | Functionality |
| :---------: | :----------:| :-----------: |
| Chrome      | ✔          | ✔             |
| Edge        | ✔          | ✔             |
| Firefox     | ✔          | ✔             |
| Safari      | ✔          | ✔             |
| IE          |deprecated by Microsoft, not tested|


### Testing User Stories (Functionality)

| Expectation (As a user, I want to...)  | Result (As a user, I...)    |
| :---------------------------------: | :------------------------------:|
| be able to read an introduction when first loading the programm | see a quick game introduction print out on the screen when the programm loads |
| read the rules to the game in short and consice text | see the game rules explained clearly as part of the introduction |
| choose a difficulty level | can choose between 3 levels: easy, medium, hard |

| be informed if my data input is not valid and why | see an error message after I input invalid data, telling me what data type is required |
||
| know when the game is over (won or lost) | can read a message telling me I either won or lost the game when the game terminates |
| be able to restart the game or not when after it's finished | can choose between a Y/N option to restart the game after finishing |

## Debugging

### Fixed Bugs

**Formatting**

To guarantee consistent line breaks, whitespaces and indentation, run.py and words.py were formatted using [Black Playground](https://black.vercel.app/)

**Word not displaying fully when game won**:

After entering the last letter of the fully guessed word, the last letter is not added to the word display. Therefore the finished word doesn't display properly.

*Solution*:

Run display_word function again when condition for game completion is met:
```
elif len(word_letters) == 0:
    display_word()
    print("🎉 Well done! You guessed the whole word 🎉")
```

### Unfixed Bugs

No unfixed bugs to date.

## Deployment

This project was deployed with Heroku using Code Institute's mock terminal as provided with the Python Essentials template.

To deploy:

- Clone or fork this public repository
- Create a Heroku account (if not already existing)
- Create a new app with Heroku
- In **Settings**, add 2 buildpacks:
    - ```Python```
    - ```NodeJS```
    
    Ensure the buildpacks are created in that order!

- Allowing Heroku access to GitHub, link the new app to the relevant repository
- Choose whether or not to enable **Automatic Deploys**. If enabled, the deployed app will update automatically with each push to GitHub
- Click **Deploy**

## Credits

### Data

- **Word List**: 



- **Logo**:

    [Text to ASCII Art Generator](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20)

    Font: Ogre.


### Code

- **Template and Terminal**

    [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template) provided by Code Institute 




### Styling

- **Colours**

    Built-in module [Colorama](https://github.com/techwithtim/ColoredTextInPython/blob/main/main.py)

- **Timing**

    [time module](https://www.freecodecamp.org/news/the-python-sleep-function-how-to-make-python-wait-a-few-seconds-before-continuing-with-example-commands/#:~:text=Make%20your%20time%20delay%20specific,after%20a%20slight%20delay.%22) and sleep() function