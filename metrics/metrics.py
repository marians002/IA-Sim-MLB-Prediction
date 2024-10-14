import pandas as pd
from scipy.stats import pearsonr

# Mapping dictionary for full team names to abbreviations
team_abbreviation_mapping = {
    'Los Angeles Dodgers': 'LAD',
    'Atlanta Braves': 'ATL',
    'New York Mets': 'NYM',
    'St. Louis Cardinals': 'STL',
    'San Diego Padres': 'SDP',
    'Philadelphia Phillies': 'PHI',
    'Milwaukee Brewers': 'MIL',
    'San Francisco Giants': 'SFG',
    'Arizona Diamondbacks': 'ARI',
    'Chicago Cubs': 'CHC',
    'Miami Marlins': 'MIA',
    'Colorado Rockies': 'COL',
    'Pittsburgh Pirates': 'PIT',
    'Cincinnati Reds': 'CIN',
    'Washington Nationals': 'WSN',
    'Houston Astros': 'HOU',
    'New York Yankees': 'NYY',
    'Toronto Blue Jays': 'TOR',
    'Cleveland Guardians': 'CLE',
    'Seattle Mariners': 'SEA',
    'Tampa Bay Rays': 'TBR',
    'Baltimore Orioles': 'BAL',
    'Chicago White Sox': 'CHW',
    'Minnesota Twins': 'MIN',
    'Boston Red Sox': 'BOS',
    'Los Angeles Angels': 'LAA',
    'Texas Rangers': 'TEX',
    'Detroit Tigers': 'DET',
    'Kansas City Royals': 'KCR',
    'Oakland Athletics': 'OAK'
}

def convert_to_abbreviations(df, mapping):
    """
    Convert full team names to abbreviations.
    
    Args:
    df (pd.DataFrame): DataFrame containing full team names.
    mapping (dict): Dictionary mapping full team names to abbreviations.
    
    Returns:
    pd.DataFrame: DataFrame with team abbreviations.
    """
    reverse_mapping = {v: k for k, v in mapping.items()}
    df['Team'] = df['Team'].map(reverse_mapping)
    return df

def top_n_comparison(df1, df2, n, mapping):
    """
    Compare the top N teams from two DataFrames.
    
    Args:
    df1 (pd.DataFrame): First DataFrame containing team rankings.
    df2 (pd.DataFrame): Second DataFrame containing team rankings.
    n (int): Number of top teams to compare.
    mapping (dict): Dictionary mapping full team names to abbreviations.
    
    Returns:
    tuple: Overlap count and percentage of overlap.
    """
    df1 = convert_to_abbreviations(df1, mapping)
    df2 = convert_to_abbreviations(df2, mapping)
    
    top_n_df1 = df1.head(n)['Team']
    top_n_df2 = df2.head(n)['Team']
    
    overlap = set(top_n_df1).intersection(set(top_n_df2))
    overlap_count = len(overlap)
    overlap_percentage = (overlap_count / n) * 100
    
    return overlap_count, overlap_percentage

def pearson_similarity(df1, df2, mapping):
    """
    Calculate the Pearson correlation coefficient between the rankings of two DataFrames.
    
    Args:
    df1 (pd.DataFrame): First DataFrame containing team rankings.
    df2 (pd.DataFrame): Second DataFrame containing team rankings.
    mapping (dict): Dictionary mapping full team names to abbreviations.
    
    Returns:
    float: Pearson correlation coefficient.
    """
    df1 = convert_to_abbreviations(df1, mapping)
    df2 = convert_to_abbreviations(df2, mapping)
    
    # Ensure both DataFrames have the same teams in the same order
    df1_sorted = df1.sort_values(by='Team').reset_index(drop=True)
    df2_sorted = df2.sort_values(by='Team').reset_index(drop=True)
    
    # Extract the rankings
    rankings_df1 = df1_sorted['Victories']
    rankings_df2 = df2_sorted['Victories']
    
    # Calculate Pearson correlation coefficient
    correlation, _ = pearsonr(rankings_df1, rankings_df2)
    
    return correlation
