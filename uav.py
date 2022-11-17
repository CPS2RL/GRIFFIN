from cmath import sqrt
import csv
from email.errors import HeaderMissingRequiredValue
from os import stat
from statistics import harmonic_mean
import geopy.distance
from scipy import rand
import utm 
import random 
import math 
import matplotlib.pyplot as plt 
import os
import psutil
from memory_profiler import profile
import time

def main(numUAV,time_array):
    coordination = []
    col = {}
    status = [0]* numUAV
    file_to_read = "UAVs_"+ str(numUAV)+"/uav_"
    read_suffix = ".csv" 

    #getting coordinations 

    for i in range(numUAV):
        fr = open(file_to_read+str(i)+read_suffix)
        reader = csv.reader(fr, delimiter=',')
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            t = int(row[2])
            coords_1= utm.to_latlon(x,y,14,"N")
            x_new = coords_1[0]
            y_new = coords_1[1]
            col[t] = {"x":x,"y":y}
        coordination.append(col.copy())
        col.clear()

    #calculating distances

    global_distance={}
    distance= []
    dis = []
    global_rssi_distance={}
    rssi_distance=[]
    rss = [] 
    
    for j in range(1,t+1):
        for i in range(numUAV):
            self_x = coordination[i][j]["x"]
            self_y = coordination[i][j]["y"]
            for uav in range(numUAV):
                if (uav==i):
                    dis.append(0)
                    continue

                x1 = coordination[uav][j]["x"]
                y1 = coordination[uav][j]["y"]
                x1_rssi = x1 + random.randint(-5, 5)
                y1_rssi = y1 + random.randint(-5, 5)

                harv_dist = math.sqrt((x1-self_x)**2 + (y1-self_y)**2)
                harv_dist_rssi = math.sqrt((x1_rssi-self_x)**2 + (y1_rssi-self_y)**2)
                dis.append(harv_dist)
                rss.append(harv_dist_rssi)
           
            distance.append(dis.copy())
            rssi_distance.append(rss.copy())
            dis.clear()
            rss.clear()
        global_distance[j] = distance.copy()
        global_rssi_distance[j] = rssi_distance.copy()
        distance.clear()
        rssi_distance.clear()

    #algorithm calculation
    for j in range(1,t+1): 
        for i in range(numUAV):
            start_time = time.time()    
            x_self = coordination[i][j]["x"]
            y_self = coordination[i][j]["y"]
            for target in range(numUAV): 
                if (target == id):
                    continue
                while True:
                    juryUAV1 = random.randint(0, numUAV-1)
                    if (juryUAV1 != id) and (juryUAV1 != target):
                        break 
                while True:
                    juryUAV2 = random.randint(0, numUAV-1)
                    if (juryUAV2 != id) and (juryUAV2 != target) and (juryUAV2 != juryUAV1):
                        break 
                x_target = coordination[target][j]["x"]
                y_target = coordination[target][j]["y"]    

                x_jury1 = coordination[juryUAV1][j]["x"]
                y_jury1 = coordination[juryUAV1][j]["y"]

                x_jury2 = coordination[juryUAV2][j]["x"]
                y_jury2 = coordination[juryUAV2][j]["y"]
                
            
                distance_1 = math.sqrt((x_target-x_self)**2 + (y_target-y_self)**2)
                
                
                testDiff_self = distance_1 - global_distance[j][i][target]

                if(testDiff_self < 1 and testDiff_self > -1):
                    status[target] = status[target] + 1 
                else:
                    status[target] = status[target] -1 
                

                rad_pow_jury1 = global_distance[j][juryUAV1][target]**2

                x_diff_jury1 = x_jury1 - x_target 
                y_diff_jury1 = y_jury1 - y_target 
                testDiff_jury1 =  rad_pow_jury1 - (x_diff_jury1**2 + y_diff_jury1**2) 

                
                rad_pow_self = global_distance[j][i][target]**2
                x_diff_self = x_self - x_target 
                y_diff_self = y_self - y_target 
                testDiff_self = rad_pow_self - (x_diff_self**2 + y_diff_self**2)
                
                rad_pow_jury2 = global_distance[j][juryUAV2][target]**2
                x_diff_jury2 = x_jury2 - x_target 
                y_diff_jury2 = y_jury2 - y_target 
                testDiff_jury2 = rad_pow_jury2 - (x_diff_jury2**2 + y_diff_jury2**2)                

                if (testDiff_jury1 < 1 and testDiff_jury1 > -1) and (testDiff_self < 1 and testDiff_self > -1) and (testDiff_jury2 < 1 and testDiff_jury2 > -1):
                    status[target] = status[target] + 1 
                else:
                    status[target] = status[target] -1 
            end_time = time.time()
            print("time overhead: ", end_time - start_time)
            if ( i == 0 ):
                time_array.append(end_time-start_time)
        #============================================================)=========================== 
        status = [0]* numUAV

numUAV = 100
filename = "time_file.txt"
time_array = []
main(numUAV,time_array)
time_file  = open(filename,"w")
for i in time_array:
    time_file.write(str(i)+"\n")
print("finisehd!")
