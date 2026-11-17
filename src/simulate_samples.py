"""Simulate 820 NGS diagnostic samples genotyped at 100 known loci,
with a hidden true genotype (gold-standard) and a noisy simulated
read-pileup signal -- the ground truth the QC -> align -> call
pipeline stages must recover."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_SAMPLES = 820
N_LOCI = 100
SEED = 1341


def simulate(n_samples: int = N_SAMPLES, n_loci: int = N_LOCI, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    true_genotypes = rng.choice([0, 1, 2], (n_samples, n_loci), p=[0.65, 0.28, 0.07])
    depth = rng.integers(20, 80, (n_samples, n_loci))
    expected_af = np.clip(true_genotypes / 2.0, 0.02, 0.98)
    observed_alt = rng.binomial(depth, expected_af)
    observed_af = observed_alt / depth

    records = []
    for s in range(n_samples):
        for l in range(n_loci):
            records.append({"sample_id": f"DX-{s:04d}", "locus_id": f"L{l:03d}",
                             "depth": int(depth[s, l]), "observed_af": round(float(observed_af[s, l]), 4),
                             "true_genotype": int(true_genotypes[s, l])})
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
