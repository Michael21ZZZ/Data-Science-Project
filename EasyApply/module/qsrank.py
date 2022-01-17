#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: qsrank.py
Group Memebers:
    George Zhang(zz3@andrew.cmu.edu)
    Michael Zhang(ruoyuzha@andrew.cmu.edu)
    Rebecca Zhang(weiyiz1@andrew.cmu.edu)
    Yu Zi(yuzi@andrew.cmu.edu)
    Yufei Zheng(yufeizhe@andrew.cmu.edu)
Imported By: project_ui.py
External Packages Used:
    selenium
    pandas
    bs4
Description:
    This file scrape University Rankings and details for each university
    from QS Rank, and load the data into a panda DataFrame. Since it takes
    a long time to load all data. An default behavior is set to load from
    local file.
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


def load_data(from_web=False):
    return load_data_from_scraping() if from_web else load_data_from_file()

def get_cities(data):
    return list(data['City'])
    
def load_data_from_scraping():
    chrome_driver = '/Users/ZHANGRY/Desktop/Project/EasyApply/chromedriver.exe'

    # Add user-agent info to access QS website
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'

    opts = Options()
    opts.add_argument("user-agent={}".format(ua))

    # Open the page
    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
    driver.get('https://www.topuniversities.com/university-rankings/world-university-rankings/2022')

    ranks = []
    def parse_data_in_table():
        locations = [x.text for x in driver.find_elements_by_xpath(
            '//div[@class="university-rank-row  "]//div[@class="location "]')]
        name_and_urls = [
            (x.get_attribute('href'), x.text) for x in driver.find_elements_by_xpath(
                '//div[@class="university-rank-row  "]//div[@class="td-wrap"]/a')]
        for loc, (url, name) in zip(locations, name_and_urls):
            # Include US Universities only
            if ',' not in loc: continue
            city, country = loc.rsplit(',', 1)
            if country != 'United States': continue
            ranks.append((name, city, url))

    def parse_data_in_university_page(url, cols):
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        infos = soup.find('div', {'class': 'uni_info'}).ul
        res = {col: '' for col in cols}
        for li in infos.children:
            col_name = li.find('span', {'class': 'info-heading'}).text
            col_value = li.find('span', {'class': 'info-setails'}).text
            
            # Only check for the required statistic fields.
            if col_name in res:
                res[col_name] = col_value
        return res

    # Click Agree for cookie policy
    time.sleep(6)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='btn btn-orrange agree-button eu-cookie-compliance-default-button']"))).click()

    # Maximize window to avoid click on hover items
    driver.maximize_window()
    time.sleep(2) #wait for the cookie window to fade off

    # Keep parse talbe items and click next to navigate to the next page
    while True:
        time.sleep(2)
        try:
            parse_data_in_table()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='page-link next']")
                )).click()
        except Exception as e:
            print(e)
            break
    
    col_names = ['Status', 'Research Output', 'Student/Faculty Ratio',
                 'Scholarships', 'International Students', 'Size', 'Total Faculty']
    records = []
    for name, city, url in ranks:
        records.append(
            {'Name': name, 'City': city, 'URL': url,
             **parse_data_in_university_page(url, col_names)})

    for r in records:
        for k in r:
            r[k] = r[k].strip() if r[k] else r[k]

    return pd.DataFrame(records)

def load_data_from_file():
    # Read the university infos from existing csv file
    return pd.read_csv('data/university_statistics.csv', delimiter='\t')
