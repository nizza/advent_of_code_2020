import os
import argparse
import re

from math import cos, sin, radians, atan, pi, sqrt

# Patterns for regex
command_pattern = re.compile(r'([NSEWLRF])([0-9]+)')

def parse_line(line):

    # Splitting action from value
    match = re.match(command_pattern, line)
    action = match[1]
    value = int(match[2])

    return action, value

# a dictionary mapping action names to functions providing
# a new position value given:
#  - current pos
#  - command value
pos_updaters_dict ={
      "N": lambda pos, value : {'x': pos['x'], 'y': pos['y']+value, 'angle':pos['angle']}
    , "S": lambda pos, value : {'x': pos['x'], 'y': pos['y']-value, 'angle':pos['angle']}
    , "E": lambda pos, value : {'x': pos['x']+value, 'y': pos['y'], 'angle':pos['angle']}
    , "W": lambda pos, value : {'x': pos['x']-value, 'y': pos['y'], 'angle':pos['angle']}
    , "L": lambda pos, value : {'x': pos['x'], 'y': pos['y'], 'angle':pos['angle']+value}
    , "R": lambda pos, value : {'x': pos['x'], 'y': pos['y'], 'angle':pos['angle']-value}
    , "F": lambda pos, value : {  'x': pos['x'] + value*cos(radians(pos['angle']))
                                , 'y': pos['y'] + value*sin(radians(pos['angle']))
                                , 'angle':pos['angle']
                                }
}

def compute_distance(a, b):

    return sqrt( (a['x']-b['x'])**2 + (a['y']-b['y'])**2)

def compute_angle(a, b):

    # computing componets of a-b vector
    x = b['x'] - a['x']
    y = b['y'] - a['y']

    # computing the angle between the a-b vector,
    # and the x-axis
    if x != 0:
        angle = atan(y/x)
    else:
        angle = pi/2
    # adding pi if vector is in the negative x subplan
    if x<0:
        angle = angle + pi

    return angle

def rotate_wp(wp, value, clockwise):

    # defining rotation angle
    if clockwise:
        angle = -value
    else:
        angle = value

    # converting to radians
    angle = radians(angle)

    # Computing the rotated position by an angle 
    # using the formulas:
    # x2 = x1*cos(angle) - y1*sin(angle)
    # y2 = x1*sin(angle) + y1*cos(angle)
    new_x = wp['x']* cos(angle) - wp['y']* sin(angle)
    new_y = wp['x']* sin(angle) + wp['y']* cos(angle)


    return {'x': new_x, 'y': new_y}



# a dictionary mapping action names to functions providing
# a new wp value given:
#  - current wp
#  - current pos
#  - command value
wp_updaters_dict ={
      "N": lambda wp, value : {'x': wp['x'], 'y': wp['y']+value}
    , "S": lambda wp, value : {'x': wp['x'], 'y': wp['y']-value}
    , "E": lambda wp, value : {'x': wp['x']+value, 'y': wp['y']}
    , "W": lambda wp, value : {'x': wp['x']-value, 'y': wp['y']}
    , "L": lambda wp, value : rotate_wp(wp, value, False)
    , "R": lambda wp, value : rotate_wp(wp, value, True)
}

def update_pos(pos, action, value):

    # Getting the updating function for the current action
    updater =  pos_updaters_dict[action]  

    # Updating the position
    new_pos = updater(pos, value)

    return new_pos

def update_waypoint(wp, action, value):

    # Getting the updating function for the current action
    updater = wp_updaters_dict[action]

    # Updating the waypoint
    new_wp = updater(wp, value)

    return new_wp


def move_pos(pos, wp, value):


    # computing new position
    new_x = pos['x'] + value * wp['x']
    new_y = pos['y'] + value * wp['y']

    return {'x': new_x, 'y': new_y}




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Parsing the lines
    commands_list = [parse_line(line) for line in lines]

    ##############################################
    #                  Part 1                    #
    ##############################################

    # initilaizing the position
    pos = {'x': 0, 'y': 0, 'angle':0}

    for  action, value in commands_list:
        pos = update_pos(pos, action, value)

    # Computing the Manhattan distance
    m_dist = abs(pos["x"]) + abs(pos["y"])

    print('Part 1')
    print(f'The manhattan distance from the start position is: {m_dist}')

    print()


    ##############################################
    #                  Part 2                    #
    ##############################################

    # initilaizing the position, and viewpoint
    pos = {'x': 0, 'y': 0}
    wp  = {'x': 10, 'y': 1}

    for  action, value in commands_list:
        
        # updating viewpoint
        if action != 'F':
            wp = update_waypoint(wp, action, value)

        # moving the position
        else:
            pos = move_pos(pos, wp, value)


    # Computing the Manhattan distance
    m_dist = abs(pos["x"]) + abs(pos["y"])

    print('Part 2')
    print(f'The manhattan distance from the start position is: {m_dist}')


