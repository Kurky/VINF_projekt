import os
import re
from glob import glob
import pandas as pd
import time

baseDir = os.path.normpath('../data/rawHTML/playersSeasons')
folders = glob(baseDir + '/*')
counter = 0
all_seasons = []
start_time = time.time()
for folder in folders:
    seasons = []
    counter = counter + 1
    print(counter)
    player_id = int(re.findall(r'\d+', folder)[0])
    f = open(folder, "r")
    rendered_html = f.read()
    matches = re.findall(r'<div class="sc-jGKxIK (carAtq|cTamTE|ceEiFm|cjpdWM|gTLwwK) rt-td ">(.+?)</div>',
                         rendered_html)
    if matches:
        values = [match[1] for match in matches]
        season = {'Player_ID': player_id}
        keys = ['Season', 'Team', 'GamePlayed', 'Goals', 'Assists', 'Points', 'PlusMinus', 'PenaltyInfractionMinutes',
                'PowerplayGoals', 'PowerplayPoints', 'ShorthandedGoals', 'ShorthandedPoints', 'TimeOnIcePerGame',
                'GameWinningGoals', 'OvertimeGoals', 'Shots', 'ShootingPercentage', 'FaceOffPercentage']
        cnt = 0
        first = False
        for value in values:
            if value == 'Career':
                seasons.append(season)
                break
            match = re.findall(r'\b\d{4}-\d{2}\b', value)
            if match:
                if first:
                    seasons.append(season)
                    season = {'Player_ID': player_id}
                    cnt = 0
                else:
                    cnt = 0
                    first = True
            else:
                if not first:
                    cnt = 0
            season[keys[cnt]] = value
            cnt = cnt + 1
    all_seasons = all_seasons + seasons
    f.close()
players_seasons_df = pd.DataFrame(all_seasons)
end_time = time.time()
elapsed_time = end_time - start_time
print('Elapsed time', elapsed_time)
print(players_seasons_df.head())
