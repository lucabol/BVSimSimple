# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Display and utility functions for beach volleyball state machines."""

from state_machine import RallyStateMachine
from state_definitions import get_winning_team


def print_state_machine_summary(state_machine: RallyStateMachine) -> None:
    """Print a summary of the state machine structure."""
    
    print("Beach Volleyball Rally State Machine Summary")
    print("=" * 50)
    print(f"Initial state: {state_machine.initial_state}")
    print(f"Total states: {len(state_machine.get_all_states())}")
    print(f"Terminal states: {len(state_machine.terminal_states)}")
    print(f"Continuation states: {len(state_machine.get_continuation_states())}")
    print(f"Probability validation: {state_machine.validate_probabilities()}")
    
    print(f"\nTerminal states:")
    for state in sorted(state_machine.terminal_states):
        winner = get_winning_team(state)
        print(f"  {state} -> {winner} team wins")
    
    print(f"\nSample transitions from initial state:")
    initial_transitions = state_machine.get_next_states(state_machine.initial_state)
    for next_state, probability, action_type in initial_transitions:
        print(f"  {state_machine.initial_state} -> {next_state} (p={probability}, {action_type})")
