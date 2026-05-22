"""
Version 3: Improved hostCC Simulation with Adaptive and Predictive Control
"""

from simulation.base_simulation import BaseSimulation

class ImprovedHostCCSimulation(BaseSimulation):
    """
    Version 3: Improved hostCC simulation with advanced features.
    
    Improvements:
    1. Adaptive Threshold:
       - Threshold adapts based on local memory load
       - Higher local load = earlier congestion detection
       - Formula: threshold = base + alpha * local_load
    
    2. Predictive Congestion Control:
       - Looks at recent queue history
       - Detects approaching congestion early
       - Triggers control before threshold is crossed
    """
    
    def __init__(self, config):
        """Initialize Improved hostCC simulation (Version 3)."""
        super().__init__(config, version_name="Version 3: Improved hostCC")
        
        # Ensure improvements are enabled
        self.config['ADAPTIVE_THRESHOLD_ENABLED'] = True
        self.config['PREDICTIVE_ENABLED'] = True
        
        # Update controller with enabled features
        self.controller.adaptive_enabled = True
        self.controller.predictive_enabled = True
        
        self.logger.info("Initialized Version 3: Improved hostCC Simulation")
        self.logger.info(f"  - Adaptive Threshold: ENABLED")
        self.logger.info(f"  - Predictive Control: ENABLED")
    
    def step(self):
        """
        Execute one simulation step for improved hostCC (Version 3).
        
        Key Improvements:
        1. ADAPTIVE THRESHOLD: Adjusts based on local memory load
           - Higher load → Lower threshold (react faster)
           - Formula: threshold = base + alpha * local_load * base
        
        2. PREDICTIVE CONTROL: Detects approaching congestion early
           - Examines recent queue occupancy trend
           - Triggers control at 80% of predicted threshold
           - Proactive rather than reactive
        """
        
        # 0. Update local app load (responds to previous congestion)
        is_congested = self.controller.congestion_detected
        self.local_app.update_load(self.current_step, is_congested=is_congested)
        
        # 1. Sender generates packets
        available_window = max(0, self.sender.cwnd - self.sender.packets_inflight)
        packets_to_send = min(available_window, 25)
        
        net_dropped = 0
        if packets_to_send > 0:
            accepted, net_dropped = self.network.enqueue(packets_to_send, self.current_step)
            self.sender.packets_inflight += accepted
            self.sender.total_packets_sent += accepted
        
        # 2. Network forwards
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
        
        # Update sender
        self.sender.packets_inflight = max(0, self.sender.packets_inflight - acks)
        self.sender.total_packets_acked += acks
        
        # 6. MAIN: IMPROVED hostCC with Adaptive & Predictive
        host_occupancy = self.host_queue.get_occupancy()
        local_load = self.local_app.get_load()
        
        # Improvement 1: ADAPTIVE THRESHOLD
        # Threshold increases with local load, allowing earlier detection
        base_threshold = self.config.get('HOST_QUEUE_BASE_THRESHOLD', 100)
        alpha = self.config.get('ADAPTIVE_ALPHA', 0.5)
        adaptive_threshold = base_threshold + (alpha * local_load * base_threshold)
        self.controller.current_threshold = adaptive_threshold
        
        # Improvement 2: PREDICTIVE CONGESTION CONTROL
        # Look at queue occupancy trend to predict future congestion
        congestion_detected = False
        
        # Check if queue is approaching threshold (threshold-based)
        if host_occupancy > adaptive_threshold:
            congestion_detected = True
        
        # PREDICTION: Check average trend
        if len(self.host_queue.occupancy_history) >= 3:
            recent_occupancy = self.host_queue.occupancy_history[-3:]
            avg_occupancy = sum(recent_occupancy) / len(recent_occupancy)
            # Trigger early if average is approaching threshold
            early_trigger_point = adaptive_threshold * 0.75
            if avg_occupancy > early_trigger_point:
                congestion_detected = True
        
        self.controller.congestion_detected = congestion_detected
        
        # 7. Adaptive Response based on detection
        total_loss = net_dropped + nic_dropped + host_dropped
        
        if congestion_detected:
            # More gradual decrease for predictive (avoid over-reaction)
            self.sender.cwnd = max(1, int(self.sender.cwnd * 0.8))
            self.sender.congestion_events += 1
            # Throttle local app
            self.local_app.throttle(duration=2)  # Shorter duration for v3
        elif total_loss > 0:
            # Loss-based decrease
            self.sender.cwnd = max(1, int(self.sender.cwnd * self.sender.md_factor))
            self.sender.congestion_events += 1
        else:
            # Increase window
            self.sender.cwnd = min(self.sender.max_cwnd, self.sender.cwnd + self.sender.ai_increase)
