import os
import argparse
from collections import defaultdict

import numpy as np


def parse_lines(lines):

    # Creating empty matrices, for position and occupation
    n_rows = len(lines)
    n_cols = len(lines[0])
    seats_map = np.zeros((n_rows, n_cols))
    seats_occupation = np.zeros((n_rows, n_cols))

    # Updating position and occupation matrices
    for i in range(n_rows):
        for j in range(n_cols):
            if lines[i][j] != '.':
                seats_map[i, j] = 1
            if lines[i][j] == '#':
                seats_occupation[i, j] = 1

    return seats_map, seats_occupation

def get_neighborhood(matrix, i, j):

    n_rows, n_cols = seats_occupation.shape

    # Compting the borders of the neighborbood
    i_start = max(0, i-1)
    i_end = min(n_rows-1, i+1)
    j_start = max(0, j-1)
    j_end = min(n_cols-1, j+1)

    return matrix[i_start:i_end+1, j_start:j_end+1]

def count_neighbours_1(seats_map, seats_occupation, i, j):

    # getting neighborhood for current seat
    square = get_neighborhood(seats_occupation, i, j)

    # counting the occupied seats in the neighborhood
    n_count = square.sum() - seats_occupation[i, j]

    return n_count

def count_neighbours_2(seats_map, seats_occupation, i, j):

    n_rows, n_cols = seats_occupation.shape

    # List of vectors defining the directions to explore
    directions = [(-1,-1), (-1, 0), (-1, 1), 
                  (0,-1) ,          (0, 1), 
                  (1,-1) , (1, 0)  , (1, 1) 
                 ]
    
    n_count = 0

    # Exploring all the directions for neighbors
    for direction in directions:
        
        # row, and col increments for this direction
        row_delta = direction[0]
        col_delta = direction[1]

        # current position
        curr_i = i + row_delta
        curr_j = j + col_delta
        found_seat = False
        while (curr_i >= 0 and curr_i < n_rows
            and curr_j >= 0 and curr_j < n_cols and not found_seat):

            if seats_map[curr_i, curr_j]:
                found_seat = True
                n_count += seats_occupation[curr_i, curr_j]

            curr_i += row_delta
            curr_j += col_delta


    return n_count


def update_occupation(seats_map, seats_occupation, exercise):

    n_rows, n_cols = seats_occupation.shape

    # initializing new seats occupation
    new_seats_occupation = seats_occupation.copy()

    # defining threshold, and  neighbours counter functions
    # depending on the  exercise
    n_counter_dict = {1: count_neighbours_1, 2: count_neighbours_2}
    n_count_th_dict = {1: 4, 2: 5}
    n_counter = n_counter_dict[exercise]
    n_count_th = n_count_th_dict[exercise]


    # updating seats
    for i in range(n_rows):
        for j in range(n_cols):

            #print(i,j)
            #print(seats_map[i, j])
            # Skipping if not a seat
            if not seats_map[i, j]:
                continue

            # counting the occupied seats in the neighborhood
            n_count = n_counter(seats_map, seats_occupation, i, j)

            # If a seat is empty  and there are no occupied seats adjacent to it
            # , the seat becomes occupied.
            if not seats_occupation[i, j] and n_count==0 :
                new_seats_occupation [i, j] = 1
            
            # If a seat is occupied  and n_count_th or more seats adjacent to it are also occupied
            # , the seat becomes empty.
            if seats_occupation[i, j] and n_count >= n_count_th:
                new_seats_occupation [i, j] = 0


    return new_seats_occupation

def print_seats(seats_occupation, seats_map):

    n_rows, n_cols = seats_occupation.shape

    for i in range(n_rows):

        map_row = seats_map[i, :]
        occup_row = seats_occupation[i, :]
       
        to_print = ''

        for j in range(n_cols):

            # seat or not ?
            if not map_row[j]:
                to_print += '.'
            # occupied or not
            elif occup_row[j]:
                to_print += '#'
            else:
                to_print += 'L'

        print(to_print)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Cleaning the lines
    lines = [line.strip() for line in lines]


    # Performing the computation for the 2 parts
    for part in [1, 2]:

        # Parsing the lines
        seats_map, seats_occupation = parse_lines(lines)

        stable = False
        cycle = 0
        while not stable:

            new_seats_occupation = update_occupation(seats_map, seats_occupation, part) 

            if (new_seats_occupation == seats_occupation).all():
                stable = True
            else:
                seats_occupation = new_seats_occupation

            cycle +=1

        print(f'Part {part}')
        print(f'The number of occupied seats is: {seats_occupation.sum()}')
        print()








        
    
   
    
    
