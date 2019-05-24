# Project: NBA Positional Scarcity
# Description: Scrape player per 100 possession table from Basketball-Reference.com
# between the 2004-2005 and 2018-2019 seasons.
# Data Sources: Basketball-Reference
# Last Updated: 4/16/2019

import numpy as np
import pandas as pd
from time import sleep

def scrape_player_per_100_possessions():
    """
    Scrape Player Per 100 Possession table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:

    Returns:
        historical_player_per_100_poss_df (DataFrame): Player Per 100 Possession
        table between 2004-2005 and 2018-2019 NBA seasons.
    """
    historical_player_per_100_poss_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}_per_poss.html#per_poss_stats::none'.format(season)
        season_player_per_100_poss_df = pd.read_html(url)[0]
        season_player_per_100_poss_df.drop('Unnamed: 29', axis=1, inplace=True)
        season_player_per_100_poss_df.columns = ['RANK', 'PLAYER', 'POSITION', 'AGE', 'TEAM', 'G', 'GS', 'MP'] + \
                                    ['PER100_' + str(col) for col in \
                                    season_player_per_100_poss_df.columns if col not in \
                                    ['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP']]
        season_player_per_100_poss_df = season_player_per_100_poss_df[season_player_per_100_poss_df['RANK']!='Rk']
        season_player_per_100_poss_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        historical_player_per_100_poss_df = historical_player_per_100_poss_df.append(season_player_per_100_poss_df, sort=False)
    column_order = ['RANK', 'PLAYER', 'SEASON', 'POSITION', 'AGE', 'TEAM', 'G', 'GS', 'MP',
       'PER100_FG', 'PER100_FGA', 'PER100_FG%', 'PER100_3P', 'PER100_3PA',
       'PER100_3P%', 'PER100_2P', 'PER100_2PA', 'PER100_2P%', 'PER100_FT',
       'PER100_FTA', 'PER100_FT%', 'PER100_ORB', 'PER100_DRB', 'PER100_TRB',
       'PER100_AST', 'PER100_STL', 'PER100_BLK', 'PER100_TOV', 'PER100_PF',
       'PER100_PTS', 'PER100_ORtg', 'PER100_DRtg']
    historical_player_per_100_poss_df = historical_player_per_100_poss_df.reindex(columns=column_order)
    dtype = {'RANK':'object', 'PLAYER':'object', 'SEASON':'object', 'POSITION':'object',
            'AGE':'int64', 'TEAM':'object', 'G':'int64', 'GS':'int64', 'MP':'int64',
            'PER100_FG':'float64', 'PER100_FGA':'float64', 'PER100_FG%':'float64',
            'PER100_3P':'float64', 'PER100_3PA':'float64', 'PER100_3P%':'float64',
            'PER100_2P':'float64', 'PER100_2PA':'float64', 'PER100_2P%':'float64',
            'PER100_FT':'float64', 'PER100_FTA':'float64', 'PER100_FT%':'float64',
            'PER100_ORB':'float64', 'PER100_DRB':'float64', 'PER100_TRB':'float64',
            'PER100_AST':'float64', 'PER100_STL':'float64', 'PER100_BLK':'float64',
            'PER100_TOV':'float64', 'PER100_PF':'float64', 'PER100_PTS':'float64',
            'PER100_ORtg':'float64', 'PER100_DRtg':'float64'}
    historical_player_per_100_poss_df = historical_player_per_100_poss_df.astype(dtype)
    return historical_player_per_100_poss_df

    if __name__=='__main__':
        historical_player_per_100_poss_df = scrape_player_per_100_possessions()
