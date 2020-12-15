import os
import argparse
import re
from collections import defaultdict

# Patterns for regex
main_pattern = re.compile(r'(nop|acc|jmp) ([+-][0-9]+)')

# A dictionary providing functions returning
#       (accumulator increase, instruction jump) 
# for each instruction name
instruction_dict = {
        'acc' : lambda x: (x, 1)
    , 'jmp' : lambda x: (0, x)
    , 'nop' : lambda x: (0, 1)
}

def parse_line(line):

    # Splitting instruction from argument
    match = re.match(main_pattern, line)
    instruction = match[1]
    argument = int(match[2])
    
    return instruction, argument

def execute_lines(lines):

    # A set tracking the lines that have been executed
    exec_lines = set()

    # Going through the lines, while the lines are new
    i = 0
    acc = 0
    while i < len(lines):

        if not i in exec_lines:
            
            # Updating set of executed lines
            exec_lines.add(i)

            # Getting the current line
            instruction, argument = lines[i]

            # Computing accumulator increase, instruction jump
            acc_delta, inst_delta = instruction_dict[instruction](argument)

            # Updating accumulator, and instruction line
            acc += acc_delta
            i += inst_delta
        else:
            break


    return acc, i


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Parsing the lines
    parsed_lines = [parse_line(line) for line in lines]

    ##############################################
    #                  Part 1                    #
    ##############################################
    
    acc, i = execute_lines(parsed_lines)

    print('Part 1')
    print(f'The accumulator value is: {acc}')


    ##############################################
    #                  Part 2                    #
    ##############################################

    # trying to change every possible instruction 
    # from nop to jmp, or viceversa
    for to_change in range(len(parsed_lines)):

        old_instruction, argument= parsed_lines[to_change]

        # Nothing to do if not 'nop' or 'jmp'
        if old_instruction == 'acc':
            continue

        # Replacing the instruction
        new_instruction_dict = {'nop':'jmp', 'jmp': 'nop'}
        new_instruction = new_instruction_dict[old_instruction]
        parsed_lines[to_change] = (new_instruction, argument)

        # Executing the instruction set
        acc, i = execute_lines(parsed_lines)

        # Stopping if next instruction is the one just after the list
        if i == len(parsed_lines):
            break

        # Restoring the modified instruction
        parsed_lines[to_change] = (old_instruction, argument)


    print('Part 2')
    print(f'The accumulator value is: {acc}')



        
    
   
    
    
