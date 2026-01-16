# Asymmetric Persistence in Online Framing of North Korea


## 📁 Repository Structure

```
.
├── annotations/          # Human-annotated validation data
├── final/               # Main datasets (posts + comments)
├── results/             # Analysis outputs and graph data
├── graphrag_config/     # Custom GraphRAG configuration
└── reproduction_scripts/  # Code to reproduce key analyses
```

---

## 📊 Data Files

### 1️⃣ Main Datasets (`final/`)

| File | Description | Rows |
|------|-------------|------|
| **final_dataset.csv** | Reddit posts (treatment + controls) with framing labels, sentiment scores | 34,929 |
| **comment_ids.csv** | Comment IDs (recursive) with metadata for Arctic Shift retrieval | 255,391 |

> **Note:** `final_dataset.csv` contains 34,929 posts (raw). Paper analyses use:
> - **Table 1 (DiD):** 29,688 posts (after filtering)
> - **High-confidence:** 27,863 posts (confidence ≥ 0.9)

---

### 2️⃣ Human Validation (`annotations/`)

| File | Description | Rows |
|------|-------------|------|
| **human_ground_truth.csv** | Gold-standard annotations (Pilot + Batch 1 + 2) | 500 |
| **validation_results.csv** | GPT-4o-mini vs human expert comparison | 500 |
| **CODEBOOK.md** | Framing category definitions and guidelines | - |

---

### 3️⃣ Analysis Results (`results/`)

#### Cross-LLM Validation
| File | Description | Rows |
|------|-------------|------|
| **cross_llm_framing.csv** | 6 models × 500 posts validation | 500 |

Models: GPT-4o-mini, GPT-4o, Claude Sonnet 4.5, Claude Haiku 4.5, Llama 3.3 70B, Llama 3.1 8B

#### DiD & Statistical Analyses
| File | Description |
|------|-------------|
| **did_results_main.json** | Core Difference-in-Differences estimates |
| **framing_did_consolidated.json** | Detailed framing DiD statistics |
| **sentiment_did_consolidated.json** | Detailed sentiment DiD statistics |

#### Graph Network Analysis

**Post-level (discourse networks from posts):**
| File | Description | Rows |
|------|-------------|------|
| **post_edge_framing_p1.csv** | Pre-Singapore edges (relationships) | 4,838 |
| **post_edge_framing_p2.csv** | Singapore-Hanoi edges | 1,838 |
| **post_edge_framing_p3.csv** | Post-Hanoi edges | 1,530 |
| **post_community_framing.csv** | Community clusters across periods | 614 |

**Comment-level (discourse networks from comments):**
| File | Description | Rows |
|------|-------------|------|
| **comment_edge_framing_p1.csv** | Pre-Singapore comment edges | 10,730 |
| **comment_edge_framing_p2.csv** | Singapore-Hanoi comment edges | 3,612 |
| **comment_edge_framing_p3.csv** | Post-Hanoi comment edges | 4,522 |
| **comment_community_framing_p1.csv** | Pre-Singapore communities | 746 |
| **comment_community_framing_p2.csv** | Singapore-Hanoi communities | 231 |
| **comment_community_framing_p3.csv** | Post-Hanoi communities | 371 |

#### Narrative Reports
| File | Description |
|------|-------------|
| **graphrag_analysis_results.json** | GraphRAG community detection results |
| **GRAPHRAG_REPORTS_CONSOLIDATED.md** | Textual analysis summaries |

---

### 4️⃣ GraphRAG Configuration (`graphrag_config/`)

Custom configuration for discourse network analysis:

```
graphrag_config/
├── settings.yaml           # Pipeline settings (model, chunking, etc.)
└── prompts/               # 13 custom extraction prompts
    ├── extract_graph.txt  # Entity extraction (+ WEAPON, POLICY types)
    └── ...
```

**Key Customization:** Extended entity types to include `WEAPON` (e.g., ICBM) and `POLICY` (e.g., denuclearization) for security domain analysis.

---

### 5️⃣ Reproduction Scripts (`reproduction_scripts/`)

| Script | Description |
|--------|-------------|
| **analyze_did.py** | Reproduce main DiD tables (Framing & Sentiment) |

---

## 📋 What's Included

✅ **Preserved columns:**
- `id` / `post_id` / `comment_id`: Reddit identifiers
- `subreddit`, `created_utc`: Metadata
- `frame`, `frame_confidence`: Framing labels (LLM predicted)
- `sentiment_score`: Sentiment analysis scores
- `period`, `country`: Analysis periods and country tags

❌ **Removed columns (anonymization):**
- `title`, `selftext`, `body`: Original text content
- `frame_reason`: LLM reasoning text
- `description`: Edge/community descriptions

---

## 🔗 Retrieving Original Text

To retrieve original post/comment text, use **Arctic Shift** with the preserved IDs:

**Arctic Shift:** [https://github.com/ArthurHeitmann/arctic_shift](https://github.com/ArthurHeitmann/arctic_shift)

Query their archive using `post_id` or `id` columns from the datasets.

---

## 📈 Cross-LLM Validation Summary

Agreement with GPT-4o-mini (N=500):

| Model | Agreement | Cohen's κ |
|-------|-----------|-----------|
| GPT-4o | 85.7% | 0.78 |
| Claude Sonnet 4.5 | 84.0% | 0.76 |
| Claude Haiku 4.5 | 81.6% | 0.73 |
| Llama 3.3 70B | 81.5% | 0.71 |
| Llama 3.1 8B | 75.3% | 0.62 |

High cross-family consistency (OpenAI, Anthropic, Meta) validates robustness of framing classifications.
