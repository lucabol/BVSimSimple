# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""State machine definitions and default probabilities for beach volleyball."""

from typing import Dict, List, Set
from decimal import Decimal
from types_ import StateTransitionTuple, ActionType
from state_machine import RallyStateMachine


def create_beach_volleyball_state_machine() -> RallyStateMachine:
    """Create the complete beach volleyball rally state machine with contextual probabilities."""
    
    # Define all state transitions with realistic probabilities that preserve context
    transitions: Dict[str, List[StateTransitionTuple]] = {
        # Initial serve - only 'ready' state we keep
        "s_serve_ready": [
            ("s_serve_ace", Decimal("0.04"), ActionType.SERVE),
            ("s_serve_error", Decimal("0.12"), ActionType.SERVE),
            ("s_serve_in_play", Decimal("0.84"), ActionType.SERVE)
        ],
        
        # Reception directly from serve quality
        "s_serve_in_play": [
            ("r_reception_error", Decimal("0.15"), ActionType.RECEPTION),
            ("r_reception_perfect", Decimal("0.35"), ActionType.RECEPTION),
            ("r_reception_good", Decimal("0.50"), ActionType.RECEPTION)
        ],
        
        # Setting quality depends on reception quality
        "r_reception_perfect": [
            ("r_set_error", Decimal("0.08"), ActionType.SET),
            ("r_set_perfect", Decimal("0.57"), ActionType.SET),
            ("r_set_good", Decimal("0.35"), ActionType.SET)
        ],
        "r_reception_good": [
            ("r_set_error", Decimal("0.18"), ActionType.SET),
            ("r_set_perfect", Decimal("0.17"), ActionType.SET),
            ("r_set_good", Decimal("0.50"), ActionType.SET),
            ("r_set_poor", Decimal("0.15"), ActionType.SET)
        ],
        
        # Attack quality depends on set quality
        "r_set_perfect": [
            ("r_attack_kill", Decimal("0.42"), ActionType.ATTACK),
            ("r_attack_error", Decimal("0.10"), ActionType.ATTACK),
            ("r_attack_blocked", Decimal("0.18"), ActionType.ATTACK),
            ("r_attack_defended", Decimal("0.30"), ActionType.ATTACK)
        ],
        "r_set_good": [
            ("r_attack_kill", Decimal("0.28"), ActionType.ATTACK),
            ("r_attack_error", Decimal("0.12"), ActionType.ATTACK),
            ("r_attack_blocked", Decimal("0.27"), ActionType.ATTACK),
            ("r_attack_defended", Decimal("0.33"), ActionType.ATTACK)
        ],
        "r_set_poor": [
            ("r_attack_kill", Decimal("0.12"), ActionType.ATTACK),
            ("r_attack_error", Decimal("0.28"), ActionType.ATTACK),
            ("r_attack_blocked", Decimal("0.35"), ActionType.ATTACK),
            ("r_attack_defended", Decimal("0.25"), ActionType.ATTACK)
        ],
        
        # Defense outcomes depend on attack type
        "r_attack_blocked": [
            ("s_block_kill", Decimal("0.20"), ActionType.BLOCK),
            ("s_block_error", Decimal("0.15"), ActionType.BLOCK),
            ("s_dig_perfect", Decimal("0.35"), ActionType.BLOCK),
            ("s_dig_good", Decimal("0.30"), ActionType.BLOCK)
        ],
        "r_attack_defended": [
            ("s_dig_error", Decimal("0.30"), ActionType.DIG),
            ("s_dig_perfect", Decimal("0.35"), ActionType.DIG),
            ("s_dig_good", Decimal("0.35"), ActionType.DIG)
        ],
        
        # Serving team setting quality depends on dig quality
        "s_dig_perfect": [
            ("s_set_error", Decimal("0.08"), ActionType.SET),
            ("s_set_perfect", Decimal("0.57"), ActionType.SET),
            ("s_set_good", Decimal("0.35"), ActionType.SET)
        ],
        "s_dig_good": [
            ("s_set_error", Decimal("0.18"), ActionType.SET),
            ("s_set_perfect", Decimal("0.17"), ActionType.SET),
            ("s_set_good", Decimal("0.50"), ActionType.SET),
            ("s_set_poor", Decimal("0.15"), ActionType.SET)
        ],
        
        # Serving team attack quality depends on set quality
        "s_set_perfect": [
            ("s_attack_kill", Decimal("0.42"), ActionType.ATTACK),
            ("s_attack_error", Decimal("0.10"), ActionType.ATTACK),
            ("s_attack_blocked", Decimal("0.18"), ActionType.ATTACK),
            ("s_attack_defended", Decimal("0.30"), ActionType.ATTACK)
        ],
        "s_set_good": [
            ("s_attack_kill", Decimal("0.28"), ActionType.ATTACK),
            ("s_attack_error", Decimal("0.12"), ActionType.ATTACK),
            ("s_attack_blocked", Decimal("0.27"), ActionType.ATTACK),
            ("s_attack_defended", Decimal("0.33"), ActionType.ATTACK)
        ],
        "s_set_poor": [
            ("s_attack_kill", Decimal("0.12"), ActionType.ATTACK),
            ("s_attack_error", Decimal("0.28"), ActionType.ATTACK),
            ("s_attack_blocked", Decimal("0.35"), ActionType.ATTACK),
            ("s_attack_defended", Decimal("0.25"), ActionType.ATTACK)
        ],
        
        # Receiving team defense depends on attack type
        "s_attack_blocked": [
            ("r_block_kill", Decimal("0.20"), ActionType.BLOCK),
            ("r_block_error", Decimal("0.15"), ActionType.BLOCK),
            ("r_dig_perfect", Decimal("0.35"), ActionType.BLOCK),
            ("r_dig_good", Decimal("0.30"), ActionType.BLOCK)
        ],
        "s_attack_defended": [
            ("r_dig_error", Decimal("0.30"), ActionType.DIG),
            ("r_dig_perfect", Decimal("0.35"), ActionType.DIG),
            ("r_dig_good", Decimal("0.35"), ActionType.DIG)
        ],
        
        # Back to receiving team setting from dig quality
        "r_dig_perfect": [
            ("r_set_error", Decimal("0.05"), ActionType.SET),
            ("r_set_perfect", Decimal("0.60"), ActionType.SET),
            ("r_set_good", Decimal("0.35"), ActionType.SET)
        ],
        "r_dig_good": [
            ("r_set_error", Decimal("0.15"), ActionType.SET),
            ("r_set_perfect", Decimal("0.20"), ActionType.SET),
            ("r_set_good", Decimal("0.50"), ActionType.SET),
            ("r_set_poor", Decimal("0.15"), ActionType.SET)
        ]
    }
    
    # Define terminal states - all error states and kill states
    terminal_states = {
        # Serving team wins
        "s_serve_ace", "r_reception_error", "r_set_error", "r_attack_error",
        "s_block_kill", "s_attack_kill", "r_dig_error", "r_block_error",
        
        # Receiving team wins  
        "s_serve_error", "r_attack_kill", "s_dig_error", "s_block_error",
        "s_set_error", "s_attack_error", "r_block_kill"
    }
    
    return RallyStateMachine(
        transitions=transitions,
        terminal_states=terminal_states,
        initial_state="s_serve_ready"
    )


def get_winning_team(terminal_state: str) -> str:
    """Determine which team wins based on terminal state."""
    serving_team_wins = {
        "s_serve_ace", "r_reception_error", "r_set_error", "r_attack_error",
        "s_block_kill", "s_attack_kill", "r_dig_error", "r_block_error"
    }
    
    receiving_team_wins = {
        "s_serve_error", "r_attack_kill", "s_dig_error", "s_block_error",
        "s_set_error", "s_attack_error", "r_block_kill"
    }
    
    if terminal_state in serving_team_wins:
        return "serving"
    elif terminal_state in receiving_team_wins:
        return "receiving"
    else:
        raise ValueError(f"State {terminal_state} is not a recognized terminal state")
