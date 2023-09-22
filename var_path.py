# url
url_scorecard = 'https://www.espncricinfo.com/series/england-tour-of-australia-1876-77-61716/australia-vs-england-1st-test-62396/full-scorecard'
url_summary = 'https://www.espncricinfo.com/series/england-tour-of-australia-1876-77-61716/australia-vs-england-1st-test-62396/live-cricket-score'
url_espn = 'https://www.espncricinfo.com/'

# Necessary xpath
## summary score card url
ground_xp = '//td[@class="ds-min-w-max"]//a/span/text()'
season_xp = '//td[@class="ds-min-w-max ds-text-typo"]/a/span/text()'  # season[0]
country_xp = '//div[@class="ds-py-2 ds-px-3 ds-border-b ds-border-line ds-uppercase ds-flex ds-justify-between"]/div/strong/text()'
run_xp = '//div[@class="ds-py-2 ds-px-3 ds-border-b ds-border-line ds-uppercase ds-flex ds-justify-between"]/div/span/strong/text()'
over_xp = '//div[@class="ds-py-2 ds-px-3 ds-border-b ds-border-line ds-uppercase ds-flex ds-justify-between"]/div/span/span/text()'
inn_xp = '//div[@class="ds-py-2 ds-px-3 ds-border-b ds-border-line ds-uppercase ds-flex ds-justify-between"]/span/text()'
won_xp = '//div[@class="ds-w-full"]/p/span/text()'
summary_xp = [ground_xp, season_xp, country_xp, run_xp, over_xp, inn_xp, won_xp]

## path in score card url
day_play_xp = '//div[@class="ds-p-4"]/div/div/span[@class="ds-text-typo-mid3"]/text()'  # how many day of playing and detail in that day
match_flow_xp = '//div[@class="ReactCollapse--content"]//li/span/text()'   # detail about match flow, general or summary of the match
toss_xp = '//span[@class="ds-text-tight-s ds-font-regular"]/text()'  # who play first
match_detail = '//td/a/span/text()'
scorecard_xp = [day_play_xp, match_flow_xp, toss_xp, match_detail]

## path in in year series
team1_xp = '//td[@class="ds-min-w-max"]/span/text()'
team2_won_ground_xp = '//td[@class="ds-min-w-max ds-text-right"]/span/text()'
team_xp = '//div/table/tbody/tr/td/span/text()'
test_no_xp = '//span/a/span[contains(text(),"Test")]/text()'
# table_xp = '//div/table/tbody/tr'
# team1_2_xp = [team1_xp, team2_won_ground_xp]
team1_2_xp = [team_xp, test_no_xp]
