# Guess a random number
import random

numToGuess = random.randint(1,25)
maxGuesses = 7
totGuesses = 0
guesses = []


def processGuess(guessNum):
    global guesses
    try:
        if int(guessNum) in guesses:
            print("You already guessed that number. Please try again.")
        else:
            if int(guessNum) == numToGuess:
                print("Good guess! You got it")
                keepGuessing = False
            else:
                print("Sorry, that guess was incorrect. Please try again.")
                if int(guessNum) < numToGuess:
                    print("Here's a hint, your guess was low.")
                else:
                    print("Here's a hint, your guess was high.")
                guesses.append(int(guessNum))
#                print(guesses)
    except ValueError:
        print("Please enter a number between 1 and 10.")

keepGuessing = True

print("What is your name? ")
player = input()
while keepGuessing:
    print(player + ", what is your guess? ")
    guessNum = input()
    totGuesses += 1
    if guessNum == 'Q' or guessNum == 'q':
        print("I hope you enjoyed playing the game.")
        break
    else: 
        processGuess(guessNum)
    if totGuesses > maxGuesses:
        print("Sorry, that was your last guess. The number was " + str(numToGuess))
        keepGuessing = False
