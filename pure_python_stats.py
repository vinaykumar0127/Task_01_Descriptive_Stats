#!/usr/bin/env python3
"""
Facebook presidential ads — descriptive statistics using Python standard library only.

Equivalent analysis: see pandas_stats.py
"""

from __future__ import annotations

import argparse
import ast
import csv
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# Default: place the CSV from your instructor / data provider under ~/Downloads/
DEFAULT_CSV = Path.home() / "Downloads" / "fb_ads_president_scored_anon.csv"


def parse_dict_field(raw: str) -> dict[str, Any]:
    if not raw or not raw.strip():
        return {}
    s = raw.strip()
    if s.startswith("{") and "'" in s and '"' not in s[:20]:
        s = s.replace("'", '"')
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return {}


def spend_midpoint(spend_raw: str) -> float | None:
    d = parse_dict_field(spend_raw)
    if not d:
        return None
    try:
        lo = int(d["lower_bound"])
    except (KeyError, ValueError, TypeError):
        return None
    hi_raw = d.get("upper_bound")
    if hi_raw is None:
        return float(lo)
    try:
        hi = int(hi_raw)
    except (ValueError, TypeError):
        return float(lo)
    return (lo + hi) / 2.0


def parse_mentions(raw: str) -> list[str]:
    if not raw or not raw.strip():
        return []
    s = raw.strip()
    if s.startswith("[") and "'" in s:
        s = s.replace("'", '"')
    try:
        v = ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return []


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def population_std(xs: list[float]) -> float:
    """Population std (divide by n); matches pandas .std(ddof=0)."""
    if not xs:
        return float("nan")
    m = mean(xs)
    var = sum((x - m) ** 2 for x in xs) / len(xs)
    return math.sqrt(var)


def sample_std(xs: list[float]) -> float:
    """Sample std (divide by n-1); matches pandas .std() default."""
    n = len(xs)
    if n < 2:
        return float("nan")
    m = mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (n - 1)
    return math.sqrt(var)


def top_n(counter: Counter[str], n: int) -> list[tuple[str, int]]:
    return counter.most_common(n)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyze(path: Path) -> None:
    rows = load_rows(path)
    spend_midpoints: list[float] = []
    by_page: defaultdict[str, float] = defaultdict(float)
    candidate_mentions = Counter()
    by_week: defaultdict[tuple[int, int], float] = defaultdict(float)

    for row in rows:
        sm = spend_midpoint(row.get("spend", ""))
        if sm is not None:
            spend_midpoints.append(sm)
            page = (row.get("page_name") or "").strip() or "(unknown page)"
            by_page[page] += sm
        for name in parse_mentions(row.get("illuminating_mentions", "")):
            candidate_mentions[name] += 1
        day_raw = (row.get("ad_delivery_start_time") or "").strip()
        if day_raw and sm is not None:
            try:
                dt = datetime.strptime(day_raw[:10], "%Y-%m-%d")
                y, w, _ = dt.isocalendar()
                by_week[(y, w)] += sm
            except ValueError:
                pass

    n = len(spend_midpoints)
    xs = spend_midpoints
    smin = min(xs) if xs else float("nan")
    smax = max(xs) if xs else float("nan")
    mu = mean(xs) if xs else float("nan")
    sd_sample = sample_std(xs)
    sd_pop = population_std(xs)

    print("=== Facebook presidential ads (pure Python / stdlib) ===")
    print(f"CSV: {path}")
    print(f"Rows (records): {len(rows)}")
    print()
    print("--- Spend midpoint (USD) per ad row ---")
    print(f"  count:                 {n}")
    print(f"  mean:                  {mu:.4f}")
    print(f"  min:                   {smin:.4f}")
    print(f"  max:                   {smax:.4f}")
    print(f"  std (sample, ddof=1):  {sd_sample:.4f}")
    print(f"  std (population):      {sd_pop:.4f}")
    print()

    print("--- Top 15 pages by total estimated spend (sum of midpoints) ---")
    for page, total in sorted(by_page.items(), key=lambda x: -x[1])[:15]:
        print(f"  {total:,.2f}  {page[:70]}")
    print()

    print("--- Candidate mention frequency (rows mentioning each name) ---")
    for name, cnt in top_n(candidate_mentions, 20):
        print(f"  {cnt:6d}  {name}")
    print()

    print("--- Weekly spend (midpoint sum) by ISO calendar week (ad_delivery_start_time) ---")
    for (y, w), tot in sorted(by_week.items()):
        print(f"  {y}-W{w:02d}  {tot:,.2f}")
    print()
    print("Done.")


def main() -> None:
    p = argparse.ArgumentParser(description="FB ads stats (stdlib only)")
    p.add_argument(
        "csv_path",
        nargs="?",
        default=str(DEFAULT_CSV),
        help=f"Path to CSV (default: {DEFAULT_CSV})",
    )
    args = p.parse_args()
    path = Path(args.csv_path).expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")
    analyze(path)


if __name__ == "__main__":
    main()
