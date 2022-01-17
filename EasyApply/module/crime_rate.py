import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
import requests

def get_state(x):
    return x.split(',')[1].split()[0]


def transform(s):
    if s == '':
        return 0
    else:
        return int(s.replace(',', ''))

URL = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-6'

def load_data(url=URL, ):
    soup = BeautifulSoup(requests.get(url).text, features="lxml")

    def get_header(tr):
        items = []
        for th in tr.find_all('th'):
            items.append(th.text.strip())
        return items

    def get_item(tr):
        items = [tr.find('th').text.strip()]
        for td in tr.find_all('td'):
            items.append(td.text.strip())
        return items

    header = get_header(soup.find('thead'))

    all_tr = soup.find_all('tr')
    datas = [get_item(tr) for i, tr in enumerate(all_tr[1:])]

    clean_datas = []
    for item in datas:
        L = [x for x in item if len(x) > 0]
        if len(L) == 2 :
            area = L[0]
        else:
            clean_item = [area] + item
            clean_datas.append(clean_item)

    city_datas = []
    for item in clean_datas:
        city = item[1]
        if city.startswith('City'):
            item[1] = city[8:]
            city_datas.append(item)
        


    city_df = pd.DataFrame(city_datas, columns=header)
    for col in city_df.columns[2:]:
        city_df[col] = city_df[col].apply(transform)

    city_df['crime rate']  = city_df.iloc[:,4:].sum(axis = 1) / city_df['Population']
    city_df['Metropolitan Statistical Area'] = city_df['Metropolitan Statistical Area'].apply(get_state)
    city_df.columns = ['state', 'cities',
           'Population', 'Violentcrime', 'Murder andnonnegligentmanslaughter',
           'Rape1', 'Robbery', 'Aggravatedassault', 'Propertycrime', 'Burglary',
           'Larceny-theft', 'Motorvehicletheft', 'crime rate']

    city_df['crime rate'] = city_df.iloc[:,4:].sum(axis = 1) / city_df['Population']

    return city_df
