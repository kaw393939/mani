# Classification and Verification Process

This document outlines the process used to classify, verify, and enrich the bibliographic data for the project. The goal is to transform raw classification data into a verified dataset with human-readable reasoning for each entry.

## 1. Input Data Source
The process begins with the `data/processed/classified_papers.csv` file. This file contains a collection of academic papers that have been preliminarily classified into specific categories based on their content.

### Input Schema
| Column | Description |
|--------|-------------|
| `DOI` | Digital Object Identifier for the paper. |
| `Year` | Publication year. |
| `Title` | Title of the paper. |
| `Primary_Class` | ID of the primary classification category. |
| `Primary_Desc` | Description of the primary classification. |
| `Secondary_Class` | ID of the secondary classification category. |
| `Secondary_Desc` | Description of the secondary classification. |
| `Tertiary_Class` | ID of the tertiary classification category. |
| `Tertiary_Desc` | Description of the tertiary classification. |
| `Confidence_Score` | A numerical score indicating the confidence of the initial classification. |
| `Abstract` | The full abstract of the paper. |

## 2. Verification and Enrichment Process
The core of the workflow involves an automated agent (AI) that processes the input file row by row to verify the relevance of the papers and generate a concise summary.

### Step-by-Step Workflow
1.  **Batch Processing**: The system reads the input CSV in batches (e.g., 50-150 rows) to manage memory and context window limits.
2.  **Analysis**: For each paper, the AI analyzes the `Title` and `Abstract`.
3.  **Reasoning Generation**: The AI generates a **"Reasoning"** field. This is a single, concise sentence that summarizes *why* the paper is relevant or what its specific contribution is. This serves as a verification step to ensure the content matches the classification.
4.  **Appending**: The processed rows, now including the new "Reasoning" column, are appended to the output file.

## 3. Output Data
The result is stored in `data/processed/verified_classification_sample.csv`. This file serves as the "Golden Set" or verified sample for downstream tasks.

### Output Schema
The output file retains all columns from the input file and adds one key column:

| Column | Description |
|--------|-------------|
| ... | *[All columns from Input Schema]* |
| `Reasoning` | A generated 1-sentence summary justifying the paper's inclusion and content. |

## 4. Classification Categories
The papers are categorized into specific domains related to ferrofluids and magnetic materials. Common categories include:
- **Computation**: Stability analysis, CFD, magnetic droplets.
- **Experimentation**: General evaluation, specific physical properties.
- **Instrumentation**: Devices using or measuring ferrofluids.
- **Applications**: Heat transfer, medical (hyperthermia, drug delivery), sealing, damping, etc.

## 5. Usage
To run or resume the classification process, the system:
1.  Checks the last processed line in `verified_classification_sample.csv`.
2.  Reads the next batch from `classified_papers.csv`.
3.  Generates reasoning for the new batch.
4.  Appends the results to the verified file.
