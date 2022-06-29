FIRST_LETTER = 'A'
BOOKED_LETTER = 'X'


def main():
    no_of_rows, no_of_seats = get_rows_columns()

    done = False
    seating = initialize_seating(no_of_rows, no_of_seats)
    display_seating(seating, no_of_rows, no_of_seats)

    while not done:
        (row, seat_letter) = get_valid_seat(no_of_rows, no_of_seats)
        success = book_seat(seating, row, seat_letter)
        if success:
            display_seating(seating, no_of_rows, no_of_seats)
            if seat_available(seating):
                answer = input("More seats (y/n)? ")
                done = answer != 'y'
            else:
                done = True
        else:
            print('That seat is taken!')


def get_rows_columns():
    ''' Returns the dimensions of the seatings '''
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of seats in each row: "))
    return rows, cols


def initialize_seating(no_of_rows, no_of_seats):
    ''' Returns an empty seating allocation: list of lists
        Each seat in each row is marked with a letter, starting from "A" '''
    seating = []
    for _ in range(0, no_of_rows):
        seats = []
        # creates consecutive letters starting from first_letter
        for col in range(0, no_of_seats):
            next_letter = chr(ord(FIRST_LETTER) + col)
            seats.append(next_letter)
        seating.append(seats)
    return seating


def display_seating(seating, no_of_rows, no_of_seats):
    ''' Displays the given seating '''
    for row in range(0, no_of_rows):
        print("{:>2d}".format(row + 1), end='  ')
        for col in range(0, no_of_seats):
            seat = seating[row][col]
            print(seat, end=' ')
            if col + 1 == no_of_seats / 2:
                print('  ', end='')
        print()


def get_valid_seat(no_of_rows, no_of_seats):
    '''Prompt the user for a seat number until a valid seat is given'''
    valid = False
    while not valid:
        row, seat_letter = get_seat(no_of_rows, no_of_seats)
        valid = valid_seat(row, seat_letter, no_of_rows, no_of_seats)
        if not valid:
            print("Seat number is invalid!")

    return (int(row), seat_letter)


def get_seat(no_of_rows, no_of_seats):
    ''' Gets a seat request from user '''
    row_seat_str = input("Input seat number (row seat): ")
    row, seat_letter = row_seat_str.strip().split()
    return row, seat_letter


def book_seat(seating, row, seat_letter):
    ''' Books a seat by user request
        Return true if booking is successful, else false'''
    col = ord(seat_letter) - ord(FIRST_LETTER)
    if seating[row - 1][col] != BOOKED_LETTER:
        seating[row - 1][col] = BOOKED_LETTER
        return True

    return False


def seat_available(seating):
    ''' Returns true if a seat is available, else false '''
    for row in seating:
        for seat in row:
            if seat != BOOKED_LETTER:
                return True
    return False


def valid_seat(row, seat_letter, no_of_rows, no_of_seats):
    ''' Returns true if the given seat is valid, else false '''
    try:
        row = int(row)
        return row >= 1 and row <= no_of_rows and seat_letter >= FIRST_LETTER and ord(seat_letter) <= ord(
            FIRST_LETTER) + no_of_seats - 1
    except ValueError:
        return False


# Main program starts here
if __name__ == "__main__":
    main()