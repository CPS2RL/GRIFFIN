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
#import psutil
import tracemalloc
import time 
#from memory_profiler import profile
logfile = open("logmain.txt","w")

#Basic scheme alogrithm 


def basicScheme(numUAV,maliciousUAV,TP,FP,FN,Accuracy,Precision, F1):
    coordination = []
    col = {}
    status = [0]* numUAV
    grd_truth = [1]* numUAV
    file_to_read = "UAVs_"+ str(numUAV)+"/uav_"
    read_suffix = ".csv" 
    maliciousUAV = maliciousUAV/100
    numMalicious = int(maliciousUAV * numUAV)
    malicious = []
    randomNumUAVs = [] 
    false_negative = 0 
    false_positive = 0 
    TrueNegative = 0 
    detected = 0 
    TruePositive = 0  
    distance_1 = 0
    recall = 0 
    islying = 0
    testcnt = 0  


    for i in range(numUAV):
        randomNumUAVs.append(i)
    #print(randomNumUAVs)
    for r in range(numMalicious):
        q = random.randint(0,len(randomNumUAVs)-1)
        #print(q)
        malicious.append(randomNumUAVs[q])
        #print(malicious)
        del randomNumUAVs[q]

    #ground_truth for k in range(len(grd_truth)):
    for mal in malicious:
        grd_truth[mal]= -1 

    #print(malicious)

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
    temp1 = 0 
    temp2 = 0 
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

                #coords_1= utm.to_latlon(self_x,self_y,14,"N")
                #coords_2= utm.to_latlon(x1,y1,14,"N")
            
                #coords_2_rssi= utm.to_latlon(x1_rssi,y1_rssi,14,"N")

                #harv_dist = geopy.distance.geodesic(coords_1, coords_2).m
                #harv_dist_rssi = geopy.distance.geodesic(coords_1, coords_2_rssi).m
                #harv_dist = math.dist([self_x,self_y],[x1,y1])
                #harv_dist_rssi = math.dist([self_x,self_y],[x1_rssi,y1_rssi])
                harv_dist = math.sqrt((x1-self_x)**2 + (y1-self_y)**2)
                harv_dist_rssi = math.sqrt((x1_rssi-self_x)**2 + (y1_rssi-self_y)**2)
                #print(harv_dist)
                #print(harv_dist_rssi)
                dis.append(harv_dist)
                rss.append(harv_dist_rssi)
            #print(dis))
            distance.append(dis.copy())
            rssi_distance.append(rss.copy())
            dis.clear()
            rss.clear()
        global_distance[j] = distance.copy()
        global_rssi_distance[j] = rssi_distance.copy()
        distance.clear()
        rssi_distance.clear()

    #print(global_rssi_distance)

    #algorithm calculation
    for j in range(1,t+1):     
        for i in range(numUAV): 
            x_self = coordination[i][j]["x"]
            y_self = coordination[i][j]["y"]
            for target in range(numUAV): 
                #print("target:",target)
                
                #if (status[i]<-1):
                #    break

                if (target == i):
                    continue
                while True:
                    juryUAV1 = random.randint(0, numUAV-1)
                    if (juryUAV1 != i) and (juryUAV1 != target):
                        break 
                while True:
                    juryUAV2 = random.randint(0, numUAV-1)
                    if (juryUAV2 != i) and (juryUAV2 != target) and (juryUAV2 != juryUAV1):
                        break 
                x_target = coordination[target][j]["x"]
                y_target = coordination[target][j]["y"]
                #print("x_target:",x_target)    
                #print("y_target:",y_target)      


                x_jury1 = coordination[juryUAV1][j]["x"]
                y_jury1 = coordination[juryUAV1][j]["y"]
                #print("jury1:",juryUAV1)
                #print("x_jury1:",x_jury1)    
                #print("y_jury1:",y_jury1)    
                
                x_jury2 = coordination[juryUAV2][j]["x"]
                y_jury2 = coordination[juryUAV2][j]["y"]
                #print("jury1:",juryUAV2)
                #print("x_jury2:",x_jury2)    
                #print("y_jury2:",y_jury2) 
                
                
                #scenario 1 : target is malicious
                #=============================================================
                # send false position in the same radius 
                # case 1 :
                # juries and receiver are non-malicious
                receiver_is_mal = 0
                jury1_is_mal = 0 
                jury2_is_mal = 0
                islying = 0 
                if (j >50 and j<150):
                    for mal in malicious: 
                        if (target==mal):
                            islying = 1 
                            res= [-1,1][random.randrange(2)]
                            if (res==1):
                                distance_1= 1
                            else:
                                r = global_distance[j][i][target]
                                theta = random.random() * 2 * math.pi
                                x_target = x_self + r * math.cos(theta)
                                y_target = y_self + r * math.sin(theta)
                                distance_1 = math.sqrt((x_target-x_self)**2 + (y_target-y_self)**2)
                        if (i==mal):
                            receiver_is_mal = 1             
                else:
                    distance_1 = math.sqrt((x_target-x_self)**2 + (y_target-y_self)**2)
                if (islying==0):
                    distance_1 = math.sqrt((x_target - x_self) ** 2 + (y_target - y_self) ** 2)
                
                difference = distance_1 - global_distance[j][i][target]
                #print("UAV "+str(i)+ "to UAV "+str(target)+" is:" +str(difference))
                #print(malicious)
                if receiver_is_mal:
                    neg_pos= 1 
                    if islying:
                        status[target] = status[target] + neg_pos
                    else:
                        status[target] = status[target] - neg_pos
                else:
                    if (difference < 2 and difference > -2):
                        status[target] = status[target] + 1 
                    else:
                        status[target] = status[target] -1 
                    #============================================================)===========================
                #receiver are non-malicious and juries are malicious 



        #check how many UAVs voted for malicious 
        if (j >50 and j<150):
            for mal in malicious: 
                grd_truth[mal]= -1
        else:
            for mal in malicious: 
                grd_truth[mal] = 1 
        #print("time: ",j)
        for k in range(len(status)):
            if (status[k]==0) and (i==k):
                continue
            elif (grd_truth[k]==-1) and (status[k]>grd_truth[k]):
                false_negative= false_negative+1 
            elif (grd_truth[k]==1) and (status[k]<grd_truth[k]):
                false_positive= false_positive+1 
            elif (grd_truth[k]==-1) and (status[k]<=grd_truth[k]):
                detected = detected + 1 
            elif (grd_truth[k]==1) and (status[k]>=grd_truth[k]):
                TrueNegative = TrueNegative + 1
            #if ((j > 5)  and (j<= 10) and (k in malicious)):
            #    logfile.write("Time slot: "+str(j)+"\r\n") 
            #    logfile.write("ground truth for UAV " +str(k)+" is: "+str(grd_truth[k])+"\r\n")
            #    logfile.write("status for UAV " +str(k)+" is: "+str(status[k])+"\r\n")
            #    logfile.write("================================================\r\n")
            #print ("UAV" + str(k) + ":" +str(status[k]))
        status = [0]* numUAV

    #print("malicious UAVs:")
    #print(malicious)
    #print("malicious UAVs: ",maliciousUAV)
    if (numMalicious!=0):
        #The false positive rate is calculated as FP/FP+TN
        #The false negative rate FN/FN+TP,
        #divide_on_false_negative = 5 * numMalicious
        #print(detected)
        FPRate = false_positive / (false_positive + TrueNegative)
        FNRate = false_negative / (false_negative + detected)
        #detArray.append(detected/divide_on_false_negative)
        acc = ( TrueNegative + detected ) / (TrueNegative + detected + false_positive + false_negative)
        # precision = tp / (tp + fp) 
        Prec = detected / (detected + false_positive)
        recall = detected / (detected + false_negative)
        if (Prec + recall == 0):
            F1.append(0)
        else:
            F1.append(200*(Prec * recall)/ (Prec + recall))
        TruePositive = detected / (detected + false_negative)
        FP.append(FPRate*100)
        FN.append(FNRate*100)
        Precision.append(Prec*100)
        Accuracy.append(acc*100)
        TP.append(TruePositive*100)
        #print("detection rate: ",detected/divide_on_false_negative)
        #print("false negative rate: ",false_negative/divide_on_false_negative)
        #print("false positive rate: ",false_positive/divide_on_false_negative)

    else:
        TP.append(100)


















def main(numUAV,maliciousUAV,TP,FP,FN,Accuracy,Precision,F1,TNRate):
    coordination = []
    col = {}
    status = [0]* numUAV
    grd_truth = [1]* numUAV
    file_to_read = "UAVs_"+ str(numUAV)+"/uav_"
    read_suffix = ".csv" 
    maliciousUAV = maliciousUAV / 100
    numMalicious = int(maliciousUAV * numUAV)
    malicious = []
    randomNumUAVs = [] 
    false_negative = 0 
    false_positive = 0 
    TrueNegative = 0 
    detected = 0 
    TruePositive = 0 
    distance_1 = 0 
    recall = 0 
    islying = 0 
    testcnt = 0  


    for i in range(numUAV):
        randomNumUAVs.append(i)
    #print(randomNumUAVs)
    for r in range(numMalicious):
        q = random.randint(0,len(randomNumUAVs)-1)
        #print(q)
        malicious.append(randomNumUAVs[q])
        #print(malicious)
        del randomNumUAVs[q]

    #ground_truth for k in range(len(grd_truth)): 



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
    temp1 = 0 
    temp2 = 0 
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

                #coords_1= utm.to_latlon(self_x,self_y,14,"N")
                #coords_2= utm.to_latlon(x1,y1,14,"N")
            
                #coords_2_rssi= utm.to_latlon(x1_rssi,y1_rssi,14,"N")

                #harv_dist = geopy.distance.geodesic(coords_1, coords_2).m
                #harv_dist_rssi = geopy.distance.geodesic(coords_1, coords_2_rssi).m
                #harv_dist = math.dist([self_x,self_y],[x1,y1])
                #harv_dist_rssi = math.dist([self_x,self_y],[x1_rssi,y1_rssi])
                harv_dist = math.sqrt((x1-self_x)**2 + (y1-self_y)**2)
                harv_dist_rssi = math.sqrt((x1_rssi-self_x)**2 + (y1_rssi-self_y)**2)
                #print(harv_dist)
                #print(harv_dist_rssi)
                dis.append(harv_dist)
                rss.append(harv_dist_rssi)
            #print(dis))
            distance.append(dis.copy())
            rssi_distance.append(rss.copy())
            dis.clear()
            rss.clear()
        global_distance[j] = distance.copy()
        global_rssi_distance[j] = rssi_distance.copy()
        distance.clear()
        rssi_distance.clear()

    #print(global_rssi_distance)

    #algorithm calculation
    for j in range(1,t+1):     
        for i in range(numUAV): 
            x_self = coordination[i][j]["x"]
            y_self = coordination[i][j]["y"]
            #tracemalloc.start()
            #start_time = time.time()

            for target in range(numUAV): 
                #print("target:",target)
                
                #if (status[i]<-1):
                #    break

                if (target == i):
                    continue
                while True:
                    juryUAV1 = random.randint(0, numUAV-1)
                    if (juryUAV1 != i) and (juryUAV1 != target):
                        break 
                while True:
                    juryUAV2 = random.randint(0, numUAV-1)
                    if (juryUAV2 != i) and (juryUAV2 != target) and (juryUAV2 != juryUAV1):
                        break 
                x_target = coordination[target][j]["x"]
                y_target = coordination[target][j]["y"]
                #print("x_target:",x_target)    
                #print("y_target:",y_target)      


                x_jury1 = coordination[juryUAV1][j]["x"]
                y_jury1 = coordination[juryUAV1][j]["y"]
                #print("jury1:",juryUAV1)
                #print("x_jury1:",x_jury1)    
                #print("y_jury1:",y_jury1)    
                
                x_jury2 = coordination[juryUAV2][j]["x"]
                y_jury2 = coordination[juryUAV2][j]["y"]
                #print("jury1:",juryUAV2)
                #print("x_jury2:",x_jury2)    
                #print("y_jury2:",y_jury2) 
                
                
                #scenario 1 : target is malicious
                #=============================================================
                # send false position in the same radius 
                # case 1 :
                # juries and receiver are non-malicious
                receiver_is_mal = 0
                jury1_is_mal = 0 
                jury2_is_mal = 0
                resGlobal = 0 
                islying = 0 
                if (j > 50 and j<150):
                    for mal in malicious:
                        if (target==mal):
                            islying = 1 
                            resGlobal= [-1,1][random.randrange(2)]
                            if (resGlobal==1):
                                distance_1= 1
                            else:
                                r = global_distance[j][i][target]
                                theta = random.random() * 2 * math.pi
                                x_target = x_self + r * math.cos(theta)
                                y_target = y_self + r * math.sin(theta)
                                #distance_1 = math.sqrt((x_target-x_self)**2 + (y_target-y_self)**2)
                        #if (juryUAV1==mal):
                        #    res =1  
                            #[1,1][random.randrange(2)]
                        #    if (res==1):
                        #        jury1_is_mal = 1 
                        #        temp1 = global_distance[j][juryUAV1][target]
                        #        global_distance[j][juryUAV1][target] = random.random()
                        #if (juryUAV2==mal):
                        #    res = 1
                            #[1,1][random.randrange(2)]
                        #    if (res==1):
                        #        jury2_is_mal = 1 
                        #        temp2 = global_distance[j][juryUAV2][target]
                        #        global_distance[j][juryUAV2][target] = random.random()
                        if (i==mal):
                            receiver_is_mal = 1 
                
                
                if resGlobal:
                    testDiff_self = distance_1 - global_distance[j][i][target]
                    if receiver_is_mal: 
                        if islying:
                            neg_pos=1  
                            #[-1,1][random.randrange(2)]
                            status[target] = status[target] + neg_pos
                        else:
                            status[target] = status[target] - neg_pos
                        islying = 0 
                        receiver_is_mal =0 
                    else:
                        if(testDiff_self < 1 and testDiff_self > -1):
                            status[target] = status[target] + 1 
                        else:
                            status[target] = status[target] -1 
                    if jury1_is_mal:
                        global_distance[j][juryUAV1][target] = temp1
                        jury1_is_mal = 0 
                    if jury2_is_mal:
                        global_distance[j][juryUAV2][target] = temp2
                        jury2_is_mal = 0 
                    continue 


                rad_pow_jury1 = global_distance[j][juryUAV1][target]**2
                #print(global_rssi_distance[j][juryUAV1][target]**2)

                x_diff_jury1 = x_jury1 - x_target 
                y_diff_jury1 = y_jury1 - y_target 
                testDiff_jury1 =  rad_pow_jury1 - (x_diff_jury1**2 + y_diff_jury1**2) 
                #print("testjury1:",testDiff_jury1)
                
                rad_pow_self = global_distance[j][i][target]**2
                x_diff_self = x_self - x_target 
                y_diff_self = y_self - y_target 
                testDiff_self = rad_pow_self - (x_diff_self**2 + y_diff_self**2)
                #print("testself:",testDiff_self)
                
                rad_pow_jury2 = global_distance[j][juryUAV2][target]**2
                x_diff_jury2 = x_jury2 - x_target 
                y_diff_jury2 = y_jury2 - y_target 
                testDiff_jury2 = rad_pow_jury2 - (x_diff_jury2**2 + y_diff_jury2**2)
                #print("testjury2:",testDiff_jury2)
                
                
                            

                if receiver_is_mal: 
                    if islying:
                        neg_pos= 1
                        status[target] = status[target] + neg_pos
                    else:
                        status[target] = status[target] - 1
                    islying = 0 
                    receiver_is_mal = 0
                else:
                    if (testDiff_jury1 < 1 and testDiff_jury1 > -1) and (testDiff_self < 1 and testDiff_self > -1) and (testDiff_jury2 < 1 and testDiff_jury2 > -1):
                        status[target] = status[target] + 1 
                    else:
                        status[target] = status[target] -1 
                    #============================================================)===========================
                if jury1_is_mal:
                    global_distance[j][juryUAV1][target] = temp1
                    jury1_is_mal = 0 
                if jury2_is_mal:
                    jury1_is_mal = 0 
                    global_distance[j][juryUAV2][target] = temp2
                #receiver are non-malicious and juries are malicious 
            #end_time = time.time() 
            #print("execution time: ",end_time-start_time)
            #print(tracemalloc.get_traced_memory()) 
            #tracemalloc.stop()


        #check how many UAVs voted for malicious 

        #print("time: ",j)
        if (j >50 and j<150):
            for mal in malicious: 
                grd_truth[mal]= -1
        else:
            for mal in malicious: 
                grd_truth[mal] = 1 
        
        for k in range(len(status)):
            if (status[k]==0) and (i==k):  
                continue
            elif (grd_truth[k]==-1) and (status[k]>grd_truth[k]):
                false_negative= false_negative+1 
            elif (grd_truth[k]==1) and (status[k]<grd_truth[k]):
                false_positive= false_positive+1 
            elif (grd_truth[k]==-1) and (status[k]<=grd_truth[k]):
                detected = detected + 1 
            elif (grd_truth[k]==1) and (status[k]>=grd_truth[k]):
                TrueNegative = TrueNegative + 1
            #if ((j > 5)  and (j<= 10) and (k in malicious)):
                #logfile.write("Time slot: "+str(j)+"\r\n") 
                #logfile.write("ground truth for UAV " +str(k)+" is: "+str(grd_truth[k])+"\r\n")
                #logfile.write("status for UAV " +str(k)+" is: "+str(status[k])+"\r\n")
                #logfile.write("================================================\r\n")
            #print ("UAV" + str(k) + ":" +str(status[k]))
        logfile.write("J=" + str(j)+"\r\n")
        logfile.write("false_positive:" +str(false_positive) +"\r\n")
        logfile.write("true negative:"+ str(TrueNegative)+"\r\n")
        logfile.write("True positive:" +str(detected) +"\r\n")
        logfile.write("false negative:"+ str(false_negative)+"\r\n")
        logfile.write("================================================\r\n")
        
        
        status = [0]* numUAV
    #print("malicious UAVs:")
    #print(malicious)
    #print("malicious UAVs: ",maliciousUAV)
    if (numMalicious!=0):
        #The false positive rate is calculated as FP/FP+TN
        #The false negative rate FN/FN+TP,
        #divide_on_false_negative = 5 * numMalicious
        #print(detected)
        FPRate = false_positive / (false_positive + TrueNegative)
        FNRate = false_negative / (false_negative + detected)
        #detArray.append(detected/divide_on_false_negative)
        acc = ( TrueNegative + detected ) / (TrueNegative + detected + false_positive + false_negative)
        #print("J=",j)
        #print("cnt: ",testcnt)
        #print("TrueNegative: ",TrueNegative)
        #print("TruePositive: ",detected)
        #print("false_positive: ",false_positive)
        #print("false_negative: ",false_negative)
        #print("Accuracy: ",acc)
        #print("=======================================")
        # precision = tp / (tp + fp) 
        Prec = detected / (detected + false_positive)
        #Recall = True Positive / (True Positive + False Negative)
        recall = detected / (detected + false_negative)
        if (Prec + recall == 0):
            F1.append(0)
        else:
            
            F1.append(200*(Prec * recall)/ (Prec + recall))
        TruePositive = detected / (detected + false_negative)
        TNRate.append((TrueNegative / (TrueNegative+ false_positive))*100) 
        FP.append(FPRate*100)
        FN.append(FNRate*100)
        Precision.append(Prec*100)
        Accuracy.append(acc*100)
        TP.append(TruePositive*100)
        #detected = 0 
        #TrueNegative = 0 
        #false_positive = 0 
        #false_negative = 0 


        #print("detection rate: ",detected/divide_on_false_negative)
        #print("false negative rate: ",false_negative/divide_on_false_negative)
        #print("false positive rate: ",false_positive/divide_on_false_negative)

    else:
        TP.append(1*100)


mali = []
j=0
numUAV = [20]
#detectedArray = []
FPArray = []
FNArray = [] 
Accuracy = []
Precision = []
TruePositiveArray = []
F1score = []
TrueNegativeArray = []
B_FPArray = []
B_FNArray = [] 
B_Accuracy = []
B_Precision = []
B_TruePositiveArray = []
B_F1score = []
font = {'family' : 'normal',
        'size'   : 14}



for i in range(14):
    j=j+5
    mali.append(j)

for n in range(1):
    for ma in mali:
        
        main(numUAV[n],ma,TruePositiveArray,FPArray,FNArray,Accuracy,Precision,F1score,TrueNegativeArray)
        basicScheme(numUAV[n],ma,B_TruePositiveArray,B_FPArray,B_FNArray,B_Accuracy,B_Precision,B_F1score)
    
    lab = "GRIFFIN"
    B_lab = "Baseline"
    f1 = plt.figure(1)
    plt.rcParams['font.size'] = 14
    plt.plot(mali,TruePositiveArray,label=lab,marker="o",color="navy")
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("Detection Rate (%)")

    plt.plot(mali,B_TruePositiveArray,label=B_lab,linestyle='dashed',marker="x",  color='maroon'  )
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("Detection Rate (%)")
    #plt.legend(edgecolor="black")
    plt.legend(edgecolor="black",prop={'size': 12})
    plt.savefig('detection.pdf')
    f2 = plt.figure(2)
    ax =plt.gca()
    ax.set_ylim([0, 100])
    plt.rcParams['font.size'] = 14
    plt.plot(mali,FPArray,label=lab,marker="o",color="navy")
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("False Positive Rate (%)")
    
    plt.plot(mali,B_FPArray,label=B_lab,linestyle='dashed',marker="x", color='maroon' )
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("False Positive Rate (%)")
    #plt.legend(edgecolor="black")
    plt.legend(edgecolor="black",prop={'size': 12})
    plt.savefig('FP.pdf')
    f3 = plt.figure(3)
    plt.rcParams['font.size'] = 14
    plt.plot(mali,FNArray,label=lab,marker="o",color="navy")
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("False Negative Rate (%)")

    plt.plot(mali,B_FNArray,label=B_lab,linestyle='dashed',marker="x", color='maroon' )
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("False Negative Rate (%)")
    plt.legend(edgecolor="black",prop={'size': 12})
    plt.savefig('FN.pdf')
    f4 = plt.figure(4)
    plt.rcParams['font.size'] = 14
    plt.plot(mali,Accuracy,label=lab,marker="o",color="navy")
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("Accuracy Rate (%)")

    plt.plot(mali,B_Accuracy,label=B_lab,linestyle='dashed',marker="x", color='maroon' )
    plt.xlabel("Number of Malicious UAVs (%)")
    plt.ylabel("Accuracy Rate (%)")
    #plt.legend(edgecolor="black")
    plt.legend(edgecolor="black",prop={'size': 12})
    plt.savefig('ACC.pdf')
    # f5 = plt.figure(5)
    # plt.plot(mali,Precision,label=lab,marker="o")
    # plt.xlabel("Num of Malicious UAVs %")
    # plt.ylabel("Precision Rate")
    # plt.legend()

    #f1 = plt.figure(1)
    #plt.plot(mali,detectedArray,label=lab,marker="o")
    #plt.xlabel("Num of Malicious UAVs %")
    #plt.ylabel("Detection Rate")
    #plt.legend()
    #f6 = plt.figure(5)
    #plt.plot(FPArray,FNArray,label=lab,marker="o")
    #plt.xlabel("Num of Malicious UAVs %")
    #plt.ylabel("ROC curve")
    #plt.legend()
    #detectedArray.clear()
    FPArray.clear()
    FNArray.clear()
    Accuracy.clear()
    Precision.clear()
    TruePositiveArray.clear()
    F1score.clear()
    TrueNegativeArray.clear()
    B_FPArray.clear()
    B_FNArray.clear()
    B_Accuracy.clear()
    B_Precision.clear()
    B_TruePositiveArray.clear()
    B_F1score.clear()


logfile.close()
plt.show()




