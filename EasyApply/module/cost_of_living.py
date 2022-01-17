# -*- coding: utf-8 -*-
"""
Filename: cost_of_living.py
Author: Michael Zhang(ruoyuzha@andrew.cmu.edu)
External Packages Used:
    pandas
    BeautifulSoup
    urlopen
    numpy
Description:
    This file includes the definition of load_data function, which is used
    to scrape the cost of living data from websites. The input of load_data
    function includes a list ('cities') and an url. The first input, 'cities',
    should be a list of names of US cities. The second input, 'url', should be 
    the website which this program scrape from. The out put of load_data function
    is a list of cost of living index for corresponding cities from the input.
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
from numpy import *
import pandas as pd
import numpy as np
#No warning
pd.options.mode.chained_assignment = None  # default='warn'

URL = "https://advisorsmith.com/data/coli/"

def load_data(cities, url = URL):
    locations = []
    cities = [item.strip() for item in cities]
    locations = list(set([item for item in cities]))
    #locations = [item for item in locations_txt]
    
    page = urlopen(URL)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    city = []
    state =[]
    col_index =[]
    for match in soup.find_all('td',class_='column-1'):
        city.append(match.text.strip())
    
    for match in soup.find_all('td',class_='column-2'):
        state.append(match.text.strip())
    
    for match in soup.find_all('td',class_='column-3'):
        col_index.append(match.text.strip())
    
    #There are some cities with the same name. Clarify the city name and state.
    Multiple_Dict={'Athens': 'GA','Portland': 'OR','Gainesville': 'FL', 'Bloomington': 'IN', 'Columbus': 'OH', 'Cleveland': 'OH',
     'Columbia': 'MO', 'Fayetteville': 'AR','Albany': 'NY','Rochester': 'NY', 'Burlington': 'VT','Auburn': 'AL','Richmond': 'VA'}
    Multiple_City=list(Multiple_Dict.keys())
    
    #There are some cities with no data point in advisorsmiths website. 
    #Manual Revison For locations and city names
    Manual_Old = [ 'Pasadena','Irving', 'New York City','Evanston','Berkeley','Cambridge','Washington D.C.','San Diego ']
    Manual_New = ['Los Angeles','Los Angeles','New York','Chicago','San Francisco','Boston','Washington', 'San Diego']
    Manual_Dict = dict(zip(Manual_Old, Manual_New))
    
    locations_new = []
    for i in range(len(locations)):
        if locations[i] in Manual_Old:
            locations_new.append(Manual_Dict[locations[i]])
        else:
            locations_new.append(locations[i])
    
    #Look up other null cities in city-state dictionary
    Null_City = [ ]  
    Null_City_Dict = {'Kent': 'WA','Williamsburg': 'VA','Houghton': 'MI', 'Richardson': 'TX', 'Princeton': 'FL', 'Northampton': 'MA', 'Irvine': 'CA', 'Pullman': 'WA', 'Waltham': 'MA', 'Clemson': 'SC', 'Davis': 'CA', 'Stony Brook': 'NY', 'West Hartford': 'CT', 'Hanover': 'MA', 'Golden': 'CO', 'Bethlehem': 'PA', 'Chapel Hill': 'NC', 'Hoboken': 'NJ', 'Denton': 'TX', 'Troy': 'OH', 'Boca Raton': 'FL', 'University Park': 'PA',
     'Rolla': 'MO','College Park': 'MD', 'Potsdam': 'NY', 'Storrs': 'CT', 'Newton': 'KS', 'Fairfax': 'VA', 'Newark': 'OH', 'Stanford': 'CA', 'New Brunswick': 'NJ', 'Starkville': 'MS', 'Oxford': 'MS', 'Arlington': 'WA', 'East Lansing': 'MI', 'Laramie': 'WY',
     'Norman': 'OK', 'Amherst': 'NY', 'West Lafayette': 'IN', 'Ashburn': 'VA', 'Santa Barbara': 'CA', 'Notre Dame': 'IN', 'Washington D.C.': 'DC'}
    
    for item in locations_new:
        if city.count(item)==0 and item not in Manual_Old:
            Null_City.append(item)
    
    #Build the output dataframe df1 with no duplicates
    df1 = pd.DataFrame({'City':locations})
    df1['State'] = 0
    df1['Cost of Living Index'] = 0
    
    for i in range(len(locations)):
        item = locations_new[i]
        if city.count(item)==0:
            df1['State'][i] = Null_City_Dict[item]
        if city.count(item)==1:
            df1['State'][i] = state[city.index(item)]
            df1['Cost of Living Index'][i] = float(col_index[city.index(item)])
        if city.count(item)>=2:
            df1['State'][i] = Multiple_Dict[item]
            city_index_pos = [ j for j in range(len(city)) if city[j] == item]
            state_index_pos = [ k for k in range(len(city)) if state[k] == Multiple_Dict[item]] 
            index_pos = [val for val in city_index_pos if val in state_index_pos]
            df1['Cost of Living Index'][i] = float(col_index[index_pos[0]])
    
    #For cities which couldn't be found in advisorsmith, use the state average to estimate the living expense
    Predicted_Index = []
    for item in Null_City_Dict.values():
        df2 = df1.loc[(df1['State'] == item)]    
        ls1 = df2['Cost of Living Index'].values.tolist()
        ls2 = [float(item) for item in ls1]
        list_non_zero = [i  for i in ls2 if i!= 0]
        if len(list_non_zero) > 0:
            Predicted_Index.append(mean(list_non_zero).round(1))
        else:
            if item == 'SC':
                Predicted_Index.append(88.50)
            elif item == 'NJ':
                Predicted_Index.append(88.40)
            elif item == 'MS':
                Predicted_Index.append(84.80)
            elif item == 'WY':
                Predicted_Index.append(98.10)
                
    Predicted_Index_Dict = dict(zip(Null_City_Dict.values(),Predicted_Index))
    
    for i in range(len(locations)):
        item = locations_new[i]
        if city.count(item)==0:
            df1['Cost of Living Index'][i] = Predicted_Index_Dict[df1['State'][i]]
    
    #The output table is df2, which includes duplicate items
    df2 = pd.DataFrame({'City':cities})
    df2['State'] = ''
    df2['Cost of Living Index'] = ''
    for i in range(len(df2)):
        for j in range(len(df1)):
            if df1.at[j,'City'] == df2.at[i,'City']:
                df2.at[i,'State'] = df1.at[j,'State']
                df2.at[i,'Cost of Living Index'] = df1.at[j,'Cost of Living Index']
            
    #df1 is the output table
    return df2.round(1)
