# Findings: Facebook Presidential Ads (2024)

This note summarizes patterns that emerge when you run `pure_python_stats.py` and `pandas_stats.py` on the scored, anonymized Facebook ads extract (`fb_ads_president_scored_anon.csv`). Exact numbers depend on the file version you use; the structure of the story should stay similar.

## Scale and spend shape

The dataset contains on the order of **hundreds of thousands** of ad rows—large enough that manual spreadsheet review is impractical and programmatic summaries are necessary. Meta reports **spend as an interval**, not an exact dollar amount. Using the **midpoint** of each interval is a simple, transparent way to turn ranges into numbers for means and standard deviations. Readers should remember that **all dollar figures are estimates** derived from those ranges, not audited invoices.

Per-row spend midpoints typically show a **strong right skew**: many ads sit in modest spend buckets, while a smaller number of rows sit in very large upper bounds. That pattern shows up as a **mean** in the low thousands of dollars (USD) per row but a **standard deviation** that is several times larger than what you would see under a symmetric distribution—evidence that a few high-spend placements pull the scale upward. **Minimum and maximum** midpoints illustrate the full spread from small tests to very large buys.

## Who spends at the page level

Aggregating midpoints by **`page_name`** highlights which **pages** (often candidate accounts, party committees, or PAC-style entities) account for the bulk of estimated spend in this slice of data. In a full run on the class file, **major-party presidential campaigns and national party brands** tend to dominate the top ranks, with additional large totals for **PACs, unions, and national media or advocacy pages** that bought significant inventory. This answers “who spent how much” at the level Meta exposes (page identity), not at the level of undisclosed donors inside a PAC.

## Which candidates appear in the text

The **`illuminating_mentions`** field encodes which candidates are referenced. A **frequency table** of mention strings shows who appears most often in ad text in this corpus. You will often see **multiple string variants** for the same person (for example, a last name versus “President …”). Those variants are counted separately unless you normalize names in a follow-on step—so the table reflects **literal string frequency**, not a perfect person-level census.

## Spending over time

Grouping by **ISO week** of **`ad_delivery_start_time`** shows how estimated spend **rises and falls** across the election cycle. Earlier calendar years in the file, if present, usually correspond to **small long-tail** activity or early testing; the **largest weekly totals** tend to cluster in the months leading up to November 2024. That temporal view supports a clear story: digital political spend is **concentrated in time**, not evenly distributed across weeks.

## Limitations (brief)

- Midpoints **understate uncertainty** inside each Meta range.
- **Mentions** are not weighted by spend; a cheap ad counts as much as an expensive one for mention frequency.
- **Page names** can change or be shared across entities; interpret “who spent” as **Meta page-level**, not necessarily legal contributor-level.

Together, these points still yield a useful first-pass picture of **scale, actors, targeting language, and timing** in a major digital political ad corpus.
