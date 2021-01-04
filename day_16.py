import os
import argparse

import re

# Patterns for regex
field_rule_pattern = re.compile(r'(.+): ([0-9]+\-[0-9]+) or ([0-9]+\-[0-9]+)')
ticket_pattern = re.compile(r'[0-9]+,')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Parsing the lines
    field_rules = list()
    tickets = list()
    for line in lines:
        command = dict() 
        
        # field rule line
        match = re.match(field_rule_pattern, line)
        if match:
            field_rule = dict()
            # Extracting the name
            field_rule['name'] = match.group(1)

            # Extracting the 2 ranges
            ranges = list()
            range_1 = [int(x) for x in match.group(2).split('-')]
            ranges.append(range_1)
            range_2 = [int(x) for x in match.group(3).split('-')]
            ranges.append(range_2)
            field_rule['ranges'] = ranges

            field_rules.append(field_rule)
    
        # ticket line
        match = re.match(ticket_pattern, line)
        if match:
            ticket = [int(x) for x in line.split(',')]
            tickets.append(ticket)

    ##############################################
    #                  Part 1                    #
    ##############################################

    # creating a set of all admissible values, across fields
    all_valid_values = set()
    for field_rule in field_rules:
        for val_range in  field_rule['ranges']:
            for i in range(val_range[0], val_range[1]+1):
                all_valid_values.add(i)


    # Analyzing nearby tickets
    invalid_values = list()
    for ticket in tickets[1:]:
        for value in ticket:
            if not value in all_valid_values:
                invalid_values.append(value)

    result = sum(invalid_values)
    

    print('Part 1')
    print(f'The answer is: {result}')

    print()


    ##############################################
    #                  Part 2                    #
    ##############################################
    
    # Removing invalid tickets
    valid_tickets = list()
    valid_tickets.append(tickets[0])   # your ticket
    for ticket in tickets[1:]:  # nearby tickets
        is_valid = True
        for value in ticket:
            if not value in all_valid_values:
                is_valid = False
                break
        if is_valid:
            valid_tickets.append(ticket) 

    # Extracting for each column, identified by its order id,
    # the list of columns that are compatible with it
    field_num = len(valid_tickets[0])
    compatible_fields_dict = dict() # the list of compatible fields, for each column
    for k in range(field_num):    # going through the columns of a ticket

        compatible_fields = list()
        for field_rule in field_rules:    # going through the list of fields

            field_range_1 = field_rule['ranges'][0]
            field_range_2 = field_rule['ranges'][1]

            # valid 
            field_is_compatible = True
            for ticket in valid_tickets:
                
                # ticket column compatible with the field
                if ((ticket[k] >= field_range_1[0] and ticket[k] <= field_range_1[1])
                    or
                    (ticket[k] >= field_range_2[0] and ticket[k] <= field_range_2[1])
                    ):   
                    continue
                # ticket column not compatible with the field
                else:
                    field_is_compatible = False

            if field_is_compatible:
                compatible_fields.append(field_rule['name'])

        compatible_fields_dict[k] = compatible_fields


    # Removing, iteratively, from compatible_fields_dict, the columns
    # that are compatible with only one field
    matched = dict()
    while len(matched) < field_num:
        
        # Looking for a field compatible with only one field
        for col, compatible_fields in compatible_fields_dict.items():

            # the column is compatibe with only one field
            if len(compatible_fields) == 1:

                matched_field = compatible_fields[0]
                matched_col = col

                # Adding this field - column tuple to the matched results
                matched[matched_field] = matched_col

                break

        # Removing the field from all other columns compatible fields
        for col, compatible_fields in compatible_fields_dict.items():
            if matched_field in compatible_fields:
                compatible_fields.remove(matched_field)
        
        # Removing the column from  compatible_fields_dict
        compatible_fields_dict.pop(matched_col)

    # Computing the result
    result = 1
    ticket = valid_tickets[0]
    for field, col in matched.items():
        if field.startswith('departure'):
            result *= ticket[col]

    print('Part 2')
    print(f'The answer is: {result}')

