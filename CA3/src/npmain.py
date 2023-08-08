import glob
from PIL import Image
from math import exp
from random import seed
from random import random
import numpy as np
import random
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

in_layer_size = 784
hid_layer_size = 50
out_layer_size = 10
iteration_length = 5000
iteration_length_stochastic = 500

dropout_percent = 0.2
do_dropout = True
r = 0.1

lr = 0.00001


#Sigmoid Function
def sigmoid (x):
    return 1/(1 + np.exp(-x))

#Derivative of Sigmoid Function
def derivatives_sigmoid(x):
    return x * (1 - x)


def gradient_descent(dataset, result, hid_w, out_w, hid_b, out_b):
    y_axis = []
    x_axis = []
    
    for k in range (iteration_length):

        #Forward Propagation
        hid_amount = dataset.dot(hid_w) + hid_b
        hid_amount_active = sigmoid(hid_amount)
        out_amount = hid_amount_active.dot(out_w) + out_b
        out_amount_active = (out_amount)


        #Backward Propagation
        E = result-out_amount_active
        slope_output_layer = derivatives_sigmoid(out_amount_active)
        slope_hidden_layer = derivatives_sigmoid(hid_amount_active)
        # d_output = E * slope_output_layer
        d_output = E 
        Error_at_hidden_layer = d_output.dot(out_w.T)
        d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
        if(do_dropout):
            hid_amount_active *=np.random.binomial([np.ones((len(dataset),hid_layer_size))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

        # w_hidden += (input_data.T.dot(d_hidden) + w_hidden * r) * lr
        # out_w += (dataset.T.dot(d_hiddenlayer) + out_w * r ) * lr
        # out_w += hid_amount_active.T.dot(d_output) *lr
        out_w += (hid_amount_active.T.dot(d_output) + out_w * r ) * lr
        # out_b += np.sum(d_output, axis=0,keepdims=True) *lr
        out_b += d_output.sum(axis=0) * lr
        # hid_w += dataset.T.dot(d_hiddenlayer) *lr
        hid_w += (dataset.T.dot(d_hiddenlayer) + hid_w * r) * lr
        # hid_b += np.sum(d_hiddenlayer, axis=0, keepdims=True) *lr
        hid_b += d_hiddenlayer.sum(axis = 0) * lr
        cost = np.mean(np.square(result - out_amount_active))
        print ("[",k,"]: ",cost)
        y_axis.append(cost)
        x_axis.append(k)
        # print (np.mean(np.square(result - out_amount_active)))
    plt.plot(x_axis,y_axis)
    plt.show()

def stochastic(new_dataset, new_result, hid_w, out_w, hid_b, out_b):
    x_axis = []
    y_axis = []
    
    for k in range (iteration_length_stochastic):
        for i in range (len(new_dataset)):
            dataset = np.zeros(((1,784)))
            dataset[0] = new_dataset[i]
            result = np.zeros((1,10))
            result[0] = new_result[i]


            #Forward Propagation
            hid_amount = dataset.dot(hid_w) + hid_b
            hid_amount_active = sigmoid(hid_amount)
            out_amount = hid_amount_active.dot(out_w) + out_b
            # out_amount_active = sigmoid(out_amount)
            out_amount_active = (out_amount)


            #Backward Propagation
            E = result-out_amount_active
            slope_output_layer = derivatives_sigmoid(out_amount_active)
            slope_hidden_layer = derivatives_sigmoid(hid_amount_active)
            # d_output = E * slope_output_layer
            d_output = E 
            Error_at_hidden_layer = d_output.dot(out_w.T)
            d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
            if(do_dropout):
                hid_amount_active *=np.random.binomial([np.ones((len(dataset),hid_layer_size))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

            # w_hidden += (input_data.T.dot(d_hidden) + w_hidden * r) * lr
            # out_w += (dataset.T.dot(d_hiddenlayer) + out_w * r ) * lr
            # out_w += hid_amount_active.T.dot(d_output) *lr
            out_w += (hid_amount_active.T.dot(d_output) + out_w * r ) * lr
            # out_b += np.sum(d_output, axis=0,keepdims=True) *lr
            out_b += d_output.sum(axis=0) * lr
            # hid_w += dataset.T.dot(d_hiddenlayer) *lr
            hid_w += (dataset.T.dot(d_hiddenlayer) + hid_w * r) * lr
            # hid_b += np.sum(d_hiddenlayer, axis=0, keepdims=True) *lr
            hid_b += d_hiddenlayer.sum(axis = 0) * lr
        cost = np.mean(np.square(result - out_amount_active))
        print ("[",k,"]: ",cost)
        y_axis.append(cost)
        x_axis.append(k)
    plt.plot(x_axis, y_axis)
    plt.show()
        

def read_images_info(dataset, result):
    path = os.getcwd() + '/' + "notMNIST_small"
    number = 1
    index = 0
    for filename in os.listdir(path):
        counter = 1
        newPath = path + '/' + filename
        if(filename != ".DS_Store"):
            tmp = []
            # print ("salammmm", number)
            for k in range(1, 11):
                if(k == number):
                    tmp.append(1)
                else:
                    tmp.append(0)
            for image in os.listdir(newPath):
                if(image != ".DS_Store"):
                    if (counter <= 300):
                        #read image 
                        image_path = newPath + '/' + image
                        image_file = Image.open(image_path)
                        
                        # image = Image.open(image_path).convert("L")
                        # arr = np.asarray(image)
                        # plt.imshow(arr, cmap='gray')
                        # plt.show()
                        
                        image_file = image_file.convert('1') # convert image to black and white
                        pix = image_file.load()
                        temp = []
                        for i in range (0, 28):
                            for j in range (0, 28):
                                temp.append(0 if pix[i,j]==0 else 1)
                        dataset[index] = (temp)
                        result[index] =(tmp)
                        index += 1
                    counter += 1
            number += 1   
            # print(counter)
def read_images_info2(dataset, result):
    path = os.getcwd() + '/' + "notMNIST_small"
    number = 1
    index = 0
    for filename in os.listdir(path):
        counter = 1
        newPath = path + '/' + filename
        if(filename != ".DS_Store"):
            tmp = []
            # print ("salammmm", number)
            for k in range(1, 11):
                if(k == number):
                    tmp.append(1)
                else:
                    tmp.append(0)
            for image in os.listdir(newPath):
                if(image != ".DS_Store"):
                    if (counter >= 601 and counter <= 900):
                        #read image 
                        image_path = newPath + '/' + image
                        image_file = Image.open(image_path)
                        
                        # image = Image.open(image_path).convert("L")
                        # arr = np.asarray(image)
                        # plt.imshow(arr, cmap='gray')
                        # plt.show()
                        
                        image_file = image_file.convert('1') # convert image to black and white
                        pix = image_file.load()
                        temp = []
                        for i in range (0, 28):
                            for j in range (0, 28):
                                temp.append(0 if pix[i,j]==0 else 1)
                        dataset[index] = (temp)
                        result[index] =(tmp)
                        index += 1
                    counter += 1
            number += 1   
            # print(counter)


dataset = np.zeros((3000,784))
result = np.zeros((3000,10))
read_images_info(dataset, result)

hid_w = np.random.uniform(-0.1,0.1,(784,hid_layer_size))
out_w = np.random.uniform(-0.1,0.1,(hid_layer_size, 10))

hid_b = np.ones(hid_layer_size)
out_b = np.ones(out_layer_size)

alg = 0
print("Please Enter Your Optimization Algorithm: 1)Gradient Descent  2)Stochastic")
alg = (int)(input())

if(alg == 1):
    gradient_descent(dataset, result, hid_w, out_w, hid_b, out_b)
else:
    stochastic(dataset, result, hid_w, out_w, hid_b, out_b)



#Trained Data Acc
hid_amount = dataset.dot(hid_w) + hid_b
hid_amount_active = sigmoid(hid_amount)
out_amount = hid_amount_active.dot(out_w) + out_b
out_amount_active = (out_amount)
cnt = 0
for i in  range (len(result)):
    if (np.argmax(result[i]) == np.argmax(out_amount_active[i])):
        cnt += 1
print("Training Acc= ", cnt/len(result) * 100, "%")

dataset2 = np.zeros((3000,784))
result2 = np.zeros((3000,10))
read_images_info2(dataset2, result2)

#Test Acc
hid_amount = dataset2.dot(hid_w) + hid_b
hid_amount_active = sigmoid(hid_amount)
out_amount = hid_amount_active.dot(out_w) + out_b
out_amount_active = (out_amount)
cnt = 0
for i in  range (len(result2)):
    if (np.argmax(result2[i]) == np.argmax(out_amount_active[i])):
        cnt += 1
print("Test Acc= ", cnt/len(result2) * 100, "%")





# print((dataset[2999]))