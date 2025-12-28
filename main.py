
import os
from src.simulation import PaintShopSimulation
from src.metrics import print_results, get_bottleneck_recommendations


def main():
    """
    Main function to run the complete simulation.
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")
    
    print("\n" + "=" * 80)
    print("PAINT SHOP CONVEYOR SYSTEM SIMULATION")
    print("=" * 80)
    print("\nInitializing simulation...")
    
    # Create and run simulation
    sim = PaintShopSimulation()
    results = sim.run()
    
    # Print results
    print_results(results)
    
    # Print optimization recommendations
    recommendations = get_bottleneck_recommendations(results)
    print(recommendations)
    
    print("\n✓ Simulation complete!")
    print(f"  - Detailed log saved to: output/simulation_log.txt")
    print(f"  - Results saved to: output/metrics_results.txt")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()