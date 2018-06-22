import random
import math
import csv

#Requests number, Resolution and file path inputs.

requests = int(input("Please enter the number of the Requests:"))
width = int(input("Please enter the width:"))
height = int(input("Please enter the height:"))
path = input("Please enter the Path of your workspace followed by the CSV filename:")

r_earth = 6373000
myfile = open(path, 'w')

#The following While loop will pick a random projection center and a point included in that specific
#projection in degrees. Then it will transform the coordinates of the point in meters using
#the equations of the orthographic projection. Finally, it will trace a random bbox centered at that point.     

count = 0
while (count <= requests):
    lat_proj = random.randint(-90, 90)
    long_proj = random.randint(-180, 180)
    lat_pt = random.randint(-90, 90)
    long_pt = random.randint(-180, 180)
     
    if math.sin(math.radians(lat_proj))*math.sin(math.radians(lat_pt)) + math.cos(math.radians(lat_proj))*math.cos(math.radians(lat_pt))*math.cos(math.radians(long_pt - long_proj))>=0:
        x_pt = r_earth*math.cos(math.radians(lat_pt))*math.sin(math.radians(long_pt - long_proj))
        y_pt = r_earth*(math.cos(math.radians(lat_proj))*math.sin(math.radians(lat_pt)) -
                    math.sin(math.radians(lat_proj))*math.cos(math.radians(lat_pt))*math.cos(math.radians(long_pt - long_proj)))
        print(x_pt,y_pt)
        print(long_proj,lat_proj)
        print(long_pt,lat_pt)
        
        xmin_bbox = x_pt - random.randint(500000,1000000)
        ymin_bbox = y_pt - (x_pt - xmin_bbox)
        xmax_bbox = x_pt + (x_pt - xmin_bbox)
        ymax_bbox = y_pt + (x_pt - xmin_bbox)
        myfile.write((str(long_proj) + ";" + str(lat_proj) + ";" + str(width) + ";" + str(height) + ";" + str(xmin_bbox) + "," + str(ymin_bbox) + "," + str(xmax_bbox) + "," + str(ymax_bbox) + '\n'))
        count+=1

    else:
        pass
    
myfile.close()    
