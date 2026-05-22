"""
Network Queue Module: Simulates the network path with delays and losses
"""

import random

class NetworkQueue:
    """
    Simulates the network path between sender and receiver NIC.
    Includes network capacity limits, delays, and potential losses.
    """
    
    def __init__(self, config):
        """
        Initialize the network queue.
        
        Args:
            config: Configuration parameters dictionary
        """
        self.config = config
        self.queue = []  # List of (packet_id, timestamp_entered)
        self.capacity = config.get('NETWORK_QUEUE_SIZE', 500)
        self.bandwidth = config.get('NETWORK_CAPACITY', 100)  # packets/step
        self.delay = config.get('NETWORK_DELAY', 5)  # steps
        self.loss_rate = config.get('BASE_NETWORK_LOSS_RATE', 0.01)
        
        # Statistics
        self.packets_entered = 0
        self.packets_exited = 0
        self.packets_dropped = 0
        self.total_delay = 0
        
    def enqueue(self, num_packets, current_step):
        """
        Add packets to network queue.
        
        Args:
            num_packets: Number of packets to enqueue
            current_step: Current simulation step
            
        Returns:
            tuple: (packets_accepted, packets_dropped_due_to_queue)
        """
        packets_dropped = 0
        
        for i in range(num_packets):
            if len(self.queue) < self.capacity:
                # Generate packet ID for tracking
                packet_id = self.packets_entered
                self.queue.append({
                    'id': packet_id,
                    'entered_at': current_step,
                    'will_exit_at': current_step + self.delay
                })
                self.packets_entered += 1
            else:
                packets_dropped += 1
        
        return num_packets - packets_dropped, packets_dropped
    
    def forward_packets(self, current_step):
        """
        Forward packets that have completed network delay.
        Applies network loss during transmission.
        
        Args:
            current_step: Current simulation step
            
        Returns:
            list: Packets ready for delivery to NIC
        """
        packets_to_forward = []
        packets_still_in_queue = []
        
        for packet in self.queue:
            if current_step >= packet['will_exit_at']:
                # Packet has traversed the network, check for loss
                if random.random() > self.loss_rate:
                    packets_to_forward.append(packet)
                else:
                    self.packets_dropped += 1
            else:
                packets_still_in_queue.append(packet)
        
        # Limit forwarding by bandwidth
        packets_to_forward = packets_to_forward[:self.bandwidth]
        forwarded_count = len(packets_to_forward)
        
        # Update queue
        self.queue = packets_still_in_queue
        
        self.packets_exited += forwarded_count
        
        return forwarded_count
    
    def get_queue_length(self):
        """Get current queue occupancy."""
        return len(self.queue)
    
    def get_state(self):
        """Get network state."""
        return {
            'queue_length': len(self.queue),
            'queue_capacity': self.capacity,
            'packets_entered': self.packets_entered,
            'packets_exited': self.packets_exited,
            'packets_dropped': self.packets_dropped,
            'loss_rate': self.loss_rate
        }
    
    def reset(self):
        """Reset network state."""
        self.queue = []
        self.packets_entered = 0
        self.packets_exited = 0
        self.packets_dropped = 0
