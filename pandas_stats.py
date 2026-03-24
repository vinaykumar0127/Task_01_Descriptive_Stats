#!/usr/bin/env python3
"""
Facebook presidential ads — same analysis as pure_python_stats.py using Pandas.
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

import pandas as pd

DEFAULT_CSV = Path.home() / "Downloads" / "fb_ads_president_scored_anon.csv"


def parse_dict_field(raw: str) -> dict:
    if not raw or not (s := raw.strip()):
        return {}
    if s.startswith("{") and "'" in s and '"' not in s[:20]:
        s = s.replace("'", '"')
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return {}


def spend_midpoint_series(spend_col: pd.Series) -> pd.Series:
    def one(cell: str) -> float | None:
        d = parse_dict_field(str(cell) if pd.notna(cell) else "")
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

    return spend_col.map(one)


def parse_mentions_list(raw: str) -> list[str]:
    if not raw or not str(raw).strip():
        return []
    s = str(raw).strip()
    if s.startswith("[") and "'" in s:
        s = s.replace("'", '"')
    try:
        v = ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return []


def analyze(path: Path) -> None:
    df = pd.read_csv(path, low_memory=False)
    df["spend_mid"] = spend_midpoint_series(df["spend"])
    valid = df["spend_mid"].notna()
    spend = df.loc[valid, "spend_mid"]

    print("=== Facebook presidential ads (Pandas analysis) ===")
    print(f"CSV: {path}")
    print(f"Rows (records): {len(df)}")
    print()
    print("--- Spend midpoint (USD) per ad row ---")
    print(f"  count:                 {int(spend.count())}")
    print(f"  mean:                  {spend.mean():.4f}")
    print(f"  min:                   {spend.min():.4f}")
    print(f"  max:                   {spend.max():.4f}")
    print(f"  std (sample, ddof=1):  {spend.std(ddof=1):.4f}")
    print(f"  std (population):      {spend.std(ddof=0):.4f}")
    print()

    by_page = (
        df.loc[valid]
        .groupby(df.loc[valid, "page_name"].fillna("(unknown page)").str.strip())["spend_mid"]
        .sum()
        .sort_values(ascending=False)
    )
    print("--- Top 15 pages by total estimated spend (sum of midpoints) ---")
    for page, total in by_page.head(15).items():
        p = page[:70] if isinstance(page, str) else str(page)[:70]
        print(f"  {total:,.2f}  {p}")
    print()

    mentions_exploded = (
        df["illuminating_mentions"]
        .fillna("")
        .map(parse_mentions_list)
        .explode()
    )
    mentions_exploded = mentions_exploded[mentions_exploded.astype(str).str.len() > 0]
    vc = mentions_exploded.value_counts()
    print("--- Candidate mention frequency (rows mentioning each name) ---")
    for name, cnt in vc.head(20).items():
        print(f"  {int(cnt):6d}  {name}")
    print()

    dfp = df.loc[valid].copy()
    dfp["dt"] = pd.to_datetime(dfp["ad_delivery_start_time"], errors="coerce")
    ic = dfp["dt"].dt.isocalendar()
    dfp = dfp.assign(_iy=ic["year"], _iw=ic["week"])
    weekly = (
        dfp.dropna(subset=["dt"])
        .groupby(["_iy", "_iw"], sort=True)["spend_mid"]
        .sum()
    )
    print("--- Weekly spend (midpoint sum) by ISO calendar week (ad_delivery_start_time) ---")
    for (y, w), tot in weekly.items():
        print(f"  {int(y)}-W{int(w):02d}  {tot:,.2f}")
    print()
    print("Done.")


def main() -> None:
    p = argparse.ArgumentParser(description="FB ads stats (Pandas)")
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
