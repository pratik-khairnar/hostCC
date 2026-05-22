"""
Logger Module: Logging utilities for simulation
"""

class Logger:
    """
    Simple logging utility for simulation.
    """
    
    def __init__(self, verbose=False):
        """
        Initialize logger.
        
        Args:
            verbose: Whether to print detailed logs
        """
        self.verbose = verbose
        self.logs = []
    
    def log(self, message, level='INFO'):
        """
        Log a message.
        
        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        log_line = f"[{level}] {message}"
        self.logs.append(log_line)
        
        if self.verbose:
            print(log_line)
    
    def info(self, message):
        """Log info message."""
        self.log(message, 'INFO')
    
    def warning(self, message):
        """Log warning message."""
        self.log(message, 'WARNING')
    
    def error(self, message):
        """Log error message."""
        self.log(message, 'ERROR')
    
    def debug(self, message):
        """Log debug message."""
        if self.verbose:
            self.log(message, 'DEBUG')
    
    def get_logs(self):
        """Get all logs."""
        return self.logs
    
    def save_logs(self, filename):
        """Save logs to file."""
        try:
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except:
            pass
        
        with open(filename, 'w') as f:
            for log in self.logs:
                f.write(log + '\n')
        
        print(f"Logs saved to {filename}")
    
    def clear(self):
        """Clear logs."""
        self.logs = []
