"""
NIC Buffer Module: Simulates the receiver NIC buffer
"""

class NICBuffer:
    """
    Simulates the NIC buffer at the receiver side.
    Packets from network arrive here and wait to be forwarded to host queue.
    """
    
    def __init__(self, config):
        """
        Initialize the NIC buffer.
        
        Args:
            config: Configuration parameters dictionary
        """
        self.config = config
        self.buffer = []  # List of packets in NIC buffer
        self.capacity = config.get('NIC_BUFFER_SIZE', 100)
        self.process_rate = config.get('NIC_PROCESS_RATE', 80)  # packets/step
        
        # Statistics
        self.packets_received = 0
        self.packets_processed = 0
        self.packets_dropped = 0
        
    def receive_packets(self, num_packets, current_step):
        """
        Receive packets from network.
        
        Args:
            num_packets: Number of packets arriving
            current_step: Current simulation step
            
        Returns:
            tuple: (packets_accepted, packets_dropped_due_to_buffer)
        """
        packets_dropped = 0
        
        for i in range(num_packets):
            if len(self.buffer) < self.capacity:
                self.buffer.append({
                    'id': self.packets_received,
                    'arrived_at': current_step
                })
                self.packets_received += 1
            else:
                packets_dropped += 1
                self.packets_dropped += 1
        
        return num_packets - packets_dropped, packets_dropped
    
    def forward_to_host_queue(self, current_step):
        """
        Forward packets from NIC buffer to host queue.
        
        Args:
            current_step: Current simulation step
            
        Returns:
            list: Packets forwarded to host queue
        """
        # Forward up to process_rate packets
        packets_to_forward = self.buffer[:self.process_rate]
        self.buffer = self.buffer[self.process_rate:]
        
        self.packets_processed += len(packets_to_forward)
        
        return packets_to_forward
    
    def get_buffer_occupancy(self):
        """Get current buffer occupancy."""
        return len(self.buffer)
    
    def get_occupancy_ratio(self):
        """Get buffer occupancy as ratio (0-1)."""
        return len(self.buffer) / self.capacity if self.capacity > 0 else 0
    
    def get_state(self):
        """Get NIC buffer state."""
        return {
            'buffer_length': len(self.buffer),
            'buffer_capacity': self.capacity,
            'occupancy_ratio': self.get_occupancy_ratio(),
            'packets_received': self.packets_received,
            'packets_processed': self.packets_processed,
            'packets_dropped': self.packets_dropped
        }
    
    def reset(self):
        """Reset NIC buffer state."""
        self.buffer = []
        self.packets_received = 0
        self.packets_processed = 0
        self.packets_dropped = 0
