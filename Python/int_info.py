def main():
    input_list = get_data()
    if input_list is not None:
        print("The numbers:", input_list)
        print("Unique numbers:", unique_elements(input_list))
        the_average = average_number(input_list)
        print("Average number: {:.2f}".format(the_average))
        print("Numbers > average:", filter_list(input_list, the_average))
        print("Numbers > average + 2:", filter_list(input_list, the_average + 2))
        freq_info = input("Frequency info? (y/n): ")
        if freq_info == 'y':
            most_frequent, frequency = get_most_frequent_number(input_list)
            print("Most frequent number is {} with frequency {}".format(most_frequent, frequency))
    else:
        print('Invalid input!')


def get_data():
    ''' Returns an ordered list of integers input by a user.
        None is returned if the input contains non-integers
    '''
    a_list = input('Enter integers separated with commas: ').split(',')
    try:
        int_list = [ int(elem) for elem in a_list]
        return sorted(int_list)
    except ValueError:
        return None


def unique_elements(a_list):
    ''' Returns a new list containing the unique elements in a_list '''
    number_set = set(a_list)
    return sorted(list(number_set))

def average_number(int_list):
    '''Returns the average of the numbers in the given list'''
    return sum(int_list) / len(int_list)


def filter_list(int_list, threshold):
    '''Returns a new list containing all numbers from int_list which are greater than the threshold'''
    new_list = [ elem for elem in int_list if elem > threshold]
    return new_list


def get_most_frequent_number(int_list):
    '''Return the most frequent number and its frequency from the int_list'''
    frequency_of_most_frequent = 0
    most_frequent_num = None

    freq_dict = build_frequency_dict(int_list)
    for num, freq in freq_dict.items():
        if freq > frequency_of_most_frequent:
            frequency_of_most_frequent = freq
            most_frequent_num = num

    return most_frequent_num, frequency_of_most_frequent


def build_frequency_dict(int_list):
    '''Returns a frequency dictionary derived from the int_list'''
    freq_dict = {}
    for elem in int_list:
        if elem not in freq_dict:
            freq_dict[elem] = 1
        else:
            freq_dict[elem] += 1

    return freq_dict


# Main program starts here
if __name__ == "__main__":
    main()