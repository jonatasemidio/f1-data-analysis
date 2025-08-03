import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def set_plotting_style():
    """
    Set the style for matplotlib plots.
    """
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12

def plot_sprint_wins(sprint_wins_df, output_dir="data/processed", save_fig=True):
    """
    Create a bar plot of sprint race wins per driver.
    
    Args:
        sprint_wins_df (pd.DataFrame): DataFrame with sprint wins count
        output_dir (str): Directory to save the plot
        save_fig (bool): Whether to save the figure to disk
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    logger.info("Creating sprint wins bar plot")
    
    set_plotting_style()
    
    fig, ax = plt.subplots()
    
    # Create the bar plot
    sns.barplot(x='sprintWins', y='driverName', data=sprint_wins_df, ax=ax)
    
    # Set labels and title
    ax.set_title('F1 Sprint Race Wins by Driver', fontsize=16)
    ax.set_xlabel('Number of Sprint Wins', fontsize=14)
    ax.set_ylabel('Driver', fontsize=14)
    
    # Tight layout
    plt.tight_layout()
    
    # Save the figure if requested
    if save_fig:
        os.makedirs(output_dir, exist_ok=True)
        output_path = Path(output_dir) / 'sprint_wins_by_driver.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig

def plot_wins_by_year(merged_df, output_dir="data/processed", save_fig=True):
    """
    Create a plot of sprint race wins by year.
    
    Args:
        merged_df (pd.DataFrame): Merged DataFrame with sprint winners
        output_dir (str): Directory to save the plot
        save_fig (bool): Whether to save the figure to disk
        
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    logger.info("Creating sprint wins by year plot")
    
    set_plotting_style()
    
    # Count wins by year
    wins_by_year = merged_df.groupby('year').size().reset_index(name='count')
    
    fig, ax = plt.subplots()
    
    # Create the line plot
    sns.lineplot(x='year', y='count', data=wins_by_year, marker='o', ax=ax)
    
    # Set labels and title
    ax.set_title('F1 Sprint Races by Year', fontsize=16)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Number of Sprint Races', fontsize=14)
    
    # Set x-ticks to show all years
    ax.set_xticks(wins_by_year['year'])
    
    # Tight layout
    plt.tight_layout()
    
    # Save the figure if requested
    if save_fig:
        os.makedirs(output_dir, exist_ok=True)
        output_path = Path(output_dir) / 'sprint_races_by_year.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {output_path}")
    
    return fig