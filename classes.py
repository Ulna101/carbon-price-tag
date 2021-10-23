# classes.py
#from geopy.distance import geodesic
#import pandas as pd
"""Calculating total carbon cost
Read two separate excel spreadsheets to calculate the total carbon cost for a preset list of classifications.
Classifications include:
    1) object type
    2) object material
    3) distance
    4) mode
"""

class obj_type:
    pass
class obj_material:
    pass
class distance:
    pass
class mode:
    pass
#create a preset dictionary
list = {obj_type: " ", obj_material: " ", mode: " ", origin: " ", destination: " "}

#capture file path
file_1 = pd.read_excel (r'C:\Users\user\Desktop\file_1.xlsx')
file_2 = pd.read_excel (r'C:\Users\user\Desktop\file_2.xlsx')

#function takes in an origin and destination
#both origin and destination are lists: origin = (22.5726, 88.3639), destination = (28.7041, 77.1025)
def calculate_distance(origin, destination):
    kilometers = geodesic(origin, destination).km 
    miles = (0.621371) * kilometers #convert to miles
    return miles



if __name__ == "__main__":
    #do some function
    pass
