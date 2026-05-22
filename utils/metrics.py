"""
Metrics Collection Module: Collects and stores simulation metrics
"""

import csv
from collections import defaultdict

class MetricsCollector:
    """
    Collects metrics throughout the simulation for analysis and visualization.
    """
    
    def __init__(self, version_name="baseline"):
        """
        Initialize metrics collector.
        
        Args:
            version_name: Name of this simulation version
        """
        self.version_name = version_name
        self.metrics = defaultdict(list)
        self.global_metrics = {}
        
    def record_step(self, step, sender_state, network_state, nic_state, 
                   host_queue_state, local_app_state, controller_state=None):
        """
        Record metrics for a single simulation step.
        
        Args:
            step: Current step number
            sender_state: Sender module state dict
            network_state: Network queue state dict
            nic_state: NIC buffer state dict
            host_queue_state: Host queue state dict
            local_app_state: Local app state dict
            controller_state: hostCC controller state dict (optional)
        """
        self.metrics['step'].append(step)
        
        # Sender metrics
        self.metrics['cwnd'].append(sender_state['cwnd'])
        self.metrics['packets_sent'].append(sender_state['total_sent'])
        self.metrics['packets_acked'].append(sender_state['total_acked'])
        self.metrics['packets_inflight'].append(sender_state['packets_inflight'])
        self.metrics['rtt'].append(sender_state['rtt'])
        self.metrics['congestion_events'].append(sender_state['congestion_events'])
        
        # Network metrics
        self.metrics['network_queue_length'].append(network_state['queue_length'])
        self.metrics['network_packets_dropped'].append(network_state['packets_dropped'])
        self.metrics['network_loss_rate'].append(network_state['loss_rate'])
        
        # NIC metrics
        self.metrics['nic_occupancy'].append(nic_state['buffer_length'])
        self.metrics['nic_occupancy_ratio'].append(nic_state['occupancy_ratio'])
        self.metrics['nic_packets_dropped'].append(nic_state['packets_dropped'])
        
        # Host queue metrics
        self.metrics['host_queue_occupancy'].append(host_queue_state['occupancy'])
        self.metrics['host_queue_occupancy_ratio'].append(host_queue_state['occupancy_ratio'])
        self.metrics['host_packets_dropped'].append(host_queue_state['packets_dropped'])
        self.metrics['host_available_bandwidth'].append(host_queue_state['available_bandwidth'])
        
        # Local app metrics
        self.metrics['local_app_load'].append(local_app_state['load'])
        self.metrics['local_bandwidth_used'].append(local_app_state['bandwidth_used'])
        self.metrics['local_is_throttled'].append(1 if local_app_state['is_throttled'] else 0)
        
        # Controller metrics
        if controller_state:
            self.metrics['congestion_detected'].append(1 if controller_state['congestion_detected'] else 0)
            self.metrics['controller_threshold'].append(controller_state['threshold'])
            self.metrics['congestion_event_count'].append(controller_state['congestion_count'])
        else:
            self.metrics['congestion_detected'].append(0)
            self.metrics['controller_threshold'].append(0)
            self.metrics['congestion_event_count'].append(0)
    
    def record_final_metrics(self, total_throughput, total_packets_sent, 
                            total_packets_dropped, avg_rtt, avg_load):
        """
        Record final simulation metrics.
        
        Args:
            total_throughput: Total throughput achieved
            total_packets_sent: Total packets sent
            total_packets_dropped: Total packets dropped
            avg_rtt: Average RTT
            avg_load: Average host queue load
        """
        self.global_metrics = {
            'total_throughput': total_throughput,
            'total_packets_sent': total_packets_sent,
            'total_packets_dropped': total_packets_dropped,
            'packet_loss_rate': total_packets_dropped / total_packets_sent if total_packets_sent > 0 else 0,
            'avg_rtt': avg_rtt,
            'avg_load': avg_load
        }
    
    def save_to_csv(self, filename):
        """
        Save metrics to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        if not self.metrics or not self.metrics['step']:
            print(f"No metrics to save for {self.version_name}")
            return
        
        try:
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except:
            pass
        
        # Get all step numbers
        steps = self.metrics['step']
        
        with open(filename, 'w', newline='') as csvfile:
            # Get all metric keys (excluding 'step')
            fieldnames = ['step'] + [k for k in sorted(self.metrics.keys()) if k != 'step']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, step in enumerate(steps):
                row = {'step': step}
                for key in self.metrics:
                    if key != 'step' and i < len(self.metrics[key]):
                        row[key] = self.metrics[key][i]
                writer.writerow(row)
        
        print(f"Metrics saved to {filename}")
    
    def get_summary(self):
        """Get summary statistics."""
        summary = {
            'version': self.version_name,
            'global': self.global_metrics,
            'max_host_occupancy': max(self.metrics.get('host_queue_occupancy', [0])),
            'avg_host_occupancy': sum(self.metrics.get('host_queue_occupancy', [0])) / max(len(self.metrics.get('host_queue_occupancy', [0])), 1),
            'max_cwnd': max(self.metrics.get('cwnd', [0])),
            'avg_cwnd': sum(self.metrics.get('cwnd', [0])) / max(len(self.metrics.get('cwnd', [0])), 1),
        }
        return summary
