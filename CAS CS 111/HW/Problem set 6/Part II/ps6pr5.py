#
# ps6pr5.py (Problem Set 6, Problem 5)
#
# TT Securities    
#
# Computer Science 111
#

import math

def display_menu():
    """ prints a menu of options
    """  
    print()
    print('(0) Input a new list of prices')
    print('(1) Print the current prices')
    print('(2) Find the latest price')
    ## Add the new menu options here.
    print('(3) Find the average price')
    print('(4) Find the standard deviation')
    print('(5) Find the max price and its day')
    print('(6) Test a threshold')
    print('(7) Your investment plan')
    print('(8) Quit')

def get_new_prices():
    """ gets a new list of prices from the user and returns it
    """
    new_price_list = eval(input('Enter a new list of prices: '))
    return new_price_list

def print_prices(prices):
    """ prints the current list of prices
        input: prices is a list of 1 or more numbers.
    """
    if len(prices) == 0:
        print('No prices have been entered.')
        return
    
    print('Day Price')
    print('--- -----')
    for i in range(len(prices)):
        print('%3d' % i, end='')
        print('%6.2f' % prices[i])

def latest_price(prices):
    """ returns the latest (i.e., last) price in a list of prices.
        input: prices is a list of 1 or more numbers.
    """
    return prices[-1]

## Add your functions for options 3-7 below.
def avg_price(prices):
    """ takes a list of 1 or more prices and computes and returns the average
        price
        input: prices is a list of 1 or more numbers
    """
    t = len(prices)
    total = 0
    for i in range(t):
        v = prices[i]
        total += v
    avg = total / t
    return avg

def std_dev(prices):
    """ takes a list of 1 or more prices and computes and returns the standard
        deviation of the prices
        input: prices is a list of 1 or more numbers.
    """
    total = 0
    for i in range(len(prices)):
        t = prices[i] - avg_price(prices)
        total += t **2
    total = total / len(prices)
    result = math.sqrt(total)
    return result

def max_day(prices):
    """ takes a list of 1 or more prices and computes and returns the day of 
        the maximun price
        input: prices is a list of 1 or more numbers.
    """
    day = 0 
    for i in range(len(prices)):
        if prices[i] > prices[day]:
            day = i
    return day
        
def any_below(prices, n):
    """ takes a list of 1 or more prices and an integer threshold, and uses a 
        loop to determine if there are any prices below that threshold
        input: prices is a list of 1 or more numbers, n is an integer threshold
    """
    for i in range(len(prices)):
        if prices[i] < n:
            return True
    return False

def find_plan(prices):
    """ takes a list of 2 or more prices, and that uses one or more loops to 
        find the best days on which to buy and sell the stock whose prices are 
        given in the list of prices
        input: prices is a list of 2 or more numbers.
    """
    n = []
    buy = 0
    sell = 0
    profit = 0
    x = 0
    for i in range(len(prices)):
        rest = prices[i+1:]
        for j in range(len(rest)):
            d = rest[j] - prices[i]
            if d > profit:
                profit = d
                x = rest[j] 
                buy = i  
    for y in range(len(prices)):
       if prices[y] == x:
          sell = y
    n =[buy] + [sell] + [profit]
    return n

def tts():
    """ the main user-interaction loop
    """
    prices = []

    while True:
        display_menu()
        choice = int(input('Enter your choice: '))
        print()

        if choice == 0:
            prices = get_new_prices()
        elif choice == 8:
            break
        elif choice < 8 and len(prices) == 0:
            print('You must enter some prices first.')
        elif choice == 1:
            print_prices(prices)
        elif choice == 2:
            latest = latest_price(prices)
            print('The latest price is', latest)
        ## add code to process the other choices here
        elif choice == 3:
            average = avg_price(prices)
            print('The average price is', average)
        elif choice == 4:
            std = std_dev(prices)
            print('The standard deviation is', std)
        elif choice == 5:
            mday = max_day(prices)
            print('The max price is',prices[mday],'on day',mday )
        elif choice == 6:
            n = eval(input('Enter the threshold: '))
            if any_below(prices, n) == False:
                print('There are no prices below',n)
            else:
                print('There are prices below',n)
        elif choice == 7:
            best_plan = find_plan(prices)
            print('Buy on day',best_plan[0],'at price',prices[best_plan[0]])
            print('sell on day',best_plan[1],'at price',prices[best_plan[1]])
            print('Total profit',best_plan[2])
            
        

            
        else:
            print('Invalid choice. Please try again.')

    print('See you yesterday!')
