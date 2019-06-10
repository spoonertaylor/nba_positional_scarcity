# Project: Target Selection
# Description: Calculate and visualize cross-correlations between various metrics
# to determine which lead and which lag across seasons. Will help determine target
# variable for player projection modeling as we want to select the metric that leads
# all others.
# Data Sources: Basketball-Reference and ESPN
# Last Updated: 6/8/2019

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Plotting Style
plt.style.use('fivethirtyeight')

def cross_correlation(field1, field2):
    array_len = len(field1)
    arg_max = np.argmax((np.correlate([float(i) for i in field1], [float(i) for i in field2], mode='full')))
    return (int(np.arange(-array_len+1, array_len)[arg_max]))

def norm_cross_correlation(field1, field2):
    if len(field1) > 4:
        central_corr = np.abs(np.array(np.correlate(field1, field2, mode='full'), dtype=np.float64)[len(field1)-5:len(field1)+4])
    else:
        central_corr = np.abs(np.array(np.correlate(field1, field2, mode='full'), dtype=np.float64))
    norm_corr = np.nan_to_num(central_corr / np.sum(central_corr))
    return norm_corr.tolist()

def pad_corr_series(corr_list):
  if len(corr_list) == 9:
    return np.array(corr_list)
  elif len(corr_list) < 9:
    if len(corr_list) % 2 == 1:
      return np.pad(np.array(corr_list), pad_width=((9-len(corr_list)) // 2), mode='constant', constant_values=0.0)
    else:
      right_pad_width = int(np.floor((9-len(corr_list)) / 2))
      left_pad_width = int(np.floor((9-len(corr_list)) / 2)) + 1
      return np.pad(np.array(corr_list), pad_width=(right_pad_width, left_pad_width), mode='constant', constant_values=0.0)
  else:
    if len(corr_list) % 2 == 1:
      too_long_start = (len(corr_list) - 9) // 2
    else:
      too_long_start = (len(corr_list) - 10) // 2
    return np.array(corr_list[too_long_start:too_long_start+9])

def plot_normalized_metric(metric):
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(18, 10), sharex=True, sharey=True)
    metric_list = ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']
    metric_list.remove(metric)
    density_hists = [np.sum(np.vstack(tuple(pad_corr_series(x) for x in df_norm[str(metric + '_' + metric2)])), axis=0) for metric2 in metric_list]
    density_bins = np.arange(-4, 5)
    axs[0, 0].bar(density_bins, density_hists[0])
    axs[0, 1].bar(density_bins, density_hists[1])
    axs[0, 2].bar(density_bins, density_hists[2])
    axs[1, 0].bar(density_bins, density_hists[3])
    axs[1, 1].bar(density_bins, density_hists[4])
    axs[1, 2].bar(density_bins, density_hists[5])
    axs[2, 1].bar(density_bins, density_hists[6])
    axs[1, 0].set_ylabel('Density')
    axs[2, 1].set_xlabel('Season Lag')
    axs[0, 0].set_title('{0} vs. {1}'.format(metric, metric_list[0]), fontsize=12)
    axs[0, 1].set_title('{0} vs. {1}'.format(metric, metric_list[1]), fontsize=12)
    axs[0, 2].set_title('{0} vs. {1}'.format(metric, metric_list[2]), fontsize=12)
    axs[1, 0].set_title('{0} vs. {1}'.format(metric, metric_list[3]), fontsize=12)
    axs[1, 1].set_title('{0} vs. {1}'.format(metric, metric_list[4]), fontsize=12)
    axs[1, 2].set_title('{0} vs. {1}'.format(metric, metric_list[5]), fontsize=12)
    axs[2, 1].set_title('{0} vs. {1}'.format(metric, metric_list[6]), fontsize=12)
    axs[2, 0].grid(False)
    axs[2, 2].grid(False)
    plt.suptitle('{0} Cross Correlations'.format(metric), fontsize=20)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()

if __name__=='__main__':
    # Read in data sources
    player_table = pd.read_csv('../../data/player_table.csv')
    espn_nba_rpm = pd.read_csv('../../data/espn_nba_rpm.csv')
    salary_df = pd.read_csv('../../data/bbref_player_data/salary_info.csv')
    bbref_player_df = pd.read_csv('../../data/bbref_player_data/bbref_player_data.csv')

    # Convert season from yyyy to yyyy-yyyy to join on
    salary_df = salary_df[salary_df['season'].notnull()]
    salary_df['season'] = salary_df.apply(lambda row: str(int(row['season'] - 1)) +  '-' +  str(int(row['season'])), axis=1)
    espn_nba_rpm['season'] = espn_nba_rpm.apply(lambda row: str(row['season'] - 1) +  '-' +  str(row['season']), axis=1)

    # Aggregatre ESPN metrics to season level to avoid problem joining traded players
    espn_nba_rpm = espn_nba_rpm.groupby(['name', 'pos', 'espn_link', 'season']).mean().reset_index()

    # Join dataframes
    player_data = (pd.merge(bbref_player_df, player_table, how='left', left_on='bbref_id', right_on='bbref_id')
                            .merge(salary_df, how='left', left_on=['bbref_id', 'SEASON'], right_on=['bbref_id', 'season'])
                            .merge(espn_nba_rpm, how='left', left_on=['espn_link', 'SEASON'], right_on=['espn_link', 'season'])
                            [['bbref_id', 'espn_link', 'PLAYER', 'AGE', 'MP', 'SEASON', 'TEAM', 'POSITION',
                            'PER100_ORtg', 'PER100_DRtg', 'OBPM', 'DBPM', 'BPM',
                            'VORP', 'orpm', 'drpm', 'rpm', 'wins', 'salary', 'salary_prop_cap']]
                            .rename(columns={'orpm':'ORPM', 'drpm':'DRPM', 'rpm':'RPM',
                                             'wins':'WINS', 'salary':'SALARY',
                                             'salary_prop_cap':'SALARY_PROP_CAP'}))

    # Clean Basketball-Reference positions to take first position listed
    player_data['POSITION'] = player_data['POSITION'].str.split('-').str[0]

    # Rookie season position or position during 2004-2005 season
    player_data = (player_data.join(player_data
                              .groupby('PLAYER')['POSITION']
                              .first(), on='PLAYER', rsuffix='_duplicate')
                              .rename(columns={'POSITION_duplicate': 'INITIAL_POSITION'}))

    # Create Net Rating for Basketball-Reference
    player_data['NET_RTG'] = player_data['PER100_ORtg'] - player_data['PER100_DRtg']

    # Remove partial seasons resulting from trades (Removes duplicate Tony Mitchells in 2013-2014. To fix groupBy bbref_id instead of player name)
    player_data_no_trades = player_data[((player_data.groupby(['PLAYER', 'SEASON'])['TEAM'].transform('size')>1) &
                            (player_data['TEAM']=='TOT')) |
                            (player_data.groupby(['PLAYER', 'SEASON'])['TEAM'].transform('size')<=1)]

    # # Non-Normalized Cross-Correlation
    df_non_norm = player_data_no_trades.groupby(['PLAYER'])['NET_RTG'].apply(list).reset_index()
    for metric in ['BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
        df_non_norm[metric] = player_data_no_trades.groupby(['PLAYER'])[metric].apply(list).reset_index()[metric]

    # df_non_norm['cross'] = df_non_norm[df_non_norm['NET_RTG'].str.len() >8].apply(lambda row: cross_correlation(row['NET_RTG'], row['BPM']), axis=1)
    for metric1 in ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
        for metric2 in ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
            if metric1 != metric2:
                df_non_norm[str(metric1 + '_' + metric2)] = df_non_norm.apply(lambda row: cross_correlation(row[metric1], row[metric2]), axis=1)

    # Aggregate to one dataframe
    corr_df = df_non_norm['NET_RTG_BPM'].value_counts().reset_index().sort_values(by='index', ascending=False)
    corr_df.columns = ['SEASON_LAG', 'NET_RTG_BPM_COUNT']
    for metric1 in ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
        for metric2 in ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
            if metric1 != metric2:
                corr_df[str(metric1 + '_' + metric2 + '_COUNT')] = df_non_norm[str(metric1 + '_' + metric2)].value_counts().reset_index().sort_values(by='index', ascending=False)[str(metric1 + '_' + metric2)]

    # Example Plot Histogram of Non-Normalized Lags (Net Rating vs. VORP vs. BPM)
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 5), sharex=True, sharey=True)
    axs[0].bar(corr_df['SEASON_LAG'], corr_df['NET_RTG_BPM_COUNT'])
    axs[1].bar(corr_df['SEASON_LAG'], corr_df['NET_RTG_VORP_COUNT'])
    axs[2].bar(corr_df['SEASON_LAG'], corr_df['BPM_VORP_COUNT'])
    axs[0].set_title('Net Rating vs. BPM')
    axs[0].set_ylabel('Player Count')
    axs[1].set_title('Net Rating vs. VORP')
    axs[1].set_xlabel('Season Lag')
    axs[2].set_title('BPM vs. VORP')
    plt.tight_layout()
    plt.show()

    # Normalized Cross-Correlation
    df_norm = player_data_no_trades.groupby(['PLAYER'])['NET_RTG'].apply(list).reset_index()
    for metric in ['BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
        df_norm[metric] = player_data_no_trades.groupby(['PLAYER'])[metric].apply(list).reset_index()[metric]

    for metric1 in ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
        for metric2 in ['NET_RTG', 'BPM', 'VORP', 'MP', 'RPM', 'WINS', 'SALARY', 'SALARY_PROP_CAP']:
            if metric1 != metric2:
                df_norm[str(metric1 + '_' + metric2)] = df_norm.apply(lambda row: norm_cross_correlation(row[metric1], row[metric2]), axis=1)


    # Example Plot Histogram of Normalized Lags (Net Rating vs. VORP vs. BPM)
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 5), sharex=True, sharey=True)
    density_hist1 = np.sum(np.vstack(tuple(pad_corr_series(x) for x in df_norm['NET_RTG_BPM'])), axis=0)
    density_hist2 = np.sum(np.vstack(tuple(pad_corr_series(x) for x in df_norm['NET_RTG_VORP'])), axis=0)
    density_hist3 = np.sum(np.vstack(tuple(pad_corr_series(x) for x in df_norm['BPM_VORP'])), axis=0)
    density_bins = np.arange(-4, 5)
    axs[0].bar(density_bins, density_hist1)
    axs[1].bar(density_bins, density_hist2)
    axs[2].bar(density_bins, density_hist3)
    axs[0].set_title('Net Rating vs. BPM')
    axs[0].set_ylabel('Density')
    axs[1].set_title('Net Rating vs. VORP')
    axs[1].set_xlabel('Season Lag')
    axs[2].set_title('BPM vs. VORP')
    plt.tight_layout()
    plt.show()

    # Plot all cross-correlations for individual metric
    plot_normalized_metric('VORP')
