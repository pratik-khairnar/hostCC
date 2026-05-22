"""
Configuration and Parameters for hostCC Simulation
"""

# Simulation Parameters
SIMULATION_TIME = 100  # Total simulation steps
STEP_DURATION = 1.0  # Duration of each step in milliseconds

# Sender Parameters
INITIAL_CWND = 80  # Initial congestion window (packets) - increased to generate traffic
MAX_CWND = 500  # Maximum congestion window
SEND_RATE_MULTIPLIER = 1.0  # Initial sending rate multiplier
RTT_INITIAL = 10  # Initial RTT in steps
AI_INCREASE = 2  # Additive increase per step (more aggressive growth)
MD_FACTOR = 0.6  # Multiplicative decrease factor (less drastic than 0.5)

# Network Parameters
NETWORK_CAPACITY = 100  # Packets per step (network bandwidth)
NETWORK_DELAY = 5  # Network RTT in steps
NETWORK_QUEUE_SIZE = 500  # Network queue buffer size
BASE_NETWORK_LOSS_RATE = 0.01  # Base network packet loss (1%)

# NIC Buffer Parameters
NIC_BUFFER_SIZE = 100  # NIC buffer capacity (packets)
NIC_PROCESS_RATE = 80  # Packets per step the NIC can forward to host queue

# Host Queue Parameters
HOST_QUEUE_SIZE = 200  # Host queue capacity (packets)
HOST_PROCESS_RATE = 50  # Packets per step that can be processed from host queue
HOST_QUEUE_BASE_THRESHOLD = 100  # Base threshold for host congestion detection

# Local Memory Application
LOCAL_APP_INITIAL_LOAD = 0.5  # Initial memory bandwidth usage ratio (50% - more aggressive)
LOCAL_APP_MAX_LOAD = 0.9  # Maximum local load
LOCAL_APP_MIN_LOAD = 0.0  # Minimum local load
HOST_TOTAL_MEMORY_BANDWIDTH = 100  # Total host memory bandwidth units
LOCAL_MEMORY_INCREASE_RATE = 0.03  # How much local load increases per step
LOCAL_MEMORY_AGGRESSIVE = 0.8  # Aggressive load level

# hostCC Controller Parameters
HOSTCC_ENABLED = True
HOST_CONGESTION_DETECTION_THRESHOLD = 100  # Static threshold for v2
HOSTCC_DETECTION_METHOD = 'queue_threshold'  # 'queue_threshold' or 'bandwidth_ratio'

# Improved hostCC (Version 3) Parameters
ADAPTIVE_THRESHOLD_ENABLED = True
ADAPTIVE_ALPHA = 0.5  # Adaptive threshold: base + alpha * local_load
PREDICTIVE_ENABLED = True
PREDICTION_WINDOW = 5  # Number of steps to look back for prediction
PREDICTION_THRESHOLD_MULTIPLIER = 0.8  # Trigger control at 80% of threshold

# Packet Loss Related
CONGESTION_NOTIFICATION_DELAY = 2  # Steps to deliver congestion notification

# Data Collection
LOG_ENABLED = True
SAVE_METRICS = True
METRICS_FILE = 'results/metrics.csv'
VERBOSE = False  # Print detailed logs

# Behavior Parameters
ENABLE_PACKET_RETRANSMISSION = False  # Simplified: no retransmission
CALCULATE_RTT = True  # Calculate RTT dynamically

# Random seed for reproducibility
RANDOM_SEED = 42
