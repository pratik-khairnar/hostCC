"""
Local Memory Application Module: Simulates memory-bound local applications
"""

import random

class LocalMemoryApp:
    """
    Simulates background memory-heavy local applications that consume
    host memory bandwidth. This affects available bandwidth for network packets.
    """
    
    def __init__(self, config):
        """
        Initialize the local memory application.
        
        Args:
            config: Configuration parameters dictionary
        """
        self.config = config
        
        # Load parameters (0-1 ratio of total bandwidth)
        self.load = config.get('LOCAL_APP_INITIAL_LOAD', 0.3)
        self.max_load = config.get('LOCAL_APP_MAX_LOAD', 0.9)
        self.min_load = config.get('LOCAL_APP_MIN_LOAD', 0.0)
        
        # Dynamics
        self.increase_rate = config.get('LOCAL_MEMORY_INCREASE_RATE', 0.02)
        self.aggressive_level = config.get('LOCAL_MEMORY_AGGRESSIVE', 0.8)
        
        # Statistics
        self.total_bandwidth = config.get('HOST_TOTAL_MEMORY_BANDWIDTH', 100)
        self.bandwidth_used = 0
        
        # State tracking
        self.is_throttled = False
        self.throttle_duration = 0
        
    def update_load(self, current_step, is_congested=False):
        """
        Update local application load over time.
        Naturally increases unless throttled by hostCC.
        
        Args:
            current_step: Current simulation step
            is_congested: Whether host congestion was detected
        """
        if is_congested and not self.is_throttled:
            # Start throttling when congestion detected
            self.throttle_duration = 5  # Throttle for 5 steps
            self.is_throttled = True
        
        if self.is_throttled:
            # Reduce load progressively
            self.load = max(self.min_load, self.load * 0.7)  # Reduce by 30%
            self.throttle_duration -= 1
            
            if self.throttle_duration <= 0:
                self.is_throttled = False
        else:
            # Naturally increase load (more applications use memory)
            # Add some randomness for realistic behavior
            random_factor = random.uniform(0.8, 1.2)
            increase = self.increase_rate * random_factor
            self.load = min(self.max_load, self.load + increase)
        
        # Ensure bounds
        self.load = max(self.min_load, min(self.max_load, self.load))
        
        # Calculate actual bandwidth used
        self.bandwidth_used = self.load * self.total_bandwidth
    
    def throttle(self, duration=5):
        """
        Throttle the application due to host congestion.
        
        Args:
            duration: Duration of throttling in steps
        """
        self.is_throttled = True
        self.throttle_duration = duration
    
    def get_bandwidth_for_network(self):
        """
        Get available bandwidth for network packets.
        
        Returns:
            float: Available bandwidth for network processing
        """
        return self.total_bandwidth * (1 - self.load)
    
    def get_load(self):
        """Get current local load (0-1)."""
        return self.load
    
    def get_state(self):
        """Get local memory app state."""
        return {
            'load': self.load,
            'bandwidth_used': self.bandwidth_used,
            'bandwidth_available_for_network': self.get_bandwidth_for_network(),
            'is_throttled': self.is_throttled,
            'throttle_remaining': self.throttle_duration if self.is_throttled else 0
        }
    
    def reset(self):
        """Reset local app state."""
        self.load = self.config.get('LOCAL_APP_INITIAL_LOAD', 0.3)
        self.is_throttled = False
        self.throttle_duration = 0
        self.bandwidth_used = 0
