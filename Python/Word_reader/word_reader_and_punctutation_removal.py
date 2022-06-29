COMPARATIVE_SUFFIX = "er"
SUPERLATIVE_SUFFIX = "est"


def main():
    file_name = input("Enter filename: ")
    file_stream = open_file(file_name)
    if file_stream:
        all_words = get_words(file_stream)
        print_word_info(all_words)

        should_remove_punct = input("Remove punctuation (y/n)?: ")
        if should_remove_punct.lower() == 'y':
            all_words = remove_punct(all_words)
            print_word_info(all_words)

        positive = input("Enter an adjective (positive form): ")
        adj_tuple = get_adjectives_tuple(positive, all_words)
        print(adj_tuple)

        file_stream.close()
    else:
        print("File {} not found!".format(file_name))


def open_file(filename):
    ''' Returns a file stream if filename found, otherwise None '''
    try:
        file_stream = open(filename, "r")
        return file_stream
    except FileNotFoundError:
        return None


def get_words(file_stream):
    '''Returns a lower case list of the words in the file (space used as a separator)'''
    all_words = []
    for line in file_stream:
        words_in_line = line.strip().split()
        for word in words_in_line:
            all_words.append(word.lower())
    return all_words


def remove_punct(word_list):
    '''Returns a new list for which punctuation has been removed from individual words in word_list'''
    new_list = []
    for word in word_list:
        alphanumeric = ''
        for character in word:
            if character.isalnum():
                alphanumeric += character
        if alphanumeric != '':
            new_list.append(alphanumeric)

    return new_list


def print_word_info(word_list):
    '''Prints info about the word list'''
    print(word_list)
    print("Found {} words".format(len(word_list)))


def get_adjectives_tuple(positive, word_list):
    '''Returns a tuple of (positive, comparative, superlative) form of an adjective.
    If any of the forms is not found, the corresponding part is empty in the tuple.'''
    comparative = positive + COMPARATIVE_SUFFIX
    superlative = positive + SUPERLATIVE_SUFFIX
    return (find_word(positive, word_list), find_word(comparative, word_list), find_word(superlative, word_list))


def find_word(word, word_list):
    '''Returns the word if it is found in word_list, otherwise ""'''
    return word if word in word_list else ''


# Main program starts here
if __name__ == "__main__":
    main()