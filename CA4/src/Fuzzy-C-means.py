import csv
import random
import math
from operator import add
from operator import sub


k = 5
m = 2
e = 0.01


def read_csv_file():
    #0.mpg, 1.cubicinches, 2.hp, 3.weightlbs, 4.time-to-60, 5.year
    data_point = []
    is_title = True
    with open('cars.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(is_title == True):
                is_title = False
                continue
            data_point.append([float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])])    
    return data_point

def initialize_membership_matrix(dp_size,cluster_num):
    mem_mtx = [[0 for x in range((dp_size))] for y in range((cluster_num))]
    for i in range(dp_size):
        index = random.randint(0,cluster_num - 1)
        mem_mtx[index][i] = 1
    return mem_mtx
def update_centeroids(dp, mem_mtx,k):
    centeroid = [[0 for x in range((len(dp[0])))] for y in range((k))] 
    nominator = 0
    denominator = 0
    for i in range(len(centeroid)):
        for j in range (len(centeroid[i])):
            for g in range(len(dp)):
                nominator += dp[g][j] * math.pow(mem_mtx[i][g],m)
                denominator += math.pow(mem_mtx[i][g],m)
            centeroid[i][j] = float(nominator / denominator)
            nominator = 0
            denominator = 0
    return centeroid
def calculate_distance_matrix(dp, centeroid, k):
    dist_matrix = [[0 for x in range(len(dp))] for y in range((k))]
    tmp_dst = 0
    for i in range(len(dist_matrix)):
        for j in range (len(dist_matrix[i])):
            for g in range (len(dp[j])):
                tmp_dst += (dp[j][g] - centeroid[i][g])*(dp[j][g] - centeroid[i][g])
            dist_matrix[i][j] = math.sqrt(tmp_dst)
            tmp_dst = 0
    return dist_matrix

def update_membership_matrix(dp,dist_matrix,centeroid, k):
    new_mem_mtx = [[0 for x in range(len(dp))] for y in range((k))]
    # print("KKKKKKK= ",k)
    # print("NEW LEN= ",len(new_mem_mtx))
    nominator = 0
    denominator = 0
    for j in range(len(new_mem_mtx)):
        for i in range (len(new_mem_mtx[j])):
            nominator = math.pow(1/dist_matrix[j][i],1/(m-1))
            for g in range (len(centeroid)):
                denominator += math.pow(1/dist_matrix[g][i],1/(m-1))
            new_mem_mtx[j][i] = nominator / denominator
            nominator = 0
            denominator = 0
    return new_mem_mtx
    
                                           
def Fuzzy_C_Means(dp, mem_mtx,k):
    # centeroid = [[0 for x in range((len(dp[0])))] for y in range((k))]
    err = 10
    while(err>e):
        # print("First K = ",k)
        centeroid = update_centeroids(dp, mem_mtx, k)
        dist_matrix = calculate_distance_matrix(dp, centeroid, k)
        new_mem_mtx = update_membership_matrix(dp, dist_matrix, centeroid, k)
        diff = []
        err = 0
        # print("Len1= ",len(mem_mtx), "  Len2= ",len(new_mem_mtx))
        for i in range(len(mem_mtx)):
            diff.append(list(map(sub,mem_mtx[i],new_mem_mtx[i])))
        for g in range (len(diff)):
            for j in range(len(diff[g])):
                err += abs(diff[g][j])
        err = err/(len(diff)*len(diff[0]))        
        print("DIFF= ",err) 
        mem_mtx = new_mem_mtx 
    return mem_mtx           
                   
    
def main():
    print("K=",k)
    dp = read_csv_file()
    membership_matrix = initialize_membership_matrix(len(dp), k)
    mem_mtx = Fuzzy_C_Means(dp, membership_matrix, k)

    # print(sum(mem_mtx[0]) + sum(mem_mtx[1]) + sum(mem_mtx[2]) + sum(mem_mtx[3]))
main()