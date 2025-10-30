# Number Guessing Game
# Author: Mohit Sai
# Description: A simple game where you try to guess the number chosen by the computer.

import random  

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

# Generate a random number
secret_number = random.randint(1, 100)
attempts = 0  # To count how many guesses the player makes

# Start the game loop
while True:
    guess = input("Enter your guess: ")

    # Validate user input
    if not guess.isdigit():
        print("Please enter a valid number!")
        continue

    guess = int(guess)
    attempts += 1

    # Compare the guess with the secret number
    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print(f"Congratulations! You guessed it in {attempts} tries.")
        break  # End the loop once guessed correctly

print("Thanks for playing!")
