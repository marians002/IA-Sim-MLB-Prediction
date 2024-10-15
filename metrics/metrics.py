import pandas as pd
import numpy as np
from tabulate import tabulate
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
    Convert full team names to abbreviations in a DataFrame.

    Args:
    df (pd.DataFrame): DataFrame containing team names.
    mapping (dict): Dictionary mapping full team names to abbreviations.

    Returns:
    pd.DataFrame: DataFrame with team names converted to abbreviations.
    """
    df['Team'] = df['Team'].map(mapping)
    return df


def top_n_comparison(df1, df2, n):
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
    top_n_df1 = df1.head(n)['Team']
    top_n_df2 = df2.head(n)['Tm']

    overlap = set(top_n_df1).intersection(set(top_n_df2))
    overlap_count = len(overlap)
    overlap_percentage = (overlap_count / n) * 100

    return overlap_count, overlap_percentage


def pearson_similarity(df1, df2):
    """
    Calculate the Pearson correlation coefficient between the rankings of two DataFrames.
    
    Args:
    df1 (pd.DataFrame): First DataFrame containing team rankings.
    df2 (pd.DataFrame): Second DataFrame containing team rankings.
    mapping (dict): Dictionary mapping full team names to abbreviations.
    
    Returns:
    float: Pearson correlation coefficient.
    """

    # Ensure both DataFrames have the same teams in the same order
    df1_sorted = df1.sort_values(by='Team').reset_index(drop=True)
    df2_sorted = df2.sort_values(by='Tm').reset_index(drop=True)

    # Extract the rankings
    rankings_df1 = df1_sorted['Victories']
    rankings_df2 = df2_sorted['W']

    # Calculate Pearson correlation coefficient
    correlation, _ = pearsonr(rankings_df1, rankings_df2)

    return correlation


def calculate_mean_squared_error(df1, df2):
    """
    Calculate the mean squared error (MSE) of win matches between two DataFrames.

    Args:
    df1 (pd.DataFrame): First DataFrame containing team statistics.
    df2 (pd.DataFrame): Second DataFrame containing team statistics.

    Returns:
    float: Mean squared error of win matches between the two DataFrames.
    """
    # Ensure both DataFrames have the same teams in the same order
    df1_sorted = df1.sort_values(by='Team').reset_index(drop=True)
    df2_sorted = df2.sort_values(by='Tm').reset_index(drop=True)

    # Extract the number of wins
    wins_df1 = df1_sorted['Victories']
    wins_df2 = df2_sorted['W']

    # Calculate the squared differences
    squared_diffs = (wins_df1 - wins_df2) ** 2

    # Calculate the mean squared error
    mse = np.mean(squared_diffs)

    return mse


def calculate_position_similarity(df1, df2):
    """
    Calculate the similarity of final positions between two DataFrames.

    Args:
    df1 (pd.DataFrame): First DataFrame containing team statistics.
    df2 (pd.DataFrame): Second DataFrame containing team statistics.

    Returns:
    float: Similarity score based on the average position differences between the two DataFrames.
    """
    # Ensure both DataFrames have the same teams in the same order
    df1_sorted = df1.sort_values(by='Team').reset_index(drop=True)
    df2_sorted = df2.sort_values(by='Tm').reset_index(drop=True)

    # Extract the final positions
    positions_df1 = df1_sorted['Position']
    positions_df2 = df2_sorted['Position']

    # Calculate the absolute differences in positions
    position_diffs = (positions_df1 - positions_df2).abs()

    # Calculate the average position difference
    similarity_score = position_diffs.mean()

    return similarity_score


def compare_metrics(nl_overall_df, al_overall_df, nl_overall_df_original, al_overall_df_original, n, graphics=False):
    # Convert team names to abbreviations
    nl_overall_df = convert_to_abbreviations(nl_overall_df, team_abbreviation_mapping)
    al_overall_df = convert_to_abbreviations(al_overall_df, team_abbreviation_mapping)

    # Compare top N teams
    nl_overlap_count, nl_overlap_percentage = top_n_comparison(nl_overall_df, nl_overall_df_original, n)
    al_overlap_count, al_overlap_percentage = top_n_comparison(al_overall_df, al_overall_df_original, n)

    # Calculate Pearson similarity
    nl_pearson = pearson_similarity(nl_overall_df, nl_overall_df_original)
    al_pearson = pearson_similarity(al_overall_df, al_overall_df_original)

    # Calculate Mean Squared Error
    nl_mse = calculate_mean_squared_error(nl_overall_df, nl_overall_df_original)
    al_mse = calculate_mean_squared_error(al_overall_df, al_overall_df_original)

    # Calculate Position Similarity
    nl_position_similarity = calculate_position_similarity(nl_overall_df, nl_overall_df_original)
    al_position_similarity = calculate_position_similarity(al_overall_df, al_overall_df_original)

    # Print results in a table-like format
    metrics = [
        ["Metric", "NL", "AL"],
        [f"Top {n} Teams Overlap", f"{nl_overlap_count} teams, {nl_overlap_percentage:.2f}%",
         f"{al_overlap_count} teams, {al_overlap_percentage:.2f}%"],
        ["Pearson Correlation", f"{nl_pearson:.2f}", f"{al_pearson:.2f}"],
        ["Mean Squared Error", f"{nl_mse:.2f}", f"{al_mse:.2f}"],
        ["Position Similarity", f"{nl_position_similarity:.2f}", f"{al_position_similarity:.2f}"]
    ]

    print(tabulate(metrics, headers="firstrow", tablefmt="grid"))
