"""Real 3-stage NGS pipeline: QC filtering (drop low-depth genotype
calls below a usable threshold), genotype calling from allele
fraction, and a per-sample concordance summary -- the real analysis
work the authored bash orchestration script sequences."""
from __future__ import annotations

import pandas as pd

MIN_DEPTH = 15


def qc_stage(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["depth"] >= MIN_DEPTH].copy()


def call_genotype(observed_af: float) -> int:
    if observed_af < 0.2:
        return 0
    elif observed_af < 0.8:
        return 1
    return 2


def call_stage(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["called_genotype"] = df["observed_af"].apply(call_genotype)
    return df


def run_pipeline(raw: pd.DataFrame) -> pd.DataFrame:
    return call_stage(qc_stage(raw))


def compute_concordance(called: pd.DataFrame) -> dict:
    concordant = (called["called_genotype"] == called["true_genotype"]).mean()
    return {"n_calls": len(called), "concordance_pct": round(float(concordant) * 100, 3)}
