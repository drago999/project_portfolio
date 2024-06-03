# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:07:02 2024

@author: GreifOfUs
"""

import numpy as np
import pandas as pd
import scipy.optimize as opt
import matplotlib.pyplot as plt

print("Start math364 Project")

##### these are to be used to check your test data #####
test_data = np.genfromtxt("2d_test_data.txt", delimiter=None, dtype=float, missing_values=None)
#print(test_data) #ok works properly #pre sorted/split
#2d_true_classification.txt
true_classification_data = np.genfromtxt("2d_true_classification.txt", delimiter=None, dtype=float, missing_values=None)
#print(true_classification_data) #ok works properly #pre sorted/split

training_data = np.genfromtxt("2d_training_data.txt", delimiter=None, dtype=float, missing_values=None)
#print(training_data) #ok works properly #also in the proper form for my program #need to split into two data sets

df = pd.DataFrame(training_data, columns = ["answer", "x_1", "x_2"])
df.insert(0, "varience", 0)
#df.insert(0, "baseline", 1)
#print(df)
##### BASELINE COMPLETE #####

def negate(num):
    return -1*num

def create_true(df):
    data_true = df.copy()
    data_true = data_true.loc[df['answer'] == 1]
    #equation form needed
    #x_1 + baseline + varience <= x_2
    data_true['varience'] = 1
    return data_true

def create_false(df):
    data_false = df.copy()
    data_false = data_false.loc[df['answer'] == 0]
    #equation form needed
    #x_1 + baseline - varience >= x_2
    #-x_1 - baseline + varience <= -x_2
    data_false = data_false.apply(negate)
    data_false['varience'] = 1
    return data_false

def get_matrixA(df):
    temp = df.copy()
    temp.drop('answer', inplace = True, axis=1)
    temp.drop('x_2', inplace = True, axis=1)
    temp = temp.to_numpy()
    return temp

def get_matrixB(df):
    temp = df['x_2']
    temp = temp.to_numpy()
    return temp

def fuse_true_false(data_true, data_false):
    data_full = pd.concat([data_true, data_false])
    return data_full

##### BASIC FUNCTIONS COMPLETE #####

data_true = create_true(df)
data_false = create_false(df)
data_full = fuse_true_false(data_true, data_false)
##### CREATING BASELINE MATRIX COMPLETE #####

A = get_matrixA(data_full) 
B = get_matrixB(data_full)
#layout of A
#baseline, varience, x_1
c = np.array([1,0]) #what you maximize/minimize
res=opt.linprog(-c,A,B,None,None,bounds = (0,None)) #currently maximized
#print(res)
##### LP processing complete #####

"""
next need to plug x array into an equation where
varience + x_1 < x_2 therefore y = 0
varience + x_1 > x_2 therefore y = 1
THE LINE < VALUE Y = 0
THE LINE > VALUE Y = 1
"""

def flag_data(line_array, data_array):
    answer = 0
    #put my equation here
    x = line_array[0]
    x += line_array[1] * data_array[0]
    if(x < data_array[1]):
        answer = 1
    return answer

line = res['x']
# data = [51.2,95.0]
# print(flag_data(line, data))

##### POST PROCESSING #####

def test_data_flag(line, test_data, test_classification):
    file = open("math364_output.txt", "a")
    file.write("Jay Ellis\nMath364\nProject\n4/28/2024\n")
    print("\nEquation: [delta, x_1]\nEquation: ", line, "\n", file=file)
    #print("\nEquation: [delta, x_1]\nEquation: ", line, "\n")
    print("\nEquation: [x_1, x_2]", file=file)
    #print("[x_1, x_2]")
    y = 0
    for x in test_data:
        print(x, "result:", flag_data(line, x), "expected:", test_classification[y], file=file)
        #print(x, "result:", flag_data(line, x), "expected:", test_classification[y])
        #file.write(x, "result:", flag_data(line, x), "expected:", test_classification[y],"\n")
        y += 1
    file.close()
    return

def plot_data(line, test_data):
    print("start plot")
    base = line[0]
    slope = line[1]
    start = 0
    stop = 100
    resolution = 50
    xs = np.linspace(start, stop, resolution)
    ys = base + slope*xs
    plt.plot(xs,ys)
    
    y = 0
    for x in test_data:
        #print(x, "result:", flag_data(line, x), "expected:")
        if(flag_data(line, x) == 0):
            plt.scatter(x[0], x[1], color = 'red')
        else:
            plt.scatter(x[0], x[1], color = 'green')
        y += 1
    plt.show()
    print("end plot")
    return

test_data_flag(line, test_data, true_classification_data)
plot_data(line, test_data)


def get_plotable_coordinates(df):
    temp = df.copy()
    temp.drop('answer', inplace = True, axis=1)
    temp.drop('varience', inplace = True, axis=1)
    temp = temp.to_numpy()
    return temp

plot_data(line, get_plotable_coordinates(df))
print("End of Program")