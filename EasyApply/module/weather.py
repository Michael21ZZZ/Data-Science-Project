#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 22:22:41 2021

@author: Weiyi
"""

import requests
import pandas as pd

# response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=832710f1afd34817a5122655210910&q=")

def load_data(from_api=False):
    return load_data_from_api() if from_api else load_data_from_file()

def load_data_from_api():

        cities = ["Cambridge, MA", "Stanford", "Pasadena", 'Chicago', 'Philadelphia', 'New Haven', 'Durham', 
                   'New York', 'Princeton', 'Ithaca', 'Ann Arbor', 'Baltimore', "Evanston", "Berkeley", "Los Angeles", 
                   'San Diego', 'Pittsburgh', 'Providence', 'Austin', 'Madison', 'Champaign', 'Seattle', 'Atlanta', 'Houston', 
                   "University Park", 'Chapel Hill', 'St. Louis', 'Boston', 'West Lafayette', 'Columbus', 'Davis',
                   'Santa Barbara', 'Rochester', 'East Lansing', "College Park", 'Cleveland', 'College Station', 
                         "Gainesville", 'Minneapolis', 'Hanover', 'Phoenix', 'Nashville', 'Notre Dame', 'Charlottesville', 
                         'Irvine', 'Amherst', 'Washington D.C.', 'Boulder', "New Brunswick", 'Tucson', 'Medford', 'Raleigh', 
                         'Bloomington', 'Miami', 'Honolulu', 'Blacksburg', 'Santa Cruz', 'Ashburn', 'Salt Lake City', 'Storrs', 
                         'Stony Brook', 'Lawrence', 'Buffalo', 'Riverside', 'Denver', 'Pullman', 'Winston-Salem', 'Fort Collins', 
                         "Troy", 'New Orleans', 'Waltham', 'Iowa City', "Golden", "Tallahassee", 'Columbia', 'Richardson', 'Newton',                  'Ames', 'Rolla', 'Detroit', 'Bethlehem', 'Corvallis', 'Newark', 'Athens', 'Knoxville', 'Lincoln', 'Tampa', 
                         'Worcester', 'Northampton', 'Cincinnati', 'Williamsburg', 'Houghton', 'Syracuse', 
                         'Lexington', 'Albuquerquel' 'Norman', 'Eugene', 'Burlington', 'Hoboken', 'Richmond', 'Potsdam', 'Albany',
                         'Orlando', 'Auburn', 'Binghamton', 'Clemson', 'Fairfax', 'Indianapolis', 'Manhattan', 'Baton Rouge', 
                         'Stillwater', 'Dallas', 'Lubbock', 'Tuscaloosa', 'West Hartford', 'Oxford', 'Kansas City', 'San Antonio',
                         'Tulsa', 'Milwaukee', 'Laramie', 'Morgantown', 'Waco', 'Provo', 'Boca Raton', 'Kent', 'Starkville', 
                         'Flagstaff', 'Portland', 'Arlington', 'Fayetteville', 'Missoula', 'Charlotte', 'Denton', 'Kingston, NY',
                         'San Francisco', 'Mobile', 'El Paso', 'Stockton', 'Logan', 'Kalamazoo', 'Terre Haute']     

        dates = ["2020-01-15", "2020-02-15", "2020-03-15", "2020-04-15", "2020-05-15", "2020-06-15",
                 "2020-07-15", "2020-08-15", "2020-09-15", "2020-10-15", "2020-11-15", "2020-12-15"]        

        city_records = []
        date_records = []
        weathers = []

        for city in cities:
            for date in dates:
                response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=832710f1afd34817a5122655210910&q="
                             + city + "&format=json&date=" + date)

                city_records.append(city.split(',')[0].strip())
                date_records.append(date)
                weather = int(response.json().get('data').get("weather")[0]["avgtempC"])
                weathers.append(weather)


        weather_df = pd.DataFrame({'city': city_records,
                                  'date': date_records,
                                  'weathers' : weathers})
        return weather_df

def load_data_from_file():
    return pd.read_csv('./data/weather.csv')
