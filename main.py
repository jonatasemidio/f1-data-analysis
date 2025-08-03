import os
import logging
import argparse
from pathlib import Path

# Import project modules
from src.data.download import download_f1_dataset
from src.data.cleaning import load_csv_data, clean_sprint_results, clean_drivers_data, clean_races_data
from src.data.validation import validate_sprint_results, validate_drivers, validate_races
from src.features.feature_engineering import (
    identify_sprint_winners, 
    merge_sprint_data, 
    calculate_sprint_wins,
    enrich_sprint_wins_data
)
from src.visualization.plots import plot_sprint_wins, plot_wins_by_year

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("f1_data_analysis.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="F1 Sprint Wins Analysis")
    parser.add_argument(
        "--data-dir", 
        type=str, 
        default="data/raw",
        help="Directory containing the F1 dataset"
    )
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="data/processed",
        help="Directory to save processed data and plots"
    )
    parser.add_argument(
        "--download", 
        action="store_true",
        help="Download the F1 dataset from Kaggle"
    )
    
    return parser.parse_args()

def main():
    """
    Main function to run the F1 Sprint Wins Analysis.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Step 1: Download the dataset if requested
        if args.download:
            data_path = download_f1_dataset(args.data_dir)
            logger.info(f"Dataset downloaded to {data_path}")
        else:
            data_path = args.data_dir
            logger.info(f"Using existing dataset at {data_path}")
        
        # Step 2: Load the data
        logger.info("Loading F1 dataset files")
        sprint_results_df = load_csv_data(data_path, "sprint_results.csv")
        drivers_df = load_csv_data(data_path, "drivers.csv")
        races_df = load_csv_data(data_path, "races.csv")
        
        # Step 3: Validate the data
        logger.info("Validating data")
        if not all([
            validate_sprint_results(sprint_results_df),
            validate_drivers(drivers_df),
            validate_races(races_df)
        ]):
            logger.error("Data validation failed. Exiting.")
            return
        
        # Step 4: Clean the data
        logger.info("Cleaning data")
        sprint_results_clean = clean_sprint_results(sprint_results_df)
        drivers_clean = clean_drivers_data(drivers_df)
        races_clean = clean_races_data(races_df)
        
        # Step 5: Feature engineering
        logger.info("Performing feature engineering")
        sprint_winners = identify_sprint_winners(sprint_results_clean)
        merged_data = merge_sprint_data(sprint_winners, races_clean, drivers_clean)
        sprint_wins = calculate_sprint_wins(merged_data)
        enriched_sprint_wins = enrich_sprint_wins_data(sprint_wins, merged_data)
        
        # Step 6: Save processed data
        output_path = Path(args.output_dir) / "sprint_wins.csv"
        enriched_sprint_wins.to_csv(output_path, index=False)
        logger.info(f"Saved processed data to {output_path}")
        
        # Step 7: Create visualizations
        logger.info("Creating visualizations")
        plot_sprint_wins(enriched_sprint_wins, args.output_dir)
        plot_wins_by_year(merged_data, args.output_dir)
        
        # Print results
        print("\nNumber of F1 Sprint race wins per driver:")
        print(enriched_sprint_wins)
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.exception(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()