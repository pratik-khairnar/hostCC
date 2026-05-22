"""
Version 1: Normal TCP Simulation (Baseline without host congestion awareness)
"""

from simulation.base_simulation import BaseSimulation

class TCPSimulation(BaseSimulation):
    """
    Version 1: Normal TCP simulation without host congestion control.
    This serves as the baseline implementation.
    
    Behavior:
    - Sender increases CWND gradually (Additive Increase)
    - On packet loss, sender decreases CWND (Multiplicative Decrease)
    - No awareness of host-side congestion
    - Normal TCP AIMD behavior
    """
    
    def __init__(self, config):
        """Initialize TCP simulation (Version 1)."""
        super().__init__(config, version_name="Version 1: Normal TCP")
        self.logger.info("Initialized Version 1: Normal TCP Simulation")
    
    def step(self):
        """
        Execute one simulation step for normal TCP with proper packet flow.
        """
        
        # 0. Update local app load (naturally increases, no control in V1)
        self.local_app.update_load(self.current_step, is_congested=False)
        
        # 1. Sender attempts to generate and send packets
        available_window = max(0, self.sender.cwnd - self.sender.packets_inflight)
        packets_to_send = min(available_window, 25)  # Limit burst to 25/step
        
        net_dropped = 0
        if packets_to_send > 0:
            accepted, net_dropped = self.network.enqueue(packets_to_send, self.current_step)
            self.sender.packets_inflight += accepted
            self.sender.total_packets_sent += accepted
        
        # 2. Network forwards delivered packets
        packets_delivered = self.network.forward_packets(self.current_step)
        
        # 3. NIC receives from network and forwards to host queue
        nic_accepted, nic_dropped = self.nic.receive_packets(packets_delivered, self.current_step)
        packets_for_host = self.nic.forward_to_host_queue(self.current_step)
        
        # 4. Host queue receives and processes
        host_accepted, host_dropped = self.host_queue.receive_packets(
            packets_for_host,
            self.current_step,
            local_app_load=self.local_app.get_load()
        )
        
        acks = self.host_queue.process_packets(
            self.current_step,
            local_app_load=self.local_app.get_load()
        )
        
        # 5. Update sender with ACKs and loss feedback
        self.sender.packets_inflight = max(0, self.sender.packets_inflight - acks)
        self.sender.total_packets_acked += acks
        
        # 6. Congestion control (AIMD)
        total_loss = net_dropped + nic_dropped + host_dropped
        
        if total_loss > 0:
            # Multiplicative Decrease
            self.sender.cwnd = max(1, int(self.sender.cwnd * self.sender.md_factor))
            self.sender.congestion_events += 1
        else:
            # Additive Increase
            self.sender.cwnd = min(self.sender.max_cwnd, self.sender.cwnd + self.sender.ai_increase)
