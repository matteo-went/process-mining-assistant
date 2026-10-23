"""Lädt das BPI-2017-Event-Log (XES) und speichert es als Parquet."""
from pathlib import Path

import pm4py

PROJECT_ROOT = Path(__file__).resolve().parent.parent
XES_FILE = PROJECT_ROOT / "data" / "raw" / "BPI Challenge 2017.xes.gz"
PARQUET_FILE = PROJECT_ROOT / "data" / "processed" / "bpi2017.parquet"


def load_xes():
    df = pm4py.read_xes(str(XES_FILE))
    return df


def check(df):
    n_events = len(df)
    n_cases = df["case:concept:name"].nunique()
    print(f"Events: {n_events:,} | Cases: {n_cases:,}")
    assert n_events == 1_202_267, "Unerwartete Anzahl Events"
    assert n_cases == 31_509, "Unerwartete Anzahl Cases"


def save_parquet(df):
    df.to_parquet(PARQUET_FILE, index=False)
    print(f"Gespeichert: {PARQUET_FILE}")


if __name__ == "__main__":
    df = load_xes()
    check(df)
    save_parquet(df)