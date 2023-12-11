import os
import re
import time
from glob import glob
from concurrent.futures import ProcessPoolExecutor
import pandas as pd


def process_html_file(folder):
    seasons = []
    player_id = int(re.findall(r'\d+', folder)[0])

    with open(folder, "r") as f:
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

    return seasons


if __name__ == "__main__":
    baseDir = os.path.normpath('../data/rawHTML/playersSeasons')
    folders = glob(baseDir + '/*')

    start_time = time.time()

    with ProcessPoolExecutor() as executor:
        all_seasons = list(executor.map(process_html_file, folders))

    flattened_seasons = [season for sublist in all_seasons for season in sublist]

    players_seasons_df = pd.DataFrame(flattened_seasons)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Elapsed time:', elapsed_time)

    print(players_seasons_df.head())
