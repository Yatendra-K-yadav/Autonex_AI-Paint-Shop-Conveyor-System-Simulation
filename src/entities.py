
class Car:
    """
    Represents a car body in the paint shop.
    Tracks all timestamps as the car moves through stations.
    """
    
    def __init__(self, car_id, arrival_time):
        """
        Initialize a new car.
        
        Args:
            car_id (int): Unique identifier for the car
            arrival_time (float): Time when car arrived at the system (simulation time)
        """
        self.car_id = car_id
        self.arrival_time = arrival_time
        
        # Timestamps for each station
        self.cleaning_start_time = None
        self.cleaning_end_time = None
        
        self.primer_start_time = None
        self.primer_end_time = None
        
        self.painting_start_time = None
        self.painting_end_time = None
        
        # System exit time
        self.exit_time = None
    
    def get_total_system_time(self):
        """Calculate total time car spent in entire system"""
        if self.exit_time is None:
            return None
        return self.exit_time - self.arrival_time
    
    def get_cleaning_wait_time(self):
        """Calculate wait time before cleaning"""
        if self.cleaning_start_time is None:
            return None
        return self.cleaning_start_time - self.arrival_time
    
    def get_primer_wait_time(self):
        """Calculate wait time before primer"""
        if self.primer_start_time is None:
            return None
        return self.primer_start_time - self.cleaning_end_time
    
    def get_painting_wait_time(self):
        """Calculate wait time before painting"""
        if self.painting_start_time is None:
            return None
        return self.painting_start_time - self.primer_end_time
    
    def __repr__(self):
        return f"Car_{self.car_id}"


class Station:
    """
    Represents a work station with metrics tracking.
    """
    
    def __init__(self, name, num_machines):
        """
        Initialize a station.
        
        Args:
            name (str): Station name (e.g., "Cleaning", "Primer", "Painting")
            num_machines (int): Number of machines at this station
        """
        self.name = name
        self.num_machines = num_machines
        self.num_busy = 0  # Current number of busy machines
        self.total_busy_time = 0  # Cumulative busy time
        self.current_queue_length = 0  # Current cars waiting
        self.max_queue_length = 0  # Peak queue length ever seen
        
        # For calculating average queue length
        self.queue_length_history = []  # List of (time, queue_length) tuples
        self.last_queue_change_time = 0
        
        # Wait times for all cars at this station
        self.wait_times = []
        
        # Processing times for all cars at this station
        self.processing_times = []
    
    def add_wait_time(self, wait_time):
        """Record a car's wait time at this station"""
        self.wait_times.append(wait_time)
    
    def add_processing_time(self, processing_time):
        """Record a car's processing time at this station"""
        self.processing_times.append(processing_time)
    
    def update_queue(self, new_length, current_time):
        """Update queue length and track history"""
        self.current_queue_length = new_length
        if new_length > self.max_queue_length:
            self.max_queue_length = new_length
        self.queue_length_history.append((current_time, new_length))
    
    def get_avg_wait_time(self):
        """Calculate average wait time at this station"""
        if len(self.wait_times) == 0:
            return 0
        return sum(self.wait_times) / len(self.wait_times)
    
    def get_avg_processing_time(self):
        """Calculate average processing time at this station"""
        if len(self.processing_times) == 0:
            return 0
        return sum(self.processing_times) / len(self.processing_times)
    
    def get_utilization(self, total_simulation_time):
        """
        Calculate machine utilization percentage.
        Utilization = (total busy time) / (num_machines * total time)
        """
        if total_simulation_time == 0:
            return 0
        return (self.total_busy_time / (self.num_machines * total_simulation_time)) * 100
    
    def __repr__(self):
        return f"Station_{self.name}"