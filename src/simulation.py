# simulation.py
# Main simulation engine using SimPy

import simpy
import config
from src.entities import Car, Station
from src.bottleneck_detector import BottleneckDetector

class PaintShopSimulation:
    """
    Main simulation class that orchestrates the entire paint shop process.
    """
    
    def __init__(self):
        """Initialize simulation"""
        # SimPy environment (the simulation clock)
        self.env = simpy.Environment()
        
        # Create stations with their resources (machines)
        self.cleaning_station = Station("Cleaning", config.CLEANING_MACHINES)
        self.primer_station = Station("Primer", config.PRIMER_MACHINES)
        self.painting_station = Station("Painting", config.PAINTING_MACHINES)
        
        # SimPy Resources (limit how many cars can use each station simultaneously)
        self.cleaning_resource = simpy.Resource(self.env, config.CLEANING_MACHINES)
        self.primer_resource = simpy.Resource(self.env, config.PRIMER_MACHINES)
        self.painting_resource = simpy.Resource(self.env, config.PAINTING_MACHINES)
        
        # Tracking variables
        self.cars_completed = []  # List of completed Car objects
        self.cars_in_system = 0  # Currently processing cars
        self.car_counter = 0  # Counter for car IDs
        self.log_file = open(config.LOG_FILE_PATH, "w")
        
        # Bottleneck detector
        self.bottleneck_detector = BottleneckDetector(config.BOTTLENECK_THRESHOLD)
        self.alert_count = 0
    
    def log(self, message):
        """Write message based on verbosity level"""
        timestamp = f"[{self.env.now:.1f}]"
        full_message = f"{timestamp} {message}"
        
        # Determine if this message should be logged
        should_log = False
        
        if config.LOG_DETAIL_LEVEL == "DETAILED":
            # Log everything
            should_log = True
        
        elif config.LOG_DETAIL_LEVEL == "SUMMARY":
            # Only log important events
            important_keywords = ["ARRIVED", "EXITED", "ALERT", "STOP accepting", "SIMULATION"]
            should_log = any(keyword in message for keyword in important_keywords)
        
        elif config.LOG_DETAIL_LEVEL == "MINIMAL":
            # Only log alerts
            should_log = "ALERT" in message or "STOP accepting" in message
        
        # Write to console and file if it should be logged
        if should_log:
            if config.VERBOSE_LOGGING:
                print(full_message)
            self.log_file.write(full_message + "\n")
        else:
            # Always write to file, just not to console
            self.log_file.write(full_message + "\n")
        
        self.log_file.flush()
    
    def car_generator(self):
        """
        Generator process that creates new cars at random intervals.
        Runs until SIMULATION_TIME is reached.
        """
        while True:
            # Wait for random interval until next car arrives
            yield self.env.timeout(config.get_car_arrival_interval())
            
            # Stop accepting new cars after 480 minutes
            if self.env.now >= config.NEW_CAR_ACCEPTANCE_TIME:
                self.log(f"STOP accepting new cars (shift end at {config.NEW_CAR_ACCEPTANCE_TIME} min)")
                break
            
            # Create new car
            self.car_counter += 1
            car = Car(self.car_counter, self.env.now)
            self.log(f"Car {car.car_id} ARRIVED")
            
            # Start car's journey through the system
            self.cars_in_system += 1
            self.env.process(self.car_journey(car))
    
    def car_journey(self, car):
        """
        Process that represents a single car's journey through all stations.
        """
        # STATION 1: CLEANING
        self.log(f"Car {car.car_id} entering Cleaning queue")
        car.cleaning_start_time = self.env.now
        
        # Request access to cleaning machine
        with self.cleaning_resource.request() as request:
            # Wait for machine to be available
            yield request
            car.cleaning_start_time = self.env.now
            
            # Update station tracking
            wait_time = car.cleaning_start_time - car.arrival_time
            self.cleaning_station.add_wait_time(wait_time)
            
            self.log(f"Car {car.car_id} STARTED Cleaning")
            
            # Process cleaning (takes 15-20 minutes)
            cleaning_time = config.get_cleaning_time()
            yield self.env.timeout(cleaning_time)
            
            car.cleaning_end_time = self.env.now
            self.cleaning_station.add_processing_time(cleaning_time)
            self.cleaning_station.total_busy_time += cleaning_time
            
            self.log(f"Car {car.car_id} FINISHED Cleaning")
        
        # Update queue status
        self.update_queue_status()
        
        # STATION 2: PRIMER APPLICATION
        self.log(f"Car {car.car_id} entering Primer queue")
        
        with self.primer_resource.request() as request:
            # Wait for machine to be available
            yield request
            car.primer_start_time = self.env.now
            
            # Update station tracking
            wait_time = car.primer_start_time - car.cleaning_end_time
            self.primer_station.add_wait_time(wait_time)
            
            self.log(f"Car {car.car_id} STARTED Primer")
            
            # Process primer (takes 25-35 minutes)
            primer_time = config.get_primer_time()
            yield self.env.timeout(primer_time)
            
            car.primer_end_time = self.env.now
            self.primer_station.add_processing_time(primer_time)
            self.primer_station.total_busy_time += primer_time
            
            self.log(f"Car {car.car_id} FINISHED Primer")
        
        # Update queue status
        self.update_queue_status()
        
        # STATION 3: PAINTING
        self.log(f"Car {car.car_id} entering Painting queue")
        
        with self.painting_resource.request() as request:
            # Wait for machine to be available
            yield request
            car.painting_start_time = self.env.now
            
            # Update station tracking
            wait_time = car.painting_start_time - car.primer_end_time
            self.painting_station.add_wait_time(wait_time)
            
            self.log(f"Car {car.car_id} STARTED Painting")
            
            # Process painting (takes 30-40 minutes)
            painting_time = config.get_painting_time()
            yield self.env.timeout(painting_time)
            
            car.painting_end_time = self.env.now
            self.painting_station.add_processing_time(painting_time)
            self.painting_station.total_busy_time += painting_time
            
            self.log(f"Car {car.car_id} FINISHED Painting")
        
        # CAR EXITS SYSTEM
        car.exit_time = self.env.now
        self.cars_completed.append(car)
        self.cars_in_system -= 1
        
        self.log(f"Car {car.car_id} EXITED SYSTEM (Total time: {car.get_total_system_time():.1f} min)")
    
    def update_queue_status(self):
        """
        Check current queue lengths and detect bottlenecks.
        """
        cleaning_queue = len(self.cleaning_resource.queue)
        primer_queue = len(self.primer_resource.queue)
        painting_queue = len(self.painting_resource.queue)
        
        # Update station queue tracking
        self.cleaning_station.update_queue(cleaning_queue, self.env.now)
        self.primer_station.update_queue(primer_queue, self.env.now)
        self.painting_station.update_queue(painting_queue, self.env.now)
        
        # Check for bottlenecks
        if self.bottleneck_detector.check_bottleneck("Cleaning", cleaning_queue, self.env.now):
            self.alert_count += 1
            self.log(f"ALERT: Queue at Cleaning has {cleaning_queue} cars waiting")
        
        if self.bottleneck_detector.check_bottleneck("Primer", primer_queue, self.env.now):
            self.alert_count += 1
            self.log(f"ALERT: Queue at Primer has {primer_queue} cars waiting")
        
        if self.bottleneck_detector.check_bottleneck("Painting", painting_queue, self.env.now):
            self.alert_count += 1
            self.log(f"ALERT: Queue at Painting has {painting_queue} cars waiting")
    
    def run(self):
        """
        Run the complete simulation.
        Start the car generator and run until all cars are processed.
        """
        self.log("=" * 80)
        self.log("PAINT SHOP CONVEYOR SYSTEM SIMULATION STARTED")
        self.log("=" * 80)
        
        # Start car generator process
        self.env.process(self.car_generator())
        
        # Run simulation
        # We simulate beyond 480 minutes to let cars in process finish
        self.env.run(until=2000)  # Large number to ensure all cars finish
        
        self.log("=" * 80)
        self.log("SIMULATION COMPLETE")
        self.log("=" * 80)
        
        self.log_file.close()
        
        return self.get_results()
    
    def get_results(self):
        """
        Calculate and return all metrics from the simulation.
        """
        simulation_time = config.SIMULATION_TIME
        
        total_cars = len(self.cars_completed)
        
        if total_cars == 0:
            avg_system_time = 0
        else:
            avg_system_time = sum([c.get_total_system_time() for c in self.cars_completed]) / total_cars
        
        results = {
            'total_cars': total_cars,
            'avg_system_time': avg_system_time,
            'cleaning_station': self.cleaning_station,
            'primer_station': self.primer_station,
            'painting_station': self.painting_station,
            'alert_count': self.alert_count,
            'cars_completed': self.cars_completed,
            'simulation_time': simulation_time
        }
        
        return results