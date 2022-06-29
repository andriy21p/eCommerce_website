import string

def main():
    filename = input("Enter file name: ")
    file_object = open_file(filename)
    if file_object is not None:
        process_file(file_object)
    else:
        print("File {} not found!".format(filename))


def open_file(filename):
    '''Opens the given file, returning its file object if found, otherwise None'''
    try:
        file_object = open(filename, 'r')
        return file_object
    except FileNotFoundError:
        return None


def process_file(file_object):
    '''Processes the given file object'''
    word_list = get_word_tag_list(file_object)
    file_object.close()

    print_with_empty_line(word_list)
    word_list = remove_punctuation(word_list)
    print_with_empty_line(word_list)
    word_classes_dict = build_word_classes_dict(word_list)
    longest_word_for_class_dict = build_longest_word_for_class_dict(word_classes_dict)
    print_pretty_sorted(word_classes_dict)
    print_pretty_sorted(longest_word_for_class_dict)


def get_word_tag_list(file_stream):
    '''Returns a list of the words and tags found in the file stream'''
    word_list = []
    for line in file_stream:
        line_list = line.strip().split()
        for word in line_list:
            word_list.append(word)
    return word_list


def print_with_empty_line(collection):
    '''Prints an empty line followed by the collection'''
    print()
    print(collection)


def remove_punctuation(word_list):
    '''Returns a new list as a result of removing punctuation strings from the given list'''
    result_list = []
    for word in word_list:
        if not word in string.punctuation:
            result_list.append(word)

    return result_list


def build_word_classes_dict(word_list):
    '''Returns a dictionary in which word classes are keys (n, l, s, f, a, c)
    and the values are a set of words belonging to the given word class'''
    word_classes_dict = {}
    for i in range(0, len(word_list), 2):
        word = word_list[i]
        tag = word_list[i + 1]
        word_class = tag[0]  # the first letter in the tag is the word class
        if not word_class in word_classes_dict:
            word_classes_dict[word_class] = set()
        word_classes_dict[word_class].add(word)

    return word_classes_dict


def build_longest_word_for_class_dict(word_class_dict):
    '''Returns a dictionary with word classes as keys and the longest word in each word class as values
    If two words are equally long, the one appearing first alphabetical order is chosen'''
    longest_word_for_class_dict = {}

    for word_class in word_class_dict:
        for word in sorted(word_class_dict[word_class]):
            if word_class not in longest_word_for_class_dict or len(word) > len(
                    longest_word_for_class_dict[word_class]):
                longest_word_for_class_dict[word_class] = word

    return longest_word_for_class_dict


def print_pretty_sorted(word_classes_dict):
    '''Prints data from the dictionary in a pretty manner.
    The words or word belonging to each word class (key) are printed sorted.'''

    print()
    for word_class in sorted(word_classes_dict):
        # The values belonging to each word class are either a set of words or a single word string
        words_or_word = word_classes_dict[word_class]
        if type(words_or_word) == set:
            sorted_word_list = sorted(words_or_word)
        elif type(words_or_word) == str:
            sorted_word_list = [words_or_word]
        else:
            sorted_word_list = []  # Just in case the values are neither a set nor a string

        print("{}:".format(word_class))
        for word in sorted_word_list:
            print("{:>20s}".format(word))


# Main program starts here
if __name__ == "__main__":
    main