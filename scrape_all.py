import requests
# from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree, html
import numpy as np
import var_path
from selenium import webdriver
from itertools import islice
import string

##### general functions

# 1. get var from list of xpath
def get_var_xpath_from_list(url, item_list):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    # var = tree.xpath(var_xpath)
    variables = []
    for item in item_list:
        var = tree.xpath(item)
        variables.append(var)

    return variables

def get_var_xpath(url, xpath):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    var = tree.xpath(xpath)

    return var

def take(n, iterable):
    """ return n index of dictionary"""
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

def merge(list1, list2):
 
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
     
    return merged_list



##### specific functions
def get_url_series_year():
    """
    year_link = link of each series(year) 
    i.e. series 1877-2023

    select period of year in this def

    want to have 100 year 

    choose >> year_link[0:100] 

    all year = 133 years
    """

    url_list_year = 'https://www.espncricinfo.com/records/list-of-match-results-by-year-307847'
    url_espn = 'https://www.espncricinfo.com/'
    x_path_list_year = '//a[contains(@href,"/records/year/team-match-results")]/span/text()'
    xpath_get_attr = '//div[@class="ds-mb-6"]/a/@href'

    page = requests.get(url_list_year)
    tree = html.fromstring(page.content)
    var = tree.xpath(x_path_list_year)
    # print(var)

    years = get_var_xpath(url_list_year, x_path_list_year)
    # print(len(years))
    link = get_var_xpath(url_list_year, xpath_get_attr)
    # print(year_link)
    year_link = []
    for item in link:
        url = url_espn + item
        year_link.append(url)

    return year_link

year_link = get_url_series_year()
# print(year_link)

url_year = ['https://www.espncricinfo.com//records/year/team-match-results/1877-1877/test-matches-1']
def get_sum_from_year_series(url_list):
    df_result = pd.DataFrame()

    for url in url_list:
        var = get_var_xpath(url, var_path.team1_2_xp)
        # print(var)
        info_list_ea_year = []

        for i, item in enumerate(var[1]):
            if item.startswith('Test #'):
                sublist = var[0][i * 5:(i + 1) * 5]
                sublist.append(item)
                info_list_ea_year.append(sublist)

        # print(info_list_ea_year)
        for item in info_list_ea_year:
            # print(item)
            countries = [item[0], item[1]]
            country_won = item[2]
            scorecard_no = item[-1]
            won = []    # won=1, lose=0, drawn=2
            if country_won == countries[0]:
                won = [1,0]
            elif country_won == 'drawn':
                won = [2,2]
            else:
                won = [0,1]

            # print(won)


            dict_match_detail = {'countries': countries,
                                'team_no': [1,2],
                                'scorecard_no': scorecard_no,
                                'country_won': country_won,
                                'won': won
                                }

            df_dict = pd.DataFrame(dict_match_detail)

            df_result = pd.concat([df_result, df_dict], ignore_index=True)

    return df_result

df_from_year = get_sum_from_year_series(url_year)
df_from_year