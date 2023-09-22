import requests
# from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree, html
import numpy as np
import var_path
from selenium import webdriver
from itertools import islice
import string

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

######## 1 get list of year-series link
def get_url_series_year():
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
    year_link = get_var_xpath(url_list_year, xpath_get_attr)

    series_year_url_list = []
    # year_list = []
    for item in year_link:
        year_url = url_espn + item
        series_year_url_list.append(year_url)
        # print(series_year_url_list)
        year_url = (years, series_year_url_list)
        # print(year_url)
        # year_list.append(year_url)
    
    # year_list = merge(years, series_year_url_list)
    # print(year_list)

    year_dict = dict(zip(years, series_year_url_list))

    return year_dict, series_year_url_list
    # return year_list
# print(len(series_year_url_list))

######## 2 get list of test matches number
test_url = 'https://www.espncricinfo.com/records/year/team-match-results/1953-1953/test-matches-1'

test_xp = '//a[contains(@href, "/series/")]/@href'
test_year = get_var_xpath(test_url, test_xp)

# yr = 'https://www.espncricinfo.com//records/year/team-match-results/1877-1877/test-matches-1'
# xp = '//span/a[contains(@href, "/series/")]/@href'
# result = get_var_xpath(yr, xp)
# print(result)
# print(len(result))



def get_url_scorecard_summary(n_items):
    """
    n_items is a list of tuple that contains (year, link_of_year) by n years
    """
    url_scorecard_all = []
    url_summary_all = []
    link_match_dict = {}
    for k,v in n_items:
        scorecard_xp = '//span/a[contains(@href, "/series/")]/@href'
        scorecard_url = get_var_xpath(v, scorecard_xp)
        for item in scorecard_url:
            url_scorecard_all.append(item)
        summary_url = []
        for item in scorecard_url:
            new_item = item.replace('full-scorecard', 'live-cricket-score')
            summary_url.append(new_item)
            url_summary_all.append(new_item)
        # print(test_year)
        link_match_dict[k] = {'url_year': v, 'url_scorecards': scorecard_url, 'url_summary': summary_url}

    # print(url_summary_all)

    return link_match_dict, url_scorecard_all, url_summary_all

# link_match_dict, url_scorecard_all, url_summary_all = get_url_scorecard_summary(n_items)
# print(url_scorecard_all)

def main():
    year_dict, url_year_list = get_url_series_year()
    # print(url_year_list)
    df_year = pd.DataFrame(url_year_list, columns =['year_link'])
    df_year.to_csv('url_year.csv', index=False)


    n_items = take(20, year_dict.items())
    # print(type(n_items))
    # print(n_items)

    # year = get_url_series_year()
    # # print(year) 
    # print('main')






if __name__ == "__main__":
    main()