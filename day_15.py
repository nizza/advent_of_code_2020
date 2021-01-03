import os
import argparse

def perform_n_steps(input, n):

    # Dictionary tracking the time of last appearence of a number
    last_seen = dict()

    # Initializing from input
    i = 0
    while i < len(input)-1:
        last_seen[input[i]] = i
        i += 1
   
    # Performing next steps
    current = input[-1]
    while i < (n-1):

        # previously seen value
        if current in last_seen:
            next = i - last_seen[current]
        # new value
        else:
            next = 0

        # updating last_seen
        last_seen[current] = i

        # updating current
        current = next

        i += 1

    return current


if __name__ == '__main__':

 
    input = [0,3,1,6,7,5]


    ##############################################
    #                  Part 1                    #
    ##############################################
  
    res = perform_n_steps(input, 2020)

    print('Part 1')
    print(f'The answer is: {res}')

    print()



    ##############################################
    #                  Part 2                    #
    ##############################################
  
    res = perform_n_steps(input, 30*10**6)

    print('Part 1')
    print(f'The answer is: {res}')




