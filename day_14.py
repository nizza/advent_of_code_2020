import os
import argparse

import re

# Patterns for regex
mask_pattern = re.compile(r'mask = ([01X]+)')
memory_pattern = re.compile(r'mem\[([0-9]+)\] = ([0-9]+)')

def apply_mask(mask, value):

    # Converting the int value to a binary string
    bin_value = format(value, 'b').zfill(len(mask))

    # initializing the result array
    result = [0 for i in range(len(mask))]
    for i in range(len(bin_value)):
        result[i] = bin_value[i]

    # applying the mask
    for i in range(len(mask)):
        if mask[i] != 'X':
            result[i] = mask[i]

    # converting the bin array to int
    str_value = ''.join(result)
    int_value = int(str_value, 2)
    return int_value

def get_possible_locations(mask, location):

    # Converting the int value to a binary string
    bin_location = format(location, 'b').zfill(len(mask))

    # initializing the location array
    arr_location = [0 for i in range(len(mask))]
    for i in range(len(bin_location)):
        arr_location[i] = bin_location[i]

    # applying mask to location: using the '1' rules
    for i in range(len(mask)):
        if mask[i] == '1':
            arr_location[i] = 1

    # Extracting positions of X in the mask
    X_pos = list()
    for i in range(len(mask)):
        if mask[i] == 'X':
            X_pos.append(i)

    # Generating list of addresses using the 'X' rule
    locations = list()
    num_locations = 2**(len(X_pos))
    for i in range(num_locations):

        # transforming i counter to bits
        bin_counter = format(i, 'b').zfill(len(X_pos))

        # initializing location candidate
        arr_possible_location = arr_location

        # applying current combination to location
        for k in range(len(bin_counter)):
            arr_possible_location[X_pos[k]] = bin_counter[k]
        
        # converting the bin array to int
        str_possible_location = ''.join([str(x) for x in arr_possible_location])
        int_possible_location = int(str_possible_location, 2)
        
        # Adding to locations resutl
        locations.append(int_possible_location)

    return locations



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Parsing the lines
    commands_list = list()
    for line in lines:
        command = dict() 
        
        # mask command
        match = re.match(mask_pattern, line)
        if match:
            command['operation'] = 'mask'
            command['data'] = match.group(1)
            commands_list.append(command)

        # memory command
        match = re.match(memory_pattern, line)
        if match:
            command['operation'] = 'memory'
            command['data'] = { 'location':int(match.group(1))
                              , 'value':int(match.group(2))
                            }
            commands_list.append(command)


    ##############################################
    #                  Part 1                    #
    ##############################################

    # Initializing the memory 
    memory = dict()

    # Executiing all the commands
    for command in commands_list:

        # Updating the mask
        if command['operation'] == 'mask': 
            mask = command['data']

        # Updating a memory location
        if command['operation'] == 'memory': 
            location = command['data']['location']
            value = command['data']['value']

            # applying mask
            masked_val = apply_mask(mask, value)

            # updating the memory location
            memory[location] = masked_val

    # Summing all the memory locations
    result = 0
    for val in memory.values():
        result += val


    print('Part 1')
    print(f'The answer is: {result}')

    print()


    ##############################################
    #                  Part 2                    #
    ##############################################
    
    # Initializing the memory 
    memory = dict()

    # Executiing all the commands
    for command in commands_list:

        # Updating the mask
        if command['operation'] == 'mask': 
            mask = command['data']

        # Updating a memory location
        if command['operation'] == 'memory': 
            location = command['data']['location']
            value = command['data']['value']

            # Getting the list of locations
            locations = get_possible_locations(mask, location)

            # updating the memory locations
            for location in locations:
                memory[location] = value

    # Summing all the memory locations
    result = 0
    for val in memory.values():
        result += val

    print('Part 2')
    print(f'The answer is: {result}')

