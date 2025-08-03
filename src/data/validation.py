import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def validate_dataframe(df, required_columns, name="DataFrame"):
    """
    Validate that a DataFrame has the required columns and no null values in key columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
        name (str): Name of the DataFrame for logging
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    logger.info(f"Validating {name}")
    
    # Check if DataFrame is empty
    if df.empty:
        logger.error(f"{name} is empty")
        return False
    
    # Check for required columns
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        logger.error(f"{name} is missing required columns: {missing_columns}")
        return False
    
    # Check for null values in required columns
    null_counts = df[required_columns].isnull().sum()
    columns_with_nulls = null_counts[null_counts > 0].index.tolist()
    if columns_with_nulls:
        logger.warning(f"{name} has null values in columns: {columns_with_nulls}")
        for col in columns_with_nulls:
            logger.warning(f"Column {col} has {null_counts[col]} null values")
    
    logger.info(f"{name} validation passed")
    return True

def validate_sprint_results(sprint_results_df):
    """
    Validate the sprint results DataFrame.
    
    Args:
        sprint_results_df (pd.DataFrame): Sprint results DataFrame
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    required_columns = ['resultId', 'raceId', 'driverId', 'position', 'positionOrder']
    return validate_dataframe(sprint_results_df, required_columns, "Sprint Results")

def validate_drivers(drivers_df):
    """
    Validate the drivers DataFrame.
    
    Args:
        drivers_df (pd.DataFrame): Drivers DataFrame
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    required_columns = ['driverId', 'forename', 'surname']
    return validate_dataframe(drivers_df, required_columns, "Drivers")

def validate_races(races_df):
    """
    Validate the races DataFrame.
    
    Args:
        races_df (pd.DataFrame): Races DataFrame
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    required_columns = ['raceId', 'year', 'name']
    return validate_dataframe(races_df, required_columns, "Races")