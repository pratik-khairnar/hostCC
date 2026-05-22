"""
hostCC Controller Module: Main decision-making module for congestion control
"""

class hostCCController:
    """
    Controls host-side congestion detection and response.
    Monitors host queue occupancy and triggers throttling/notification.
    """
    
    def __init__(self, config):
        """
        Initialize the hostCC controller.
        
        Args:
            config: Configuration parameters dictionary
        """
        self.config = config
        
        # Detection parameters
        self.base_threshold = config.get('HOST_QUEUE_BASE_THRESHOLD', 100)
        self.current_threshold = self.base_threshold
        
        # For improved version
        self.adaptive_enabled = config.get('ADAPTIVE_THRESHOLD_ENABLED', False)
        self.alpha = config.get('ADAPTIVE_ALPHA', 0.5)
        
        self.predictive_enabled = config.get('PREDICTIVE_ENABLED', False)
        self.prediction_window = config.get('PREDICTION_WINDOW', 5)
        self.prediction_threshold_multiplier = config.get('PREDICTION_THRESHOLD_MULTIPLIER', 0.8)
        
        # State
        self.congestion_detected = False
        self.congestion_count = 0
        self.last_action_step = -1
        
        # History
        self.detection_history = []
        
    def detect_congestion(self, host_queue_occupancy, host_queue_capacity, 
                         local_app_load, version=2):
        """
        Detect host congestion based on queue occupancy.
        
        Args:
            host_queue_occupancy: Current host queue occupancy
            host_queue_capacity: Host queue capacity
            local_app_load: Local memory load (0-1)
            version: Simulation version (1=TCP, 2=hostCC, 3=improved)
            
        Returns:
            bool: Whether congestion is detected
        """
        if version == 1:
            # Version 1: No host congestion detection
            return False
        
        # Base threshold
        self.current_threshold = self.base_threshold
        
        # Update threshold based on version
        if version >= 2 and self.adaptive_enabled:
            # Adaptive threshold: higher load means lower tolerance
            self.current_threshold = self.base_threshold + (self.alpha * local_app_load * self.base_threshold)
        
        # Check for congestion
        congestion = host_queue_occupancy > self.current_threshold
        
        # Update state
        if congestion:
            self.congestion_count += 1
            self.congestion_detected = True
        else:
            self.congestion_detected = False
        
        return congestion
    
    def get_notification_signal(self):
        """
        Generate congestion notification for sender.
        Similar to ECN (Explicit Congestion Notification) in TCP.
        
        Returns:
            bool: Whether sender should reduce rate
        """
        return self.congestion_detected
    
    def get_throttle_signal(self):
        """
        Signal to throttle local application.
        
        Returns:
            bool: Whether to throttle local app
        """
        return self.congestion_detected
    
    def get_state(self):
        """Get controller state."""
        return {
            'threshold': self.current_threshold,
            'base_threshold': self.base_threshold,
            'congestion_detected': self.congestion_detected,
            'congestion_count': self.congestion_count,
            'adaptive_enabled': self.adaptive_enabled,
            'predictive_enabled': self.predictive_enabled
        }
    
    def reset(self):
        """Reset controller state."""
        self.current_threshold = self.base_threshold
        self.congestion_detected = False
        self.congestion_count = 0
        self.last_action_step = -1
        self.detection_history = []
