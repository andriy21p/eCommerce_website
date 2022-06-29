import random

MAX_GUESSES = 12
CHAR_PLACEHOLDER = '-'


def main():
    file_name = input("Enter filename: ")
    file_object = open_file(file_name)
    if file_object is not None:
        random_seed()
        word_list = get_words_from_file(file_object)
        secret_word = get_secret_word(word_list)
        guess_word = initialize_guess_word(secret_word)
        print_instructions(guess_word)
        play(secret_word, guess_word)
    else:
        print("File {} not found!".format(file_name))


def open_file(filename):
    '''Opens the given file, returning its file object if found, otherwise None'''
    try:
        file_object = open(filename, 'r')
        return file_object
    except FileNotFoundError:
        return None


def random_seed():
    '''Initializes the random number generator'''
    seed = int(input("Random seed: "))
    random.seed(seed)


def get_secret_word(word_list):
    '''Returns a random secret word from the given word list'''
    secret_word = random.choice(word_list)
    return secret_word


def get_words_from_file(file_object):
    '''Returns a list of words read from the file object'''
    word_list = []
    for word in file_object:
        word_list.append(word.strip())

    return word_list


def initialize_guess_word(secret_word):
    '''Returns an initialized guess word in the form of a list'''
    guess_word = [CHAR_PLACEHOLDER] * len(secret_word)
    return guess_word


def print_instructions(guess_word):
    print("The secret word has", len(guess_word), "characters")


def print_current_guess_word(guess_word):
    print("Word to guess: {}".format(" ".join(guess_word)))


def process_guess(guess, num_guesses, secret_word, guess_word, letter_storage):
    '''Processes the guess and prints out appropriate messages'''
    if guess in letter_storage:
        print("Duplicate guess!")
    else:
        letter_storage.add(guess)
        num_guesses += 1
        if guess in secret_word:
            print("You guessed correctly!")
            for i in range(0, len(secret_word)):
                if secret_word[i] == guess:
                    guess_word[i] = guess
        else:
            print("Incorrect letter!")
    return num_guesses


def play(secret_word, guess_word):
    '''Plays the game'''
    letter_storage = set()
    num_guesses = 1
    has_won = False

    while num_guesses <= MAX_GUESSES and not has_won:
        print("\nGuess {} of {}".format(num_guesses, MAX_GUESSES))
        print_current_guess_word(guess_word)
        guess = input("Choose a letter: ").lower()
        num_guesses = process_guess(guess, num_guesses, secret_word, guess_word, letter_storage)
        if not CHAR_PLACEHOLDER in guess_word:
            print("You won!")
            has_won = True

    if not has_won:
        print("You lost! The secret word was {}".format(secret_word))


# Main program starts here
if __name__ == "__main__":
    main()