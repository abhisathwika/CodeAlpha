import random
import nltk

# Ensure necessary corpora are downloaded
nltk.download('words')
from nltk.corpus import words

# Function to choose a random word from the nltk words corpus
def get_random_word():
    word_list = words.words()  # List of English words from nltk corpus
    return random.choice(word_list).lower()

# Function to display the current state of the word
def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += " _ "
    return display

# Main function to run the game
def hangman():
    word = get_random_word()  # Randomly select a word from nltk
    guessed_letters = []  # List of guessed letters
    incorrect_guesses = 0  # Number of incorrect guesses
    max_incorrect_guesses = 6  # Limit on the number of incorrect guesses allowed

    print("Welcome to Hangman!")
    print("Try to guess the word.")

    while incorrect_guesses < max_incorrect_guesses:
        print("\nCurrent word: ", display_word(word, guessed_letters))
        print(f"Incorrect guesses left: {max_incorrect_guesses - incorrect_guesses}")
        print("Guessed letters: ", guessed_letters)

        # Get user input
        guess = input("Guess a letter: ").lower()

        # Check if input is valid (single letter)
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a valid letter.")
            continue

        # Check if the letter has already been guessed
        if guess in guessed_letters:
            print("You've already guessed that letter.")
            continue

        guessed_letters.append(guess)

        # Check if the guessed letter is in the word
        if guess in word:
            print(f"Good guess! The letter '{guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print(f"Wrong guess! The letter '{guess}' is not in the word.")

        # Check if the player has won
        if all(letter in guessed_letters for letter in word):
            print("\nCongratulations! You've guessed the word:", word)
            break
    else:
        print(f"\nGame over! You've run out of guesses. The word was: {word}")

# Start the game
hangman()
