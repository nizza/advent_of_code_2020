import os
import argparse



def is_tree(line, pos):

    if line[pos%len(line)] == '#':
        return True
    else:
        return False

def count_trees(lines, row_step, col_step):

     # initializing row, and column indexes
    i = 0
    j = 0

    # Initializing tree counter
    trees_count = 0

    # Visiting the map
    while i < len(lines):
        line = lines[i]

        # Checking for trees
        if is_tree(line, j):
            trees_count += 1

        # Updating row and column index
        i += row_step
        j += col_step

    return trees_count

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.read().splitlines()
    
    # Defining the list of steps cominations to be tested
    steps_list = [(1, 1),
                    (1, 3),
                    (1, 5),
                    (1, 7),
                    (2, 1),
                ]

    mult = 1
    for row_step, col_step  in  steps_list:
        trees_count = count_trees(lines, row_step, col_step)
        print(f'({row_step}, {col_step}) => {trees_count}')
        mult *= trees_count

    print(mult)


