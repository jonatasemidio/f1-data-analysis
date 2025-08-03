import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def identify_sprint_winners(sprint_results_df):
    """
    Identify sprint race winners from the sprint results DataFrame.
    
    Args:
        sprint_results_df (pd.DataFrame): Sprint results DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with only the sprint winners (position 1)
    """
    logger.info("Identifying sprint race winners")
    
    # Filter for position 1 (winners)
    winners_df = sprint_results_df[sprint_results_df['positionOrder'] == 1].copy()
    
    logger.info(f"Found {len(winners_df)} sprint race winners")
    
    return winners_df

def merge_sprint_data(sprint_winners_df, races_df, drivers_df):
    """
    Merge sprint winners with race and driver information.
    
    Args:
        sprint_winners_df (pd.DataFrame): Sprint winners DataFrame
        races_df (pd.DataFrame): Races DataFrame
        drivers_df (pd.DataFrame): Drivers DataFrame
        
    Returns:
        pd.DataFrame: Merged DataFrame with sprint winners and their details
    """
    logger.info("Merging sprint winners with race and driver information")
    
    # Merge with races to get race information
    merged_df = pd.merge(
        sprint_winners_df, 
        races_df[['raceId', 'year', 'name']], 
        on='raceId'
    )
    
    # Merge with drivers to get driver names
    merged_df = pd.merge(
        merged_df,
        drivers_df[['driverId', 'forename', 'surname', 'fullName']],
        on='driverId'
    )
    
    logger.info(f"Merged data shape: {merged_df.shape}")
    
    return merged_df

def calculate_sprint_wins(merged_df):
    """
    Calculate the number of sprint wins for each driver.
    
    Args:
        merged_df (pd.DataFrame): Merged DataFrame with sprint winners
        
    Returns:
        pd.DataFrame: DataFrame with sprint wins count per driver
    """
    logger.info("Calculating sprint wins per driver")
    
    # Count wins by driver
    sprint_wins = merged_df['fullName'].value_counts().reset_index()
    sprint_wins.columns = ['driverName', 'sprintWins']
    
    # Sort by number of wins in descending order
    sprint_wins = sprint_wins.sort_values('sprintWins', ascending=False).reset_index(drop=True)
    
    logger.info(f"Calculated sprint wins for {len(sprint_wins)} drivers")
    
    return sprint_wins

def enrich_sprint_wins_data(sprint_wins_df, merged_df):
    """
    Enrich the sprint wins data with additional features.
    
    Args:
        sprint_wins_df (pd.DataFrame): Sprint wins count DataFrame
        merged_df (pd.DataFrame): Merged DataFrame with sprint winners
        
    Returns:
        pd.DataFrame: Enriched DataFrame with additional features
    """
    logger.info("Enriching sprint wins data with additional features")
    
    # Create a copy to avoid modifying the original
    enriched_df = sprint_wins_df.copy()
    
    # Add latest win year for each driver
    latest_wins = merged_df.sort_values('year', ascending=False).drop_duplicates('fullName')
    latest_wins = latest_wins[['fullName', 'year']]
    latest_wins.columns = ['driverName', 'latestWinYear']
    
    # Merge with the sprint wins DataFrame
    enriched_df = pd.merge(enriched_df, latest_wins, on='driverName', how='left')
    
    # Calculate win percentage (if we had total races data)
    # This would require additional data processing
    
    logger.info(f"Enriched sprint wins data with {len(enriched_df.columns) - 2} additional features")
    
    return enriched_df