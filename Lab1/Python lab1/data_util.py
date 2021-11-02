import os
import math
import pathlib

def get_filepaths(folder):
    root_dir = folder
    file_set = set()

    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            rel_file = "Lab1/Python lab1/Raw_data_exp" + rel_file[1:]
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

def print_AFS_SD_SE():
    path = pathlib.Path(__file__).parent.resolve()
    filepaths = get_filepaths("Lab1/Python lab1/Raw_data_exp")
    final_speeds = get_final_speeds(filepaths)
    average_final_speed = get_average_final_speed(final_speeds)
    standard_deviation = get_standard_deviation(final_speeds)
    standard_error = get_standard_error(standard_deviation, len(final_speeds))
    print("average final speed: ", average_final_speed, ", standard_deviation: ", standard_deviation, "standard error: ", standard_error)


def get_lists_from_file(filepath):
    f = open(filepath, "r")
    t = 0
    t_list = []
    x = 0
    x_list = []
    y = 0
    y_list = []
    v = ""
    v_list = []
    for line in f:
        pos = 0
        for letter in line:
            
            if(pos == 0):
                if(letter.isnumeric() or letter == '.'):
                    t = t + letter
            elif(pos == 1):
                if(letter.isnumeric() or letter == '.'):
                    x = x + letter
            elif(pos == 2):
                if(letter.isnumeric() or letter == '.'):
                    y = y + letter
            elif(pos == 3):
                if(letter.isnumeric() or letter == '.'):
                    v = v + letter

            if(letter == '\t'):
                pos += 1
        if(t != ''):
            t_list.append(float(t))
        if(x != ''):
            x_list.append(float(x))
        if(y != ''):
            y_list.append(float(y))
        if(v != ''):
            v_list.append(float(v))
        
        t = ""
        x = ""
        y = ""
        v = ""
            
    return t_list, x_list, y_list , v_list

def get_mean_experiment_lists(experiment_list):
    for experiment in experiment_list:
        a=0

def get_list_from_files(parent_path, experiment_file_number):  # "Lab1/Python lab1/Raw_data_exp"
    filepaths = get_filepaths(parent_path)
    experiment_lists = [] # shape [[t_list1, x_list1, y_list1, v_list1], [t_list2, x_list2, y_list2, [v21, v22, v23]] , ....]
    t_lists = []
    x_lists = [] 
    y_lists = [] 
    v_lists = []
    
    for filepath in filepaths:
        t_list, x_list, y_list, v_list = get_lists_from_file(filepath)
        experiment_lists.append([t_list, x_list, y_list, v_list])
        t_lists.append(t_list)
        x_lists.append(x_list)
        y_lists.append(y_list)
        v_lists.append(v_list)
    
    comp_t_list = t_lists[experiment_file_number]
    comp_x_list = x_lists[experiment_file_number]
    comp_y_list = y_lists[experiment_file_number]
    comp_v_list = v_lists[experiment_file_number]
    
    return comp_t_list, comp_x_list, comp_y_list, comp_v_list

comp_t_list, comp_x_list, comp_y_list, comp_v_list = get_list_from_files("Lab1/Python lab1/Raw_data_exp", 1)
a= 0
