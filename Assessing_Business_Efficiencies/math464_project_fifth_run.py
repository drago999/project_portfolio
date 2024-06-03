# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 08:26:04 2024

@author: GreifOfUs
"""

import numpy as np
import scipy.optimize as opt
import pandas as pd

pd.set_option('display.max_columns', None)

"""
maintenance costs per car, salaries per employee, advertising costs per advance booking, and complaints per rental
Revenue will be treated separately on its own as a numerator.
"""

raw_data = pd.read_csv("math464_data_file.csv")
print(raw_data)
#[site,fleet,employees,salaries,maintenanceCosts,advertizingCosts,rentals,revenue,advanceBookings,Complaints]

def relativising_data(pandas_data):
    #car per cost, salaries per employee, advertising costs per advance booking, and rental per complaint
    pandas_data['cars/cost'] = pandas_data.apply(lambda row: row.fleet / row.maintenanceCosts, axis = 1)
    pandas_data.drop('maintenanceCosts', inplace = True, axis = 1)
    pandas_data.drop('fleet', inplace = True, axis = 1)
    
    pandas_data['salarie/employee'] = pandas_data.apply(lambda row: row.salaries / row.employees, axis = 1)
    pandas_data.drop('salaries', inplace = True, axis = 1)
    pandas_data.drop('employees', inplace = True, axis = 1)
    
    pandas_data['advertisingCosts/advanceBooking'] = pandas_data.apply(lambda row: row.advertizingCosts / row.advanceBookings, axis = 1)
    pandas_data.drop('advertizingCosts', inplace = True, axis = 1)
    pandas_data.drop('advanceBookings', inplace = True, axis = 1)
    
    pandas_data['revenue/rental'] = pandas_data.apply(lambda row: row.revenue / row.rentals, axis = 1)
    pandas_data.drop('revenue', inplace = True, axis = 1)
    
    pandas_data['rentals/complaint'] = pandas_data.apply(lambda row: row.rentals / row.Complaints, axis = 1)
    pandas_data.drop('Complaints', inplace = True, axis = 1)
    pandas_data.drop('rentals', inplace = True, axis = 1)
    
    #print(pandas_data)
    print(pandas_data.columns)
    return pandas_data

#revenue is a positive and everything else is a negative
#['site', 'revenue', 'costs/car', 'salarie/employee', 'advertisingCosts/advanceBooking', 'complaints/rental']

def remove_site(data_frame):
    new_data_frame = data_frame.copy()
    new_data_frame.drop('site', inplace = True, axis = 1)
    return new_data_frame

def negate(x):
    return -x

def negate_denom(data_frame):
    #denominator = ['costs/car', 'salarie/employee', 'advertisingCosts/advanceBooking', 'complaints/rental']
    data_frame['salarie/employee'] = data_frame['salarie/employee'].apply(negate)
    data_frame['advertisingCosts/advanceBooking'] = data_frame['advertisingCosts/advanceBooking'].apply(negate)
    return data_frame

def grab_site_data(data_frame, site):
    site_data_frame = data_frame[data_frame['site'] == site].copy()
    return site_data_frame

def relative_lp_site(data_frame, site):
    site_data = grab_site_data(data_frame, site)
    #print(site_data)#proper pd.data_frame good...
    return site_data

def create_site_array(data_frame):
    site_array = data_frame['site'].copy()
    site_array = site_array.to_numpy()
    return site_array

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
    #numerator = 'costs/car', 'salarie/employee', 'advertisingCosts/advanceBooking', 'complaints/rental'
    for x in site_data:
        #print(x) #x is name of column
        if(x != 'revenue/rental' and x != 'rentals/complaint' and x != 'cars/cost'):
            #site_data.drop(x, inplace = True, axis = 1)
            #wrong method needs to set to 0
            if(x == 'site'):
                site_data.drop(x, inplace = True, axis = 1)
            else:
                site_data[x] = 0
    return site_data

def clear_numer(data_frame):
    data_frame['revenue/rental'] = 0
    data_frame['rentals/complaint'] = 0
    data_frame['cars/cost'] = 0 
    return data_frame

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
    print("\nstarting data loop\n\n")
    for site in site_array:
        #run program that uses data_frame and site and returns lp result
        current_site = relative_lp_site(data_frame, site)
        print(current_site)
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

def adding_employee(pandas_data, site, employee_increase, salary):
    temp = pandas_data.copy()
    print("changing values")
    print("site:", site)
    print("employee increase:", employee_increase)
    print("salary per employee:", salary)
    #location = temp['site'] == site
    temp.loc[temp['site'] == site, ['employees']] += employee_increase
    temp.loc[temp['site'] == site, ['salaries']] += employee_increase * salary
    return temp
#raw_data = adding_employee(raw_data, 'WallaWalla', 2, 2000)
# print(raw_data)
def adding_car(pandas_data, site, ammount):
    temp = pandas_data.copy()
    print("changing values")
    print("site:", site)
    print("fleet increase:", ammount)
    temp.loc[temp['site'] == site, ['fleet']] += ammount
    return temp
def moving_cars(pandas_data, site_give, site_take, ammount):
    temp = pandas_data.copy()
    temp = adding_car(pandas_data, site_give, -ammount)
    temp = adding_car(pandas_data, site_take, ammount)
    return temp
#raw_data = moving_cars(raw_data, 'Sea-Tac', 'WallaWalla', 23)
#print(raw_data)
def data_changes(pandas_data):
    temp = pandas_data.copy()
    print("changing WallaWalla")
    temp = adding_employee(temp, 'WallaWalla', 2, 2000)
    temp = moving_cars(temp, 'Sea-Tac', 'WallaWalla', 23)
    print("changing Elensburg")
    temp = adding_employee(temp, 'WallaWalla', 2, 2000)
    temp = moving_cars(temp, 'Sea-Tac', 'Ellensburg', 25)
    return temp

raw_data = data_changes(raw_data)
print(raw_data)

raw_data = relativising_data(raw_data)
print(raw_data)

data_loop(raw_data)