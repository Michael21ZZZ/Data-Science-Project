# -*- coding: utf-8 -*-
"""
Filename: group_15_easyapply_project.py
Group Memebers:
    George Zhang(zz3@andrew.cmu.edu)
    Michael Zhang(ruoyuzha@andrew.cmu.edu)
    Rebecca Zhang(weiyiz1@andrew.cmu.edu)
    Yu Zi(yuzi@andrew.cmu.edu)
    Yufei Zheng(yufeizhe@andrew.cmu.edu)
Import: qsrank,cost_of_living,weather,crime_rate
External Packages Used:
    pandas
    tabulate
    matplotlib.pyplot
Description:
    This file is the main file of the product. It loads the data from 4
    difference sources and asks users to choose from 2 functions. The first
    function is to search for some universities' information by entering
    some filters, like rank, living cost or cities and shows the detailed
    information about the universities. The second function is to compare
    directly 2 universities by entering the universities' name and shows
    the compared table and a graph.

"""

import module.qsrank as qs
import module.cost_of_living as cl
import module.weather as w
import module.crime_rate as cr
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt



# function1, filter query loop
def filter_loop(filt):
    answer = ''
    result = []
    state_result = []
    state_result_index = []
    city_result = []
    list_single_index =[]
    list_filt_index = []
    while answer == '':
        print('\n        Do you want to filter universities by '+filt+' ?\n')
        whether = input('        Enter Yes or No: ').strip()
        if whether.lower() == 'yes':
            if filt == 'rank':
                print('\n        Please enter the range of '+filt+' you prefer. The rank is between 1 and 177')
                result.append(input('        The starting '+filt+': ').strip())
                result.append(input('        The ending '+filt+': ').strip())
                answer = 'finish'

            elif filt == 'city':
                #Search the state first
                print('\n        To help you find the cities, please first enter the states you prefer. Example: MA for Massachusetts, CA for California.' )                
                state_result.append(input('\n        Please enter the abbreviation of the state name\n        (Use comma to separate multiple items.):').strip())
                state_result = [item.strip() for item in state_result[0].split(',')]
                state_result = [item.upper() for item in state_result] #upper case
                print('\n        Here are the cities in the states you choose. ')
                for i in range(len(state_result)):
                    item = state_result[i]
                    if  item in cost_of_living['State'].tolist():
                        state_result_index.extend(cost_of_living[cost_of_living.State == item].index.tolist()) #return the index list of cities in certain states
                    else:
                        print('\n        There is an invalid input!')

                #Search all the cities in these states
                city_filt_list =[cost_of_living.at[item, 'City'] for item in state_result_index]
                state_filt_list =[cost_of_living.at[item, 'State'] for item in state_result_index]
                list_filt= list(zip(city_filt_list, state_filt_list))
                list_filt_single = list(set(list_filt))
                for i in range(len(list_filt_single)):
                    print('        '+str(i)+' '+str(list_filt_single[i][0])+', '+str(list_filt_single[i][1]))

                #Let the user select the state
                list_single_index.append(input('\n        Please enter the number in front of city you are interested in:\n         (Use comma to separate multiple items.)').strip())
                list_single_index = [int(item.strip()) for item in list_single_index[0].split(',')]
                for item in list_single_index:
                    obj_city = list_filt_single[item][0]
                    obj_state = list_filt_single[item][1]
                    list_filt_index.extend(cost_of_living[(cost_of_living.State == obj_state) & (cost_of_living.City == obj_city)].index.tolist())
                result = list(set(list_filt_index).intersection(set(state_result_index)))
                answer = 'finish'

            elif filt == 'living expense':
                print('\n        Please enter the range of '+filt+' you prefer.\n        (Enter 4 for the highest 25% of living expense, 3 for 25%-50%, 2 for 50%-75%, and 1 for Lowest 25%)')
                result.append(input('        Your choice is '+filt+': ').strip())
                answer = 'finish'

        elif whether.lower() == 'no':
            if filt == 'rank':
                result = 0
            elif filt == 'city':
                result = 0
            elif filt == 'living expense':
                result = 0
            answer = 'finish'
        else:
            print('\n        Your input is invalid, please enter yes or no!\n')
    return result


# function2, compare and output the information of two universities
def get_compare_info(uni1, uni2):

  # Merge the cost of living data and crime rate together
    living_crime = pd.merge(cost_of_living, crime_rate, left_on = ['City','State'],right_on = ['cities','state'], how = 'left')
    living_crime = living_crime.rename(columns={'crime rate':'Crime Rate'})

    # get the cities of two universities
    rank1 = qs_rank.loc[qs_rank['Name']==uni1]
    rank2 = qs_rank.loc[qs_rank['Name']==uni2]
    city1 = rank1['City'].values[0]
    city2 = rank2['City'].values[0]

    # get the weather of two cities
    weather1 = weathers.loc[weathers['city']==city1]
    weather2 = weathers.loc[weathers['city']==city2]

    # change the format of the output table and print
    info = pd.concat([rank1,rank2]).iloc[:,0:rank1.shape[1]-1]
    info = pd.concat([info,living_crime['Crime Rate']],axis=1,join='inner')
    info = info.T
    print(tabulate(info, headers='firstrow',tablefmt='psql'))

    # show the image of teamperature curve of two cities
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aus','Sep','Oct','Nov','Dec']
    plt.plot(month,weather1['weathers'],'o-',color = 'g',label=uni1)
    plt.plot(month,weather2['weathers'],'o-',color = 'r',label=uni2)
    plt.title('Temperature Curve')
    plt.xlabel('Month')
    plt.ylabel('Centigrade')
    plt.figure(figsize=(10,20))
    plt.legend(loc='best')
    plt.show()






# begin of ui query
print('''
        Hi! Welcome to EasyApply!
        Our product provides reliable and free information about US undergraduate programs.''')

load_flag = ''
while not load_flag or load_flag not in 'YyNn' :
    load_flag = input('''
        It might take a long time to scrape the University Ranking data 
        from website. Do you want to load from local file instead ? (Y/N)''').strip()
    if load_flag not in 'YyNn':
        print("        Only Y or N is accepted")

web = True if load_flag in 'Nn' else False

# loading data from 4 different source
qs_rank = qs.load_data(from_web=web)
qs_rank.loc[qs_rank['City'] == 'New York City','City'] = 'New York'
cities = qs.get_cities(qs_rank)
cost_of_living = cl.load_data(cities)
crime_rate = cr.load_data()
weathers = w.load_data()

# enter the query loop
answer_main_menu = ''
while answer_main_menu != 'Q' and answer_main_menu != 'q':
    print('''
        Please select from this menu:

        1)    Search for some universities' information by entering some filters
        2)    Compare directly 2 universities by entering the universities' name
        Q)    Quit from this program.
        ''')

    answer_main_menu = input('        Your choice: ').strip()

    if answer_main_menu == '1':
           # function1
           filtered_index = []
           filtered_city_index = []
           filtered_rank_index = []
           filtered_cost_index = []

           # filter by rank
           rank_result = filter_loop('rank')
           if rank_result == 0:
               filtered_rank_index = list(range(len(qs_rank)))
           else:
               filtered_rank_index = list(range(int(rank_result[0])-1,int(rank_result[1])))

           # filtered by city
           city_result = filter_loop('city')
           if city_result == 0:
               filtered_city_index = list(range(len(qs_rank)))
           else:
               filtered_city_index = [item for item in city_result]

           # filter by living expense
           cost_result = filter_loop('living expense')
           Q1 = cost_of_living['Cost of Living Index'].quantile(0.25)
           Q2 = cost_of_living['Cost of Living Index'].quantile(0.5)
           Q3 = cost_of_living['Cost of Living Index'].quantile(0.75)
           cost_list = cost_of_living['Cost of Living Index'].tolist()
           if cost_result == ['1']:
               filtered_cost_index = [i for i in range(len(cost_list)) if cost_list[i] < Q1]
           elif cost_result == ['2']:
               filtered_cost_index = [i for i in range(len(cost_list)) if Q1 < cost_list[i] < Q2]
           elif cost_result == ['3']:
               filtered_cost_index = [i for i in range(len(cost_list)) if Q2 < cost_list[i] < Q3]
           elif cost_result == ['4']:
               filtered_cost_index = [i for i in range(len(cost_list)) if Q3 < cost_list[i]]
           else:
               filtered_cost_index = list(range(len(cost_list)))

            # Intersect the filtered index
           filtered_index = list(set(filtered_city_index).intersection(set(filtered_rank_index),set(filtered_cost_index)))
           if len(filtered_index) == 0:
               print('\n        Sorry, we cannot find any university. What about CMU? You would definitely love it! \n')
           else:
               for i in filtered_index:
                   i = int(i)
                   j = i + 1
                   print('\n        This is university ' + str(j) +': '+qs_rank.at[i,'Name'])
               # Detailed information
               print('\n        Want to see the detailed information? \n')
               whether = input('        Enter Yes or No. Type anything other than yes to quit: ').strip()
               if whether.lower() =='yes':
                   interested_index = int(input('        Just type the number before the university name. Your choice is: ').strip())-1
                   print('\n        Here is the detailed information:')
                   print('\n        Name:'+qs_rank.at[interested_index,'Name'])
                   print('\n        Locations:'+cost_of_living.at[interested_index,'City']+','+cost_of_living.at[interested_index, 'State'])
                   print('\n        Rank:'+str(interested_index+1))
                   print('\n        Private or Public:'+qs_rank.at[interested_index,'Status'])
                   print('\n        Research Output:'+qs_rank.at[interested_index,'Research Output'])
                   print('\n        Student to Faculty Ratio:'+str(qs_rank.at[interested_index,'Student/Faculty Ratio']))
                   print('\n        International Student Number:'+str(qs_rank.at[interested_index,'International Students']))
                   print('\n        Size:'+qs_rank.at[interested_index,'Size'])
                   print('\n        Cost of Living (100 is the average in United States):'+str(cost_of_living.at[interested_index,'Cost of Living Index']))
                   #Output weather in certain location
                   print('\n        The monthly average temperature in '+cost_of_living.at[interested_index,'City']+', '+cost_of_living.at[interested_index, 'State']+' in 2020 is:')
                   weather_dict = {'1/15/20':'Jan','2/15/20':'Feb','3/15/20':'Mar','4/15/20':'Apr','5/15/20':'May','6/15/20':'Jun',
                                   '7/15/20':'Jul','8/15/20':'Aug','9/15/20':'Sep','10/15/20':'Oct','11/15/20':'Nov','12/15/20':'Dec'}
                   weather = []
                   weathers['month']= weathers['date'].apply(lambda x: weather_dict[x])
                   weather_index = weathers[weathers.city == cost_of_living.at[interested_index,'City']].index.tolist()
                   weather_df = pd.DataFrame(columns = ['Month','Average Monthly Temperature in Celsius'])
                   for i in range(12):
                       item = weather_index[i]
                       weather_df.at[i,'Month'] = weathers.at[item,'month']
                       weather_df.at[i,'Average Monthly Temperature in Celsius'] = weathers.at[item,'weathers']
                   print(tabulate(weather_df, headers='keys', tablefmt ='psql'))
                   print('\n        Website:'+str(qs_rank.at[interested_index,'URL']))

    elif answer_main_menu == '2':
        #function2
        print('\n        Which two universities you want to compare?\n        (Please enter the exact full name of university)')
        uni1 = input('        First university: ').strip()
        uni2 = input('        Second university: ').strip()

        try:
            get_compare_info(uni1, uni2)
        except:
            print('No data of relevant schools was found, please re-enter')

    elif answer_main_menu == 'Q' or answer_main_menu == 'q': pass
    else:
        print('\n        Your choice is invalid, please enter a valid figure!\n')