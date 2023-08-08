import math
import matplotlib.pyplot as plt
import numpy as np

alpha = 0.0001 #Learning Rate
landa = 0.1 #L2_Norm Parameter
diff_factor = 0.000001

def read_housing_data_and_initialize_teta2():
    file = open("housing.data.txt")
    price = []
    fields = []
    Max = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    Min = [10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000]
    Avg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    minn = 100000 
    maxx = 0
    for line in file :
        fields.append(list(map(float,line.split())))#All House Parameters
        price.append(fields[len(fields)-1][13])
    house_param = np.ones(shape=(len(fields),14))
    teta = np.zeros(shape=(14,1))
    matx_price = np.zeros(shape=(len(fields), 1))
    for g in range(len(price)):
        matx_price[g][0] = price[g]
    for i in range(len(fields[0])):
        for j in range(len(fields)):
            if(fields[j][i] > maxx):
                maxx = fields[j][i]
            if(fields[j][i] < minn):
                minn = fields[j][i]
        Max[i] = maxx
        Min[i] = minn
        Avg[i] = (maxx-minn)/506
        minn = 100000 
        maxx = 0
    for i in range(len(fields[0])):
        for j in range(len(fields)):
            fields[j][i] = ((fields[j][i]) - Avg[i])/Max[i]        
    for i in range(len(fields)):
        for j in range(len(fields[i])):
            if(j <= 12):
                house_param[i][j+1] = (fields[i][j])
    # print(house_param)
    return house_param, price, teta, matx_price
def calculate_error(house_param, price, teta, input_size, matx_price):
    err1 = np.matmul(house_param ,teta) - matx_price
    err1 = np.power(err1, 2)
    err1 = err1.sum()
    return err1 / (2*input_size)
def gradian_descent(house_param, price, teta, input_size, has_L2, matx_price):
    sigma = 0
    new_teta = np.zeros(shape=(14,1))
    matmultiply = np.matmul(house_param,teta) - matx_price
    matmultiply = np.matmul(matmultiply.transpose(), house_param)
    sigma = matmultiply.transpose()
    if(has_L2):
        new_teta = teta - alpha*((1/input_size)*sigma - 2*landa*teta)
        return new_teta
    new_teta = teta - alpha*((1/input_size)*sigma)
    return new_teta
        
            
def Multivariate_Regression(house_param, price, teta, input_size, has_L2, matx_price):
    diff = 10
    errors = []
    while(abs(diff) > diff_factor):
        curr_err = calculate_error(house_param, price, teta, input_size, matx_price)
        errors.append(curr_err)
        teta = gradian_descent(house_param, price, teta, input_size, has_L2, matx_price)
        if(len(errors) == 1):
            diff = errors[0]
        else:
            index = len(errors) - 1
            diff = errors[index] - errors[index-1]
        print("ERROR= ", curr_err)
        print("DIFF= ",diff)
        print("--------------------------------------")
    return errors, teta
        
    
def main():
    house_param, price, teta, matx_price = read_housing_data_and_initialize_teta2()
    errors, teta = Multivariate_Regression(house_param, price, teta, len(price),False, matx_price)
    predicted_price = []
    for i in range(len(price)):
        predicted_price.append(np.matmul(house_param[i],teta))
    print("Teta=" , teta)
    plt.figure("Error")
    plt.plot(errors)
    plt.figure("Real Prices")
    plt.plot(price, 'ro')
    plt.figure("Predicted Prices")
    plt.plot(predicted_price, 'ro')
    plt.figure("Both")
    plt.plot(predicted_price, price)
    plt.xlabel("predicted")
    plt.ylabel("actual")
    plt.show()

main()

