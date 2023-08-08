import math
import matplotlib.pyplot as plt
import numpy as np

alpha = 0.001

def read_housing_data():
    file = open("housing.data.txt")
    fields = []
    for i in range(3):
        fields.append([])
    for line in file :
        fields[0].append(list(map(float,line.split()))[0])#Crime
        fields[1].append(list(map(float,line.split()))[2])#Tax
        fields[2].append(list(map(float,line.split()))[13])#Price
    print("fields = ",fields)
    return fields
def calculate_error(house_data, input_size, input_index, teta):
    err = 0
    for i in range(input_size):
        err += math.pow((teta[0] + house_data[input_index][i]*teta[1]) - house_data[2][i],2)
    err = err / (2*input_size)
    return err
def gradient_descent(house_data, input_size, input_index, teta):
    new_teta = []
    sigma = [0,0]
    for i in range(input_size):
        sigma[0] += (teta[0] + house_data[input_index][i]*teta[1]) - house_data[2][i]
        sigma[1] += ((teta[0] + house_data[input_index][i]*teta[1]) - house_data[2][i])*house_data[input_index][i]

    for i in range(len(teta)):
        if(i == 0):
            new_teta.append(teta[i] - alpha*(1/input_size)*sigma[i])
        else:
            new_teta.append(teta[i] - alpha*(1/input_size)*sigma[i])
    return new_teta
        
def Univariate_Linear_Regression(house_data, input_size, input_index):
    teta = [0,0]
    diff = 10
    errors = []
    while(abs(diff) > 0.0001):
        curr_err = calculate_error(house_data, input_size, input_index, teta)
        errors.append(curr_err)
        teta = gradient_descent(house_data, input_size, input_index, teta)
        if(len(errors) == 1):
            diff = errors[0]
        else:
            index = len(errors) - 1
            diff = errors[index] - errors[index-1]
        print("ERROR= ", curr_err)
        print("DIFF= ",diff)
        print("Teta= ",teta)
        print("--------------------------------------")
    return errors, teta
def main():
    in_var = 0 #Crime as Input = 0 | Tax as Input = 1
    house_data = read_housing_data()
    errors, teta = Univariate_Linear_Regression(house_data, len(house_data[in_var]), in_var)#Linear Regression according to Crime Input or Tax Input
    # """Plot a line from slope and intercept"""
    plt.plot(house_data[in_var], house_data[2], 'ro')
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = teta[0] + teta[1] * x_vals
    plt.plot(x_vals, y_vals, '--')
    plt.figure("Error")
    plt.plot(errors)
    plt.show()
main()

