import os
import argparse

import re


# Patterns for regex
key_pattern = re.compile(r'([a-z]+):')
key_value_pattern = re.compile(r'([a-z]+):(\S+)\s')
height_pattern = re.compile(r'^([0-9]+)(cm|in)$')
haircolor_pattern = re.compile(r'^#[0-9a-f]{6}$')
eyecolor_pattern = re.compile(r'^(amb|blu|brn|gry|grn|hzl|oth)$')
pid_pattern = re.compile(r'^[0-9]{9}$')


mandatory_fields = ['byr', 
                    'iyr', 
                    'eyr', 
                    'hgt', 
                    'hcl', 
                    'ecl', 
                    'pid' 
]

def check_byr(entry):

    try:
        entry = int(entry)
        if entry >= 1920 and entry <= 2002:
            return True
        else:
            return False
    except:
        return False

def check_iyr(entry):

    try:
        entry = int(entry)
        if entry >= 2010 and entry <= 2020:
            return True
        else:
            return False
    except:
        return False

def check_eyr(entry):

    try:
        entry = int(entry)
        if entry >= 2020 and entry <= 2030:
            return True
        else:
            return False
    except:
        return False

def check_hgt(entry):

    # accepted ranges, for each unit
    limits = { 'cm': (150, 193)
              , 'in': (59, 76) }

    try:
        match = height_pattern.match(entry)
        value = int(match[1])
        unit = match[2]

        min_val, max_val = limits[unit]
        if value >= min_val and value <= max_val:
            return True
        else:
            return False
    except:
        return False



# Dictionary listing for each field the corresponding check function
check_functions = { 'byr' : check_byr
                  , 'iyr': check_iyr
                  , 'eyr': check_eyr
                  , 'hgt': check_hgt
                  , 'hcl': lambda entry: True if haircolor_pattern.match(entry) else False
                  , 'ecl': lambda entry: True if eyecolor_pattern.match(entry) else False
                  , 'pid': lambda entry: True if pid_pattern.match(entry) else False
                  , 'cid': lambda entry: True

}

def check_document(document):

    matches = key_pattern.findall(document)

    # Checking whether all the required fields are present
    for field in mandatory_fields:
        if not field in matches:
            return False
    return True

def check_fields(document):

    # print(document)

    matches = key_value_pattern.findall(document)
    #print(matches)

    # Returning False if any entry is not valid
    for k, v in matches:
        check_function = check_functions[k]
        if not check_function(v):
            return False
    return True
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        documents = input_file.read().split('\n\n')

        # Adding newline at the end of each document
        documents = [document+'\n' for document in documents]

    # Checking the documents
    all_fields_count = 0
    valid_fields_count = 0
    for document in documents:

        if check_document(document):
            all_fields_count += 1

            if check_fields(document):
                valid_fields_count += 1
        

    print(all_fields_count)
    print(valid_fields_count)
    

    


