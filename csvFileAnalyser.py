import csv
fileName = "/home/test/IdeaProjects/ArduSim/target/2022-6-23_12-10-29 experiment_"
fileSuffix = "_path_test.csv"
numUAV = 5 

file_to_write = "/home/test/Desktop/uav_"
writer_suffix = ".csv"



for i in range(numUAV):
	f = fileName+str(i)+fileSuffix
	fw = open(file_to_write+str(i)+writer_suffix, mode="w")
	writer = csv.writer(fw, delimiter=',')
	with open(f) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    counter = 0
	    x1 = 0 
	    y1 = 0
	    line_count = 0  
	    lines_per_second = 0 
	    for row in csv_reader:
	    	if (line_count==0):
	    		line_count = 1 
	    		continue
	    	x = float(row[0])
	    	y = float(row[1])
	    	t = float(row[5])
	    	if (int(t)==counter):
	    		x1 = x1 + x 
	    		y1 = y1 + y 
	    		lines_per_second = lines_per_second + 1  
	    	else:
	    		if (lines_per_second == 0):
	    			lines_per_second = 1
	    		x1 = x1 / lines_per_second
	    		y1 = y1 / lines_per_second
	    		writer.writerow([x1,y1,counter])
	    		x1 = 0 
	    		y1 = 0
	    		counter = counter + 1 
	    		lines_per_second = 0 


