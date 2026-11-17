import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_samples import simulate
from src.pipeline_stages import run_pipeline, compute_concordance
from src.validation_suite import run_validation_suite, CHECKS


def test_at_least_800_samples():
    raw = simulate()
    assert raw["sample_id"].nunique() >= 800


def test_18_checks_defined():
    assert len(CHECKS) == 18


def test_concordance_is_high():
    raw = simulate()
    called = run_pipeline(raw)
    concordance = compute_concordance(called)
    assert concordance["concordance_pct"] >= 85.0


def test_validation_suite_first_pass_accuracy_is_high():
    raw = simulate()
    called = run_pipeline(raw)
    validation = run_validation_suite(called)
    assert validation["first_pass_accuracy_pct"] >= 85.0


def test_qc_stage_removes_low_depth_calls():
    raw = simulate()
    called = run_pipeline(raw)
    assert (called["depth"] >= 15).all()
