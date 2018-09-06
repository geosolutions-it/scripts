import random
import csv

#Requests number, file path inputs.

requests = int(input("Please enter the number of the Requests:"))
path = input("Please enter the Path of your workspace followed by the CSV filename:")


myfile = open(path, 'w')


#The while loop will generate randomly the following parameters for the WMS request: angle, width and height, bbox

count = 0
while (count <= requests):
        x_pt = random.randint(-18000000,18000000)
        y_pt = random.randint(-8000000,15000000)
        angle = random.randint(-360,360)
        width = random.randint(256,1024)
        height = width
        xmin_bbox = x_pt - random.randint(0,1000000)
        ymin_bbox = y_pt - (x_pt - xmin_bbox)
        xmax_bbox = x_pt + (x_pt - xmin_bbox)
        ymax_bbox = y_pt + (x_pt - xmin_bbox)
        myfile.write((str(angle) + ";" + str(width) + ";" + str(height) + ";" + str(xmin_bbox) + "," + str(ymin_bbox) + "," + str(xmax_bbox) + "," + str(ymax_bbox) + '\n'))
        count+=1


    
myfile.close()    
