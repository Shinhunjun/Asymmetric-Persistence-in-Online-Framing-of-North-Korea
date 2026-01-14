# Anonymized Data for Reproducibility

This folder contains anonymized versions of the research data and reproduction scripts for public sharing.

## Data Structure

### 1. Main Dataset (`final/`)

| Filename | Description | Rows |
|----------|-------------|------|
| **`final_dataset.csv`** | Complete merged dataset for DiD analysis. Includes North Korea (Treatment) and China, Iran, Russia (Controls). Contains framing labels, sentiment scores, and metadata. | 34,929 |
| **`comment_ids.csv`** | All comment IDs (recursive) with parent post IDs, timestamp, and country. Use for Arctic Shift text retrieval. | 255,391 |

### 2. Annotations (`annotations/`)

| Filename | Description | Rows |
|----------|-------------|------|
| **`human_ground_truth.csv`** | Consolidated human annotations (Pilot + Batch 1 + Batch 2). | 500 |
| **`validation_results.csv`** | Model validation results comparing LLM predictions with human labels. | 500 |
| **`CODEBOOK.md`** | Detailed definitions of the framing categories and annotation guidelines. | - |

### 3. Analysis Results (`results/`)

| Filename | Description |
|----------|-------------|
| **`cross_llm_framing.csv`** | Cross-LLM validation results: GPT-4o-mini, GPT-4o, Claude Sonnet 4.5, Claude Haiku 4.5, Llama 3.3 70B, Llama 3.1 8B (N=500) |
| **`did_results_main.json`** | Core Difference-in-Differences analysis results |
| **`framing_did_consolidated.json`** | Detailed DiD statistics for Framing |
| **`sentiment_did_consolidated.json`** | Detailed DiD statistics for Sentiment |
| **`graphrag_analysis_results.json`** | Results from GraphRAG and community detection |
| **`GRAPHRAG_REPORTS_CONSOLIDATED.md`** | Textual analysis reports |

### 4. GraphRAG Configuration (`graphrag_config/`)

Customized GraphRAG indexing configuration for discourse network analysis:

| File | Description |
|------|-------------|
| **`settings.yaml`** | GraphRAG pipeline settings (model config, chunking, etc.) |
| **`prompts/`** | Customized extraction prompts including entity types: person, country, event, organization, **weapon**, **policy** |

**Key Customization:** Entity types extended to include `WEAPON` (e.g., ICBM, nuclear warhead) and `POLICY` (e.g., denuclearization, maximum pressure) for security domain analysis.

### 5. Reproduction Scripts (`reproduction_scripts/`)

| Script | Description |
|--------|-------------|
| **`analyze_did.py`** | Python script to reproduce the main DiD analysis tables |

---

## What's Included

✅ **Preserved columns:**

- `id` / `post_id`: Reddit post/comment identifier
- `subreddit`, `created_utc`: Metadata
- `frame`, `frame_confidence`: Framing labels (LLM predicted)
- `sentiment_score`: Sentiment analysis scores
- `period`, `country`: Analysis periods and country tags

❌ **Removed columns:**

- `title`, `selftext`, `body`: Original text content
- `frame_reason`: LLM reasoning text

## Retrieving Original Text

To retrieve original post/comment text for analysis, use the **Arctic Shift** archive with the preserved IDs.

1. **Arctic Shift**: We used the [Arctic Shift API/Archive](https://github.com/ArthurHeitmann/arctic_shift) to collect historical data. Original text can be retrieved by querying their archives using the `post_id` or `id` columns.

## Cross-LLM Validation

We validated our primary classifier (GPT-4o-mini) against multiple alternative models on 500 posts:

| Model | Agreement | Cohen's κ |
|-------|-----------|-----------|
| GPT-4o | 85.7% | 0.78 |
| Claude Sonnet 4.5 | 84.0% | 0.76 |
| Claude Haiku 4.5 | 81.6% | 0.73 |
| Llama 3.3 70B | 81.5% | 0.71 |
| Llama 3.1 8B | 75.3% | 0.62 |
