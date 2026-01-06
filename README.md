# Anonymized Data for Reproducibility

This folder contains anonymized versions of the research data and reproduction scripts for public sharing.

## Data Structure

### 1. Main Dataset (`final/`)

| Filename | Description | Rows |
|----------|-------------|------|
| **`final_dataset.csv`** | **The complete merged dataset** used for DiD analysis. Includes data from **North Korea** (Treatment) and **China, Iran, Russia** (Controls). Contains framing labels, sentiment scores, and metadata. | 34,927 |

### 2. Annotations (`annotations/`)

| Filename | Description | Rows |
|----------|-------------|------|
| **`human_ground_truth.csv`** | Consolidated human annotations (Pilot + Batch 1 + Batch 2). | 499 |
| **`validation_results.csv`** | Model validation results comparing LLM predictions with human labels. | 501 |
| **`CODEBOOK.md`** | Detailed definitions of the framing categories and annotation guidelines. | - |

### 3. Analysis Results (`results/`)

Analysis outputs are consolidated into categorized JSON/Markdown files:

- **`did_results_main.json`**: Core Differences-in-Differences (DiD) analysis results.
- **`graphrag_analysis_results.json`**: Results from GraphRAG and community detection.
- **`framing_did_consolidated.json`**: Detailed DiD statistics for Framing.
- **`sentiment_did_consolidated.json`**: Detailed DiD statistics for Sentiment.
- **`GRAPHRAG_REPORTS_CONSOLIDATED.md`**: Textual analysis reports.

### 4. Reproduction Scripts (`reproduction_scripts/`)

| Script | Description |
|--------|-------------|
| **`analyze_did.py`** | Python script to reproduce the main DiD analysis tables (Framing & Sentiment) directly from the anonymized dataset. |

---

## What's Included

✅ **Preserved columns:**

- `id` / `post_id`: Reddit post identifier
- `subreddit`, `created_utc`: Metadata
- `frame`, `frame_confidence`: Framing labels (LLM predicted)
- `sentiment_score`: Sentiment analysis scores
- `period`, `topic`: Analysis periods
- `country`: Country tag

❌ **Removed columns:**

- `title`, `selftext`, `body`: Original text content
- `frame_reason`: LLM reasoning text

## Retrieving Original Text

To retrieve original post text for analysis, use the Reddit post IDs with:

1. **Pushshift API** (archived data):

   ```
   https://api.pushshift.io/reddit/submission/search?ids={post_id}
   ```

2. **Reddit API** (current data):

   ```
   https://www.reddit.com/api/info.json?id=t3_{post_id}
   ```

## Citation

If you use this data, please cite:

```
[Paper citation to be added after publication]
```
