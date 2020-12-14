import os
import argparse
import re
from collections import defaultdict

# Patterns for regex
main_pattern = re.compile(r'(.+) bags contain (.+)\.')
content_pattern = re.compile(r'([0-9]+) (.+) bag')

def parse_line(line):

    # Splitting container from content
    match = re.match(main_pattern, line)
    container = match[1]
    content = match[2]
    
    content_dict = dict()
    # Splitting the different content parts
    for content_entry in content.split(','):
        
        # Extracting color and quantity
        match = re.match(content_pattern, content_entry.strip())
        if match:
            quantity = match[1]
            color = match[2]
            content_dict[color] = int(quantity)

    return container, content_dict



def get_colors_containing(bag_definitions, bag_color, target_color):

    # Getting the content of this bag_color
    bag_content = bag_definitions[bag_color]

    # base case: this bag doesn't contain any bag
    if not bag_content:
        return set()
    
    # initiaizing set for colors
    colors_set = set()

    # getting colors set for each bag contained here
    for sub_bag_color in bag_content:
        
        colors_set.update(get_colors_containing(bag_definitions, sub_bag_color, target_color))

        # Adding to the set the current color,
        # if the sub bag is of the target color
        if sub_bag_color == target_color:
            colors_set.add(bag_color)

    # Adding the current color if the colors set is not empty
    if colors_set:
        colors_set.add(bag_color)
    
    return colors_set

def count_content(bag_definitions, bag_color):

    # Getting the content of this bag_color
    bag_content = bag_definitions[bag_color]

    # base case: this bag doesn't contain any bag
    if not bag_content:
        return 0
    
    bags_counter = 0
    # Checking the content of each subbag
    for sub_bag_color, sub_bag_count in bag_content.items():

        # Adding the content of the sub_bags
        bags_counter += sub_bag_count * count_content(bag_definitions, sub_bag_color) 
        # Adding the sub_bags
        bags_counter += sub_bag_count

    return bags_counter

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Creating a dictionary mapping each color to the content
    bags_definitions = dict()
    for line in lines:

        container, content = parse_line(line)
        bags_definitions[container] = content


    # Counting the colors that can contain a 'shiny gold' bag
    shiny_gold_containers = set()
    for bag_color in bags_definitions:
        shiny_gold_containers.update(get_colors_containing(bags_definitions, bag_color, 'shiny gold'))
    print(f'Colors containig shiny gold: {len(shiny_gold_containers)}')

    # Counting the content of a 'shiny gold' bag
    shiny_gold_content_count = count_content(bags_definitions, 'shiny gold')
    print(f'Content size for shiny gold: {shiny_gold_content_count}')


    


        
    
   
    
    
