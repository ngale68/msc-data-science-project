# Multimodal Extraction of Financial Metrics from UK Companies House Annual Accounts

MSc Data Science project, Birkbeck, University of London.

## Research question

Does combining table and narrative evidence improve the extraction of selected financial metrics from UK Companies House annual accounts compared with table-only and narrative-only approaches?

## Target metrics

- Turnover/revenue
- Profit before tax
- Total assets
- Net assets

## Experimental systems

1. Table-only
2. Text-only
3. Multimodal fusion

## Main evaluation

The primary evaluation unit is a complete financial record consisting of:

- metric
- value
- unit
- reporting period

Primary metrics:

- Precision
- Recall
- Micro-F1

Secondary analysis:

- Macro-F1
- Per-metric performance
- Field-level performance
- Error analysis
- Bootstrap uncertainty

## Project structure

- `data/` — datasets and annotations
- `notebooks/` — exploratory analysis
- `src/` — reusable Python code
- `configs/` — experiment configuration
- `results/` — experimental outputs
- `dissertation/` — dissertation materials