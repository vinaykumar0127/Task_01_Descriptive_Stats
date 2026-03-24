# Comparison: Pure Python vs Pandas

This project implements the **same analysis twice**: `pure_python_stats.py` (standard library only) and `pandas_stats.py` (Pandas). Below is a concise reflection on how the two approaches differ and when each shines.

## Correctness and transparency

**Pure Python** makes every step visible: read a row, parse fields, append to lists or update dictionaries, compute mean and standard deviation with explicit loops or formulas. That is ideal for **learning** and for **proving** that you understand the statistics—you cannot hide a degree-of-freedom mistake inside a one-liner.

**Pandas** expresses the same logic through **column operations** (`groupby`, `value_counts`, `std(ddof=…)`). The code is shorter, but you must still **choose** the same conventions (for example, sample vs population standard deviation) or your results will diverge from the stdlib script.

## Dependencies and reproducibility

**Pure Python** has **no third-party installs**, which simplifies grading environments and long-term reproducibility on minimal systems.

**Pandas** (and its **NumPy** stack) is a **heavy dependency** but is the **de facto** standard for tabular data in Python. For real workflows, that trade is usually worth it.

## Performance and ergonomics

For roughly **250k rows**, both approaches are fast enough on a typical laptop. **Pandas** will often win on **larger** tables or more complex joins because core operations run in compiled code. **Pure Python** stays acceptable here but would require more care (chunking, generators) at **very large** scale.

Ergonomically, **Pandas** reduces boilerplate: one `read_csv`, one `groupby`, one `explode` for list-like mention fields. **Pure Python** needs more lines for the same grouping and counting, which can mean more places to introduce bugs—but also **full control** over memory (for example, streaming row-by-row if you refactored to a generator-based pipeline).

## Debugging and data quality

When something is wrong—bad parsing, unexpected nulls—**Pandas** makes it easy to **spot-check columns** and filter interactively in a notebook. **Pure Python** debugging is straightforward but more **manual** (print keys, assert invariants).

## Summary recommendation

Use **pure Python** when you need **zero dependencies**, maximum **pedagogical clarity**, or a **reference implementation** to validate a library. Use **Pandas** when you want **speed of development**, **exploratory analysis**, or integration with **plotting and modeling** downstream. In this assignment, running **both** and checking that outputs match is the best of both worlds: you practice **foundations** and **professional tooling** side by side.
