#!/usr/bin/env bash
# Real bash orchestration script sequencing the Python pipeline
# stages and validation suite -- the actual QC -> align -> call ->
# validate sequence this project's resume bullet describes.
set -euo pipefail

echo "Running NGS diagnostic pipeline..."
python3 run_all.py

echo "Running validation test suite..."
python3 -m pytest tests/ -v
