import requests
import pandas as pd
from lxml import etree, html
import numpy as np
import var_path
import re
import get_url
import time 


def get_df():
    df = pd.read_csv('url_scorecard_summary.csv')
    df_year = pd.read_csv('url_year.csv')

    # list of year, range of needed url
    year_df = df_year.iloc[125:133, 0]
    list_year = list(year_df)

    # list scorecard
    score_df = df.iloc[2196:2515, 0]
    list_score = list(score_df)

    # list summary
    summary_df = df.iloc[2196:2515, 1]
    list_summary = list(summary_df)

    return list_year, list_summary, list_score 

def get_var_xpath(url, item_list):
    """
    url = url of that page
    item_list = list of xpath that you want to get in that page
    """
    page = requests.get(url)
    tree = html.fromstring(page.content)
    # var = tree.xpath(var_xpath)
    variables = []
    for item in item_list:
        var = tree.xpath(item)
        variables.append(var)

    return variables

def extract_run(runsandout):
    for i in runsandout:
        if i.isnumeric() == False:
            runsandout.remove(i)
    runs = []
    for item in runsandout:
        item = int(item)
        if item > 10:
            runs.append((item))

    return runs

def extract_over(input):
    old_overs = [item for item in input if item not in ('(', ')')]
    # print(old_overs)
    overs_list = []
    for item in old_overs:
        word = item.split(' ')
        overs_list.append(word)

    overs = []
    for item in overs_list:
        overs.append(item[0])

    return overs

## with year link
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

def get_summary_info(list_url):
    df_result = pd.DataFrame()

    for url in list_url:
        try:
            result_sum = get_var_xpath(url, var_path.summary_xp)
            grounds = result_sum[0]
            ground = grounds[0].split(' ')

            #runs 
            runs_out = result_sum[3]
            runs_all = extract_run(runs_out)

            over_input = result_sum[4]
            overs = extract_over(over_input)

            # print(runs_all, url)
            if len(runs_all) > 1:
                runs = [runs_all[0], runs_all[1]]
                ## run
                team1_runs_inn1 = [runs_all[0], 0]
                team2_runs_inn1 = [0, runs_all[1]]
                if len(runs_all) > 3:
                    team1_runs_inn2 = [runs_all[2], 0]
                    team2_runs_inn2 = [0, runs_all[3]]
                elif len(runs_all) > 2:
                    team1_runs_inn2 = [runs_all[2], 0]
                    team2_runs_inn2 = [0, 0]
                else:
                    team1_runs_inn2 = [0, 0]
                    team2_runs_inn2 = [0, 0]
                ## over
                team1_inn1_over = overs[0]
                team2_inn1_over = overs[1]

                overs = [overs[0], overs[1]]
                innings = [result_sum[5][0], result_sum[5][1]]
                countries = [result_sum[2][0], result_sum[2][1]]
            
            else:
                try:
                    runs = [runs_all[0], 0]
                except IndexError:
                    runs = [None, None]
                
                team1_inn1_over = overs[0]
                team2_inn1_over = 0
                overs = [overs[0], 0]
                innings = result_sum[5][0]
                countries = [result_sum[2][0], None]
            
            # else:
            #     runs = [None, None]
            #     team1_inn1_over = overs[0]
            #     team2_inn1_over = 0
            #     overs = [overs[0], 0]
            #     innings = result_sum[5][0]
            #     countries = [result_sum[2][0], None]

            scorecard_no = result_sum[1][1].replace('no.', '#')
            
            # country and innings
            inns = [inn.replace('INNINGS', '') for inn in result_sum[5]]
            count_inn = []
            for c, i in zip(result_sum[2], inns):
                combined = c + ' ' + i
                count_inn.append(combined.strip())
            country_inn_testno = [item+' '+result_sum[1][1] for item in count_inn]
            
            # run for each team in inning 1
            # print(runs_all, url)
            # team1_runs_inn1 = [runs_all[0], 0]
            # team2_runs_inn1 = [0, runs_all[1]]
            # # print(runs_all)
            
            # if len(runs_all) > 3:
            #     team1_runs_inn2 = [runs_all[2], 0]
            #     team2_runs_inn2 = [0, runs_all[3]]
            # else:
            #     team1_runs_inn2 = [runs_all[2], 0]
            #     team2_runs_inn2 = [0, 0]
            
            # first inn lead another team
            try:
                first_inn_lead_team1 = [runs[0] - runs[1], -(runs[0] - runs[1])]
            except TypeError:
                first_inn_lead_team1 = [None, None]

            dict_match_detail = {'ground': ground[0],
                            'season': result_sum[1][0],
                            'scorecard_no': scorecard_no,
                            'countries': countries,
                            'runs': runs,
                            'overs': overs,
                            'innings': innings,
                            'team1_inn1': team1_runs_inn1,
                            'team2_inn1': team2_runs_inn1,
                            'first_inn_lead_of_team1': first_inn_lead_team1,
                            'team1_inn2': team1_runs_inn2,
                            'team2_inn2': team2_runs_inn2,
                            'team1_inn1_over': [team1_inn1_over,0],
                            'team2_inn1_over': [0, team2_inn1_over]
                            }


            df_dict = pd.DataFrame(dict_match_detail)

            df_result = pd.concat([df_result, df_dict], ignore_index=True)
        except IndexError:
            pass
        # df_result = df_result[df_result['innings'] == '1st INNINGS']
        # print(df_result)

    return df_result

def get_scorecard_info(list_score):
    df_result = pd.DataFrame()
    for url in list_score:
        try:
            result_sum = get_var_xpath(url, var_path.scorecard_xp)
            # print(result_sum)
            # print(url)
            test_no = result_sum[3][2]
            # print(test_no, url)
            scorecard_no = test_no.replace('no.', '#')

            day_result = result_sum[0]

            # innings play on what day. like 1st inning play day 1, day 2, day 3
            day_ea = []
            day_country = []
            for day in day_result:
                day1 = re.split('-|innings', day)
                day2 = day1[0:2]
                if 'rest' in day2[0]:
                    pass
                else:
                    day_ea.append(day2[0])
                    day_country.append(day2[1].strip())
            innings = []
            for item in day_country:
                # print(item)
                split = item.split()
                # print(split)
                if split[-1] == '1st' or split[-1] == '2nd':
                    inns =  split[-1] + ' INNINGS'
                else:
                    inns = 'no play'
                innings.append(inns)
            # print(innings, url)

            # innings = []
            # for item in day_country:
            #     split = item.split()
            #     inns = split[1] + ' INNINGS'
            #     # print(inns)
            #     innings.append(inns)

            country_inn_testno = [item+' '+test_no for item in day_country]

            total_day = len(day_result)
            # print(total_day)
            rest = [] # 1 = the day that they rest before thier inning
            for i in range(len(day_result)):
                if 'rest' in day_result[i]:
                    rest_day = i+1
                    rest.append(1)
                else:
                    rest.append(0)
            if 1 in rest:
                rest.pop()

            toss_result = result_sum[2]
            country_bat_first = 0
            country_field_first = 0
            for toss in toss_result:
                # print(toss)
                if 'bat' in toss:
                    bat_first = re.split(',', toss)
                    country_bat_first = bat_first[0]
                elif 'field' in toss:
                    field_first = re.split(',', toss)
                    country_field_first = field_first[0]

            dict_match_detail = { #'rest_day': rest,
                                'total_day': total_day,
                                'bat_first': country_bat_first,
                                'field_first': country_field_first,
                                #  'country_inn_testno': country_inn_testno,
                                #  'day_of_play': day_ea,
                                'innings': ['1st INNINGS', '1st INNINGS'],
                                'scorecard_no': scorecard_no
                                }

            try:
                df_dict = pd.DataFrame(dict_match_detail)

                df_result = pd.concat([df_result, df_dict], ignore_index=True)
            except ValueError:
                pass
        except IndexError:
            pass

    return df_result


def main():
    start_time = time.time()    
    list_year, list_summary, list_scorecard = get_df()

    #### get info from year link
    print('df_from_year')
    df_from_year = get_sum_from_year_series(list_year)
    print("--- %s seconds ---" % (time.time() - start_time))

    #### get info from summary
    print('df_summary')
    df_summary = get_summary_info(list_summary)
    print("--- %s seconds ---" % (time.time() - start_time))
    # df_summary.to_csv('df_summary4_23sept.csv', encoding='utf-8')

    #### get info from scorecard
    print('df_scorecard')
    df_scorecard = get_scorecard_info(list_scorecard)
    print("--- %s seconds ---" % (time.time() - start_time))

    #### merge summary and scorecard
    print('df_summ_score')
    df_summ_score = pd.merge(df_summary, df_scorecard, how='inner', 
                     left_on=['scorecard_no'],
                     right_on=['scorecard_no']).drop_duplicates()
    print("--- %s seconds ---" % (time.time() - start_time))

    #### merge summary_score and df from year
    print('df_result')
    df_result = pd.merge(df_summ_score, df_from_year, how='inner', 
                     left_on=['scorecard_no', 'countries'],
                     right_on=['scorecard_no', 'countries' ]).drop_duplicates()
    print("--- %s seconds ---" % (time.time() - start_time))
    
    #### convert from df to csv
    print('df_result.csv')
    df_result.to_csv('df_result_5_23sept.csv', encoding='utf-8')
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
    main()