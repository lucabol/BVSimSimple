# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Functions for building custom state machines from team probabilities."""

from typing import Dict, List, Tuple
from decimal import Decimal
from types_ import StateTransitionTuple, ActionType, ProbabilityTransitions
from state_machine import RallyStateMachine
from state_definitions import create_beach_volleyball_state_machine


def create_state_machine_from_teams(
    team_serving_probs: ProbabilityTransitions, 
    team_receiving_probs: ProbabilityTransitions
) -> RallyStateMachine:
    """Create a custom state machine from team-specific probability dictionaries."""
    
    # Start with the default state machine structure
    default_sm = create_beach_volleyball_state_machine()
    
    # Create a copy of the default transitions
    custom_transitions: Dict[str, List[StateTransitionTuple]] = {}
    
    # Process serving team probabilities
    for state, prob_transitions in team_serving_probs.items():
        _validate_state_probabilities(state, prob_transitions)
        custom_transitions[state] = [
            (next_state, prob, _infer_action_type(state))
            for next_state, prob in prob_transitions
        ]
    
    # Process receiving team probabilities
    for state, prob_transitions in team_receiving_probs.items():
        _validate_state_probabilities(state, prob_transitions)
        custom_transitions[state] = [
            (next_state, prob, _infer_action_type(state))
            for next_state, prob in prob_transitions
        ]
    
    return RallyStateMachine(
        transitions=custom_transitions,
        terminal_states=default_sm.terminal_states,
        initial_state=default_sm.initial_state
    )


def _infer_action_type(state_name: str) -> ActionType:
    """Infer the action type from the state name."""
    if 'serve' in state_name:
        return ActionType.SERVE
    elif 'reception' in state_name:
        return ActionType.RECEPTION
    elif 'set' in state_name:
        return ActionType.SET
    elif 'attack' in state_name:
        return ActionType.ATTACK
    elif 'dig' in state_name:
        return ActionType.DIG
    elif 'block' in state_name:
        return ActionType.BLOCK
    elif 'transition' in state_name:
        return ActionType.TRANSITION
    else:
        return ActionType.TRANSITION


def _validate_state_probabilities(state: str, transitions: List[Tuple[str, Decimal]]) -> None:
    """Validate that probabilities for a state sum to 1.0."""
    total_prob = sum(prob for _, prob in transitions)
    if abs(total_prob - Decimal("1.0")) > Decimal("0.001"):
        raise ValueError(
            f"Probabilities for state '{state}' sum to {total_prob}, not 1.0. "
            f"Transitions: {transitions}"
        )
