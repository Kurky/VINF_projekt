from selenium import webdriver
import re
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.keys import Keys
import pandas as pd


def getNumberOfPages(driver):
    numberOfPages = 76
    WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, 'sc-feUZmu')))
    rendered_html = driver.page_source
    match = re.search(r'<input type="number" min="1" max="(\d+)" class="sc-feUZmu dhSqUd"', rendered_html)
    if match:
        numberOfPages = match.group(1)

    return numberOfPages


def getPlayerIds(driver, pageNumber):
    players = {}
    WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, 'td-fixed-last')))
    rendered_html = driver.page_source
    f = open("data/rawHTML/listsOfPlayers/PlayersListPage" + str(pageNumber) + ".html", "w")
    f.write(rendered_html)
    f.close()
    matches = re.findall(r'<a href="https://www.nhl.com/player/(\d+)">(.+?)</a>', rendered_html)
    if matches:
        player_ids = [match[0] for match in matches]
        player_names = [match[1] for match in matches]
        players = {int(player_ids[i]): player_names[i] for i in range(len(player_ids))}
    return players


def createPlayersIDsCsv(driver, numberOfPages):
    page_url = 'https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20232024&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100'
    driver.get(page_url)
    for pageNumber in range(1, int(numberOfPages) + 1):
        print(pageNumber)
        driver.set_window_size(1920, 1080)
        WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, 'sc-feUZmu'))).send_keys(
            Keys.BACK_SPACE + Keys.BACK_SPACE + str(pageNumber))
        WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, 'sc-fHjqPf'))).click()
        time.sleep(1)
        players = getPlayerIds(driver, pageNumber)
        print(players)
        players_df = pd.DataFrame(list(players.items()), columns=['Player_ID', 'Player_Name'])
        if pageNumber == 1:
            players_df.to_csv('data/csvFiles/playersIDs.csv', index=False)
        else:
            players_df.to_csv('data/csvFiles/playersIDs.csv', mode='a', index=False, header=False)


def getPlayersInfo(driver, player_id):
    player = {'Player_ID': player_id}
    seasons = []
    page_url = 'https://www.nhl.com/player/' + str(player_id)
    driver.get(page_url)
    WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, 'sc-jGKxIK')))
    time.sleep(1)
    rendered_html = driver.page_source
    f = open("data/rawHTML/playersSeasons/Player" + str(player_id) + ".html", "w")
    f.write(rendered_html)
    f.close()

    # Player seasons
    matches = re.findall(r'<div class="sc-jGKxIK (carAtq|cTamTE|ceEiFm|cjpdWM|gTLwwK) rt-td ">(.+?)</div>',
                         rendered_html)
    if matches:
        values = [match[1] for match in matches]
        season = {'Player_ID': player_id}
        keys = ['Season', 'Team', 'GamePlayed', 'Goals', 'Assists', 'Points', 'PlusMinus', 'PenaltyInfractionMinutes',
                'PowerplayGoals', 'PowerplayPoints', 'ShorthandedGoals', 'ShorthandedPoints', 'TimeOnIcePerGame',
                'GameWinningGoals', 'OvertimeGoals', 'Shots', 'ShootingPercentage', 'FaceOffPercentage']
        counter = 0
        for value in values:
            if value == 'Career':
                break
            season[keys[counter]] = value
            counter = counter + 1
            if counter == 18:
                seasons.append(season)
                season = {'Player_ID': player_id}
                counter = 0

    # Player info
    matches = re.findall(r'<div class="sc-iEXKAA gHsVrV"><b class="sc-eZYNyq kfVwxD">(.+?): </b>(.+?)</div>',
                         rendered_html)
    if matches:
        keys = [match[0] for match in matches]
        values = [match[1] for match in matches]
        for i in range(len(keys)):
            values[i] = re.sub(r'<span>', '', values[i])
            values[i] = re.sub(r'</span>', '', values[i])
            player[keys[i]] = values[i]

    matches = re.findall(r'<div class="sc-jGKxIK knlIUT rt-td ">(.+?)</div>',
                         rendered_html)
    matches = matches[5:]
    if matches:
        keys = ['GamePlayed', 'Goals', 'Assists', 'Points', 'PlusMinus']
        values = [match for match in matches]
        for i in range(len(keys)):
            player[keys[i]] = values[i]

    return [player], seasons


def createPlayersInfoCsv(driver):
    players = pd.read_csv('data/csvFiles/playersIDs.csv')
    players_ids = players['Player_ID'].values
    players_name = players['Player_Name'].values
    f = open("data/downloaded_cnt.txt", "r")
    downloaded_cnt = int(f.read())
    f.close()
    cnt = 0
    for player_id, player_name in zip(players_ids, players_name):
        if cnt >= downloaded_cnt:
            print(cnt, player_name)
            start_time = time.time()
            player, season = getPlayersInfo(driver, player_id)
            players_info_df = pd.DataFrame(player)
            players_seasons_df = pd.DataFrame(season)
            if cnt == 0:
                players_info_df.to_csv('data/csvFiles/playersInfo.csv', index=False)
                players_seasons_df.to_csv('data/csvFiles/playersSeasons.csv', index=False)
            else:
                players_info_df.to_csv('data/csvFiles/playersInfo.csv', mode='a', index=False, header=False)
                players_seasons_df.to_csv('data/csvFiles/playersSeasons.csv', mode='a', index=False, header=False)
                f = open("data/downloaded_cnt.txt", "w")
                f.write(str(cnt))
                f.close()
            elapsed_time = time.time() - start_time
            print(elapsed_time)
            time.sleep(5)
        cnt = cnt + 1


if __name__ == '__main__':
    # driver defining
    firefox_options = Options()
    firefox_options.headless = True
    gecko_driver_path = '/Users/matejkuran/School/2023:2024/Zimny_semester/VINF/VINF_projekt/geckodriver'
    driver = webdriver.Firefox(executable_path=gecko_driver_path, options=firefox_options)

    # # getting number of pages with players list
    # main_url = 'https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20232024&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=1&pageSize=100'
    # driver.get(main_url)
    # numberOfPages = getNumberOfPages(driver)
    # print('Number of pages is:', numberOfPages)
    #
    # # creating players csv
    # createPlayersIDsCsv(driver, numberOfPages)

    createPlayersInfoCsv(driver)

    driver.quit()
