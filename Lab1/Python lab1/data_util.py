import os
import math

def get_filepaths(folder):
    root_dir = folder
    file_set = set()

    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            rel_file = "Python lab1\Raw_data_exp" + rel_file[1:]
            file_set.add(rel_file)
    return file_set

def get_final_speed(filepath):
    f = open(filepath, "r")
    v = ""
    v_list = []
    for line in f:
        pos = 0
        for letter in line:
            
            if(pos == 3):
                if(letter.isnumeric() or letter == '.'):
                    v = v + letter
            if(letter == '\t'):
                pos += 1
        if(v != ''):
            v_list.append(float(v))
        v = ""
    final_v = v_list[len(v_list) - 1]
            
    return final_v

def get_final_speeds(filepaths):
    final_speeds = []
    for filepath in filepaths:
        final_speeds.append(get_final_speed(filepath))
    return final_speeds

def get_average_final_speed(final_speeds):
    sum = 0
    for speed in final_speeds:
        sum += speed
    return sum / len(final_speeds)

def get_standard_deviation(list):
    average_x = get_average_final_speed(list)
    N = len(list)
    sum = 0
    for value in list:
        sum += (value - average_x)**2
    
    return math.sqrt((1/(N-1))*sum)

def get_standard_error(standard_deviation, number_of_samples):
    return standard_deviation / math.sqrt(number_of_samples)

filepaths = get_filepaths("Python lab1\Raw_data_exp")
final_speeds = get_final_speeds(filepaths)
average_final_speed = get_average_final_speed(final_speeds)
standard_deviation = get_standard_deviation(final_speeds)
standard_error = get_standard_error(standard_deviation, len(final_speeds))
print("average final speed: ", average_final_speed, ", standard_deviation: ", standard_deviation, "standard error: ", standard_error)