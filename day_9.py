import os
import argparse


def find_sum(numbers_list, target_sum):

    N = len(numbers_list)
    found = False
    for i in range(N-1):

        # Skipping if bigger target
        if numbers_list[i] > target_sum:
            continue

        for j in range(i+1, N):
            if numbers_list[i] + numbers_list[j] == target_sum:
                found = True
                break

        if found:
            break
    
    return found



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Parsing the lines
    numbers_list = [int(line) for line in lines]

    ##############################################
    #                  Part 1                    #
    ##############################################

    # Checking for each number, starting from the 26th, if the previous 25 
    # contain a pair which sum to the current number
    for i in range(25, len(numbers_list)):
        current_number = numbers_list[i]
        previous_numbers =  numbers_list[i-25: i]

        if not find_sum(previous_numbers, current_number):
            break

    print('Part 1')
    print(f'The first number not matching is: {current_number}')


    ##############################################
    #                  Part 2                    #
    ##############################################

    i = 0
    j = 1
    N = len(numbers_list)
    found = False
    while i < N-1 and not found:
        j = i +1
        while j < N and not found:
            res = sum(numbers_list[i: j+1])
            if res == current_number:
                found = True
            elif res > current_number:
                break
            j += 1

        i += 1

    output  = min(numbers_list[i: j+1]) + max(numbers_list[i: j+1])

    print('Part 2')
    print(f'The encryption weakness is: {output}')




        
    
   
    
    
