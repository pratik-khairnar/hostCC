# Host Congestion Control (hostCC) Simulation Project

This repository contains a Python software simulation of the host congestion control (hostCC) idea that was originally implemented in hardware. The project models packet flow through a sender, network queue, NIC buffer, host queue, and a background local memory application, then compares three variants of the control strategy:

- V1: Normal TCP baseline
- V2: hostCC baseline with host-side congestion awareness
- V3: Improved hostCC with adaptive and predictive control

The goal is to compare throughput, packet loss, CWND evolution, host queue occupancy, and the effect of local memory pressure on packet processing.

## Features

- Step-based simulation with reproducible random seed control
- Modular pipeline for sender, network, NIC, host queue, local app, and controller
- Metrics collection for each step and final summary statistics
- CSV log export for all three versions
- Comparison JSON output for post-run analysis
- Plot generation and detailed analysis script for visual comparison

## Simulation Versions

### V1: Normal TCP

Baseline AIMD-style TCP behavior without host-side congestion awareness. The sender increases CWND when there is no loss and reduces it when packet loss occurs.

### V2: hostCC Baseline

Adds host-side congestion detection using host queue occupancy. When congestion is detected, the sender reduces its sending window and the local application can be throttled.

### V3: Improved hostCC

Extends the baseline hostCC approach with two improvements:

- Adaptive thresholding: the congestion threshold changes with local memory load
- Predictive control: recent queue occupancy history is used to detect congestion earlier

## Repository Structure

```text
config/               Simulation parameters
modules/              Core simulation components
simulation/           V1/V2/V3 simulation implementations
utils/                Logging and metrics helpers
results/              CSV and summary output from runs
logs/                 Per-version simulation logs
run_simulation.py     Main entry point for running all versions
analyze_results.py    Plotting and analysis script
```

## Requirements

The project uses Python 3 and the packages listed in `requirements.txt`:

- pandas
- numpy
- matplotlib
- seaborn

> Note: the repository does not include a virtual environment. You can run it directly with your system Python or create a venv first.

## Setup

1. Clone the repository.
2. Open a terminal in the project root.
3. Install dependencies:

```powershell
pip install -r requirements.txt
```

If you want an isolated environment, create and activate a virtual environment before installing packages.

## Run The Simulation

Run all three versions and generate metrics, logs, and a comparison summary:

```powershell
python run_simulation.py
```

This creates or updates:

- `results/v1_metrics.csv`
- `results/v2_metrics.csv`
- `results/v3_metrics.csv`
- `results/comparison_summary.json`
- `logs/v1_log.txt`
- `logs/v2_log.txt`
- `logs/v3_log.txt`

## Analyze Results

After the simulation finishes, generate plots and detailed analysis:

```powershell
python analyze_results.py
```

This script reads the CSV outputs and writes comparison plots into `results/`, including:

- `results/comprehensive_comparison.png`
- `results/metric_*.png`

## Configuration

All tunable parameters live in `config/parameters.py`, including:

- simulation duration
- CWND and AIMD settings
- network capacity, delay, and loss rate
- NIC and host queue sizes
- local memory load behavior
- hostCC thresholding and prediction settings

The main runner copies these values into a config dictionary before starting each simulation version.

## Output Summary

Each run records:

- total packets sent and acknowledged
- total packets dropped and packet loss rate
- throughput in packets per step
- average RTT
- host queue occupancy statistics
- CWND statistics
- controller threshold and congestion events

## Notes

- The code is designed as a software approximation of the hardware hostCC idea.
- Results are reproducible because the simulation uses a fixed random seed by default.
- If you regenerate the outputs, the files in `results/` and `logs/` will be updated.

## Future Work

- Add a real report summary section with the final measured results
- Add a requirements lock file or pinned environment setup if you want fully repeatable installs
- Add notebooks or scripts for comparing results across multiple runs

This is a Python-based simulation of the hostCC research paper concepts.
It implements three versions of congestion control to compare their effectiveness.

To run the simulations:
    python run_simulation.py

This will generate:
    - results/v1_metrics.csv (Version 1: Normal TCP)
    - results/v2_metrics.csv (Version 2: hostCC Baseline)
    - results/v3_metrics.csv (Version 3: Improved hostCC)
    - results/comparison_summary.json
    - logs/v1_log.txt, logs/v2_log.txt, logs/v3_log.txt

Edit config/parameters.py to adjust simulation parameters.
"""
