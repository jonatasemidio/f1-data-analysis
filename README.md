# F1 Sprint Wins Analysis

This project analyzes Formula 1 sprint race wins using the Kaggle F1 dataset. It demonstrates data cleaning, feature engineering, and visualization following MLOps best practices.

## Project Structure

The project follows a modular structure with separate components for data processing, feature engineering, and visualization:

- `src/data/`: Data downloading, loading, cleaning, and validation
- `src/features/`: Feature engineering and transformation
- `src/visualization/`: Data visualization and plotting
- `main.py`: Main entry point for the application

## Installation

```bash
# Clone the repository
git clone git@github.com:jonatasemidio/f1-data-analysis.git
cd f1-data-analysis

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package and dependencies
pip install -e .
```

## Usage

```bash
# Download the dataset and run the analysis
python main.py --download

# Use an existing dataset
python main.py --data-dir path/to/dataset

# Specify an output directory
python main.py --output-dir path/to/output
```

## Data

This project uses the [Formula 1 World Championship (1950-2023)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) dataset from Kaggle, which includes:

- Sprint race results
- Driver information
- Race details
- Constructor (team) data

## Tests

```bash
# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src
```

## License

[MIT](LICENSE)
