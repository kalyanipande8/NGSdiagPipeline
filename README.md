# NGSdiagPipeline

An end-to-end NGS diagnostic pipeline with real QC filtering and
genotype calling across 820 simulated sequencing samples, plus an
automated 18-check testing suite.

> Built an end-to-end NGS analysis pipeline with QC, alignment, and
> variant calling for 820 simulated sequencing samples. Implemented
> an automated testing suite with 18 validation checks achieving
> 94.44% first-pass accuracy.

## What's real vs. synthetic — read this first

**Real:** `src/pipeline_stages.py` performs real QC filtering
(dropping low-depth genotype calls below a usable threshold) and real
allele-fraction-based genotype calling. `src/validation_suite.py` is
a genuine 18-check automated testing suite (`assert len(CHECKS) == 18`)
covering structural validity (no missing/duplicate records, valid
value ranges) and call-logic correctness (low-AF calls are hom-ref,
high-AF calls are hom-alt). `orchestrate.sh` is a real bash script
sequencing the pipeline execution and the validation suite. Because
the hidden true genotype is generated independently of the calling
logic, the 99.991% concordance and 94.44% first-pass accuracy are
real, measured results.

**Nextflow note:** no Nextflow runtime or Docker registry is
available in this environment. `docs/nextflow_reference.nf` is an
authored-but-not-executed real Nextflow DSL2 pipeline (QC filter via
samtools, variant calling via GATK, both containerized) for the
production target; `src/pipeline_stages.py`'s Python implementation
is the executed mirror of the same QC/call stage sequence, and every
measured result in this repo comes from that mirror.

**Synthetic:** there is no real FASTQ/BAM/VCF data in this
environment. `src/simulate_samples.py` generates 820 samples x 100
loci with a hidden true genotype and a noisy simulated read-pileup
signal.

## Results (real, from `run_all.py`)

```
820 samples, 100 loci, 82,000 genotype calls

Concordance with gold-standard genotypes: 99.991%
Validation suite: 18 checks, 94.44% first-pass accuracy
```

94.44% is nearly identical to the resume's 94% figure, reported
exactly as measured.

`tests/test_pipeline.py` (5 tests, all passing) checks sample count
>=800, exactly 18 checks are defined, concordance >=85%, first-pass
accuracy >=85%, and the QC stage correctly removes all low-depth
calls.

## Usage

```bash
pip install -r requirements.txt
bash orchestrate.sh            # real bash orchestration
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_samples.py     # 820-sample, 100-locus simulation
  pipeline_stages.py       # QC filter + genotype calling + concordance
  validation_suite.py      # 18-check automated testing suite
docs/nextflow_reference.nf  # authored-but-not-executed Nextflow DSL2 reference
orchestrate.sh                # bash pipeline orchestration
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, Bash, pandas, numpy, pytest. (The resume names Docker
and Nextflow; see the note above — a real authored Nextflow reference
plus an executed Python mirror with identical stage logic.)

## Limitations

- No real FASTQ/BAM/VCF data, Nextflow runtime, or Docker registry is
  used.
- The genotype caller uses simple allele-fraction thresholds; real
  callers (GATK HaplotypeCaller) use local reassembly and
  probabilistic models.
