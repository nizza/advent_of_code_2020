import os
import argparse
from collections import defaultdict


def count_deltas(numbers_list):

    deltas_dict = defaultdict(int)

    for i in range(1, len(numbers_list)):

        # Computing delta between current and previous element
        delta = numbers_list[i] - numbers_list[i-1]

        # Updating deltas dictionary
        deltas_dict[delta] += 1

    return deltas_dict

def count_paths(numbers_list, start, partial_results):

    # Extracting sublist
    sublist = numbers_list[start:]

    # base case : 2 elements list
    # Returning 1, if difference at most 3
    #           0, otherwise
    if len(sublist) == 2:
        diff = sublist[1] - sublist[0]
        if diff <= 3:
            partial_results[start] = 1
        else:
            partial_results[start] = 0
        return partial_results

    # Counting the paths for sublists
    #  - starting from elements that have a distance <= 3 from the first one 
    #  - have lenghth >= 2        
    paths_counter =0
    k = 1
    while ( (sublist[k] - sublist[0]) <= 3
            and
             len(sublist[k:]) >= 2
          ):

          # Computing the possible solutions starting at start+k
          # if not yet done
          if not start+k in partial_results:
            partial_results = count_paths(numbers_list, start+k, partial_results)
          paths_counter += partial_results[start+k]
          k += 1
    
    # Setting the result for the current starting position
    partial_results[start] = paths_counter

    # Returning partial_results, or current counter, if start is 0
    if start == 0:
        return paths_counter
    else:
        return partial_results

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

    # Adding value for input socket (0), and device input (max+3)
    numbers_list.extend([0, max(numbers_list) + 3])

    # Sorting
    numbers_list = sorted(numbers_list)

    ##############################################
    #                  Part 1                    #
    ##############################################

    # Computing delta
    deltas = count_deltas(numbers_list)

    print('Part 1')
    print(f'The answer is: {deltas[1]*deltas[3]}')


    ##############################################
    #                  Part 2                    #
    ##############################################

    possible_paths = count_paths(numbers_list, 0, dict())
    print('Part 2')
    print(f'The answer is: {possible_paths}')





        
    
   
    
    
