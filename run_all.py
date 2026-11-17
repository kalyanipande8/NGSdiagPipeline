import json
import os

from src.simulate_samples import simulate
from src.pipeline_stages import run_pipeline, compute_concordance
from src.validation_suite import run_validation_suite


def main():
    raw = simulate()
    called = run_pipeline(raw)
    concordance = compute_concordance(called)
    validation = run_validation_suite(called)

    summary = {"n_samples": raw["sample_id"].nunique(), "concordance": concordance,
               "validation": {"n_checks": validation["n_checks"],
                              "first_pass_accuracy_pct": validation["first_pass_accuracy_pct"]}}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
