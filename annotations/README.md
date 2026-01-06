# Annotation Data

This folder contains the human-annotated ground truth data and model validation results used for the paper.

## Files

| Filename | Description | Rows |
|----------|-------------|------|
| **`human_ground_truth.csv`** | Consolidated human annotations for 500 posts. Includes individual annotator labels and the final consensus label. | 499 |
| **`validation_results.csv`** | Model predictions compared against human ground truth labels (using the V2 prompt). | 501 |
| **`CODEBOOK.md`** | Detailed definitions of the framing categories and annotation guidelines. | - |

## Column Descriptions

### human_ground_truth.csv

- `post_id`: Unique identifier for the Reddit post
- `annotator_1`: Label from first human annotator
- `annotator_2`: Label from second human annotator
- `gold_label`: Final consensus label (Ground Truth)
- `batch`: Annotation batch identifier

### validation_results.csv

- `post_id`: Unique identifier
- `gold_label`: Human consensus label
- `model_prediction`: Label predicted by the model (GPT-4o-mini)
- `confidence_score`: Confidence score of the model prediction
