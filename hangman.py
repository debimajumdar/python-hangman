# assignment: Hangman
# author: Debi Majumdar
# date: 1/22/2023
# file: hangman.py is a program that allows one to play the game Hangman
# input: No file input @ command time (Scripts will collect and parse user input via prompts to get settings and guesses)
# output: (Terminal output to show status of game and prompts to play the game)

from random import choice

dictionary_file = "dictionary-short.txt"  # make a dictionary.txt in the same folder where hangman.py is located


# make a dictionary from a dictionary file ('dictionary.txt', see above)
# dictionary keys are word sizes (1, 2, 3, 4, …, 12), and values are lists of words
# for example, dictionary = { 2 : ['Ms', 'ad'], 3 : ['cat', 'dog', 'sun'] }
# if a word has the size more than 12 letters, put it into the list with the key equal to 12

def import_dictionary(filename):
    dictionary = {Lenlist: [] for Lenlist in range(1, 13)}
    try:
        f = open(filename, "r")
        max_size = 12
        for line in f:
            word = line.strip()
            word_length = len(word)
            if word_length > 0:
                if word_length < max_size:
                    dictionary[word_length].append(word)
                else:
                    dictionary[max_size].append(word)
        # categorize dictionary keys
        return dictionary
    except Exception as e:
        print(e)


# print the dictionary (use only for debugging)
def print_dictionary(dictionary):
    pass



def get_game_options():
    print('Please choose a size of a word to be guessed [3 - 12, default any size]:')
    user_input_size = input()
    print('The word size is set to ' + user_input_size + '.')
    if (user_input_size.strip().isdigit()):
        size = int(user_input_size)
        # invalid range then throw error
        if (size not in range(1, 12)):
            pass
    print('Please choose a number of lives [1 - 10, default 5]:')
    user_input_lives = None
    lives = 5
    while user_input_lives is None:
        user_input_lives = input()
        if (user_input_lives.strip().isdigit()):
            lives = int(user_input_lives)
            # invalid range then throw error
            if (lives not in range(1, 12)):
                pass
    print('You have ' + str(lives) + ' lives.')
    return (size, lives)


def uppercase(letter):
    return letter.capitalize()


def lowercase(letter):
    return letter.lower()


def print_status(lives_remaining, letters_used, word, num_lives):
    lives_status = ''
    for i in range(num_lives - lives_remaining):
        lives_status += 'X'
    for i in range(lives_remaining):
        lives_status += 'O'
    print('Letters chosen:', end=' ')
    formatted_letters_used = list(map(uppercase, letters_used))
    print(*formatted_letters_used, sep=', ')
    letters_status = ''
    for letter in word.lower():
        if letter in list(map(lowercase, letters_used)) or letter == '-':
            letters_status += letter.capitalize()
        else:
            letters_status += '__'
        letters_status += ' '

    print('{} lives: {} {}'.format(letters_status, lives_remaining, lives_status))


# MAIN

if __name__ == '__main__':
    # make a dictionary from a dictionary file
    dictionary = import_dictionary(dictionary_file)

    # print the dictionary (use only for debugging)

    # print a game introduction
    print('Welcome to the Hangman Game!')
    # START MAIN LOOP (OUTER PROGRAM LOOP)
    play = True
    while play:
        # set up game options (the word size and number of lives)
        word_size, num_lives = get_game_options()


        possible_words = dictionary[word_size]
        word = choice(possible_words)
        display_word = word
        # Adjust for dashes in words like T-shirt or Self-Esteem
        word.replace('-', '.')
        letters_chosen = []
        lives_remaining = num_lives
        print_status(lives_remaining, letters_chosen, display_word, num_lives)
        # START GAME LOOP   (INNER PROGRAM LOOP)
        while lives_remaining > 0:

            guess = ''
            # collect input until valid
            while len(guess) != 1 or not guess.isalpha() or guess in letters_chosen:
                print('Please choose a new letter >')
                guess = input()
                # if the letter is correct update the hidden word,
                # else update the number of lives
                # and print interactive messages
                if guess is not None:
                    if guess in letters_chosen:
                        print('You have already chosen this letter.')
            # Valid one letter alphabetic input then ->
            if guess not in word:
                lives_remaining -= 1
                print('You guessed wrong, you lost one life.')
            else:
                print('You guessed right!')
            letters_chosen.append(guess)
            # print the status once the processing has been completed
            print_status(lives_remaining, letters_chosen, word, num_lives)
            if all(guessed in list(map(lowercase, letters_chosen)) for guessed in word.replace('-', '').lower()):
                print('Congratulations!!! You won! The word is {}!'.format(word.upper()))
                print('Would you like to play again [Y/N]?')
                break
        # If no more lives are remaining, then declare the game lost and ask about replaying
        if lives_remaining == 0:
            print('You lost! The word is {}!'.format(word.upper()))
            print('Would you like to play again [Y/N]?')

        # Get play input for the letter
        play_input = input()
        # set boolean to if play == Y, since that means TRUE(play)
        play = play_input == 'Y' or play_input == 'y'

        # check if the user guesses the word correctly or lost all lives,
        # if yes finish the game
    print('Goodbye!')
    # END MAIN LOOP (OUTER PROGRAM LOOP)

    # ask if the user wants to continue playing,
    # if yes start a new game, otherwise terminate the program\
