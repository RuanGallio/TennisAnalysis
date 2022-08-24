import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

fmt = '%Y%m%d'
pd.set_option('display.max_columns', 49)
df = pd.read_csv('tennis_atp/atp_matches_2020.csv')

def clean():
    df['tourney_date'] =  df['tourney_date'].apply(lambda x: dt.strptime(str(x), fmt))
    df['winner_name'] = df['winner_name'].str.lower().str.replace(' ', '_')
    df['loser_name'] = df['loser_name'].str.lower().str.replace(' ', '_')
    df['tourney_name'] = df['tourney_name'].str.lower().str.replace(' ', '_')
    df['surface'] = df['surface'].str.lower()


tourneyLevels = {
  0: ["A", "C", "G", "M", "F", "S", "D"],
  1: ["G", "M", "B"]
}


def filt(p1="", tourneyLevel=0, surface="", startDate="", endDate=""):
    """
    Filters the dataframe by the given parameters.
    """
    
    surface = surface.lower()
    p1 = p1.lower().replace(' ', '_')
    startDate = dt.strptime(str(startDate), fmt)
    endDate = dt.strptime(str(endDate), fmt)

    tourneyLevel = tourneyLevels[tourneyLevel]
    filtre = (((df['winner_name'] == p1) | (df['loser_name'] == p1)) &
       (endDate >= df['tourney_date']) & (df['tourney_date'] >= startDate) &
        df['tourney_level'].isin(tourneyLevel) &
        df['surface'].str.contains('hard'))

    return df.loc[filtre]
    

# filt(p1='novak_djokovic', tourneyLevel=0, surface='hard', startDate="20200106", endDate='20210131')

def get_players_filtered_means(p1:str="", tourneyLevel:int=0, surface:str="", startDate:str="", endDate:str="") -> pd.DataFrame:
    """
        Returns a dataframe with the means of the filtered dataframe.
    """

    p1_table = filt(p1=p1, tourneyLevel=tourneyLevel, surface=surface, startDate=startDate, endDate=endDate)
    p1_win_table = p1_table[p1_table['winner_name'] == p1]
    p1_lose_table = p1_table[p1_table['loser_name'] == p1]
    try:
        qnty_won = p1_table['winner_name'].value_counts().loc[p1] 
        win_pct = qnty_won / p1_table['winner_name'].shape[0]
    except KeyError:
        qnty_won = 0
        win_pct = 0
    
    loss_pct = 1 - win_pct
    
    # p1_stats = p1_table.describe()
    p1_win_stats = p1_win_table.describe()
    p1_lose_stats = p1_lose_table.describe()

    
    stats = {'win_pct': win_pct, 'loss_pct': loss_pct,
        'when_win_w_ace_mean': p1_win_stats.loc['mean', 'w_ace'],
        'when_win_w_df_mean': p1_win_stats.loc['mean', 'w_df'],
        'when_win_w_svpt_mean': p1_win_stats.loc['mean', 'w_svpt'],
        'when_win_w_1stIn_mean': p1_win_stats.loc['mean', 'w_1stIn'],
        'when_win_w_1stWon_mean': p1_win_stats.loc['mean', 'w_1stWon'],
        'when_win_w_2ndWon_mean': p1_win_stats.loc['mean', 'w_2ndWon'],
        'when_win_w_SvGms_mean': p1_win_stats.loc['mean', 'w_SvGms'],
        'when_win_w_bpSaved_mean': p1_win_stats.loc['mean', 'w_bpSaved'],
        'when_win_w_bpFaced_mean': p1_win_stats.loc['mean', 'w_bpFaced'],
        'when_win_l_ace_mean': p1_win_stats.loc['mean', 'l_ace'],
        'when_win_l_df_mean': p1_win_stats.loc['mean', 'l_df'],
        'when_win_l_svpt_mean': p1_win_stats.loc['mean', 'l_svpt'],
        'when_win_l_1stIn_mean': p1_win_stats.loc['mean', 'l_1stIn'],
        'when_win_l_1stWon_mean': p1_win_stats.loc['mean', 'l_1stWon'],
        'when_win_l_2ndWon_mean': p1_win_stats.loc['mean', 'l_2ndWon'],
        'when_win_l_SvGms_mean': p1_win_stats.loc['mean', 'l_SvGms'],
        'when_win_l_bpSaved_mean': p1_win_stats.loc['mean', 'l_bpSaved'],
        'when_win_l_bpFaced_mean': p1_win_stats.loc['mean', 'l_bpFaced'],
        'when_lose_w_ace_mean': p1_lose_stats.loc['mean', 'w_ace'],
        'when_lose_w_df_mean': p1_lose_stats.loc['mean', 'w_df'],
        'when_lose_w_svpt_mean': p1_lose_stats.loc['mean', 'w_svpt'],
        'when_lose_w_1stIn_mean': p1_lose_stats.loc['mean', 'w_1stIn'],
        'when_lose_w_1stWon_mean': p1_lose_stats.loc['mean', 'w_1stWon'],
        'when_lose_w_2ndWon_mean': p1_lose_stats.loc['mean', 'w_2ndWon'],
        'when_lose_w_SvGms_mean': p1_lose_stats.loc['mean', 'w_SvGms'],
        'when_lose_w_bpSaved_mean': p1_lose_stats.loc['mean', 'w_bpSaved'],
        'when_lose_w_bpFaced_mean': p1_lose_stats.loc['mean', 'w_bpFaced'],
        'when_lose_l_ace_mean': p1_lose_stats.loc['mean', 'l_ace'],
        'when_lose_l_df_mean': p1_lose_stats.loc['mean', 'l_df'],
        'when_lose_l_svpt_mean': p1_lose_stats.loc['mean', 'l_svpt'],
        'when_lose_l_1stIn_mean': p1_lose_stats.loc['mean', 'l_1stIn'],
        'when_lose_l_1stWon_mean': p1_lose_stats.loc['mean', 'l_1stWon'],
        'when_lose_l_2ndWon_mean': p1_lose_stats.loc['mean', 'l_2ndWon'],
        'when_lose_l_SvGms_mean': p1_lose_stats.loc['mean', 'l_SvGms'],
        'when_lose_l_bpSaved_mean': p1_lose_stats.loc['mean', 'l_bpSaved'],
        'when_lose_l_bpFaced_mean': p1_lose_stats.loc['mean', 'l_bpFaced']
     }
    return pd.DataFrame(stats, index=[p1]).fillna(0)

def generate_mean_df(tourneyLevel:int=0, surface:str="", startDate:str="", endDate:str=""):
    """
    Generates a dataframe with the means of the stats for each player
    """
    all_players_stats_df = pd.DataFrame()
    players = []
    for i in df["winner_name"]:
        if i not in players:
            players.append(i)
    for i in df["loser_name"]:
        if i not in players:
            players.append(i)
    for i in players:
        playr_df = get_players_filtered_means(p1=i, tourneyLevel=tourneyLevel, surface=surface, startDate=startDate, endDate=endDate)
        all_players_stats_df = pd.concat((all_players_stats_df, playr_df), axis=0)
    
    return all_players_stats_df


# clean()
# general_stats = df.describe()
# get_players_filtered_means(p1='novak_djokovic', tourneyLevel=0, surface='hard', startDate="20200106", endDate='20210131')
# generate_mean_df( tourneyLevel=0, surface='hard', startDate="20200106", endDate='20210131')