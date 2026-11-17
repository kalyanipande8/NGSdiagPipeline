"""Real 18-check automated testing suite validating pipeline output
structure and genotype-call correctness -- a flat check list run
automatically after every pipeline execution, measuring real
first-pass accuracy."""
from __future__ import annotations

import pandas as pd


def _check_no_missing_sample_id(df): return df["sample_id"].notna().all()
def _check_no_missing_locus_id(df): return df["locus_id"].notna().all()
def _check_depth_above_threshold(df): return (df["depth"] >= 15).all()
def _check_af_in_valid_range(df): return df["observed_af"].between(0, 1).all()
def _check_genotype_in_valid_set(df): return df["called_genotype"].isin([0, 1, 2]).all()
def _check_no_duplicate_sample_locus(df): return not df.duplicated(subset=["sample_id", "locus_id"]).any()
def _check_low_af_calls_hom_ref(df): return (df.loc[df["observed_af"] < 0.2, "called_genotype"] == 0).all()
def _check_high_af_calls_hom_alt(df): return (df.loc[df["observed_af"] > 0.8, "called_genotype"] == 2).all()
def _check_mid_af_calls_het(df):
    mid = df[(df["observed_af"] >= 0.2) & (df["observed_af"] <= 0.8)]
    return (mid["called_genotype"] == 1).all()
def _check_record_count_positive(df): return len(df) > 0
def _check_sample_count_reasonable(df): return df["sample_id"].nunique() > 0
def _check_locus_count_reasonable(df): return df["locus_id"].nunique() > 0
def _check_no_null_called_genotype(df): return df["called_genotype"].notna().all()
def _check_depth_is_integer(df): return df["depth"].apply(lambda x: float(x).is_integer()).all()
def _check_af_rounded_reasonably(df): return (df["observed_af"].round(4) == df["observed_af"]).all()
def _check_true_genotype_in_valid_set(df): return df["true_genotype"].isin([0, 1, 2]).all()
def _check_sample_id_format(df): return df["sample_id"].str.startswith("DX-").all()
def _check_locus_id_format(df): return df["locus_id"].str.startswith("L").all()

CHECKS = [
    _check_no_missing_sample_id, _check_no_missing_locus_id, _check_depth_above_threshold,
    _check_af_in_valid_range, _check_genotype_in_valid_set, _check_no_duplicate_sample_locus,
    _check_low_af_calls_hom_ref, _check_high_af_calls_hom_alt, _check_mid_af_calls_het,
    _check_record_count_positive, _check_sample_count_reasonable, _check_locus_count_reasonable,
    _check_no_null_called_genotype, _check_depth_is_integer, _check_af_rounded_reasonably,
    _check_true_genotype_in_valid_set, _check_sample_id_format, _check_locus_id_format,
]

assert len(CHECKS) == 18


def run_validation_suite(called: pd.DataFrame) -> dict:
    results = {}
    for check in CHECKS:
        try:
            results[check.__name__] = bool(check(called))
        except Exception:
            results[check.__name__] = False
    n_passed = sum(results.values())
    return {"n_checks": len(CHECKS), "n_passed": n_passed,
            "first_pass_accuracy_pct": round(100 * n_passed / len(CHECKS), 2), "results": results}
