# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Pre-defined team probability templates for different skill levels."""

from typing import Dict, List, Tuple
from decimal import Decimal
from types_ import ProbabilityTransitions


def get_common_state_templates() -> Dict[str, ProbabilityTransitions]:
    """Get common probability templates for different team skill levels."""
    
    templates = {
        "elite_team": {
            # Serving states
            "s_serve_ready": [
                ("s_serve_ace", Decimal("0.12")),
                ("s_serve_error", Decimal("0.04")),
                ("s_serve_in_play", Decimal("0.84"))
            ],
            "s_dig_perfect": [
                ("s_set_error", Decimal("0.03")),
                ("s_set_perfect", Decimal("0.65")),
                ("s_set_good", Decimal("0.32"))
            ],
            "s_dig_good": [
                ("s_set_error", Decimal("0.10")),
                ("s_set_perfect", Decimal("0.25")),
                ("s_set_good", Decimal("0.55")),
                ("s_set_poor", Decimal("0.10"))
            ],
            "s_set_perfect": [
                ("s_attack_kill", Decimal("0.60")),
                ("s_attack_error", Decimal("0.03")),
                ("s_attack_blocked", Decimal("0.12")),
                ("s_attack_defended", Decimal("0.25"))
            ],
            "s_set_good": [
                ("s_attack_kill", Decimal("0.40")),
                ("s_attack_error", Decimal("0.08")),
                ("s_attack_blocked", Decimal("0.22")),
                ("s_attack_defended", Decimal("0.30"))
            ],
            "s_set_poor": [
                ("s_attack_kill", Decimal("0.18")),
                ("s_attack_error", Decimal("0.20")),
                ("s_attack_blocked", Decimal("0.32")),
                ("s_attack_defended", Decimal("0.30"))
            ],
            
            # Receiving states
            "s_serve_in_play": [
                ("r_reception_error", Decimal("0.08")),
                ("r_reception_perfect", Decimal("0.42")),
                ("r_reception_good", Decimal("0.50"))
            ],
            "r_reception_perfect": [
                ("r_set_error", Decimal("0.03")),
                ("r_set_perfect", Decimal("0.65")),
                ("r_set_good", Decimal("0.32"))
            ],
            "r_reception_good": [
                ("r_set_error", Decimal("0.10")),
                ("r_set_perfect", Decimal("0.25")),
                ("r_set_good", Decimal("0.55")),
                ("r_set_poor", Decimal("0.10"))
            ],
            "r_set_perfect": [
                ("r_attack_kill", Decimal("0.60")),
                ("r_attack_error", Decimal("0.03")),
                ("r_attack_blocked", Decimal("0.12")),
                ("r_attack_defended", Decimal("0.25"))
            ],
            "r_set_good": [
                ("r_attack_kill", Decimal("0.40")),
                ("r_attack_error", Decimal("0.08")),
                ("r_attack_blocked", Decimal("0.22")),
                ("r_attack_defended", Decimal("0.30"))
            ],
            "r_set_poor": [
                ("r_attack_kill", Decimal("0.18")),
                ("r_attack_error", Decimal("0.20")),
                ("r_attack_blocked", Decimal("0.32")),
                ("r_attack_defended", Decimal("0.30"))
            ],
            "r_attack_blocked": [
                ("s_block_kill", Decimal("0.25")),
                ("s_block_error", Decimal("0.15")),
                ("s_dig_perfect", Decimal("0.30")),
                ("s_dig_good", Decimal("0.30"))
            ],
            "r_attack_defended": [
                ("s_dig_error", Decimal("0.25")),
                ("s_dig_perfect", Decimal("0.40")),
                ("s_dig_good", Decimal("0.35"))
            ],
            "s_attack_blocked": [
                ("r_block_kill", Decimal("0.25")),
                ("r_block_error", Decimal("0.15")),
                ("r_dig_perfect", Decimal("0.30")),
                ("r_dig_good", Decimal("0.30"))
            ],
            "s_attack_defended": [
                ("r_dig_error", Decimal("0.25")),
                ("r_dig_perfect", Decimal("0.40")),
                ("r_dig_good", Decimal("0.35"))
            ],
            "r_dig_perfect": [
                ("r_set_error", Decimal("0.03")),
                ("r_set_perfect", Decimal("0.65")),
                ("r_set_good", Decimal("0.32"))
            ],
            "r_dig_good": [
                ("r_set_error", Decimal("0.10")),
                ("r_set_perfect", Decimal("0.25")),
                ("r_set_good", Decimal("0.55")),
                ("r_set_poor", Decimal("0.10"))
            ]
        }
    }
    
    return templates
