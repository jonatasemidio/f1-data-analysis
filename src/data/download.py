import os
import logging
import kagglehub
from pathlib import Path

logger = logging.getLogger(__name__)

def download_f1_dataset(output_dir="data/raw"):
    """
    Download the Formula 1 dataset from Kaggle.
    
    Args:
        output_dir (str): Directory to save the dataset
        
    Returns:
        str: Path to the downloaded dataset
    """
    logger.info("Downloading F1 dataset from Kaggle")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Download the dataset
        path = kagglehub.dataset_download(
            "rohanrao/formula-1-world-championship-1950-2020",
            output_dir
        )
        logger.info(f"Dataset downloaded successfully to {path}")
        return path
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        raise