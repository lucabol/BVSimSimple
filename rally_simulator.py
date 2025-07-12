# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Rally simulation functions for beach volleyball state machines."""

from typing import Optional, List, Tuple
import random
from state_machine import RallyStateMachine
from state_definitions import get_winning_team


def simulate_rally_step(state_machine: RallyStateMachine, current_state: str) -> Optional[str]:
    """Simulate one step of the rally using weighted random selection."""
    
    if state_machine.is_terminal_state(current_state):
        return None
    
    transitions = state_machine.get_next_states(current_state)
    if not transitions:
        return None
    
    # Extract states and probabilities for weighted random selection
    states = [transition[0] for transition in transitions]
    probabilities = [float(transition[1]) for transition in transitions]
    
    # Use weighted random choice based on probabilities
    selected_state = random.choices(states, weights=probabilities, k=1)[0]
    return selected_state


def simulate_complete_rally(state_machine: RallyStateMachine, max_steps: int = 50) -> Tuple[List[str], str]:
    """Simulate a complete rally from start to finish."""
    
    rally_sequence = []
    current_state = state_machine.initial_state
    step = 0
    
    while not state_machine.is_terminal_state(current_state) and step < max_steps:
        rally_sequence.append(current_state)
        next_state = simulate_rally_step(state_machine, current_state)
        
        if next_state is None:
            break
            
        current_state = next_state
        step += 1
    
    # Add the final terminal state
    if state_machine.is_terminal_state(current_state):
        rally_sequence.append(current_state)
        winner = get_winning_team(current_state)
        outcome = f"{winner} team wins"
    else:
        outcome = f"Rally exceeded {max_steps} steps"
    
    return rally_sequence, outcome
