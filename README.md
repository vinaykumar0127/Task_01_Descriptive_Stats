# Task 01: Descriptive Statistics (Pure Python vs Pandas)

This repository compares **two equivalent analyses** of a Facebook political advertising dataset from the **2024 U.S. presidential** period: one script uses **only the Python standard library**; the other uses **Pandas**. Both print the same categories of descriptive statistics so you can verify they agree.

**Do not commit the dataset.** This repo is intended for code and documentation only.

## Project description

Each row in the CSV represents an ad placement that references one or more presidential candidates. The analysis:

1. Derives a **numeric spend** per row from Meta’s **range** fields (`lower_bound` / `upper_bound` in USD) using the **midpoint** \((\text{lower} + \text{upper}) / 2\).
2. Reports **count, mean, min, max**, and **standard deviation** (sample with `ddof=1` and population with `ddof=0`) on those midpoints.
3. Ranks **advertiser pages** (`page_name`) by **total** estimated spend (sum of midpoints).
4. Builds a **frequency distribution** of **candidate names** parsed from `illuminating_mentions`.
5. Aggregates estimated spend by **ISO calendar week** of `ad_delivery_start_time` to show how spending moves over time.

## Data source

**Dataset download:** [fb_ads_president_scored_anon.zip on Google Drive](https://drive.google.com/file/d/1gvtvX8fATFrrzraPmTSf205U8u3JExUR/view).


## Dependencies

- **Pure Python script:** Python 3.9+ (stdlib only: `csv`, `ast`, `math`, `collections`, etc.).
- **Pandas script:** install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## How to run

From the repository root:

```bash
python3 pure_python_stats.py
python3 pandas_stats.py
```

Or specify the CSV explicitly:

```bash
python3 pure_python_stats.py /path/to/fb_ads_president_scored_anon.csv
python3 pandas_stats.py /path/to/fb_ads_president_scored_anon.csv
```

On the same input file, both scripts should produce **matching** numeric summaries (counts, means, extremes, standard deviations, grouped totals, and weekly sums).

## Written analysis

- **[FINDINGS.md](FINDINGS.md)** — narrative summary of patterns and insights in the data (about 1–2 pages).
- **[COMPARISON.md](COMPARISON.md)** — reflection on pure Python vs Pandas: tradeoffs, pros, and cons.

