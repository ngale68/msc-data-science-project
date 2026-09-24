# Corpus Selection Protocol

## Purpose

Define the criteria used to construct the discovery corpus for the extraction experiments. The protocol is intended to provide a consistent and reproducible basis for screening Companies House annual accounts.

## Inclusion criteria

A filing is eligible for the discovery corpus if:

1. It is an electronically filed Companies House accounts document available as usable HTML/iXBRL.
2. The document can be parsed successfully and contains usable visible financial-account information.
3. The reporting period can be identified from evidence within the filing.
4. The filing contains sufficient financial-statement and/or narrative content to support meaningful annotation of the selected target metrics.

## Exclusion criteria

A filing is excluded if:

- the HTML/iXBRL content cannot be parsed or is unusable;
- the reporting period cannot be identified;
- the document contains insufficient financial information to support meaningful annotation of the target metrics;
- it is a duplicate of another filing selected for the corpus.

Dormant-company status is not, by itself, an exclusion criterion. However, dormant or other minimal accounts may be excluded where their limited financial content does not provide sufficient evidence for the extraction task.

## Reporting-period identification

The reporting period should be established from the filing itself rather than inferred solely from the filename.

Relevant evidence may include expressions such as:

- `year ended [date]`
- `period ended [date]`
- `as at [date]`

The filename reporting-period field is retained as metadata but is not treated as the sole evidence of the accounting period.

## Metric feasibility

The four initial target concepts are:

- turnover/revenue
- profit before taxation
- total assets
- net assets

Preliminary keyword or terminology matching is used only for discovery and feasibility assessment. A filing is not excluded solely because a simple lexical search fails to identify a metric.

Final metric availability will be determined during annotation.

A target metric will be replaced or removed if it appears in fewer than 25% of eligible development filings or produces fewer than 20 target records in the development set, as specified in the project proposal.

## Corpus and split

The discovery corpus is expected to contain approximately 250–400 eligible filings.

From this corpus, approximately 80–100 filings will be manually annotated:

- 30–40 development filings
- 50–60 frozen test filings

Where feasible, sampling will be stratified by reporting year and filing structure.

All filings from the same company will remain within the same split. The test set will be selected and frozen before refinement of extraction rules, dictionaries, or fusion weights.

## Screening principle

The screening process prioritises suitability for the research question rather than superficial structural characteristics. In particular, HTML table count, file size and exact keyword counts are not used as standalone eligibility criteria.