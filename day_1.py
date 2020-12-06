import os
import argparse

def find_sum_2(elements, target_sum):

    for i in range(len(elements)-1):
        for j in range(i+1, len(elements)):
            if elements[i] + elements[j] == target_sum:
                return elements[i] * elements[j]
    
    # No couple found
    return None

def find_sum_3(elements, target_sum):

    for i in range(len(elements)-2):
        for j in range(i+1, len(elements)-1):
            for k in range(j+1, len(elements)):
                if elements[i] + elements[j] + elements[k] == target_sum:
                    return elements[i] * elements[j] * elements[k]
    
    # No tupel found
    return None

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()
    
    # Casting to numbers
    numbers = list(map(int, lines))

    # Computing result
    print(find_sum_2(numbers, 2020))
    print(find_sum_3(numbers, 2020))
