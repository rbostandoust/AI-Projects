import csv
import random
import math
import matplotlib.pyplot as plt
from operator import add
from operator import sub


def read_csv_file():
    #mpg, cubicinches, hp, weightlbs, time-to-60, year, whichCluster
    data_point = []
    is_title = True
    with open('cars.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(is_title == True):
                is_title = False
                continue
            data_point.append([float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),0])    
    return data_point

def select_initial_centeroids(dp, k):
    init_cent = []
    for i in range (k):
        c_index = random.randint(0,260)
        init_cent.append(dp[c_index])
    return init_cent

def calculate_euclidian_distance(p1, p2):
    dist = 0
    for i in range (len(p1)-1):
        dist += (p1[i] - p2[i])*(p1[i] - p2[i])
    return math.sqrt(dist)

def K_Means_Cluster(dp, centeroid, k):
    min_dist = 0
    new_cntroid = [[0 for x in range(len(centeroid[0]))] for y in range(len(centeroid))]
    size_each_cluster = [0 for r in range(len(centeroid))]
    index_of_membered_cluster = 0
    for i in range (len(dp)):
        for j in range (len(centeroid)):
            dist = calculate_euclidian_distance(dp[i],centeroid[j])
            if(j==0):
                min_dist = dist
                index_of_membered_cluster = j
            elif(dist < min_dist):
                min_dist = dist
                index_of_membered_cluster = j
        dp[i][6] = index_of_membered_cluster
        new_cntroid[index_of_membered_cluster] = list(map(add,new_cntroid[index_of_membered_cluster],dp[i]))
        new_cntroid[index_of_membered_cluster][6] = 0
        size_each_cluster[index_of_membered_cluster] += 1
    for g in range (len(centeroid)):
        for k in range(len(centeroid[g])):
            new_cntroid[g][k] /= size_each_cluster[g]
    centeroid = new_cntroid
    return centeroid , dp
def cost_function(dp , centeroid):
    cost = 0
    input_size = len(dp)
    for i in range(input_size):
        cost += math.pow (calculate_euclidian_distance(dp[i],centeroid[dp[i][len(dp[i])-1]]),2)
    return cost / input_size   
def Start(k , can_plot):
    dp = read_csv_file()
    centeroid = select_initial_centeroids(dp,k)
    which_cluster = []
    for i in range (200):
        centeroid , dp = K_Means_Cluster(dp,centeroid,k)
    for j in range(len(dp)):
        if(can_plot):
            print (dp[j])
        which_cluster.append(dp[j][len(dp[j])-1])
    y_axis = []
    for i in range(len(dp)):
        y_axis.append(i)
    Cost = cost_function(dp, centeroid)
    if(can_plot):
        plt.figure("K-Means-Clustering")
        plt.plot(which_cluster,y_axis , 'ro')
        plt.xlabel("Cluster Number")
        plt.ylabel("Data Index")
        plt.show()
    return Cost

def main():
    one_run = False 
    if(one_run):
        k = 6
        print("Cost = ",Start(k,True))
    else: #We want to run with different Ks to plot the desired Diagram
        k_array = [ 2 ,3 , 5 , 6]
        x_axis = [2, 2, 2, 3, 3, 3, 5, 5, 5, 6, 6, 6]
        cost_array = []
        for i in range(len(k_array)):
            for j in range(3):
                cost_array.append(Start(k_array[i] , False))
        print("COST ARR = ", cost_array)
        plt.figure("Cost FUnction Diagram")
        plt.plot(x_axis,cost_array )
        plt.xlabel("Number of Clusters")
        plt.ylabel("Cost")
        plt.plot(x_axis,cost_array , 'ro')
        plt.show()        
main()

