import math
import matplotlib.pyplot as plt
import numpy as np

alpha = 0.00001
landa = 0.1 #L2_Norm Parameter
diff_factor = 0.0000001

def read_data_and_initialize():
    file = open("logistic_and_svm_data.txt")
    input_size = 0
    fields = []
    for line in file:
        fields.append(list(map(float,line.split(','))))#All Parameters
        input_size += 1
    y = np.zeros(shape=(1 , len(fields)))
    x = np.ones(shape=(len(fields[0]), len(fields)))
    teta = np.zeros(shape=(len(fields[0]) , 1))
    for i in range(len(fields[0])-1):
        for j in range(input_size):
            x[i+1][j] = fields[j][i]
    for i in range(len(fields)):
        y[0][i] = fields[i][2]
    file.close()
    return input_size, x, y, teta
def sigmoid(z):
      return 1.0 / (1 + np.exp(-z))
def calculate_error(y, h, input_size):
    l1 = np.log(h)
    l2 = np.log((1-h))
    err = (-1/input_size) * (np.matmul(y,l1.transpose()) + np.matmul(1-y, l2.transpose()))
    return err[0][0]

def gradient_descent(x , y , teta, h, input_size, has_L2):
    v = h - y
    dj_dtetaj = np.matmul(v, x.transpose())
    dj_dtetaj = dj_dtetaj.transpose()
    if(has_L2):
        new_teta = teta - alpha*(dj_dtetaj - 2*landa*teta)
        return new_teta
    new_teta = teta - alpha*dj_dtetaj
    return new_teta
    
def Logistic_Regression(x , y , teta, input_size, has_L2):
    diff = 10
    errors = []
    
    while(abs(diff) > diff_factor):
        h = sigmoid(np.matmul(teta.transpose(),x))
        curr_err = calculate_error(y, h, input_size)
        teta = gradient_descent(x, y, teta, h, input_size, has_L2)
        errors.append(curr_err)
        if(len(errors) == 1):
            diff = errors[0]
        else:
            index = len(errors) - 1
            diff = errors[index] - errors[index-1]
        print("ERROR= ", curr_err)
        print("DIFF= ",diff)
        # print("Teta= ",teta)
        print("--------------------------------------")
    return errors, teta
def diagnose(teta, file_name):
    file = open(file_name)
    input_size = 0
    fields = []
    for line in file:
        fields.append(list(map(float,line.split(','))))#All Parameters
        input_size += 1
    y = np.zeros(shape=(1 , len(fields)))
    my_predicted_res = np.zeros(shape=(1 , len(fields)))
    x = np.ones(shape=(len(fields[0]), len(fields))) #Assume each line has 3 parameters [A,B,isSick] => len(fields[0]) = 3
    for i in range(len(fields[0])-1):#First Row of X is filled with 1
        for j in range(input_size):
            x[i+1][j] = fields[j][i]
    for i in range(len(fields)):
        y[0][i] = fields[i][2]
    h = sigmoid(np.matmul(teta.transpose(),x))
    for i in range(len(h[0])):
        if(h[0][i] > 0.5):
            my_predicted_res[0][i] = 1
    counter = 0
    for j in range (len(my_predicted_res[0])):
        if(y[0][j] == my_predicted_res[0][j]):
            counter += 1
    print("ACCURACY = ", counter/len(my_predicted_res[0])*100 , " %")  
def main():
    input_size, x, y, teta = read_data_and_initialize()
    errors, teta = Logistic_Regression(x, y, teta, input_size, False)
    print("Teta=" , teta)
    diagnose(teta, "logistic_and_svm_data.txt")
    plt.figure("Error")
    plt.plot(errors)
    plt.show()
main()