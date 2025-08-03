import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_csv_data(data_path, filename):
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        data_path (str): Path to the data directory
        filename (str): Name of the CSV file
        
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    file_path = Path(data_path) / filename
    logger.info(f"Loading data from {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded {filename} with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        raise

def clean_sprint_results(sprint_results_df):
    """
    Clean the sprint results DataFrame.
    
    Args:
        sprint_results_df (pd.DataFrame): Sprint results DataFrame
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    logger.info("Cleaning sprint results data")
    
    # Make a copy to avoid modifying the original
    df = sprint_results_df.copy()
    
    # Convert position to numeric, handling non-numeric values
    df['position'] = pd.to_numeric(df['position'], errors='coerce')
    
    # Filter out rows with missing position values
    df_cleaned = df.dropna(subset=['position'])
    
    # Convert relevant columns to appropriate types
    df_cleaned['raceId'] = df_cleaned['raceId'].astype(int)
    df_cleaned['driverId'] = df_cleaned['driverId'].astype(int)
    
    # Log the cleaning results
    logger.info(f"Removed {len(df) - len(df_cleaned)} rows with missing position values")
    logger.info(f"Cleaned sprint results shape: {df_cleaned.shape}")
    
    return df_cleaned

def clean_drivers_data(drivers_df):
    """
    Clean the drivers DataFrame.
    
    Args:
        drivers_df (pd.DataFrame): Drivers DataFrame
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    logger.info("Cleaning drivers data")
    
    # Make a copy to avoid modifying the original
    df = drivers_df.copy()
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]
    
    # Convert dob to datetime
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
    
    # Create a full name column
    df['fullName'] = df['forename'] + ' ' + df['surname']
    
    logger.info(f"Cleaned drivers data shape: {df.shape}")
    
    return df

def clean_races_data(races_df):
    """
    Clean the races DataFrame.
    
    Args:
        races_df (pd.DataFrame): Races DataFrame
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    logger.info("Cleaning races data")
    
    # Make a copy to avoid modifying the original
    df = races_df.copy()
    
    # Convert date columns to datetime
    date_columns = ['date', 'sprint_date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Extract year from date if year column is missing
    if 'year' not in df.columns and 'date' in df.columns:
        df['year'] = df['date'].dt.year
    
    logger.info(f"Cleaned races data shape: {df.shape}")
    
    return df