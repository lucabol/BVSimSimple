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
    """Simulate a specified number of points alternating serving teams.
    
    Args:
        team_a_template: Complete probability transitions for team A (both serving and receiving)
        team_b_template: Complete probability transitions for team B (both serving and receiving) 
        num_points: Number of points to simulate
        
    Returns:
        float: Win percentage for team A
    """
    if not team_a_template or not team_b_template:
        raise ValueError("Team templates cannot be empty")
    
    team_a_wins = 0
    
    for point in range(num_points):
        # Alternate serving team based on point number
        if point % 2 == 0:
            # Team A serves, Team B receives
            serving_states, _ = _separate_team_states(team_a_template)
            _, receiving_states = _separate_team_states(team_b_template)
            serving_team_is_a = True
        else:
            # Team B serves, Team A receives
            serving_states, _ = _separate_team_states(team_b_template)
            _, receiving_states = _separate_team_states(team_a_template)
            serving_team_is_a = False
            
        # Combine states for this point
        combined_states = {**serving_states, **receiving_states}
        
        # Create state machine for this point
        sm = create_state_machine_from_teams(combined_states, {})
        rally_sequence, outcome = simulate_complete_rally(sm)
        
        # Determine winner based on serving team and outcome
        if "serving" in outcome:
            if serving_team_is_a:
                team_a_wins += 1
        elif "receiving" in outcome:
            if not serving_team_is_a:
                team_a_wins += 1
    
    return team_a_wins / num_points


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
