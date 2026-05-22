"""
Version 2: hostCC Baseline Simulation (Paper's original concept)
"""

from simulation.base_simulation import BaseSimulation

class hostCCSimulation(BaseSimulation):
    """
    Version 2: hostCC simulation with basic host congestion control.
    Implements the original paper's concept.
    
    Behavior:
    - Monitors host queue occupancy (virtual IIO)
    - When host queue exceeds threshold:
      * Reduces local application memory load
      * Sends congestion notification to sender
    - Sender reacts to host congestion similar to ECN
    """
    
    def __init__(self, config):
        """Initialize hostCC simulation (Version 2)."""
        super().__init__(config, version_name="Version 2: hostCC Baseline")
        self.logger.info("Initialized Version 2: hostCC Baseline Simulation")
    
    def step(self):
        """
        Execute one simulation step for hostCC (Version 2).
        
        Main difference from V1:
        - Monitor host queue occupancy
        - When queue fills up, throttle local app and notify sender
        - Sender backs off BEFORE packets drop
        """
        
        # 0. Update local app load (responds to previous congestion detection)
        is_congested = self.controller.congestion_detected
        self.local_app.update_load(self.current_step, is_congested=is_congested)
        
        # 1. Sender attempts to generate packets (limited by CWND)
        available_window = max(0, self.sender.cwnd - self.sender.packets_inflight)
        packets_to_send = min(available_window, 25)
        
        net_dropped = 0
        if packets_to_send > 0:
            accepted, net_dropped = self.network.enqueue(packets_to_send, self.current_step)
            self.sender.packets_inflight += accepted
            self.sender.total_packets_sent += accepted
        
        # 2. Network forwards delivered packets
        packets_delivered = self.network.forward_packets(self.current_step)
        
        # 3. NIC receives and forwards
        nic_accepted, nic_dropped = self.nic.receive_packets(packets_delivered, self.current_step)
        packets_for_host = self.nic.forward_to_host_queue(self.current_step)
        
        # 4. Host queue receives
        host_accepted, host_dropped = self.host_queue.receive_packets(
            packets_for_host,
            self.current_step,
            local_app_load=self.local_app.get_load()
        )
        
        # 5. Host queue processes
        acks = self.host_queue.process_packets(
            self.current_step,
            local_app_load=self.local_app.get_load()
        )
        
        # Update sender with ACKs
        self.sender.packets_inflight = max(0, self.sender.packets_inflight - acks)
        self.sender.total_packets_acked += acks
        
        # 6. MAIN: hostCC detects host congestion
        host_occupancy = self.host_queue.get_occupancy()
        congestion_detected = self.controller.detect_congestion(
            host_queue_occupancy=host_occupancy,
            host_queue_capacity=self.host_queue.capacity,
            local_app_load=self.local_app.get_load(),
            version=2
        )
        
        # 7. Respond to congestion detection
        total_loss = net_dropped + nic_dropped + host_dropped
        
        if congestion_detected:
            # Reduce CWND to back off sender (like receiving ECN)
            self.sender.cwnd = max(1, int(self.sender.cwnd * 0.75))  # Less aggressive than MD_FACTOR
            self.sender.congestion_events += 1
            # Throttle local app to reduce bandwidth contention
            self.local_app.throttle(duration=3)
        elif total_loss > 0:
            # Loss-based decrease (normal TCP)
            self.sender.cwnd = max(1, int(self.sender.cwnd * self.sender.md_factor))
            self.sender.congestion_events += 1
        else:
            # No congestion - increase window
            self.sender.cwnd = min(self.sender.max_cwnd, self.sender.cwnd + self.sender.ai_increase)
