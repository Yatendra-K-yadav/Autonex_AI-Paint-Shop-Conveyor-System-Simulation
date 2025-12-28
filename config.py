# Configuration file for Paint Shop Simulation
# All parameters in one place for easy modification

import random

# ============================================================================
# SIMULATION TIMING PARAMETERS
# ============================================================================
SIMULATION_TIME = 480  # 8 hours in minutes
NEW_CAR_ACCEPTANCE_TIME = 480  # Stop accepting new cars after 480 minutes

# ============================================================================
# CAR ARRIVAL PARAMETERS
# ============================================================================
CAR_ARRIVAL_INTERVAL_MIN = 8  # Minimum minutes between arrivals
CAR_ARRIVAL_INTERVAL_MAX = 12  # Maximum minutes between arrivals

# ============================================================================
# STATION 1: CLEANING
# ============================================================================
CLEANING_MACHINES = 1
CLEANING_TIME_MIN = 15  # minutes
CLEANING_TIME_MAX = 20  # minutes

# ============================================================================
# STATION 2: PRIMER APPLICATION
# ============================================================================
PRIMER_MACHINES = 2
PRIMER_TIME_MIN = 25  # minutes
PRIMER_TIME_MAX = 35  # minutes

# ============================================================================
# STATION 3: PAINTING
# ============================================================================
PAINTING_MACHINES = 1
PAINTING_TIME_MIN = 30  # minutes
PAINTING_TIME_MAX = 40  # minutes

# ============================================================================
# BOTTLENECK DETECTION PARAMETERS
# ============================================================================
BOTTLENECK_THRESHOLD = 3  # Alert if queue > this many cars

# ============================================================================
# LOGGING PARAMETERS
# ============================================================================
VERBOSE_LOGGING = True  # Set to False to reduce console output
LOG_DETAIL_LEVEL = "SUMMARY"  # Only logs arrivals, exits, alerts
LOG_FILE_PATH = "output/simulation_log.txt"
RESULTS_FILE_PATH = "output/metrics_results.txt"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_car_arrival_interval():
    """Returns random arrival interval in minutes"""
    return random.uniform(CAR_ARRIVAL_INTERVAL_MIN, CAR_ARRIVAL_INTERVAL_MAX)

def get_cleaning_time():
    """Returns random cleaning time in minutes"""
    return random.uniform(CLEANING_TIME_MIN, CLEANING_TIME_MAX)

def get_primer_time():
    """Returns random primer time in minutes"""
    return random.uniform(PRIMER_TIME_MIN, PRIMER_TIME_MAX)

def get_painting_time():
    """Returns random painting time in minutes"""
    return random.uniform(PAINTING_TIME_MIN, PAINTING_TIME_MAX)