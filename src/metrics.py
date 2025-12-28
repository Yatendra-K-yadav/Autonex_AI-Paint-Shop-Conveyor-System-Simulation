# metrics.py
# Calculates and formats metrics from simulation results

def print_results(results):
    """
    Print simulation results in a formatted way.
    
    Args:
        results (dict): Dictionary containing simulation results
    """
    
    total_cars = results['total_cars']
    avg_system_time = results['avg_system_time']
    cleaning_station = results['cleaning_station']
    primer_station = results['primer_station']
    painting_station = results['painting_station']
    alert_count = results['alert_count']
    simulation_time = results['simulation_time']
    
    # Build output string
    output = []
    output.append("\n" + "=" * 80)
    output.append("PAINT SHOP CONVEYOR SYSTEM SIMULATION - RESULTS")
    output.append("=" * 80)
    
    output.append(f"\nSimulation Duration: {simulation_time} minutes (8 hours)")
    output.append(f"Total Cars Completed: {total_cars}")
    
    if total_cars > 0:
        output.append(f"Average System Time per Car: {avg_system_time:.2f} minutes")
    else:
        output.append("Average System Time per Car: N/A (No cars completed)")
    
    # STATION 1: CLEANING
    output.append("\n" + "-" * 80)
    output.append("STATION 1: CLEANING")
    output.append("-" * 80)
    output.append(f"Number of Machines: {cleaning_station.num_machines}")
    output.append(f"Utilization: {cleaning_station.get_utilization(simulation_time):.2f}%")
    output.append(f"Max Queue Length: {cleaning_station.max_queue_length} cars")
    output.append(f"Average Wait Time: {cleaning_station.get_avg_wait_time():.2f} minutes")
    output.append(f"Average Processing Time: {cleaning_station.get_avg_processing_time():.2f} minutes")
    output.append(f"Total Cars Processed: {len(cleaning_station.processing_times)}")
    
    # STATION 2: PRIMER
    output.append("\n" + "-" * 80)
    output.append("STATION 2: PRIMER APPLICATION")
    output.append("-" * 80)
    output.append(f"Number of Machines: {primer_station.num_machines}")
    output.append(f"Utilization: {primer_station.get_utilization(simulation_time):.2f}%")
    output.append(f"Max Queue Length: {primer_station.max_queue_length} cars")
    output.append(f"Average Wait Time: {primer_station.get_avg_wait_time():.2f} minutes")
    output.append(f"Average Processing Time: {primer_station.get_avg_processing_time():.2f} minutes")
    output.append(f"Total Cars Processed: {len(primer_station.processing_times)}")
    
    # STATION 3: PAINTING
    output.append("\n" + "-" * 80)
    output.append("STATION 3: PAINTING")
    output.append("-" * 80)
    output.append(f"Number of Machines: {painting_station.num_machines}")
    output.append(f"Utilization: {painting_station.get_utilization(simulation_time):.2f}%")
    output.append(f"Max Queue Length: {painting_station.max_queue_length} cars")
    output.append(f"Average Wait Time: {painting_station.get_avg_wait_time():.2f} minutes")
    output.append(f"Average Processing Time: {painting_station.get_avg_processing_time():.2f} minutes")
    output.append(f"Total Cars Processed: {len(painting_station.processing_times)}")
    
    # BOTTLENECK ANALYSIS
    output.append("\n" + "-" * 80)
    output.append("BOTTLENECK ANALYSIS")
    output.append("-" * 80)
    output.append(f"Total Alerts Triggered: {alert_count}")
    
    # Identify bottleneck station
    utilizations = {
        "Cleaning": cleaning_station.get_utilization(simulation_time),
        "Primer": primer_station.get_utilization(simulation_time),
        "Painting": painting_station.get_utilization(simulation_time)
    }
    
    most_utilized = max(utilizations, key=utilizations.get)
    output.append(f"Most Utilized Station: {most_utilized} ({utilizations[most_utilized]:.2f}%)")
    
    output.append("\n" + "=" * 80)
    
    # Print to console and file
    full_output = "\n".join(output)
    print(full_output)
    
    # Save to file
    with open(config.RESULTS_FILE_PATH, "w") as f:
        f.write(full_output)
    
    return full_output


def get_bottleneck_recommendations(results):
    """
    Analyze simulation results and provide optimization recommendations.
    
    Args:
        results (dict): Dictionary containing simulation results
    
    Returns:
        str: Recommendations for bottleneck mitigation
    """
    
    cleaning_station = results['cleaning_station']
    primer_station = results['primer_station']
    painting_station = results['painting_station']
    simulation_time = results['simulation_time']
    
    recommendations = []
    recommendations.append("\n" + "=" * 80)
    recommendations.append("OPTIMIZATION RECOMMENDATIONS")
    recommendations.append("=" * 80)
    
    # Check each station's utilization
    cleaning_util = cleaning_station.get_utilization(simulation_time)
    primer_util = primer_station.get_utilization(simulation_time)
    painting_util = painting_station.get_utilization(simulation_time)
    
    # High utilization (>80%) means the station is a bottleneck
    if cleaning_util > 80:
        recommendations.append(f"\n❌ BOTTLENECK: Cleaning Station (Utilization: {cleaning_util:.2f}%)")
        recommendations.append("   → Consider adding a 2nd cleaning machine")
        recommendations.append(f"   → Current max queue: {cleaning_station.max_queue_length} cars")
        recommendations.append(f"   → Current avg wait: {cleaning_station.get_avg_wait_time():.2f} min")
    else:
        recommendations.append(f"\n✓ Cleaning Station is OK (Utilization: {cleaning_util:.2f}%)")
    
    if primer_util > 80:
        recommendations.append(f"\n❌ BOTTLENECK: Primer Station (Utilization: {primer_util:.2f}%)")
        recommendations.append("   → Consider adding a 3rd primer machine")
        recommendations.append(f"   → Current max queue: {primer_station.max_queue_length} cars")
        recommendations.append(f"   → Current avg wait: {primer_station.get_avg_wait_time():.2f} min")
    else:
        recommendations.append(f"\n✓ Primer Station is OK (Utilization: {primer_util:.2f}%)")
    
    if painting_util > 80:
        recommendations.append(f"\n❌ BOTTLENECK: Painting Station (Utilization: {painting_util:.2f}%)")
        recommendations.append("   → Consider adding a 2nd painting machine")
        recommendations.append(f"   → Current max queue: {painting_station.max_queue_length} cars")
        recommendations.append(f"   → Current avg wait: {painting_station.get_avg_wait_time():.2f} min")
    else:
        recommendations.append(f"\n✓ Painting Station is OK (Utilization: {painting_util:.2f}%)")
    
    recommendations.append("\n" + "=" * 80)
    
    return "\n".join(recommendations)


# Import config at the end to avoid circular imports
import config