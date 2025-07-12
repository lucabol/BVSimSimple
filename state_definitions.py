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
    """Create the complete beach volleyball rally state machine with default probabilities."""
    
    # Define all state transitions with realistic probabilities
    transitions: Dict[str, List[StateTransitionTuple]] = {
        # Serving team states
        "s_serve_ready": [
            ("s_serve_ace", Decimal("0.08"), ActionType.SERVE),
            ("s_serve_error", Decimal("0.12"), ActionType.SERVE),
            ("s_serve_in_play", Decimal("0.80"), ActionType.SERVE)
        ],
        "s_serve_in_play": [
            ("r_reception_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "s_dig_ready": [
            ("s_dig_error", Decimal("0.30"), ActionType.DIG),
            ("s_dig_success", Decimal("0.70"), ActionType.DIG)
        ],
        "s_dig_success": [
            ("s_set_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "s_set_ready": [
            ("s_set_error", Decimal("0.10"), ActionType.SET),
            ("s_set_success", Decimal("0.90"), ActionType.SET)
        ],
        "s_set_success": [
            ("s_attack_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "s_attack_ready": [
            ("s_attack_kill", Decimal("0.40"), ActionType.ATTACK),
            ("s_attack_error", Decimal("0.15"), ActionType.ATTACK),
            ("s_attack_in_play", Decimal("0.45"), ActionType.ATTACK)
        ],
        "s_attack_in_play": [
            ("r_dig_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "s_block_ready": [
            ("s_block_kill", Decimal("0.20"), ActionType.BLOCK),
            ("s_block_error", Decimal("0.15"), ActionType.BLOCK),
            ("s_block_in_play", Decimal("0.65"), ActionType.BLOCK)
        ],
        "s_block_in_play": [
            ("s_dig_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],

        # Receiving team states
        "r_reception_ready": [
            ("r_reception_error", Decimal("0.15"), ActionType.RECEPTION),
            ("r_reception_success", Decimal("0.85"), ActionType.RECEPTION)
        ],
        "r_reception_success": [
            ("r_set_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "r_dig_ready": [
            ("r_dig_error", Decimal("0.30"), ActionType.DIG),
            ("r_dig_success", Decimal("0.70"), ActionType.DIG)
        ],
        "r_dig_success": [
            ("r_set_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "r_set_ready": [
            ("r_set_error", Decimal("0.10"), ActionType.SET),
            ("r_set_success", Decimal("0.90"), ActionType.SET)
        ],
        "r_set_success": [
            ("r_attack_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "r_attack_ready": [
            ("r_attack_kill", Decimal("0.40"), ActionType.ATTACK),
            ("r_attack_error", Decimal("0.15"), ActionType.ATTACK),
            ("r_attack_in_play", Decimal("0.45"), ActionType.ATTACK)
        ],
        "r_attack_in_play": [
            ("s_block_ready", Decimal("1.0"), ActionType.TRANSITION)
        ],
        "r_block_ready": [
            ("r_block_kill", Decimal("0.20"), ActionType.BLOCK),
            ("r_block_error", Decimal("0.15"), ActionType.BLOCK),
            ("r_block_in_play", Decimal("0.65"), ActionType.BLOCK)
        ],
        "r_block_in_play": [
            ("r_dig_ready", Decimal("1.0"), ActionType.TRANSITION)
        ]
    }
    
    # Define terminal states
    terminal_states = {
        "s_serve_ace", "s_serve_error", "r_reception_error", "r_set_error",
        "r_attack_kill", "r_attack_error", "s_dig_error", "s_block_kill",
        "s_block_error", "s_set_error", "s_attack_kill", "s_attack_error",
        "r_dig_error", "r_block_kill", "r_block_error"
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
