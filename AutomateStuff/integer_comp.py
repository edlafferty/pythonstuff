# Script to determine the sum of the divisors of a number such that each divisor yields 0 remainder
import time

print("Enter an integer and I will determine the smallest sum of divisors that result in ")
print("a zero remainder (mod 0).")
while True:
    # List to store modulo divisors
    modList = []
    getNum = input("What is your number? (Enter q to quit.) ")
    startTime = time.time()  # Start processing
    if getNum == "Q" or getNum == "q":
        # Does user want to quit or keep playing?
        print("Thanks for playing.")
        break
    else:
        try:
            getNum = int(getNum)
            # If we start w/ the square root of the number, we have fewer values to check
            divisor = int(getNum ** .5 / 1)
            while divisor > 0:
                if getNum % divisor == 0:
                    # The divisors will result in mod 0. Append to list.
                    modList.append(int(divisor + (getNum / divisor)))
                divisor -= 1
            # Sort list so smallest value is index 0
            modList.sort()
            endTime = time.time()
            # Print results
            print("The smallest possible sum of modulo divisors is " + str(modList[0]))
            print("Answered in {:5.2f} seconds.".format(endTime - startTime))
            print("")
        except ValueError:
            # User entered something we didn't expect
            print("Please enter a number or Q/q to quit.")
            print("")
