# classes.py
from typing import ItemsView
import geopy
from geopy.distance import geodesic
from geopy import distance
# from geopy.geocoders import GoogleV3 --- this would improve quality of life
import os
import pandas as pd
import sys
import numpy as np
"""Calculating total carbon cost
Read two separate excel spreadsheets to calculate the total carbon cost for a preset list of classifications.
Classifications include:
    1) object type
    2) object material
    3) distance
    4) mode
"""
#capture file path
memo = {}

module_dir = os.path.dirname(__file__)
carbon_item_data = pd.read_excel(module_dir + '/static/item.xlsx')
transport_carbon_data = pd.read_excel(module_dir + '/static/transport.xlsx')

GEOLOCATOR = geopy.geocoders.Nominatim(user_agent="carbon-tag")

def data_headings():
    def get_tuples(dict, key):
        return  [(s, s.capitalize()) for s in dict[key].unique()]
    return {'item': get_tuples(carbon_item_data, 'item'), 
            'material': get_tuples(carbon_item_data, 'material'), 
            'transport': get_tuples(transport_carbon_data, 'method')}

def avarage_cost(item):
    all_items = carbon_item_data[(carbon_item_data['item'] == item)]
    return round(np.average(all_items['carbon']))
    
def carbon_cost(dict):
    dist = calculate_distance(dict["origin"], dict["destination"])
    carbon = get_carbon(dict["item"], dict["material"])
    method = get_method(dict["transport"])
    return round(calculate_carbon(dist, carbon, method))

def get_carbon(item, mat):
    #get appropriate DataFrames for each excel file
    data_df = carbon_item_data

    carbon = data_df[(data_df['item'] == item) & (data_df['material'] == mat)]['carbon'].iloc[0]
    return carbon

def get_method(transport):
    method_df = transport_carbon_data

    #calculate appropriate variables
    mode = method_df[method_df['method'] == transport]['carbon per mile'].iloc[0]
    return mode

#calculate the distance from an origin to a destination
def calculate_distance(origin, destination):
    
    def get_loc(loc_name):
        if loc_name in memo: memo[loc_name]
        else: memo[loc_name] = GEOLOCATOR.geocode(loc_name)
        location = memo[loc_name]
        return (location.latitude, location.longitude)
    
    kilometers = geodesic(get_loc(origin), get_loc(destination)).km 
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
    item = sys.argv[1] #item
    mat = sys.argv[2] #material
    method = sys.argv[3] #method of transportation
    #num4 = sys.argv[4] #latitude
    #num5 = sys.argv[5] #longitude

    # #get appropriate DataFrames for each excel file
    # data = [['cotton', 't-shirt', 2177], ['cotton', 'dress', 5000]] #CHANGE THIS
    # data_df = pd.DataFrame(data, columns = ['Fiber Type','Item','Carbon'])
    # #create dataframe for method
    # method = [['boat', 5], ['plane', 16]] #CHANGE THIS
    # method_df = pd.DataFrame(method, columns = ['Method', 'CPM'])
    # #calculate appropriate variables
    # carbon = data_df.loc[data_df['Fiber Type'] == num1].loc[data_df['Item'] == num2].at[0, 'Carbon']
    # mode = method_df.loc[method_df['Method'] == num3].at[0, 'CPM']

    carbon = get_carbon(item, mat)
    mode = get_method(method)

    ###MAKE APPROPRIATE CHANGES IF USING GEOLOCATOR###
    ###uncomment lines 60-63
    # loc1 = geolocator.geocode(num1)
    # loc2 = geolocator.geocode(num2)
    # a = (loc1.latitude, loc2.longitude)
    # b = (loc2.latitude, loc2.longitude)
    #destination preset to Shanghai and New York City
    direction = [[(31.2304, 121.4737), (40.7128, 74.0060)]] 
    direction_df = pd.DataFrame(direction, columns = ['Origin', 'Destination'], index=None)
    distance = calculate_distance("Shanghai", "New York City")
    #final calculation
    print(carbon)
    print('Carbon: {0}'.format(round(calculate_carbon(distance, carbon, mode))))
