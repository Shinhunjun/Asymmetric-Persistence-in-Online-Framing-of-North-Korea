# Reproduction Scripts

This folder contains Python scripts to reproduce the core analysis results presented in the paper using the anonymized dataset.

## Scripts

### `analyze_did.py`

Reproduces the Differences-in-Differences (DiD) analysis for Framing and Sentiment scores.

- **Main Analysis**: Uses continuous Framing Score (Diplomacy=+2, Threat=-2, Neutral=0) and Sentiment Score.
- **Robustness Check**: Uses binary outcome indicators (Proportion of Threat/Diplomacy posts).
- **Comparison Control**: Replicates results for China, Iran, and Russia control groups.

## How to Run

1. Install dependencies:

   ```bash
   pip install pandas numpy statsmodels
   ```

2. Run the script:

   ```bash
   python analyze_did.py
   ```

3. Expected Output:
   The script will print DiD estimtates, confidence intervals, and p-values for:
   - Framing Score Changes (Singapore & Hanoi Summits)
   - Sentiment Score Changes
   - Binary Threat/Diplomacy Proportions

## Data Source

The script reads from `../final/final_dataset.csv`, which contains the fully merged anonymized data for all countries.
