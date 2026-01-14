
"""
Reproduction Script: Differences-in-Differences (DiD) Analysis
==============================================================

This script reproduces the main DiD analysis results presented in the paper.

Methodology:
1. Framing Score (Main Result):
   - DIPLOMACY = +2
   - THREAT = -2
   - Others (NEUTRAL, ECONOMIC, HUMANITARIAN) = 0
   
2. Sentiment Score:
   - RoBERTa raw output (-1 to 1 range)

3. Binary Proportions (Robustness Check):
   - Proportion of DIPLOMACY posts
   - Proportion of THREAT posts

Usage:
    python analyze_did.py
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# --- Configuration ---
DATA_PATH = Path('../final/final_dataset.csv')

# Period definitions based on Summit dates
# P1: Pre-Summit (Until 2018-06-12)
# P2: Singapore-Hanoi (2018-06-13 ~ 2019-02-27)
# P3: Post-Hanoi (2019-02-28 ~)
PERIOD_CUTOFFS = {
    'Singapore': '2018-06-12',
    'Hanoi': '2019-02-28'
}

def load_and_preprocess():
    """Load data and compute framing scores."""
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH, low_memory=False)
    
    # Convert datetime
    df['datetime'] = pd.to_datetime(df['created_utc'], unit='s')
    df['date'] = df['datetime'].dt.date
    df['month_str'] = df['datetime'].dt.strftime('%Y-%m')
    
    # 1. Framing Score Mapping (+2, -2, 0)
    frame_map = {
        'DIPLOMACY': 2.0,
        'THREAT': -2.0,
        'NEUTRAL': 0.0,
        'ECONOMIC': 0.0,
        'HUMANITARIAN': 0.0
    }
    df['framing_score'] = df['frame'].map(frame_map).fillna(0.0)
    
    # 2. Binary indicators (for robustness)
    df['is_diplomacy'] = (df['frame'] == 'DIPLOMACY').astype(float)
    df['is_threat'] = (df['frame'] == 'THREAT').astype(float)
    
    return df

def aggregate_monthly(df):
    """Aggregate individual posts into monthly metrics."""
    print("Aggregating monthly statistics...")
    
    monthly = df.groupby(['country', 'month_str']).agg({
        'framing_score': 'mean',  # Main Framing Metric
        'sentiment_score': 'mean', # Main Sentiment Metric
        'is_diplomacy': 'mean',   # Robustness
        'is_threat': 'mean',      # Robustness
        'id': 'count'
    }).rename(columns={'id': 'post_count'}).reset_index()
    
    # Add datetime for period assignment
    monthly['date'] = pd.to_datetime(monthly['month_str'])
    
    return monthly

def assign_period(date_val):
    """Assign period ID based on date."""
    date_str = str(date_val)
    # Using month-level approximation matching the paper's monthly analysis
    if date_str < '2018-06':
        return 1 # Pre-Singapore
    elif '2018-06' <= date_str < '2019-03':
        return 2 # Singapore-Hanoi
    elif date_str >= '2019-03':
        return 3 # Post-Hanoi
    return 0

def run_did_comparison(df, target_col, title, control_country='CHINA'):
    """Run DiD for a specific target and control group."""
    
    # Filter for Target Control + NK
    subset = df[df['country'].isin(['NK', control_country])].copy()
    
    subset['period_id'] = subset['month_str'].apply(assign_period)
    subset['treatment'] = (subset['country'] == 'NK').astype(int)
    
    comparisons = [
        ('Singapore (P1->P2)', 1, 2),
        ('Hanoi (P2->P3)', 2, 3)
    ]
    
    results = []
    
    for comp_name, p_pre, p_post in comparisons:
        data = subset[subset['period_id'].isin([p_pre, p_post])].copy()
        
        # Post indicator
        data['post'] = (data['period_id'] == p_post).astype(int)
        
        # DiD Interaction
        data['did'] = data['treatment'] * data['post']
        
        # Regression
        # Clustered SE by month is ideal, but with aggregated data we use robust SE
        model = smf.ols(f"{target_col} ~ treatment + post + did", data=data).fit(cov_type='HC3')
        
        did_est = model.params['did']
        p_val = model.pvalues['did']
        ci = model.conf_int().loc['did']
        
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
        
        results.append({
            'Event': comp_name,
            'Control': control_country,
            'Est': did_est,
            'CI': (ci[0], ci[1]),
            'P': p_val,
            'Sig': sig
        })
        
    return results

def main():
    # 1. Load Data
    raw_df = load_and_preprocess()
    
    # 2. Aggregate Monthly
    monthly_df = aggregate_monthly(raw_df)
    
    # 3. Run Analysis
    print(f"\n{'='*70}")
    print("REPRODUCTION RESULTS (Monthly Aggregated DiD)")
    print(f"{'='*70}")
    
    metrics = [
        ('framing_score', 'Framing Score (-2 to +2)'),
        ('sentiment_score', 'Sentiment Score (-1 to +1)'),
        ('is_threat', 'Threat Proportion (Binary)')
    ]
    
    controls = ['CHINA', 'IRAN', 'RUSSIA']
    
    for col, name in metrics:
        print(f"\n--- {name} ---")
        print(f"{'Event':<20} {'Control':<10} {'Est.':<10} {'95% CI':<20}")
        print("-" * 65)
        
        for control in controls:
            results = run_did_comparison(monthly_df, col, name, control)
            for res in results:
                ci_str = f"[{res['CI'][0]:.2f}, {res['CI'][1]:.2f}]"
                print(f"{res['Event']:<20} {res['Control']:<10} {res['Est']:+.3f}{res['Sig']:<3} {ci_str:<20}")

if __name__ == "__main__":
    main()
