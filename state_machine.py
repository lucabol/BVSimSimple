# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Core state machine implementation for beach volleyball."""

from typing import Dict, List, Set
from dataclasses import dataclass
from decimal import Decimal
from types_ import StateTransitionTuple


@dataclass
class RallyStateMachine:
    """Dictionary-based rally state machine for beach volleyball.
    
    This class encapsulates the state machine logic using a dictionary representation
    where each state maps to possible transitions with their probabilities and action types.
    """
    
    transitions: Dict[str, List[StateTransitionTuple]]
    terminal_states: Set[str]
    initial_state: str = "s_serve_ready"
    
    def get_next_states(self, current_state: str) -> List[StateTransitionTuple]:
        """Get possible next states from current state."""
        if current_state not in self.transitions:
            raise ValueError(f"Invalid state: {current_state}")
        return self.transitions[current_state]
    
    def is_terminal_state(self, state: str) -> bool:
        """Check if a state is terminal (ends the rally)."""
        return state in self.terminal_states
    
    def is_valid_transition(self, from_state: str, to_state: str) -> bool:
        """Check if a transition between states is valid."""
        if from_state not in self.transitions:
            return False
        valid_next_states = [transition[0] for transition in self.transitions[from_state]]
        return to_state in valid_next_states
    
    def get_acting_team(self, state: str) -> str:
        """Get which team is acting in the given state."""
        if state.startswith('s_'):
            return 'serving'
        elif state.startswith('r_'):
            return 'receiving'
        else:
            return 'terminal'
    
    def get_all_states(self) -> Set[str]:
        """Get all states in the state machine."""
        all_states = set(self.transitions.keys())
        all_states.update(self.terminal_states)
        return all_states
    
    def get_continuation_states(self) -> Set[str]:
        """Get all non-terminal states."""
        return self.get_all_states() - self.terminal_states
    
    def validate_probabilities(self) -> bool:
        """Validate that all transition probabilities sum to 1.0 for each state."""
        from decimal import Decimal
        
        for state, transitions in self.transitions.items():
            if not transitions:
                continue
                
            total_probability = sum(transition[1] for transition in transitions)
            if abs(total_probability - Decimal("1.0")) > Decimal("0.001"):
                print(f"Warning: State {state} probabilities sum to {total_probability}, not 1.0")
                return False
        
        return True
