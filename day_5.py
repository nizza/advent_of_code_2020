import os
import argparse

import unittest

def parse_ticket(ticket):

    # Extracting row, and  column
    row = ticket[:7]
    column = ticket[7:]

    ###########################
    #     Row                 #
    ###########################
    # Converting to '0's and '1's 
    row = row.replace('B','1').replace('F','0')
    # Converting binary string to int
    row = int(row, 2)

    ###########################
    #     Column              #
    ###########################
    # Converting to '0's and '1's 
    column = column.replace('R','1').replace('L','0')
    # Converting binary string to int
    column = int(column, 2)

    return row, column

class TestDay5(unittest.TestCase):

    def test_parse_ticket(self):

        ticket = 'BFFFBBFRRR'
        row, column = parse_ticket(ticket)
        self.assertEqual(row, 70)
        self.assertEqual(column, 7)

    def test_parse_ticket_1(self):

        ticket = 'FFFBBBFRRR'
        row, column = parse_ticket(ticket)
        self.assertEqual(row, 14)
        self.assertEqual(column, 7)
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        tickets = input_file.readlines()



    # Checking the tickets
    max_seat_id = 0
    all_seats_id = list()
    for ticket in tickets:

        row, column = parse_ticket(ticket)
        seat_id = row * 8 + column
        all_seats_id.append(seat_id)
        if seat_id > max_seat_id:
            max_seat_id = seat_id
    
    # Sorting seats_id
    all_seats_id = sorted(all_seats_id)
    # Looking for missing element 
    for i in range(len(all_seats_id)-1):
        if all_seats_id[i+1] !=  all_seats_id[i]+1:
            missing_id = all_seats_id[i]+1

        

    print(f'Max seat id: {max_seat_id}')
    print(f'Missing id {missing_id}')

    

    


