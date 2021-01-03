import os
import argparse

def find_min_departure_time(x):
    pass

def is_prime(num):

    res = True
    div = 2
    while div < num:
        if not num % div:
            res = False
            break
        div += 1

    return res


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file',
                    help='Path to the input file')
    args = parser.parse_args()

    # Reading the input file
    with open(args.input_file, 'r') as input_file:
        lines = input_file.readlines()



    ##############################################
    #                  Part 1                    #
    ##############################################

    # Parsing the lines
    departure_time = int(lines[0])
    bus_times = lines[1].strip().split(',')
    bus_times = [int(bus_time) for bus_time in bus_times if bus_time.isdigit()]
  

    # Computing the minpython waiting time among the buses
    min_wait = max(bus_times)
    min_bus = max(bus_times)

    for bus_time in bus_times:
        # if the departure time is a multiple of the 
        # bus frequency the wait is 0
        if  departure_time % bus_time == 0 : 
            wait = 0
        # Otherwise the wait is the complement of modulo
        else:
            wait = bus_time - (departure_time  % bus_time)
        
        if wait < min_wait:
            min_wait = wait
            min_bus = bus_time

    print('Part 1')
    print(f'The answer is: {min_wait*min_bus}')

    print()




    ##############################################
    #                  Part 2                    #
    ##############################################
    # Parsing the lines
    bus_times = lines[1].strip().split(',')
    bus_times_dict = dict()
    for i in range(len(bus_times)):
        bus_time = bus_times[i]
        if bus_time.isdigit():

            bus_time = int(bus_time)

            bus_times_dict[i] = bus_time
    
    print(bus_times_dict)


    # Looking for the max frequency of bus
    # This will be used as step when looking
    # for the departure time
    bus_times_dict_1 = bus_times_dict.copy()
    for k,v in bus_times_dict.items():
        for k1, v1 in bus_times_dict.items():
  
            if k == k1:
                continue
            
            if not (k-k1) % v1:
                bus_times_dict_1[k] *= v1
                
    max_key, max_val = max(bus_times_dict_1.items(), key=lambda item: item[1])
    print(max_key, max_val)



    # looking for the first departure_time meeting the
    # constraints
    step = 1
    found = False
    while  not found:

        departure_time = step* max_val - max_key
        #print(departure_time)

        # Checking whether the current departure_time meets
        # all the constraints
        found = True
        for k, v in bus_times_dict.items():
            if (departure_time+k) % v:
                found = False
                break

        # Moving to next departure_time
        if not found:
            step += 1

    #bus_times = [int(bus_time) for bus_time in bus_times if bus_time.isdigit()]


    print('Part 2')
    print(f'The answer is: {departure_time}')

