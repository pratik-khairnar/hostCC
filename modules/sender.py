"""
Sender Module: Simulates the packet sender with congestion control
"""

class Sender:
    """
    Sender module that generates packets based on sending rate and
    adapts to congestion feedback.
    """
    
    def __init__(self, config):
        """
        Initialize the sender.
        
        Args:
            config: Configuration parameters dictionary
        """
        self.config = config
        
        # Window and rate control
        self.cwnd = config.get('INITIAL_CWND', 10)  # Congestion window
        self.max_cwnd = config.get('MAX_CWND', 1000)
        
        # Sending state
        self.packets_to_send = 0
        self.packets_sent = 0
        self.packets_inflight = 0
        
        # RTT and timing
        self.rtt = config.get('RTT_INITIAL', 10)
        self.rtt_min = config.get('RTT_INITIAL', 10)
        
        # Congestion control parameters
        self.ai_increase = config.get('AI_INCREASE', 1)
        self.md_factor = config.get('MD_FACTOR', 0.5)
        
        # Statistics
        self.total_packets_sent = 0
        self.total_packets_acked = 0
        self.congestion_events = 0
        
        # History for feedback
        self.last_packet_send_time = 0
        self.ack_received = 0
        
    def update_window(self, ack_count, loss_detected=False, host_congestion=False):
        """
        Update congestion window based on ACK and loss signals.
        
        Args:
            ack_count: Number of packets acknowledged
            loss_detected: Whether packet loss was detected
            host_congestion: Whether host congestion was detected
        """
        self.packets_inflight = max(0, self.packets_inflight - ack_count)
        
        if loss_detected or host_congestion:
            # Multiplicative decrease (MD)
            self.cwnd = max(1, int(self.cwnd * self.md_factor))
            if loss_detected or host_congestion:
                self.congestion_events += 1
        else:
            # Additive increase (AI)
            self.cwnd = min(self.max_cwnd, self.cwnd + self.ai_increase)
    
    def generate_packets(self, current_step):
        """
        Generate packets based on current cwnd.
        
        Args:
            current_step: Current simulation step
            
        Returns:
            int: Number of packets to send this step
        """
        # Can send up to cwnd - inflight packets
        available_to_send = max(0, self.cwnd - self.packets_inflight)
        
        # Send based on available window
        packets_this_step = min(available_to_send, 10)  # Limit per step
        
        if packets_this_step > 0:
            self.packets_inflight += packets_this_step
            self.total_packets_sent += packets_this_step
            self.last_packet_send_time = current_step
            
        return packets_this_step
    
    def receive_acks(self, ack_count):
        """
        Process received ACKs.
        
        Args:
            ack_count: Number of ACKs received
        """
        self.total_packets_acked += ack_count
        self.ack_received += ack_count
    
    def get_state(self):
        """
        Get current sender state.
        
        Returns:
            dict: Current state information
        """
        return {
            'cwnd': self.cwnd,
            'packets_inflight': self.packets_inflight,
            'total_sent': self.total_packets_sent,
            'total_acked': self.total_packets_acked,
            'rtt': self.rtt,
            'congestion_events': self.congestion_events
        }
    
    def reset(self):
        """Reset sender state for new simulation."""
        self.cwnd = self.config.get('INITIAL_CWND', 10)
        self.packets_to_send = 0
        self.packets_sent = 0
        self.packets_inflight = 0
        self.total_packets_sent = 0
        self.total_packets_acked = 0
        self.congestion_events = 0
        self.ack_received = 0
