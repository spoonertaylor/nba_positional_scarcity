# Project: NBA Positional Scarcity
# Description: Scrape player advance stats table from Basketball-Reference.com
# between the 2004-2005 and 2018-2019 seasons.
# Data Sources: Basketball-Reference
# Last Updated: 4/16/2019

import numpy as np
import pandas as pd
from time import sleep

def scrape_player_advanced_stats():
    """
    Scrape Player Advanced Stats table within NBA Season Summary Page on
    Basketball-Reference.com.

    Args:

    Returns:
        historical_player_per_100_poss_df (DataFrame): Player Advanced Stats
        table between 2004-2005 and 2018-2019 NBA seasons.
    """
    historical_player_advanced_df = pd.DataFrame()
    for season in np.arange(2005, 2020):
        sleep(np.random.randint(10, 15))
        url = 'https://www.basketball-reference.com/leagues/NBA_{0}_advanced.html#advanced_stats::none'.format(season)
        season_player_advanced_df = pd.read_html(url)[0]
        season_player_advanced_df.drop(['Unnamed: 19', 'Unnamed: 24'], axis=1, inplace=True)
        season_player_advanced_df.columns = ['RANK', 'PLAYER', 'POSITION', 'AGE',
                                             'TEAM', 'G', 'MP', 'PER', 'TS%', '3PA_RATE',
                                             'FT_RATE', 'ORB%', 'DRB%', 'TRB%', 'AST%',
                                             'STL%', 'BLK%', 'TOV%', 'USG%',
                                             'OWS', 'DWS', 'WS', 'WS/48', 'OBPM',
                                             'DBPM', 'BPM', 'VORP']
        season_player_advanced_df = season_player_advanced_df[season_player_advanced_df['RANK']!='Rk']
        season_player_advanced_df['SEASON'] = '{0}-{1}'.format(season-1, season)
        historical_player_advanced_df = historical_player_advanced_df.append(season_player_advanced_df, sort=False)
    column_order = ['RANK', 'PLAYER', 'SEASON', 'POSITION', 'AGE', 'TEAM', 'G',
                    'MP', 'PER', 'TS%', '3PA_RATE', 'FT_RATE', 'ORB%', 'DRB%',
                    'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS',
                    'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']
    historical_player_advanced_df = historical_player_advanced_df.reindex(columns=column_order)
    dtype = {'RANK':'object', 'PLAYER':'object', 'SEASON':'object', 'POSITION':'object',
             'AGE':'int64', 'TEAM':'object', 'G':'int64', 'MP':'int64', 'PER':'float64',
             'TS%':'float64', '3PA_RATE':'float64', 'FT_RATE':'float64', 'ORB%':'float64',
             'DRB%':'float64', 'TRB%':'float64', 'AST%':'float64', 'STL%':'float64',
             'BLK%':'float64', 'TOV%':'float64', 'USG%':'float64', 'OWS':'float64',
             'DWS':'float64', 'WS':'float64', 'WS/48':'float64', 'OBPM':'float64',
             'DBPM':'float64', 'BPM':'float64', 'VORP':'float64'}
    historical_player_advanced_df = historical_player_advanced_df.astype(dtype)
    return historical_player_advanced_df

    if __name__=='__main__':
        historical_player_advanced_df = scrape_player_advanced_stats()
