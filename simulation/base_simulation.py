"""
Base Simulation Class: Common functionality for all simulation versions
"""

from modules.sender import Sender
from modules.network_queue import NetworkQueue
from modules.nic_buffer import NICBuffer
from modules.host_queue import HostQueue
from modules.local_app import LocalMemoryApp
from modules.hostcc_controller import hostCCController
from utils.metrics import MetricsCollector
from utils.logger import Logger
import random

class BaseSimulation:
    """
    Base class for all simulation versions.
    Provides common simulation infrastructure.
    """
    
    def __init__(self, config, version_name="baseline"):
        """
        Initialize simulation.
        
        Args:
            config: Configuration parameters dictionary
            version_name: Name of this simulation version
        """
        self.config = config
        self.version_name = version_name
        self.current_step = 0
        self.total_steps = config.get('SIMULATION_TIME', 100)
        
        # Initialize random seed
        random.seed(config.get('RANDOM_SEED', 42))
        
        # Initialize modules
        self.sender = Sender(config)
        self.network = NetworkQueue(config)
        self.nic = NICBuffer(config)
        self.host_queue = HostQueue(config)
        self.local_app = LocalMemoryApp(config)
        self.controller = hostCCController(config)
        
        # Metrics and logging
        self.metrics = MetricsCollector(version_name)
        self.logger = Logger(config.get('VERBOSE', False))
        
        # State tracking
        self.packets_in_flight = {}  # Track packets for RTT calculation
    
    def run(self):
        """
        Run the simulation.
        
        Returns:
            MetricsCollector: Collected metrics
        """
        self.logger.info(f"Starting {self.version_name} simulation for {self.total_steps} steps")
        
        for step in range(self.total_steps):
            self.current_step = step
            self.step()
            
            # Record metrics every step
            self._record_metrics()
        
        # Calculate final metrics
        self._finalize_metrics()
        
        self.logger.info(f"Simulation {self.version_name} completed")
        
        return self.metrics
    
    def step(self):
        """
        Execute one simulation step.
        To be overridden by subclasses for different behaviors.
        """
        pass
    
    def _sender_generates_packets(self):
        """
        Sender generates packets based on congestion window.
        
        Returns:
            int: Number of packets generated
        """
        packets_to_send = self.sender.generate_packets(self.current_step)
        
        if packets_to_send > 0:
            # Packets enter network queue
            accepted, dropped = self.network.enqueue(packets_to_send, self.current_step)
            
            # Track for RTT calculation
            for i in range(accepted):
                packet_id = len(self.packets_in_flight)
                self.packets_in_flight[packet_id] = {
                    'sent_at': self.current_step,
                    'acked': False
                }
        
        return packets_to_send
    
    def _network_forwards_packets(self):
        """
        Network forwards packets that completed transit.
        
        Returns:
            int: Number of packets forwarded
        """
        packets_forwarded = self.network.forward_packets(self.current_step)
        return packets_forwarded
    
    def _nic_receives_and_forwards(self):
        """
        NIC receives packets and forwards to host queue.
        
        Returns:
            tuple: (packets_to_host, packets_dropped_at_nic)
        """
        packets_from_network = self.network.forward_packets(self.current_step)
        
        if packets_from_network > 0:
            # Receive at NIC
            accepted, dropped = self.nic.receive_packets(
                [{'id': i} for i in range(packets_from_network)],
                self.current_step
            )
        
        # Forward from NIC to host queue
        packets = self.nic.forward_to_host_queue(self.current_step)
        
        return len(packets), self.nic.get_state()['packets_dropped']
    
    def _host_queue_process(self):
        """
        Host queue receives and processes packets.
        
        Returns:
            int: Number of packets processed
        """
        # This is called after packets arrive at host queue
        # The actual packet flow is more detailed in subclasses
        return 0
    
    def _record_metrics(self):
        """Record metrics for current step."""
        self.metrics.record_step(
            self.current_step,
            self.sender.get_state(),
            self.network.get_state(),
            self.nic.get_state(),
            self.host_queue.get_state(),
            self.local_app.get_state(),
            self.controller.get_state()
        )
    
    def _finalize_metrics(self):
        """Calculate and record final metrics."""
        sender_state = self.sender.get_state()
        total_sent = sender_state['total_sent']
        total_acked = sender_state['total_acked']
        total_dropped = (
            self.network.get_state()['packets_dropped'] +
            self.nic.get_state()['packets_dropped'] +
            self.host_queue.get_state()['packets_dropped']
        )
        
        # Calculate throughput (packets per step)
        throughput = total_acked / self.total_steps if self.total_steps > 0 else 0
        
        # Average RTT
        avg_rtt = sender_state['rtt']
        
        # Average host queue load
        avg_load = self.host_queue.get_average_occupancy()
        
        self.metrics.record_final_metrics(
            throughput,
            total_sent,
            total_dropped,
            avg_rtt,
            avg_load
        )
    
    def reset(self):
        """Reset simulation to initial state."""
        self.current_step = 0
        self.sender.reset()
        self.network.reset()
        self.nic.reset()
        self.host_queue.reset()
        self.local_app.reset()
        self.controller.reset()
        self.metrics = MetricsCollector(self.version_name)
        self.packets_in_flight = {}
    
    def get_metrics(self):
        """Get collected metrics."""
        return self.metrics
