# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:14:11 2024

@author: GreifOfUs
"""

import numpy as np
import scipy.optimize as opt
import pandas as pd

"""
#does not work as is, might need pandas to deal with first column and first row
temp = np.genfromtxt("math464_data_file.csv", delimiter=",")
print(temp)
"""

"""
Data layout:
site,fleet,employees,salaries,maintenanceCosts,advertizingCosts,rentals,revenue,advanceBookings,Complaints
use pandas?
"""
raw_data = pd.read_csv("math464_data_file.csv")
print(raw_data)
"""
now that I have the data in pandas, I need to create my denominator terms

denominator terms: salaries, maintenance costs, advertizing costs, complaints
numeraotr terms: fleet, employees, rentals, revenue, advance bookings

may need advanced column data like salary/employee, complaints/rental, maintenance/car
"""
#print(raw_data.columns)
"""
Index(['site', 'fleet', 'employees', 'salaries', 'maintenanceCosts',
       'advertizingCosts', 'rentals', 'revenue', 'advanceBookings',
       'Complaints'],
      dtype='object')
11 rows x 10 columns: only 9 are used numerically
"""
"""
numerator = raw_data.filter(['site', 'fleet', 'employees', 'rentals', 'revenue', 'advanceBookings'], axis = 1)
denominator = raw_data.filter(['site', 'salaries', 'maintenanceCosts', 'advertizingCosts', 'Complaints'], axis = 1)
print(numerator)
print(denominator)
"""
"""
ok think it out now,
I need to do two things to the data in the lp
1)
    I need to have a separate 10x10 matrix filled with the denominators
    and a subsiquent 10x10 matrix that is the negative of it
    denom = 1 -> denom <= 1 and -denom <= -1
2)
    I need to set the original matrix denominator values to negative original

then they must be attached together making more rows instead of columns combining the three different matrixes

"""
def negate(x):
    return -x

def negate_denom(data_frame):
    #denominator = raw_data.filter(['site', 'salaries', 'maintenanceCosts', 'advertizingCosts', 'Complaints'], axis = 1)
    data_frame['salaries'] = data_frame['salaries'].apply(negate)
    data_frame['maintenanceCosts'] = data_frame['maintenanceCosts'].apply(negate)
    data_frame['advertizingCosts'] = data_frame['advertizingCosts'].apply(negate)
    data_frame['Complaints'] = data_frame['Complaints'].apply(negate)
    return data_frame
#print(negate_denom(raw_data))
def clear_numer(data_frame):
    #numerator = raw_data.filter(['site', 'fleet', 'employees', 'rentals', 'revenue', 'advanceBookings'], axis = 1)
    data_frame['fleet'] = data_frame['fleet'].mask(data_frame['fleet'] > 0, 0)
    data_frame['employees'] = data_frame['employees'].mask(data_frame['employees'] > 0, 0)
    data_frame['rentals'] = data_frame['rentals'].mask(data_frame['rentals'] > 0, 0)
    data_frame['revenue'] = data_frame['revenue'].mask(data_frame['revenue'] > 0, 0)
    data_frame['advanceBookings'] = data_frame['advanceBookings'].mask(data_frame['advanceBookings'] > 0, 0)
    return data_frame
#print(clear_numer(raw_data))

"""
now that I have functions that can cleen up the data, I need to remove site from the data I will manipulate
"""
def remove_site(data_frame):
    new_data_frame = data_frame.copy()
    new_data_frame.drop('site', inplace = True, axis = 1)
    return new_data_frame

"""
#CREATE BASE MATRIX
# =============================================================================
# HOLD UP! problem!
# I need a LP PER site
# where:
#     max the numer of the site
#     s.t
#         numerator - denom <=0 of ALL sites
#         denom of the site = 1
#     weghts >= 0
# =============================================================================
base_data = remove_site(raw_data)
#print(base_data.columns)
#print(base_data)

#CREATE DENOMINATORS
denominatorA = base_data.copy()
denominatorA = clear_numer(denominatorA)
#print(denominatorA)
denominatorB = denominatorA.copy()
denominatorB = negate_denom(denominatorB)
#print(denominatorB)

#ADD ANSWERS: aka b you want this to be in proper order to whatever it fuses at the end


#FUSE TOGETHER
data_full = pd.concat([base_data, denominatorA, denominatorB])
print(data_full)

### LP
A = np.array([[2,3,-1,1],
              [-3,-1,-2,-1],
              [-1,-1,2,1],
              [1,1,-2,-1]])
b = np.array([0,-3,6,-6])
c = np.array([1,-1,0,0])
bounds=((-np.inf,0), (0,np.inf), (0,np.inf),(-np.inf,np.inf))

res=opt.linprog(c,A,b,None,None,bounds) #currently minimized

print(res)
"""

"""
ok I need to create a function that itteratively goes through each SITE and runs the LP of each

so to pull it off I need to do some extra stuff...
1) 
    I must pull the site names into an array
2)
    I must make code go through the list itteratively
3)
    I need it to create the weight array for c based off of the numerator values

"""
def grab_site_data(data_frame, site):
    site_data_frame = data_frame[data_frame['site'] == site].copy()
    return site_data_frame

#print(grab_site_data(raw_data, 'Olympia'))
"""
ok the above works by returning the copy of the row based on site name
"""
def create_site_array(data_frame):
    site_array = data_frame['site'].copy()
    site_array = site_array.to_numpy()
    return site_array
#print(create_site_array(raw_data))
"""
ok that works as well... I can set up a for loop using that I believe
"""
def relative_lp_site(data_frame, site):
    site_data = grab_site_data(data_frame, site)
    #print(site_data)#proper pd.data_frame good...
    return site_data

def negate_copy(data_frame):
    columns = data_frame.columns
    #print(columns)
    temp = data_frame.copy()
    for item in columns:
        #print(item)
        if(item != 'site'):
            temp[item] = temp[item].apply(negate)
    return temp

def clear_denom(data_frame):
    site_data = data_frame.copy()
    #numerator = raw_data.filter(['site', 'fleet', 'employees', 'rentals', 'revenue', 'advanceBookings'], axis = 1)
    for x in site_data:
        #print(x) #x is name of column
        if(x != 'fleet' and x != 'employees' and x != 'rentals' and
           x != 'revenue' and x != 'advanceBookings'):
            #site_data.drop(x, inplace = True, axis = 1)
            #wrong method needs to set to 0
            if(x == 'site'):
                site_data.drop(x, inplace = True, axis = 1)
            else:
                site_data[x] = 0
    return site_data

def combine_matrix(everything_array, site_array):
    """
    the everything aray will have an answer <=0
    the site array will have an answer == 1
    
    will need to remove 'site' from the data
    """
    #print(everything_array, site_array, "\n\n")
    temp1 = everything_array.copy()
    # print(temp1)
    temp2 = site_array.copy()
    # print(temp2)
    temp1.insert(0, "answer", 0)
    temp2.insert(0, "answer", 1)
    #print(temp1,"\n\n", temp2)
    temp3 = temp2.copy()
    # #proceed to negate all terms in temp 3
    temp3 = negate_copy(temp3)
    #print(temp3)
    output = pd.concat([temp1, temp2, temp3])
    return output

def print_weighting_per_item(current_site, result_array):
    item = current_site.columns
    x = 0
    for y in item:
        if y != 'site':
            print(y, "\tWieghting:",result_array[x])
            x += 1 
    print("\n")
    return

def data_loop(data_frame):
    site_array = create_site_array(data_frame)
    print("starting data loop\n\n")
    for site in site_array:
        #print(site)
        #run program that uses data_frame and site and returns lp result
        current_site = relative_lp_site(data_frame, site)
        #print(current_site)
        """
        need to use the current site data in two forms
        need to use a copy of the original data frame
        """
        """
        # base_data = remove_site(raw_data)
        # #print(base_data.columns)
        # #print(base_data)

        # #CREATE DENOMINATORS
        # denominatorA = base_data.copy()
        # denominatorA = clear_numer(denominatorA)
        # #print(denominatorA)
        # denominatorB = denominatorA.copy()
        # denominatorB = negate_denom(denominatorB)
        # #print(denominatorB)
        """
        matrix_A = data_frame.copy()
        matrix_A = negate_denom(matrix_A) #this sets up the majority
        temp = current_site.copy()
        temp = clear_numer(temp)
        # print(temp)
        # print("\n", matrix_A, "\n\n")
        matrix_A = combine_matrix(matrix_A, temp) #mixes the necessary bits
        matrix_A.drop('site', inplace = True, axis=1) #removes the 'site' column
        matrix_B = matrix_A['answer'] #copies the answer column
        matrix_A.drop('answer', inplace = True, axis = 1) #removes the answer column from matrix_A
        matrix_C = current_site.copy() #next need to create matrix_C
        matrix_C = clear_denom(matrix_C)
        #next need to make them convert to numpy arrays
        matrix_A = matrix_A.to_numpy()
        matrix_B = matrix_B.to_numpy()
        matrix_C = matrix_C.to_numpy() #may need an additional transform...
        matrix_C = matrix_C.flatten() #change from 2d array to 1d array
        # print(matrix_A)
        # print(matrix_B)
        # print(matrix_C)
        
        #next need to generate linear program + results of said LPs
        result = opt.linprog(-matrix_C, matrix_A, matrix_B,None,None, bounds=(0, None)) #currently maximized
        #don't know how to generate the bounds for this... since I DON'T want to hard-code a set (right now)
        print(site, "\t", -result['fun']*100,"%")
        print_weighting_per_item(current_site, result['x'])
        
    print("\n\nend data loop\n\n")
    return
data_loop(raw_data)


