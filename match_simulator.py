# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Match-level simulation functions for beach volleyball."""

from typing import Dict, List, Tuple
from decimal import Decimal
from types_ import ProbabilityTransitions
from state_machine_builder import create_state_machine_from_teams
from rally_simulator import simulate_complete_rally


def simulate_match_points(
    team_a_template: ProbabilityTransitions, 
    team_b_template: ProbabilityTransitions, 
    num_points: int
) -> float:
    """Simulate a specified number of points alternating serving teams."""
    
    # Implementation of match simulation logic
    # ... (moved from original file)
    
    return 0.5  # Placeholder, implement actual win percentage calculation


def _separate_team_states(team_template: ProbabilityTransitions) -> Tuple[
    ProbabilityTransitions, ProbabilityTransitions
]:
    """Separate a team template into serving (s_) and receiving (r_) states."""
    serving_states = {}
    receiving_states = {}
    
    for state, transitions in team_template.items():
        if state.startswith('s_'):
            serving_states[state] = transitions
        elif state.startswith('r_'):
            receiving_states[state] = transitions
    
    return serving_states, receiving_states
