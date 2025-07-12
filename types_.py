# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Core types and constants for the beach volleyball state machine."""

from typing import Dict, List, Tuple, Optional, Set
from decimal import Decimal
from dataclasses import dataclass
from enum import Enum


class ActionType(str, Enum):
    """Types of actions that can occur in a rally."""
    
    SERVE = "serve"
    RECEPTION = "reception"
    SET = "set"
    ATTACK = "attack"
    DIG = "dig"
    BLOCK = "block"
    TRANSITION = "transition"


# Type alias for state transition tuple
StateTransitionTuple = Tuple[str, Decimal, ActionType]

# Type alias for probability transitions
ProbabilityTransitions = Dict[str, List[Tuple[str, Decimal]]]
