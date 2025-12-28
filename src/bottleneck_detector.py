# bottleneck_detector.py
# Detects when queues exceed threshold and triggers alerts

class BottleneckDetector:
    """
    Monitors queue lengths at each station.
    Triggers alerts when queues exceed a defined threshold.
    """
    
    def __init__(self, threshold=3):
        """
        Initialize bottleneck detector.
        
        Args:
            threshold (int): Queue length threshold for alert (default: 3)
        """
        self.threshold = threshold
        self.alerts = {}  # Track alerts per station to avoid duplicates
        
    def check_bottleneck(self, station_name, current_queue_length, current_time):
        """
        Check if a station has a bottleneck (queue exceeds threshold).
        
        Args:
            station_name (str): Name of the station to check
            current_queue_length (int): Current number of cars waiting
            current_time (float): Current simulation time
        
        Returns:
            bool: True if bottleneck detected, False otherwise
        """
        # If queue exceeds threshold, it's a bottleneck
        if current_queue_length > self.threshold:
            return True
        
        return False
    
    def reset_alerts(self):
        """Clear alert history"""
        self.alerts = {}