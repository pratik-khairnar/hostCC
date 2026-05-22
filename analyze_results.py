"""
Graph Generation and Analysis Script for hostCC Simulations
Run this script to generate comparison graphs from the CSV results

Usage:
    python analyze_results.py

This script generates:
- Throughput comparison graph
- Packet loss comparison graph
- Host queue occupancy over time
- CWND (Congestion Window) evolution
- Local app load vs time
- Comprehensive multi-metric comparison
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

def load_data():
    """Load metrics from CSV files."""
    print("Loading simulation results...")
    
    v1 = pd.read_csv('results/v1_metrics.csv')
    v2 = pd.read_csv('results/v2_metrics.csv')
    v3 = pd.read_csv('results/v3_metrics.csv')
    
    with open('results/comparison_summary.json', 'r') as f:
        summary = json.load(f)
    
    print(f"✓ Loaded V1: {len(v1)} steps")
    print(f"✓ Loaded V2: {len(v2)} steps")
    print(f"✓ Loaded V3: {len(v3)} steps")
    
    return v1, v2, v3, summary

def create_comparison_plots(v1, v2, v3, summary):
    """Create comprehensive comparison plots."""
    
    fig = plt.figure(figsize=(18, 12))
    
    # Plot 1: Host Queue Occupancy
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(v1['step'], v1['host_queue_occupancy'], label='V1: TCP', linewidth=2, marker='o', markersize=3)
    ax1.plot(v2['step'], v2['host_queue_occupancy'], label='V2: hostCC', linewidth=2, marker='s', markersize=3)
    ax1.plot(v3['step'], v3['host_queue_occupancy'], label='V3: Improved', linewidth=2, marker='^', markersize=3)
    ax1.axhline(y=100, color='r', linestyle='--', alpha=0.5, label='Threshold')
    ax1.set_xlabel('Simulation Step')
    ax1.set_ylabel('Host Queue Occupancy (packets)')
    ax1.set_title('Host Queue Behavior')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: CWND Evolution
    ax2 = plt.subplot(3, 3, 2)
    ax2.plot(v1['step'], v1['cwnd'], label='V1: TCP', linewidth=2, marker='o', markersize=3)
    ax2.plot(v2['step'], v2['cwnd'], label='V2: hostCC', linewidth=2, marker='s', markersize=3)
    ax2.plot(v3['step'], v3['cwnd'], label='V3: Improved', linewidth=2, marker='^', markersize=3)
    ax2.set_xlabel('Simulation Step')
    ax2.set_ylabel('Congestion Window (packets)')
    ax2.set_title('CWND Evolution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Cumulative Packets Sent
    ax3 = plt.subplot(3, 3, 3)
    ax3.plot(v1['step'], v1['packets_sent'], label='V1: TCP', linewidth=2, marker='o', markersize=3)
    ax3.plot(v2['step'], v2['packets_sent'], label='V2: hostCC', linewidth=2, marker='s', markersize=3)
    ax3.plot(v3['step'], v3['packets_sent'], label='V3: Improved', linewidth=2, marker='^', markersize=3)
    ax3.set_xlabel('Simulation Step')
    ax3.set_ylabel('Cumulative Packets Sent')
    ax3.set_title('Total Packets Sent')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Local App Load
    ax4 = plt.subplot(3, 3, 4)
    ax4.plot(v1['step'], v1['local_app_load'], label='V1: TCP', linewidth=2, marker='o', markersize=3)
    ax4.plot(v2['step'], v2['local_app_load'], label='V2: hostCC', linewidth=2, marker='s', markersize=3)
    ax4.plot(v3['step'], v3['local_app_load'], label='V3: Improved', linewidth=2, marker='^', markersize=3)
    ax4.set_xlabel('Simulation Step')
    ax4.set_ylabel('Local App Load (0-1)')
    ax4.set_title('Local Application Memory Load')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 1)
    
    # Plot 5: Congestion Events
    ax5 = plt.subplot(3, 3, 5)
    ax5.plot(v1['step'], v1['congestion_detected'], label='V1: TCP', linewidth=2, drawstyle='steps-post')
    ax5.plot(v2['step'], v2['congestion_detected'], label='V2: hostCC', linewidth=2, drawstyle='steps-post')
    ax5.plot(v3['step'], v3['congestion_detected'], label='V3: Improved', linewidth=2, drawstyle='steps-post')
    ax5.set_xlabel('Simulation Step')
    ax5.set_ylabel('Congestion Detected (0/1)')
    ax5.set_title('Congestion Detection Events')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(-0.1, 1.1)
    
    # Plot 6: Controller Threshold
    ax6 = plt.subplot(3, 3, 6)
    ax6.plot(v1['step'], v1['controller_threshold'], label='V1: TCP', linewidth=2)
    ax6.plot(v2['step'], v2['controller_threshold'], label='V2: hostCC', linewidth=2)
    ax6.plot(v3['step'], v3['controller_threshold'], label='V3: Improved', linewidth=2)
    ax6.set_xlabel('Simulation Step')
    ax6.set_ylabel('Congestion Threshold')
    ax6.set_title('Dynamic Threshold Value')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    # Plot 7: Throughput over time (rolling average)
    ax7 = plt.subplot(3, 3, 7)
    # Calculate rolling throughput
    window = 5
    v1_throughput = v1['packets_acked'].diff().rolling(window=window, min_periods=1).mean()
    v2_throughput = v2['packets_acked'].diff().rolling(window=window, min_periods=1).mean()
    v3_throughput = v3['packets_acked'].diff().rolling(window=window, min_periods=1).mean()
    
    ax7.plot(v1['step'], v1_throughput, label='V1: TCP', linewidth=2, marker='o', markersize=3)
    ax7.plot(v2['step'], v2_throughput, label='V2: hostCC', linewidth=2, marker='s', markersize=3)
    ax7.plot(v3['step'], v3_throughput, label='V3: Improved', linewidth=2, marker='^', markersize=3)
    ax7.set_xlabel('Simulation Step')
    ax7.set_ylabel('Throughput (pkts/step)')
    ax7.set_title(f'Throughput ({window}-step moving avg)')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    
    # Plot 8: Packets in Flight
    ax8 = plt.subplot(3, 3, 8)
    ax8.plot(v1['step'], v1['packets_inflight'], label='V1: TCP', linewidth=2, marker='o', markersize=3)
    ax8.plot(v2['step'], v2['packets_inflight'], label='V2: hostCC', linewidth=2, marker='s', markersize=3)
    ax8.plot(v3['step'], v3['packets_inflight'], label='V3: Improved', linewidth=2, marker='^', markersize=3)
    ax8.set_xlabel('Simulation Step')
    ax8.set_ylabel('Packets In Flight')
    ax8.set_title('Network Packets In Flight')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    
    # Plot 9: Summary Bar Chart - Overall Statistics
    ax9 = plt.subplot(3, 3, 9)
    versions = ['V1: TCP', 'V2: hostCC', 'V3: Improved']
    throughputs = [
        summary['v1']['summary']['global']['total_throughput'],
        summary['v2']['summary']['global']['total_throughput'],
        summary['v3']['summary']['global']['total_throughput']
    ]
    packet_losses = [
        summary['v1']['summary']['global']['packet_loss_rate'] * 100,
        summary['v2']['summary']['global']['packet_loss_rate'] * 100,
        summary['v3']['summary']['global']['packet_loss_rate'] * 100
    ]
    
    x = np.arange(len(versions))
    width = 0.35
    
    ax9_twin = ax9.twinx()
    bars1 = ax9.bar(x - width/2, throughputs, width, label='Throughput', alpha=0.8, color='blue')
    bars2 = ax9_twin.bar(x + width/2, packet_losses, width, label='Loss Rate %', alpha=0.8, color='red')
    
    ax9.set_xlabel('Simulation Version')
    ax9.set_ylabel('Throughput (pkt/step)', color='blue')
    ax9_twin.set_ylabel('Packet Loss Rate (%)', color='red')
    ax9.set_title('Overall Performance Summary')
    ax9.set_xticks(x)
    ax9.set_xticklabels(versions)
    ax9.tick_params(axis='y', labelcolor='blue')
    ax9_twin.tick_params(axis='y', labelcolor='red')
    ax9.grid(True, alpha=0.3, axis='y')
    
    # Add legend
    lines1, labels1 = ax9.get_legend_handles_labels()
    lines2, labels2 = ax9_twin.get_legend_handles_labels()
    ax9.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    
    # Save figure
    output_file = 'results/comprehensive_comparison.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved comprehensive comparison to {output_file}")
    
    return fig

def print_detailed_analysis(v1, v2, v3, summary):
    """Print detailed analysis statistics."""
    
    print("\n" + "="*70)
    print("DETAILED SIMULATION ANALYSIS")
    print("="*70)
    
    for version, data, key in [('V1: Normal TCP', v1, 'v1'),
                              ('V2: hostCC Baseline', v2, 'v2'),
                              ('V3: Improved hostCC', v3, 'v3')]:
        
        print(f"\n{version}")
        print("-" * 70)
        
        global_stats = summary[key]['summary']['global']
        local_stats = summary[key]['summary']
        
        print(f"  Total Throughput:           {global_stats['total_throughput']:.4f} pkt/step")
        print(f"  Total Packets Sent:         {global_stats['total_packets_sent']}")
        print(f"  Total Packets Dropped:      {global_stats['total_packets_dropped']}")
        print(f"  Packet Loss Rate:           {global_stats['packet_loss_rate']:.4f} ({global_stats['packet_loss_rate']*100:.2f}%)")
        print(f"  Average RTT:                {global_stats['avg_rtt']}")
        print(f"  Average Load:               {global_stats['avg_load']:.2f}")
        
        print(f"\n  Host Queue Statistics:")
        print(f"    Max Occupancy:            {local_stats['max_host_occupancy']:.0f} packets")
        print(f"    Avg Occupancy:            {local_stats['avg_host_occupancy']:.2f} packets")
        print(f"    Occupancy Head Room:      {200 - local_stats['max_host_occupancy']:.0f} packets")
        
        print(f"\n  Congestion Window Statistics:")
        print(f"    Max CWND:                 {local_stats['max_cwnd']:.0f}")
        print(f"    Avg CWND:                 {local_stats['avg_cwnd']:.2f}")
        
        print(f"\n  Dynamic Metrics:")
        congestion_count = data['congestion_detected'].sum()
        throttle_count = data['local_is_throttled'].sum()
        print(f"    Congestion Events:        {congestion_count} times")
        print(f"    Throttling Periods:       {throttle_count} steps")
        print(f"    Avg Host Queue (last 10): {data['host_queue_occupancy'].tail(10).mean():.2f}")

def create_individual_metric_plots(v1, v2, v3):
    """Create individual detailed plots for each metric."""
    
    metrics = [
        ('host_queue_occupancy', 'Host Queue Occupancy (packets)', 'Host Queue Behavior'),
        ('cwnd', 'Congestion Window (packets)', 'CWND Evolution'),
        ('local_app_load', 'Local App Load (0-1)', 'Memory Load Over Time'),
        ('packets_sent', 'Cumulative Packets Sent', 'Total Packets Sent'),
        ('packets_acked', 'Cumulative Packets Acked', 'Total Packets Acknowledged'),
    ]
    
    for metric, ylabel, title in metrics:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(v1['step'], v1[metric], label='V1: Normal TCP', linewidth=2.5, marker='o', markersize=4, alpha=0.7)
        ax.plot(v2['step'], v2[metric], label='V2: hostCC Baseline', linewidth=2.5, marker='s', markersize=4, alpha=0.7)
        ax.plot(v3['step'], v3[metric], label='V3: Improved hostCC', linewidth=2.5, marker='^', markersize=4, alpha=0.7)
        
        ax.set_xlabel('Simulation Step', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Save figure
        filename = f'results/metric_{metric}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Saved {title} plot to {filename}")
        plt.close()

def main():
    """Main analysis function."""
    
    print("\n" + "="*70)
    print("hostCC Simulation Analysis Tool")
    print("="*70)
    
    # Check if results exist
    if not os.path.exists('results/v1_metrics.csv'):
        print("\n❌ No simulation results found!")
        print("Run 'python run_simulation.py' first to generate results.")
        return
    
    # Load data
    v1, v2, v3, summary = load_data()
    
    # Create comprehensive plots
    print("\nGenerating plots...")
    create_comparison_plots(v1, v2, v3, summary)
    
    # Create individual metric plots
    print("Creating individual metric plots...")
    create_individual_metric_plots(v1, v2, v3)
    
    # Print detailed analysis
    print_detailed_analysis(v1, v2, v3, summary)
    
    print("\n" + "="*70)
    print("✓ Analysis complete!")
    print("="*70)
    print("\nGenerated files:")
    print("  - results/comprehensive_comparison.png")
    print("  - results/metric_*.png (individual metrics)")
    print("\nOpen these images to visualize the results!")

if __name__ == '__main__':
    main()
