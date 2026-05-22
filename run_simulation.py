"""
Main Simulation Runner: Orchestrates all three versions of simulation
"""

import sys
import os
from config.parameters import *
from simulation.tcp_simulation import TCPSimulation
from simulation.hostcc_simulation import hostCCSimulation
from simulation.improved_hostcc_sim import ImprovedHostCCSimulation
import json

def create_config():
    """
    Create configuration dictionary from parameters.
    
    Returns:
        dict: Configuration parameters
    """
    config = {
        'SIMULATION_TIME': SIMULATION_TIME,
        'STEP_DURATION': STEP_DURATION,
        'INITIAL_CWND': INITIAL_CWND,
        'MAX_CWND': MAX_CWND,
        'SEND_RATE_MULTIPLIER': SEND_RATE_MULTIPLIER,
        'RTT_INITIAL': RTT_INITIAL,
        'AI_INCREASE': AI_INCREASE,
        'MD_FACTOR': MD_FACTOR,
        'NETWORK_CAPACITY': NETWORK_CAPACITY,
        'NETWORK_DELAY': NETWORK_DELAY,
        'NETWORK_QUEUE_SIZE': NETWORK_QUEUE_SIZE,
        'BASE_NETWORK_LOSS_RATE': BASE_NETWORK_LOSS_RATE,
        'NIC_BUFFER_SIZE': NIC_BUFFER_SIZE,
        'NIC_PROCESS_RATE': NIC_PROCESS_RATE,
        'HOST_QUEUE_SIZE': HOST_QUEUE_SIZE,
        'HOST_PROCESS_RATE': HOST_PROCESS_RATE,
        'HOST_QUEUE_BASE_THRESHOLD': HOST_QUEUE_BASE_THRESHOLD,
        'LOCAL_APP_INITIAL_LOAD': LOCAL_APP_INITIAL_LOAD,
        'LOCAL_APP_MAX_LOAD': LOCAL_APP_MAX_LOAD,
        'LOCAL_APP_MIN_LOAD': LOCAL_APP_MIN_LOAD,
        'HOST_TOTAL_MEMORY_BANDWIDTH': HOST_TOTAL_MEMORY_BANDWIDTH,
        'LOCAL_MEMORY_INCREASE_RATE': LOCAL_MEMORY_INCREASE_RATE,
        'LOCAL_MEMORY_AGGRESSIVE': LOCAL_MEMORY_AGGRESSIVE,
        'HOSTCC_ENABLED': HOSTCC_ENABLED,
        'HOST_CONGESTION_DETECTION_THRESHOLD': HOST_CONGESTION_DETECTION_THRESHOLD,
        'HOSTCC_DETECTION_METHOD': HOSTCC_DETECTION_METHOD,
        'ADAPTIVE_THRESHOLD_ENABLED': ADAPTIVE_THRESHOLD_ENABLED,
        'ADAPTIVE_ALPHA': ADAPTIVE_ALPHA,
        'PREDICTIVE_ENABLED': PREDICTIVE_ENABLED,
        'PREDICTION_WINDOW': PREDICTION_WINDOW,
        'PREDICTION_THRESHOLD_MULTIPLIER': PREDICTION_THRESHOLD_MULTIPLIER,
        'CONGESTION_NOTIFICATION_DELAY': CONGESTION_NOTIFICATION_DELAY,
        'LOG_ENABLED': LOG_ENABLED,
        'SAVE_METRICS': SAVE_METRICS,
        'METRICS_FILE': METRICS_FILE,
        'VERBOSE': VERBOSE,
        'ENABLE_PACKET_RETRANSMISSION': ENABLE_PACKET_RETRANSMISSION,
        'CALCULATE_RTT': CALCULATE_RTT,
        'RANDOM_SEED': RANDOM_SEED,
    }
    return config

def run_all_simulations():
    """
    Run all three versions of simulation.
    
    Returns:
        dict: Results from all simulations
    """
    print("="*70)
    print("Host Congestion Control (hostCC) Simulation")
    print("="*70)
    print()
    
    # Create configuration
    config = create_config()
    
    # Create output directories
    os.makedirs('results', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    results = {}
    simulations = [
        ('v1', TCPSimulation, 'Normal TCP'),
        ('v2', hostCCSimulation, 'hostCC Baseline'),
        ('v3', ImprovedHostCCSimulation, 'Improved hostCC'),
    ]
    
    print("Configuration Summary:")
    print(f"  Simulation Time: {config['SIMULATION_TIME']} steps")
    print(f"  Initial CWND: {config['INITIAL_CWND']}")
    print(f"  Host Queue Threshold: {config['HOST_QUEUE_BASE_THRESHOLD']}")
    print(f"  Initial Local Load: {config['LOCAL_APP_INITIAL_LOAD']:.2f}")
    print()
    
    # Run each simulation
    for version_id, SimClass, description in simulations:
        print(f"\nRunning {description} ({version_id})...")
        print("-" * 70)
        
        # Create and run simulation
        sim = SimClass(config)
        metrics = sim.run()
        
        # Save metrics
        metrics_file = f'results/{version_id}_metrics.csv'
        metrics.save_to_csv(metrics_file)
        
        # Save logs
        log_file = f'logs/{version_id}_log.txt'
        sim.logger.save_logs(log_file)
        
        # Get summary
        summary = metrics.get_summary()
        results[version_id] = {
            'description': description,
            'summary': summary,
            'metrics': metrics
        }
        
        # Print summary
        print(f"\nResults for {description}:")
        print(f"  Total packets sent: {summary['global'].get('total_packets_sent', 0)}")
        print(f"  Total packets dropped: {summary['global'].get('total_packets_dropped', 0)}")
        print(f"  Packet loss rate: {summary['global'].get('packet_loss_rate', 0):.4f}")
        print(f"  Throughput: {summary['global'].get('total_throughput', 0):.2f} pkt/step")
        print(f"  Max host queue occupancy: {summary.get('max_host_occupancy', 0):.0f}")
        print(f"  Avg host queue occupancy: {summary.get('avg_host_occupancy', 0):.1f}")
        print(f"  Max CWND: {summary.get('max_cwnd', 0):.0f}")
        print(f"  Avg CWND: {summary.get('avg_cwnd', 0):.1f}")
    
    # Save comparison results
    print("\n" + "="*70)
    print("COMPARISON SUMMARY")
    print("="*70)
    
    comparison_file = 'results/comparison_summary.json'
    with open(comparison_file, 'w') as f:
        # Convert metrics objects to dict for JSON serialization
        json_results = {}
        for version_id, data in results.items():
            json_results[version_id] = {
                'description': data['description'],
                'summary': data['summary']
            }
        json.dump(json_results, f, indent=2)
    
    print(f"\nComparison saved to {comparison_file}")
    
    # Print comparison table
    print("\nPerformance Comparison:")
    print("-" * 70)
    print(f"{'Version':<30} {'Throughput':<15} {'Packet Loss':<15} {'Avg CWND':<15}")
    print("-" * 70)
    
    for version_id, data in results.items():
        desc = data['description']
        throughput = data['summary']['global'].get('total_throughput', 0)
        loss_rate = data['summary']['global'].get('packet_loss_rate', 0)
        avg_cwnd = data['summary'].get('avg_cwnd', 0)
        
        print(f"{desc:<30} {throughput:<15.4f} {loss_rate:<15.4f} {avg_cwnd:<15.2f}")
    
    print()
    print("="*70)
    print("Simulation Complete!")
    print("="*70)
    print(f"\nOutput files:")
    print(f"  Metrics: results/v1_metrics.csv, results/v2_metrics.csv, results/v3_metrics.csv")
    print(f"  Logs: logs/v1_log.txt, logs/v2_log.txt, logs/v3_log.txt")
    print(f"  Summary: {comparison_file}")
    print()
    print("Ready for graph generation and analysis!")
    
    return results

if __name__ == "__main__":
    results = run_all_simulations()
