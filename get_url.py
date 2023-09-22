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

##### get 
def get_specific_year(year):
    """
    get link that contain year and return list of year in between 

    do that later after getting all the data and model
    """
    year_link  = get_url_series_year()
    if year in year_link:
        pass


def get_url_scorecard_summary(year_link): 
    """
    year_link = link of each series(year) 
    choose the period of time from 
        year_link = get_url_series_year()
        year_link[1:100]
    
    return url_scorecacrd, url_summary
    (all in one list separately according to year_link)
    """

    url_espn = 'https://www.espncricinfo.com/'
    scorecard_xp = '//span/a[contains(@href, "/series/")]/@href'
    url_scorecard = []
    url_summary = []
    for year_url in year_link:
        # print(year_url)
        url = get_var_xpath(year_url, scorecard_xp)
        # print(url)
        for item in url:
            url_item = url_espn + item
            url_scorecard.append(url_item)

        summary_url = []
        for item in url:
            new_item = item.replace('full-scorecard', 'live-cricket-score')
            url_item = url_espn + new_item
            url_summary.append(url_item)

    return url_scorecard, url_summary


def main():
    """
    year_link = 133 links
    meaning >> 133 year series

    url_scorecard = 2515 links
    url_summary = 2515 links
    meaning >> 2515 test cards

    with ~65 seconds to create these lists
    """
    # print('this is main')

    year_link  = get_url_series_year()
    df_year = pd.DataFrame(year_link, columns =['year_link'])
    df_year.to_csv('url_year.csv', index=False)
    # print(year_link)
    url_scorecard, url_summary = get_url_scorecard_summary(year_link)

    df = pd.DataFrame(url_scorecard, columns =['scorecard'])
    df['summary'] = url_summary
    # print(df)
    df.to_csv('url_scorecard_summary.csv', index=False)


    # print(url_scorecard)
    # print(len(year_link))
    # print(len(url_scorecard))
    # print(len(url_summary))


if __name__ == "__main__":
    import time
    start_time = time.time()    

    main()
    print('main')

    print("--- %s seconds ---" % (time.time() - start_time))



