# classes.py
import geopy
from geopy.distance import geodesic
from geopy import distance
# from geopy.geocoders import GoogleV3 --- this would improve quality of life
import os
import pandas as pd
import sys

"""Calculating total carbon cost
Read two separate excel spreadsheets to calculate the total carbon cost for a preset list of classifications.
Classifications include:
    1) object type
    2) object material
    3) distance
    4) mode
"""
#capture file path

# module_dir = os.path.dirname(__file__)
# carbon_item_data = pd.read_excel(module_dir + '/static/item.xlsx')
# transport_carbon_data = pd.read_excel(module_dir + '/static/transport.xlsx')

GEOLOCATOR = geopy.geocoders.Nominatim(user_agent="carbon-tag")

def carbon_cost(dict):
    orig = get_loc(dict["origin"])
    dest = get_loc(dict["destination"])
    dist = calculate_distance(orig, dest)
    carbon = get_carbon(dict["material"], dict["item"])
    method = get_method(dict["transport"])
    return round(calculate_carbon(dist, carbon, method), 3)


def get_loc(loc_name):
    location = GEOLOCATOR.geocode(loc_name)
    return (location.latitude, location.longitude)

# TODO: look on excel spreadsheets to see these valeus
def get_carbon(mat, item):
    #get appropriate DataFrames for each excel file
    data = [['cotton', 't-shirt', 2177], ['cotton', 'dress', 5000]] #CHANGE THIS
    data_df = pd.DataFrame(data, columns = ['Fiber Type','Item','Carbon'])
    
    carbon = data_df[(data_df['Fiber Type'] == mat) & (data_df['Item'] == item)]['Carbon'].iloc[0]

    return carbon

def get_method(transport):
    method = [['boat', 5], ['plane', 16]] #CHANGE THIS
    method_df = pd.DataFrame(method, columns = ['Method', 'CPM'])

    #calculate appropriate variables
    mode = method_df[method_df['Method'] == transport]['CPM'].iloc[0]
    return mode

#calculate the distance from an origin to a destination
def calculate_distance(origin, destination):
    kilometers = geodesic(origin, destination).km 
    miles = (0.621371) * kilometers #convert to miles
    return miles

#calculate the carbon usage
def calculate_carbon(dist, carbon, mode):
    total_carbon = carbon + dist * mode
    return total_carbon

#we have a library with the geopy indicator, but it costs money. we are assuming that you are going to give us the longitude
#and latitude but there is a quality of life feature you can also use which is commented out.
#all you have to do is input...geolocator = GoogleV3()
if __name__ == "__main__":
    #Input 3 arguments (5 if library geolocator is used)
    num1 = sys.argv[1] #fiber type
    num2 = sys.argv[2] #item
    num3 = sys.argv[3] #method of transportation
    #num4 = sys.argv[4] #latitude
    #num5 = sys.argv[5] #longitude
    #get appropriate DataFrames for each excel file
    data = [['cotton', 't-shirt', 2177], ['cotton', 'dress', 5000]] #CHANGE THIS
    data_df = pd.DataFrame(data, columns = ['Fiber Type','Item','Carbon'])
    #create dataframe for method
    method = [['boat', 5], ['plane', 16]] #CHANGE THIS
    method_df = pd.DataFrame(method, columns = ['Method', 'CPM'])
    #calculate appropriate variables
    carbon = data_df.loc[data_df['Fiber Type'] == num1].loc[data_df['Item'] == num2].at[0, 'Carbon']
    mode = method_df.loc[method_df['Method'] == num3].at[0, 'CPM']
    ###MAKE APPROPRIATE CHANGES IF USING GEOLOCATOR###
    ###uncomment lines 60-63
    # loc1 = geolocator.geocode(num1)
    # loc2 = geolocator.geocode(num2)
    # a = (loc1.latitude, loc2.longitude)
    # b = (loc2.latitude, loc2.longitude)
    #destination preset to Shanghai and New York City
    direction = [[(31.2304, 121.4737), (40.7128, 74.0060)]] 
    direction_df = pd.DataFrame(direction, columns = ['Origin', 'Destination'], index=None)
    distance = calculate_distance(direction_df.at[0, "Origin"], direction_df.at[0, "Destination"])
    #final calculation
    print('Carbon: {0}'.format(round(calculate_carbon(distance, carbon, mode))))
