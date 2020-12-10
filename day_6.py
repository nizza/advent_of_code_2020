import os
import argparse
import re
from collections import defaultdict


def count_answers_any(group):

    answers = set()

    # Cleaning group answers (newlines, spaces..)
    group = re.sub('\s+','',group)
    for char in group:
        answers.add(char)

    return len(answers)

def count_answers_all(group):

    # Splitting group by lines
    lines = group.split('\n')

    # Cleaning lines (newlines, spaces..)
    lines = [ re.sub('\s+','',line) for line in lines]

    # Removing empty lines
    lines = [line for line in lines if len(line)>0]
    n = len(lines)

    
    # Counting the occurencies of different answers
    answers = defaultdict(int)
    for line in lines:
        for char in line:
            answers[char] += 1


    # Counting the number of answers appearing on each line
    count_all = 0
    for v in answers.values():
        if v == n:
            count_all += 1

    return count_all


    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        groups = input_file.read().split('\n\n')


    # Checking the documents
    any_answers_count = 0
    all_answers_count = 0
    for group in groups:

        #print(group)
        any_answers_count += count_answers_any(group)
        all_answers_count += count_answers_all(group)
        
    
    print(f'Any answer count: {any_answers_count}')
    print(f'All answers count {all_answers_count}')
    
    
