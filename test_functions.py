# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Test functions for the beach volleyball state machine."""

from decimal import Decimal
from types_ import ActionType
from state_definitions import create_beach_volleyball_state_machine, get_winning_team
from rally_simulator import simulate_rally_step, simulate_complete_rally
from team_templates import get_common_state_templates
from match_simulator import simulate_match_points
from display import print_state_machine_summary


def test_state_machine_creation() -> None:
    """Test the creation and basic properties of the state machine."""
    sm = create_beach_volleyball_state_machine()
    assert sm.initial_state == "s_serve_ready"
    assert len(sm.terminal_states) > 0
    assert sm.validate_probabilities()
    print("State machine creation test passed!")


def test_winning_conditions() -> None:
    """Test the win conditions for different terminal states."""
    test_cases = [
        ("s_serve_ace", "serving"),
        ("s_serve_error", "receiving"),
        ("r_attack_kill", "receiving"),
        ("s_block_kill", "serving")
    ]
    
    for state, expected_winner in test_cases:
        winner = get_winning_team(state)
        assert winner == expected_winner, f"Expected {expected_winner} for {state}, got {winner}"
    
    print("Win conditions test passed!")


def test_rally_simulation() -> None:
    """Test the rally simulation functions."""
    sm = create_beach_volleyball_state_machine()
    
    # Test single step simulation
    next_state = simulate_rally_step(sm, "s_serve_ready")
    assert next_state is not None
    assert sm.is_valid_transition("s_serve_ready", next_state)
    print(f"Single step: s_serve_ready -> {next_state}")
    
    # Test complete rally simulation
    print("\nComplete rally simulations (5 rallies):")
    print("-" * 50)
    
    for i in range(5):
        rally_sequence, outcome = simulate_complete_rally(sm)
        
        # Print the rally history
        print(f"Rally {i+1}:")
        print(f"  Sequence: {' -> '.join(rally_sequence)}")
        print(f"  Length: {len(rally_sequence)} states")
        print(f"  Outcome: {outcome}")
        print(f"  Terminal state: {rally_sequence[-1]}")
        print()
        
        # Run assertions
        assert len(rally_sequence) > 0
        assert sm.is_terminal_state(rally_sequence[-1])
        assert "wins" in outcome
    
    print("Rally simulation test passed!")


def test_simulate_match_points() -> None:
    """Test the simulate_match_points function with identical teams."""
    
    # Get common templates
    templates = get_common_state_templates()
    
    # Test with identical elite teams
    elite_win_pct = simulate_match_points(
        templates["elite_team"],
        templates["elite_team"],
        num_points=1000
    )
    
    print(f"Elite vs Elite win percentage: {elite_win_pct:.2f}")
    assert abs(elite_win_pct - 0.5) < 0.1, "Expected ~50% win rate for identical teams"
    
    print("Match points simulation test passed!")


def test_display_functions() -> None:
    """Test the display and utility functions."""
    sm = create_beach_volleyball_state_machine()
    print("\nTesting display functions:")
    print_state_machine_summary(sm)
    print("\nDisplay functions test passed!")


def run_comprehensive_tests() -> None:
    """Run comprehensive tests and examples for the beach volleyball state machine."""
    print("\nRunning comprehensive tests...")
    print("=" * 50)
    
    # Run all test functions
    test_state_machine_creation()
    test_winning_conditions()
    test_rally_simulation()
    test_simulate_match_points()
    test_display_functions()
    
    print("\nAll tests completed successfully!")
