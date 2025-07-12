# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Main entry point for the beach volleyball state machine."""

import argparse
from tests.test_functions import run_comprehensive_tests


def simulate_points(num_points: int) -> None:
    """Simulate N points and print concise history for each point."""
    from state_definitions import create_beach_volleyball_state_machine
    from rally_simulator import simulate_complete_rally
    
    sm = create_beach_volleyball_state_machine()
    
    print(f"Simulating {num_points} points:")
    print("=" * 50)
    
    for point in range(1, num_points + 1):
        rally_sequence, outcome = simulate_complete_rally(sm)
        
        # Create full rally description
        sequence_str = " -> ".join(rally_sequence)
        
        # Extract winner from outcome
        winner = "S" if "serving" in outcome else "R"
        
        print(f"Point {point:2d}: {sequence_str} ({len(rally_sequence)} states, {winner} wins)")


def main() -> None:
    """Main entry point with command-line argument parsing."""
    
    parser = argparse.ArgumentParser(
        description="Beach Volleyball Rally State Machine - Dictionary Representation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --test         # Run comprehensive tests
  python main.py --points 20    # Simulate 20 points
  python main.py                # Show basic usage information
        """
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run comprehensive tests and demonstrations of the state machine'
    )
    
    parser.add_argument(
        '--points',
        type=int,
        nargs='?',
        const=10,
        default=None,
        metavar='N',
        help='Simulate N points and show concise history (default: 10 if --points used without value)'
    )
    
    args = parser.parse_args()
    
    if args.test:
        run_comprehensive_tests()
    elif args.points is not None:
        simulate_points(args.points)
    else:
        print("Beach Volleyball Rally State Machine - Dictionary Representation")
        print("=" * 65)
        print("This module provides a functional approach to modeling beach volleyball")
        print("rally states using a dictionary-based representation.")
        print()
        print("Basic usage:")
        print("  from state_definitions import create_beach_volleyball_state_machine")
        print("  from rally_simulator import simulate_complete_rally")
        print("  sm = create_beach_volleyball_state_machine()")
        print("  rally_sequence, outcome = simulate_complete_rally(sm)")
        print()
        print("For comprehensive tests and examples, run:")
        print("  python main.py --test")
        print("  python main.py --points 20")


if __name__ == "__main__":
    main()
