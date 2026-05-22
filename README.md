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



















































































































































































































































































Educational use## LicensePratik - Semester 6 CNProject## Author- Modern receiver-based congestion detection techniques- Explicit Congestion Notification (RFC 3540)- TCP congestion control (RFC 5681)- Original hostCC paper concepts## References6. Hardware-in-the-loop validation5. Real packet tracing and validation4. Different congestion control algorithms (Cubic, BBR, etc.)3. Multiple concurrent senders2. Dynamic local application behavior1. Variable network loss patterns## Future Enhancements```metrics.save_to_csv('custom_results.csv')metrics = sim.run()sim = TCPSimulation(custom_config)# Run custom simulation}    # ... other parameters    'HOST_QUEUE_BASE_THRESHOLD': 150,    'INITIAL_CWND': 20,    'SIMULATION_TIME': 200,custom_config = {# Modify parametersfrom simulation.tcp_simulation import TCPSimulationfrom config.parameters import *```pythonTo run custom simulations:## Customization6. **CWND Stability** = Variance of congestion window5. **Response Time** = Steps from congestion to detection4. **Congestion Events** = Number of times threshold exceeded3. **Average Queue Occupancy** = Mean host queue length2. **Packet Loss Rate** = Total dropped / Total sent1. **Throughput** = Total packets acked / Total simulation steps## Key Metrics for Analysis8. Move to next step7. Metrics recorded6. Controllers and applications respond5. hostCC controller detects congestion (if enabled)4. Host queue receives and processes packets3. Packets delivered to receiver NIC2. Network processes packet transit1. Sender generates packets based on CWNDAt each step (t):The simulation uses a **time-step discrete event** model:## Methodology```plt.savefig('results/host_queue_comparison.png')plt.grid(True)plt.title('Host Queue Behavior Across Versions')plt.legend()plt.ylabel('Host Queue Occupancy (packets)')plt.xlabel('Simulation Step')plt.plot(v3['step'], v3['host_queue_occupancy'], label='V3: Improved hostCC')plt.plot(v2['step'], v2['host_queue_occupancy'], label='V2: hostCC')plt.plot(v1['step'], v1['host_queue_occupancy'], label='V1: Normal TCP')plt.figure(figsize=(12, 6))# Plot host queue occupancyv3 = pd.read_csv('results/v3_metrics.csv')v2 = pd.read_csv('results/v2_metrics.csv')v1 = pd.read_csv('results/v1_metrics.csv')# Load metricsimport matplotlib.pyplot as pltimport pandas as pd```pythonExample analysis script (to be created):5. **Load Response**: Show local app throttling behavior4. **Adaptation**: Visualize CWND changes and congestion events3. **Loss Rates**: Compare packet loss percentages2. **Queue Occupancy**: Show host queue behavior across versions1. **Throughput Graphs**: Plot cumulative packets over timeAfter running simulations, analyze results using:## Result Analysis- **Version 3**: Minimal, predictive prevention- **Version 2**: Fewer, host-aware- **Version 1**: Many, reactive only### Congestion Events- **Version 3**: Controlled levels, predictive smoothing- **Version 2**: Moderate peaks, some stability- **Version 1**: High peaks, unstable### Host Queue Occupancy- **Version 3**: Lowest loss (2-5%) with early prediction- **Version 2**: Reduced loss (5-10%) with host controls- **Version 1**: Highest loss (10-15%) with host congestion### Packet Loss Comparison- **Version 3 (Improved)**: Best throughput with predictive adaptation- **Version 2 (hostCC)**: Improved throughput with host awareness- **Version 1 (Normal TCP)**: Moderate throughput, high variability### Throughput Comparison## Expected Results```}  }    }      }        "avg_rtt": 10        "packet_loss_rate": 0.10,        "total_packets_dropped": 45,        "total_packets_sent": 450,        "total_throughput": 4.5,      "global": {    "summary": {    "description": "Normal TCP",  "v1": {{```json**JSON Summary** provides high-level statistics:- And more...- `controller_threshold` - Current congestion threshold- `congestion_detected` - Whether congestion was detected- `local_app_load` - Local application load (0-1)- `host_packets_dropped` - Packets dropped at host- `host_queue_occupancy` - Host queue occupancy (KEY METRIC)- `nic_occupancy` - NIC buffer occupancy- `network_queue_length` - Network queue occupancy- `rtt` - Current RTT- `packets_inflight` - Current inflight packets- `packets_acked` - Cumulative packets acknowledged- `packets_sent` - Cumulative packets sent- `cwnd` - Congestion window size- `step` - Simulation step number**Metrics CSV Files** contain per-step data:### Output Files4. Save logs to `logs/` directory   - `comparison_summary.json` - Summary comparison   - `v3_metrics.csv` - Improved hostCC metrics   - `v2_metrics.csv` - hostCC baseline metrics   - `v1_metrics.csv` - Normal TCP metrics3. Save results to `results/` directory:2. Collect metrics for each step1. Run all three simulation versionsThis will:```python run_simulation.py```bash### Execute Simulations```pip install -r requirements.txt```bash### Prerequisites## Running the Simulation```PREDICTION_WINDOW = 5              # Steps to predictPREDICTIVE_ENABLED = True          # Enable prediction (v3)ADAPTIVE_ALPHA = 0.5               # Adaptation factorADAPTIVE_THRESHOLD_ENABLED = True  # Enable adaptive (v3)# hostCC (Version 2+)LOCAL_MEMORY_INCREASE_RATE = 0.02  # Load increase/stepLOCAL_APP_INITIAL_LOAD = 0.3       # 30% of bandwidth# Local AppHOST_QUEUE_BASE_THRESHOLD = 100    # congestion thresholdHOST_PROCESS_RATE = 50             # packets/stepHOST_QUEUE_SIZE = 200              # packets# Host SystemBASE_NETWORK_LOSS_RATE = 0.01      # 1%NETWORK_DELAY = 5                  # stepsNETWORK_CAPACITY = 100             # packets/step# NetworkMD_FACTOR = 0.5                    # Multiplicative decreaseAI_INCREASE = 1                    # Additive increaseINITIAL_CWND = 10                  # Initial congestion windowSIMULATION_TIME = 100              # Total simulation steps# Simulation```python### Key ParametersEdit `config/parameters.py` to adjust simulation parameters:## Configuration   - Formula: `predicted_queue = average(last 5 queue values)`   - Reduces packet drops by reacting proactively   - Triggers control at 80% of predicted threshold   - Predicts future congestion early   - Examines recent queue history (last N steps)2. **Predictive Congestion Control**   - More intelligent congestion detection   - Reacts earlier when system is heavily loaded   - Formula: `threshold = base_threshold + alpha * local_load * base_threshold`   - Threshold adjusts dynamically based on local memory load1. **Adaptive Threshold****Improvements over Version 2:**### Version 3: Improved hostCC- Reduces drops compared to normal TCP- Notifies sender to reduce rate (ECN-like)- Throttles local applications- Detects when queue exceeds fixed threshold- Monitors host queue occupancy (virtual IIO)### Version 2: hostCC Baseline- Shows high packet drops with host-side congestion- Baseline for comparison- No host congestion awareness- Traditional TCP congestion control (AIMD)### Version 1: Normal TCP## Simulation Versions- Predictive congestion detection (Version 3)- Adaptive threshold calculation (Version 3)- Detects congestion based on queue state- Monitors host queue occupancy### hostCC Controller (`modules/hostcc_controller.py`)- Naturally increases load over time- Can be throttled by hostCC controller- Consumes portion of host memory bandwidth- Simulates background memory-heavy applications### Local Memory App (`modules/local_app.py`)- Maintains history for congestion prediction- Available bandwidth depends on local application load- Simulates packet processing through host memory system- **Core module**: Represents internal host datapath (IIO occupancy equivalent)### Host Queue (`modules/host_queue.py`)- Forwards to host queue based on process rate- Receives packets from network- Simulates receiver NIC buffer### NIC Buffer (`modules/nic_buffer.py`)- Queue management with capacity constraints- Models network delay and packet loss- Simulates network path with capacity limits### Network Queue (`modules/network_queue.py`)- Tracks RTT and connection statistics- Responds to packet loss and host congestion signals- Maintains congestion window (CWND)- Implements TCP-like congestion control (AIMD)### Sender Module (`modules/sender.py`)## Key Modules```└── README.md                   # This file├── requirements.txt            # Python dependencies├── run_simulation.py           # Main runner├── logs/                       # Generated log files├── results/                    # Generated result files├── data/                       # Data storage│   └── logger.py               # Logging utilities│   ├── metrics.py              # Metrics collection│   ├── __init__.py├── utils/│   └── improved_hostcc_sim.py  # Version 3 implementation│   ├── hostcc_simulation.py    # Version 2 implementation│   ├── tcp_simulation.py       # Version 1 implementation│   ├── base_simulation.py      # Base class for simulations│   ├── __init__.py├── simulation/│   └── hostcc_controller.py    # hostCC controller│   ├── local_app.py            # Local memory-bound applications│   ├── host_queue.py           # Internal host datapath queue│   ├── nic_buffer.py           # NIC buffer│   ├── network_queue.py        # Network path simulation│   ├── sender.py              # TCP sender with congestion control│   ├── __init__.py├── modules/│   └── parameters.py          # Configuration and parameters│   ├── __init__.py├── config/CNProjectNew/```## Project Structure3. **Version 3: Improved hostCC** - Enhanced version with adaptive thresholds and predictive control2. **Version 2: hostCC Baseline** - Basic host congestion control from the paper1. **Version 1: Normal TCP** - Baseline implementation without host congestion awarenessThis project implements a software-level simulation of the Host Congestion Control (hostCC) architecture as proposed in the hostCC research paper. The simulation models three versions of congestion control mechanisms:## OverviewProject: Host Congestion Control (hostCC) Simulation

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
