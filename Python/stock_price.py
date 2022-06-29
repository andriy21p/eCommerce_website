def main():
    repeat = 'y'
    while repeat.lower() == 'y':
        shares = get_shares()
        if shares is not None:
            dollars, numer, denom = get_price_info()
            price = convert(dollars, numer, denom)
            market_value = price * shares
            display_result(shares, dollars, numer, denom, market_value)
            repeat = input("Continue (y/n): ")
        else:
            print("Invalid number of shares!")


def get_shares():
    '''Returns the number of shares input by user'''
    shares_str = input("Enter number of shares: ")
    try:
        shares_int = int(shares_str)
        return shares_int
    except ValueError:
        return None


def get_price_info():
    '''Returns price info input by user'''
    dollars, numerator, denominator = input("Enter price (dollars, numerator, denominator): ").split()
    return int(dollars), int(numerator), int(denominator)


def convert(dollars, numerator, denominator):
    '''Converts a price stated with integer values into a float'''
    return dollars + numerator / denominator


def display_result(shares, dollars, numerator, denominator, value):
    """Display results"""
    print("{:d} shares with market price {:d} {:d}/{:d} have value ${:.2f}".format(shares, dollars, numerator,
                                                                                   denominator, value))


# Main program starts here
if __name__ == "__main__":
    main()