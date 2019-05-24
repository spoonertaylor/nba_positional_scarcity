# Project: NBA Positional Scarcity
# Description: Scrape player totals table from Basketball-Reference.com
# between the 2004-2005 and 2018-2019 seasons.
# Data Sources: Basketball-Reference
# Last Updated: 4/16/2019

import numpy as np
import pandas as pd
from time import sleep

def scrape_player_total_stats():
    """
    Scrape Player Total Stats table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:

    Returns:
        historical_player_totals_df (DataFrame): Player Total Stats
        table between 2004-2005 and 2018-2019 NBA seasons.
    """
    historical_player_totals_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}_totals.html#totals_stats::none'.format(season)
        season_player_totals_df = pd.read_html(url)[0]
        season_player_totals_df.columns = ['RANK', 'PLAYER', 'POSITION', 'AGE',
                                           'TEAM', 'G', 'GS', 'MP', 'FG', 'FGA',
                                           'FG%', '3P', '3PA', '3P%', '2P', '2PA',
                                           '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                                           'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
                                           'PF', 'PTS']
        season_player_totals_df = season_player_totals_df[season_player_totals_df['RANK']!='Rk']
        season_player_totals_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        historical_player_totals_df = historical_player_totals_df.append(season_player_totals_df, sort=False)
    column_order = ['RANK', 'PLAYER', 'SEASON', 'POSITION', 'AGE', 'TEAM', 'G',
                    'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA',
                    '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST',
                    'STL', 'BLK', 'TOV', 'PF', 'PTS']
    historical_player_totals_df = historical_player_totals_df.reindex(columns=column_order)
    dtype = {'RANK':'object', 'PLAYER':'object', 'SEASON':'object', 'POSITION':'object',
             'AGE':'int64', 'TEAM':'object', 'G':'int64', 'GS':'int64', 'MP':'int64',
             'FG':'int64', 'FGA':'int64', 'FG%':'float64', '3P':'int64', '3PA':'int64',
             '3P%':'float64', '2P':'int64', '2PA':'int64', '2P%':'float64', 'eFG%':'float64',
             'FT':'int64', 'FTA':'int64', 'FT%':'float64', 'ORB':'int64', 'DRB':'int64',
             'TRB':'int64', 'AST':'int64', 'STL':'int64', 'BLK':'int64', 'TOV':'int64',
             'PF':'int64', 'PTS':'int64'}
    historical_player_totals_df = historical_player_totals_df.astype(dtype)
    return historical_player_totals_df

if __name__ == '__main__':
    historical_player_totals_df = scrape_player_total_stats()
