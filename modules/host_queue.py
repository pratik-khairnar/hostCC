"""
Host Queue Module: Simulates the internal host datapath queue (IIO occupancy)
This is the core of host congestion detection.
"""

class HostQueue:
    """
    Simulates the internal host queue that represents the path
    from NIC -> PCIe/IIO -> Memory/CPU.
    This queue's occupancy is analogous to IIO occupancy in the paper.
    """
    
    def __init__(self, config):
        """
        Initialize the host queue.
        
        Args:
            config: Configuration parameters dictionary
        """
        self.config = config
        self.queue = []  # Packets waiting to be processed
        self.capacity = config.get('HOST_QUEUE_SIZE', 200)
        self.base_process_rate = config.get('HOST_PROCESS_RATE', 50)  # packets/step
        
        # Available memory bandwidth depends on local app load
        self.available_bandwidth = self.base_process_rate
        
        # Statistics
        self.packets_received = 0
        self.packets_processed = 0
        self.packets_dropped = 0
        
        # History for congestion detection
        self.occupancy_history = []
        self.max_history_length = 10
        
    def receive_packets(self, packets, current_step, local_app_load=0.0):
        """
        Receive packets from NIC buffer.
        
        Args:
            packets: List of packet objects
            current_step: Current simulation step
            local_app_load: Local memory load (0-1)
            
        Returns:
            tuple: (packets_accepted, packets_dropped_due_to_queue)
        """
        # Calculate available bandwidth based on local app load
        # Less local load = more bandwidth for network packets
        network_bandwidth = self.base_process_rate * (1 - local_app_load)
        self.available_bandwidth = network_bandwidth
        
        packets_dropped = 0
        
        for packet in packets:
            if len(self.queue) < self.capacity:
                self.queue.append({
                    'id': packet['id'],
                    'arrived_at': current_step,
                    'timestamp': current_step
                })
                self.packets_received += 1
            else:
                packets_dropped += 1
                self.packets_dropped += 1
        
        return len(packets) - packets_dropped, packets_dropped
    
    def process_packets(self, current_step, local_app_load=0.0):
        """
        Process packets from the host queue.
        Processing rate depends on available bandwidth (affected by local load).
        
        Args:
            current_step: Current simulation step
            local_app_load: Local memory load (0-1)
            
        Returns:
            int: Number of packets processed
        """
        # Recalculate available bandwidth
        network_bandwidth = self.base_process_rate * (1 - local_app_load)
        self.available_bandwidth = network_bandwidth
        
        # Process packets based on available bandwidth
        packets_to_process = min(int(network_bandwidth), len(self.queue))
        
        if packets_to_process > 0:
            self.queue = self.queue[packets_to_process:]
            self.packets_processed += packets_to_process
        
        # Record history for prediction
        self.occupancy_history.append(len(self.queue))
        if len(self.occupancy_history) > self.max_history_length:
            self.occupancy_history.pop(0)
        
        return packets_to_process
    
    def get_occupancy(self):
        """Get current queue occupancy."""
        return len(self.queue)
    
    def get_occupancy_ratio(self):
        """Get occupancy as ratio (0-1)."""
        return len(self.queue) / self.capacity if self.capacity > 0 else 0
    
    def get_average_occupancy(self, window_size=5):
        """
        Get average occupancy over recent history.
        Used for predictive congestion detection.
        
        Args:
            window_size: Number of steps to average
            
        Returns:
            float: Average occupancy
        """
        if len(self.occupancy_history) == 0:
            return 0
        
        recent = self.occupancy_history[-window_size:]
        return sum(recent) / len(recent)
    
    def get_state(self):
        """Get host queue state."""
        return {
            'occupancy': len(self.queue),
            'capacity': self.capacity,
            'occupancy_ratio': self.get_occupancy_ratio(),
            'available_bandwidth': self.available_bandwidth,
            'packets_received': self.packets_received,
            'packets_processed': self.packets_processed,
            'packets_dropped': self.packets_dropped,
            'avg_occupancy': self.get_average_occupancy()
        }
    
    def reset(self):
        """Reset host queue state."""
        self.queue = []
        self.packets_received = 0
        self.packets_processed = 0
        self.packets_dropped = 0
        self.occupancy_history = []
