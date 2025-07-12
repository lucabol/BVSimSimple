# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Main entry point for the beach volleyball state machine."""

import argparse
from test_functions import run_comprehensive_tests


def main() -> None:
    """Main entry point with command-line argument parsing."""
    
    parser = argparse.ArgumentParser(
        description="Beach Volleyball Rally State Machine - Dictionary Representation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --test    # Run comprehensive tests
  python main.py           # Show basic usage information
        """
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run comprehensive tests and demonstrations of the state machine'
    )
    
    args = parser.parse_args()
    
    if args.test:
        run_comprehensive_tests()
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


if __name__ == "__main__":
    main()
