import os
import argparse

import re

# Pattern for regex
pattern = re.compile('([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)')

def check_pwd_1(char, min_occ, max_occ, pwd):
    
    # Counting  the occurrencies
    char_occ = pwd.count(char)

    if char_occ >= min_occ  and char_occ <= max_occ:
        return True
    else:
        return False

def check_pwd_2(char, pos_1, pos_2, pwd):
    
    # Extracting characters at specified positions (index from 1)
    sub = pwd[pos_1-1] + pwd[pos_2-1]

    # Counting  the occurrencies
    char_occ = sub.count(char)

    if char_occ == 1:
        return True
    else:
        return False

def split_line(line):

    match = pattern.match(line)

    min_occ = int(match[1])
    max_occ = int(match[2])
    char = match[3]
    pwd = match[4]

    return char, min_occ, max_occ, pwd

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()
    
    correct_count_1 = 0
    correct_count_2 = 0
    # Checking each line
    for line in lines:

        # Parsing the line
        char, min_occ, max_occ, pwd = split_line(line)

        # Checking the line (both policies)
        check_1 = check_pwd_1(char, min_occ, max_occ, pwd)
        if check_1:
            correct_count_1 += 1
        check_2 = check_pwd_2(char, min_occ, max_occ, pwd)
        if check_2:
            correct_count_2 += 1

    print(correct_count_1)
    print(correct_count_2)


